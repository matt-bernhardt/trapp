# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class Team():

    def __init__(self):
        self.data = {}
        self.data["ID"] = 0

    def connectDB(self):
        self.db = Database()
        self.db.connect()

    def disconnectDB(self):
        self.db.disconnect()
        del self.db

    def checkData(self, data, required):
        # This checks a submitted data dictionary for required fields.
        # 1) data must be a dictionary
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # 2) data must have certain fields
        missing = []
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError(
                'Submitted data is missing the following fields: ' +
                str(missing)
            )

    def lookupID(self, data, log):
        # Check for required parameters
        required = ['teamname']
        self.checkData(data, required)

        # see if any team matches this name
        sql = ('SELECT ID '
               'FROM tbl_teams '
               'WHERE teamname = %s')
        rs = self.db.query(sql, (data['teamname'], ))
        if (rs.with_rows):
            records = rs.fetchall()
        teams = []
        for team in records:
            teams.append(team[0])

        # Return list of matched IDs
        return teams
