# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.spreadsheet import Spreadsheet
from trapp.game import Game
from trapp.player import Player
from trapp.team import Team


class Importer():

    def __init__(self, importFile, logFile):
        # Counters for reporting outcomes
        self.imported = 0
        self.skipped = 0
        self.errored = 0
        # This probably needs to check the submitted file type and read in the
        # appropriate shim.
        # For now, though, only Excel spreadsheets are supported.
        self.source = Spreadsheet(importFile)
        self.fields = self.source.fields()
        self.checkData()
        self.setLog(logFile)

    def adjustStoppageTime(self, minute):
        # Remove +, cast to integer for numeric comparison
        minute = int(minute.replace('+', ''))

        # Correct to last break:
        # - A minute before the end of a game/extra time
        # - The exact minute for midpoints (45, 105)
        if (minute > 120):
            return 119
        elif (minute > 105):
            return 105
        elif (minute > 90):
            return 89

        return 45

    def checkFields(self, fields):
        # This checks the imported spreadsheet for a dictionary of required
        # fields
        missingFields = []

        for col in fields:
            if col not in self.fields:
                missingFields.append(col)
        if (len(missingFields) > 0):
            raise RuntimeError(
                'Submitted data is missing the following columns: ' +
                str(missingFields)
            )

        return True

    def checkData(self):
        # This performs basic integrity checks on the data to be imported

        # Check for one worksheet
        if (len(self.source.data.sheets()) > 1):
            raise RuntimeError('Submitted data has more than one worksheet.')
        self.sheet = self.source.data.sheets()[0]

        # Check for at least one data row
        if (self.sheet.nrows < 2):
            raise RuntimeError('Submitted data has nothing to import.')

        return True

    def correctValues(self):
        # This is overwritten in child objects depending on the corrective
        # steps needed with the data.
        return True

    def doImport(self):
        # Prepare records
        self.records = self.source.buildRecords()

        # Correct values
        self.correctValues()

        # Iterate over records
        [self.importRecord(record) for record in self.records]

        self.reportStatus()

        return True

    def importRecord(self, record):
        # This is overwritten in child objects
        print('Importing record ' + str(record))
        g = Game()
        g.connectDB()
        # Look up whether the record already exists
        found = g.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            g.saveDict(record, self.log)
        else:
            # Some other number of games was found
            print('Found ' + str(found) + ' games already exist')
        return True

    def parseMinute(self, minute):
        # This reads in a string representing a minute denotation, and
        # adjusts it for format:
        # - removes ' characters
        # - detects + notations, and reduces value to the end of that period
        # It returns an integer

        # Cast to string so the next two steps don't fail
        minute = str(minute)

        # Remove ' if found
        minute = minute.replace("'", "")

        # Correct stoppage time back to end of that period
        # This assumes 45 minute halves, and 15 minute extra time periods
        # (those may not be valid assumptions)
        if (minute.find('+') > 0):
            minute = self.adjustStoppageTime(minute)

        # Cast back to integer
        minute = int(minute)
        return minute

    def setLog(self, log):
        self.log = log
        self.log.message('Log transferred')
        return True

    def reportStatus(self):
        self.log.message('\nImport results:')
        self.log.message(str(self.imported) + ' imported')
        self.log.message(str(self.skipped) + ' skipped')
        self.log.message(str(self.errored) + ' errored')
        print(str(self.imported) + ' imported')
        print(str(self.skipped) + ' skipped')
        print(str(self.errored) + ' errored')
        return True


class ImporterGames(Importer):

    def correctValues(self):
        for record in self.records:
            record['MatchTime'] = self.source.recoverDate(record['MatchTime'])

        return True

    def importRecord(self, record):
        self.log.message('Importing game ' + str(record))
        g = Game()
        g.connectDB()

        # Does the record exist?
        found = g.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            g.saveDict(record, self.log)
            self.imported += 1
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(found) + ' matching games')
            self.skipped += 1

        return True


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
        if (len(game) > 1):
            self.log.message('Multiple games found')
            self.skipped += 1
            return False
            # If that's the case, then we need to abort processing this game
        elif (len(game) == 0):
            self.log.message('No matching games found')
            self.skipped += 1
            return False
            # If that's the case, then we need to abort processing this game

        # If we make it to this point, then procesing can continue

        # Parse lineup string
        self.parseLineup(record['Lineup'], game, teamID)

        # At this point we have self.players - but need to store them

        return True

    def lookupTeamID(self, teamname):
        team = Team()
        team.connectDB()
        teamID = team.lookupID({'teamname': teamname}, self.log)
        if (len(teamID) > 1):
            raise RuntimeError('Ambiguous team name: ' + str(teamname))
        elif (len(teamID) == 0):
            raise RuntimeError('Team not found: ' + str(teamname))
        # At this point we know teamID is a list of length 1, so we return
        # the first value only
        return teamID[0]

    def parseLineup(self, lineup, game, teamID):
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

        self.players = []
        for starter in self.starters:
            batch = self.parsePlayer(starter, game, teamID)
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

    def parsePlayer(self, starter, gameID, teamID):
        result = []
        timeoff = 90

        while (starter.find('(') > 0):
            # calculate boundaries
            begin = starter.find('(')
            end = starter.rfind(')')
            # split into outer and starter
            outer = starter[:begin - 1]
            starter = starter[begin + 1:end]
            # split time from outer
            timeon = self.parsePlayerTimeOn(outer)
            outer = self.parsePlayerRemoveTime(outer)
            # store outer
            result.append({
                'PlayerName': outer.strip(),
                'TimeOn': timeon,
                'TimeOff': timeoff,
                'Ejected': False,
                'GameID': gameID,
                'TeamID': teamID
            })

        # parse last value
        timeon = self.parsePlayerTimeOn(starter)
        starter = self.parsePlayerRemoveTime(starter)
        # store last value
        result.append({
            'PlayerName': starter.strip(),
            'TimeOn': timeon,
            'TimeOff': timeoff,
            'Ejected': False,
            'GameID': gameID,
            'TeamID': teamID
        })

        # Transfer timeon values to previous player's timeoff
        result = self.adjustTimeOff(result, timeoff)

        return result


class ImporterPlayers(Importer):

    def correctValues(self):
        for record in self.records:
            record['DOB'] = self.source.recoverDate(record['DOB'])

        return True

    def importRecord(self, record):
        self.log.message('Importing player ' + str(record))
        p = Player()
        p.connectDB()

        # Does the record exist?
        found = p.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            p.saveDict(record, self.log)
            self.imported += 1
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(found) + ' matching players')
            self.skipped += 1

        return True
