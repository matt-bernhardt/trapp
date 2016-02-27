# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.spreadsheet import Spreadsheet
from trapp.game import Game
from trapp.team import Team


class Importer():

    def __init__(self, importFile, logFile):
        # Counters for reporting outcomes
        self.imported = 0
        self.skipped = 0
        self.errored = 0
        # List for storing missing records
        self.missing = []
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
        # This is overwritten in child objects depending on the corrective
        # steps needed with the data.
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
        if (len(self.missing) > 0):
            self.log.message('\nMissing records:')
            self.missing.sort()
            for item in self.missing:
                self.log.message(str(item))
        return True
