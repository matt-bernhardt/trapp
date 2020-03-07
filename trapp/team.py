# -*- coding: utf-8 -*-
from trapp.record import Record


class Team(Record):

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
