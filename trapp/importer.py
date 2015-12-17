# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.spreadsheet import Spreadsheet
from trapp.game import Game
from trapp.player import Player
from trapp.team import Team


class Importer():

    def __init__(self, importFile, logFile):
        # This probably needs to check the submitted file type and read in the
        # appropriate shim.
        # For now, though, only Excel spreadsheets are supported.
        self.source = Spreadsheet(importFile)
        self.fields = self.source.fields()
        self.checkData()
        self.setLog(logFile)
        # TODO: Variables to track outcomes of import steps:
        #       - Successful import
        #       - Duplicate records
        #       - Other errors
        # TODO: Method to check outcome counts

    def checkFields(self, fields):
        # This checks the imported spreadsheet for a dictionary of required fields
        missingFields = []

        for col in fields:
            if col not in self.fields:
                missingFields.append(col)
        if (len(missingFields) > 0):
            raise RuntimeError('Submitted data is missing the following columns: ' + str(missingFields))

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

    def setLog(self, log):
        self.log = log
        self.log.message('Log transferred')
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
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(found) + ' matching games')

        return True


class ImporterLineups(Importer):

    def correctValues(self):
        for record in self.records:
            record['Date'] = self.source.recoverDate(record['Date'])

        return True

    def importRecord(self, record):
        self.log.message('Importing lineup ' + str(record))
        # Need to identify gameID
        g = Game()
        g.connectDB()
        # TODO: Need to build a dictionary from record
        # TODO: Need Teams model

        # TeamID
        teamID = self.lookupTeamID(record['Team'])

        # OpponentID
        opponentID = self.lookupTeamID(record['Opponent'])

        # Sort home/away teams
        if (record['H/A'] == 'H'):
            homeID = teamID
            awayID = opponentID
        elif (record['H/A'] == 'A'):
            homeID = opponentID
            awayID = teamID

        needle = {
            'MatchTime': record['Date'],
            'HTeamID': homeID,
            'ATeamID': awayID,
        }
        game = g.lookupID(needle, self.log)

        self.log.message('Found games: ' + str(game))
        if (len(game) > 1):
            self.log.message('Multiple games found')
        elif (len(game) == 0):
            self.log.message('No matching games found')

        # Parse lineup string

        # Iterate over every player, keeping in mind that data may
        # already exist

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
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(found) + ' matching players')

        return True
