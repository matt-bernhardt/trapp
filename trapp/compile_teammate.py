# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
from trapp.combo import Combo
from trapp.compiler import Compiler
from trapp.game import Game
from trapp.gameminute import GameMinute
from trapp.season import Season


class CompilerTeammates(Compiler):

    def assembleCombos(self, players):
        # This takes a list of players and returns a list of player pairings
        combos = []

        for p1 in players:
            for p2 in players:
                if p1 > p2:
                    combos.append({
                        'player1': int(p1[0]),
                        'player2': int(p2[0])
                    })

        return combos

    def calculateGame(self, p1, p2, duration):
        # This takes a dictionary of entrance and exit times, and parses
        # playing time into one of four buckets: one, two, both, neither

        self.log.message('Comparing ' + str(p1) + ' with ' + str(p2))

        record = {}
        record['one'] = 0
        record['two'] = 0
        record['both'] = 0
        record['neither'] = 0

        # First we determine if the players overlapped
        if (p1['off'] > p2['on'] and p2['off'] > p1['on']):
            self.log.message('Overlap Yes')

            # Who entered first?
            if (p1['on'] < p2['on']):
                record['one'] = p2['on'] - p1['on']
            elif (p1['on'] > p2['on']):
                record['two'] = p1['on'] - p2['on']
            # Who left first?
            if (p1['off'] < p2['off']):
                record['two'] += p2['off'] - p1['off']
            elif (p1['off'] > p2['off']):
                record['one'] += p1['off'] - p2['off']

            record['both'] = min(p1['off'],p2['off']) - max(p1['on'],p2['on'])
            record['neither'] = min(p1['on'],p2['on']) + (duration - max(p1['off'],p2['off']))

        else:
            self.log.message('Overlap No')
            record['one'] = p1['off'] - p1['on']
            record['two'] = p2['off'] - p2['on']
            record['both'] = 0
            record['neither'] = duration - (record['one'] + record['two'])

        # Debug
        self.log.message(str(record))
        if (duration == record['one'] + record['two'] + record['both'] + record['neither']):
            self.log.message('Consistent')
        else:
            self.log.message('Consistency check failed!')
            self.log.message(str(record['one'] + record['two'] + record['both'] + record['neither']))

        return record

    def calculateTeammates(self, combo, season, games):
        # This calculates teammate statistics for a given combo in a given
        # season

        self.log.message('\nCalculating data for:')
        self.log.message(str(combo))
        self.log.message(str(season))
        self.log.message(str(games))

        # Init
        one = 0
        two = 0
        both = 0
        neither = 0

        # Iterate through game list, building stats
        for game in games:

            self.log.message('Comparing game records')

            # Lookup game duration
            g = Game()
            g.connectDB()
            duration = g.lookupDuration(game[0], self.log)
            g.disconnectDB()

            # Retrieve appearance data for this game for these players
            gm = GameMinute()
            gm.connectDB()
            needle = {}
            needle['GameID'] = game[0]
            needle['TeamID'] = season['TeamID']
            needle['PlayerID'] = combo['player1']
            p1 = gm.loadRecord(needle, self.log)
            needle['PlayerID'] = combo['player2']
            p2 = gm.loadRecord(needle, self.log)
            gm.disconnectDB()

            self.log.message('Appearances:')
            self.log.message(str(p1))
            self.log.message(str(p2))

            # records come back as a list of one tuple, so this removes the
            # list. If the returned value is empty, then use zeroes.
            if (len(p1) == 1):
                p1 = p1[0]
            else:
                p1 = (0, 0, 0)
            player1 = {}
            player1['on'] = p1[0]
            player1['off'] = p1[1]

            if (len(p2) == 1):
                p2 = p2[0]
            else:
                p2 = (0, 0, 0)
            player2 = {}
            player2['on'] = p2[0]
            player2['off'] = p2[1]

            # Break down minutes played into one of four categories:
            # one - only p1 on field
            # two - only p2 on field
            # both - both p1 and p2 on field
            # neither - neither p1 nor p2 on field
            pairing = self.calculateGame(player1, player2, duration)

            # add this game's counts to totals
            one += pairing['one']
            two += pairing['two']
            both += pairing['both']
            neither += pairing['neither']

            self.log.message('')

        self.log.message(
            str(one) + ' _ ' +
            str(two) + ' _ ' +
            str(both) + ' _ ' +
            str(neither)
        )

        return True

    def doCompile(self):

        # First, we get a list of team-seasons recorded in the data
        s = Season()
        s.connectDB()
        self.seasons = s.loadAll()
        self.log.message(str(len(self.seasons)) + ' seasons')

        # Second, for each team-season:
        for item in self.seasons:

            print(str(item))
            self.log.message(str(item))

            # Get the list of players to have appeared in this season
            self.players = s.loadPlayerList(item)

            # If we have records for fewer than two players, then there
            # are no combinations to calculate - so we skip to the next season
            if(len(self.players) < 2):
                self.log.message('')
                print('')
                continue

            self.log.message(str(len(self.players)) + ' players this season')
            print(str(len(self.players)) + ' players')

            # Iterate over the list of players, building player pairs
            self.combos = self.assembleCombos(self.players)
            self.log.message(str(len(self.combos)) + ' combos this season')
            print(str(len(self.combos)) + ' combos')

            # Make sure each pair is recorded initially
            self.lookupCombos()

            # Build data for each pair
            games = s.loadGameList(item)
            [self.calculateTeammates(combo, item, games)
             for combo
             in self.combos]

            # Store data for each pair

            # Delay a bit so the database can keep up
            time.sleep(0.1)

            self.log.message('')
            print('\n')

        s.disconnectDB()

        return True

    def lookupCombos(self):
        # This iterates over the self.combos array and looks up whether each
        # is recorded already

        c = Combo()
        c.connectDB()

        for group in self.combos:

            self.log.message(str(group))

            group['combos'] = c.lookupCombos(
                group['player1'],
                group['player2']
            )

            # There should be four id values:
            # both, neither, one, and the other
            # Just looking at counts isn't enough, but it is a start.
            if(len(group['combos']) == 4):
                # No action needed
                self.log.message('All present')
            elif(len(group['combos']) == 0):
                # None exist - so we create them
                self.log.message('Create all')
                c.registerCombo(
                    group['player1'],
                    group['player2']
                )
            else:
                # Some other number exists. WTF?
                self.log.message('Some present')
                raise RuntimeError('Incorrect number of combinations found')

            self.log.message('')

        c.disconnectDB()

        return True
