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

    def lookupID(self, data, log):
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # check for required fields
        missing = []
        required = ['teamname']
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError(
                'Submitted data is missing the following fields: ' +
                str(missing)
            )

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
