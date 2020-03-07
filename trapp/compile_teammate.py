# -*- coding: utf-8 -*-
import time
from trapp.combo import Combo
from trapp.compiler import Compiler
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

    def doCompile(self):

        # First, we get a list of team-seasons recorded in the data
        s = Season()
        s.connectDB()
        self.seasons = s.loadAll()
        self.log.message(str(len(self.seasons)) + ' seasons')

        # Second, for each team-season:
        for item in self.seasons:

            print((str(item)))
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
            print((str(len(self.players)) + ' players'))

            # Iterate over the list of players, building player pairs
            self.combos = self.assembleCombos(self.players)
            self.log.message(str(len(self.combos)) + ' combos this season')
            print((str(len(self.combos)) + ' combos'))

            # Make sure each pair is recorded initially
            self.lookupCombos()

            # print(str(self.combos))

            # Build data for each pair

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
