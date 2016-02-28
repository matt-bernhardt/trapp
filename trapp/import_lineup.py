# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.importer import Importer
from trapp.game import Game
from trapp.gameminute import GameMinute
from trapp.player import Player


class ImporterLineups(Importer):

    def adjustTimeOff(self, result, lastOff):
        sentOff = False

        # Need to track backwards through list, transferring timeoff
        for x in reversed(result):
            x['TimeOff'] = lastOff
            if (sentOff is True):
                x['Ejected'] = True
                sentOff = False
            if (x['PlayerName'] == 'sent off' or x['PlayerName'] == 'ejected'):
                result.remove(x)
                sentOff = True
            lastOff = x['TimeOn']

        return result

    def correctValues(self):
        for record in self.records:
            record['Date'] = self.source.recoverDate(record['Date'])
        return True

    def importPlayer(self, player):
        self.log.message(str(player))
        gm = GameMinute()
        gm.connectDB()
        appearanceID = gm.lookupID(player, self.log)
        if (len(appearanceID) > 1):
            # We have more than one record of this player/team/game.
            # This is a problem.
            self.errored += 1
        elif (len(appearanceID) == 1):
            # We already have a record of this player/team/game.
            # We add that appearanceID, to ensure an update operation.
            player['ID'] = appearanceID[0]
            gm.saveDict(player, self.log)
            self.imported += 1
        else:
            gm.saveDict(player, self.log)
            self.imported += 1
        return True

    def importRecord(self, record):
        self.log.message('Importing lineup ' + str(record))

        # Need to identify gameID
        g = Game()
        g.connectDB()

        # Team and Opponent ID
        teamID = self.lookupTeamID(record['Team'])
        opponentID = self.lookupTeamID(record['Opponent'])

        # Sort home/away teams
        if (record['H/A'] == 'H'):
            homeID = teamID
            awayID = opponentID
        elif (record['H/A'] == 'A'):
            homeID = opponentID
            awayID = teamID

        # Lookup this gameID
        needle = {
            'MatchTime': record['Date'],
            'HTeamID': homeID,
            'ATeamID': awayID,
        }
        game = g.lookupID(needle, self.log)

        self.log.message('Found games: ' + str(game))

        if (len(game) != 1):
            self.log.message('Found wrong number of games: ' + str(len(game)))
            self.skipped += 1
            # If we didn't find one gameID, then we abort processing this game
            return False

        # Need to convert gameID from a list of 1 number to an integer
        game = game[0]

        # Lookup game duration
        duration = g.lookupDuration(game, self.log)

        # Parse lineup string
        self.parseLineup(record['Lineup'], game, teamID, duration)

        # At this point we have self.players - but need to store them
        [self.importPlayer(player) for player in self.players]

        return True

    def parseLineup(self, lineup, game, teamID, duration):
        # Parses a long string of starters and substitutes, populating
        # self.players with records for each player who appeared in the
        # game.
        self.log.message(str(lineup))
        self.starters = lineup.split(',')
        if (len(self.starters) != 11):
            # We don't raise an error for a short lineup, as the records
            # can still be safely parsed and stored - just log for inspection
            # later.
            self.log.message('ERROR: Wrong number of starters')
            self.errored += 1

        # self.starters has strings for every starter, combined with any
        # substitutes or sendings off. These need to be split into separate
        # records for every player, which is done in parsePlayer
        self.players = []
        for starter in self.starters:
            batch = self.parsePlayer(starter, game, teamID, duration)
            for item in batch:
                self.players.append(item)
        self.log.message(str(self.players))

        # This method returns nothing, as its work is recorded in
        # self.starters and self.players.

    def parsePlayerTimeOn(self, string):
        # This splits off the last word/blob in a player string, and parses
        # it as a time denotation. If it passes, this is the time the player
        # entered the game. If it is not a time, then it is the player's last
        # name, and they started the game.
        candidate = string[string.rfind(' '):].strip()
        try:
            timeon = self.parseMinute(candidate)
        except ValueError:
            timeon = 0
        return timeon

    def parsePlayerRemoveTime(self, string):
        # This strips away a time designation from a player string, and
        # returns only the player name.
        time = self.parsePlayerTimeOn(string)
        if (time > 0):
            return str(string[:string.rfind(' ')])
        return string

    def parsePlayer(self, starter, gameID, teamID, duration):
        result = []

        # Set default timeoff to game duration
        timeoff = duration

        # Split the player string into a list
        result = self.parsePlayerSplit(starter)

        augmented = []
        # parse each member of the list
        for string in result:
            # Split time from player name
            timeon = self.parsePlayerTimeOn(string)
            player = self.parsePlayerRemoveTime(string).strip()

            # Look up playerID
            playerID = [0]
            if (player != 'sent off' and player != 'ejected'):
                p = Player()
                p.connectDB()
                needle = {
                    'PlayerName': player,
                }
                playerID = p.lookupIDbyName(needle, self.log)

            if (len(playerID) == 1):
                playerID = playerID[0]
                augmented.append({
                    'PlayerID': playerID,
                    'PlayerName': player,
                    'TimeOn': timeon,
                    'TimeOff': timeoff,
                    'Ejected': False,
                    'GameID': gameID,
                    'TeamID': teamID
                })
            else:
                self.processMissingRecord(player, len(playerID))

        # Transfer timeon values to previous player's timeoff
        result = self.adjustTimeOff(augmented, timeoff)

        return result

    def parsePlayerSplit(self, inputString):
        # This takes in a string and splits it into a list. For example:
        # "Player Name" -> ["Player Name"]
        # "Player Name (Substitute 63)" -> ["Player Name", "Substitute 65"]
        # ... and so fort
        result = []

        while (inputString.find('(') > 0):
            # Find boundaries to split
            begin = inputString.find('(')
            end = inputString.rfind(')')
            # Perform the split
            outer = inputString[:begin - 1]
            inputString = inputString[begin + 1:end]
            # Append results
            result.append(outer)

        # Do stuff
        result.append(inputString)

        return result
