# -*- coding: utf-8 -*-
from trapp.record import Record


class Team(Record):

    def lookupID(self, data, log):
        # This takes a dictionary and validates it against existing records.
        # Do we already have a record of this team?
        # The data must have the following keys:
        # - teamname (string - the colloquial name of the team,
        #             i.e. "Columbus Crew")
        required = ['teamname']
        self.checkData(data, required)

        # See if any team matches this name
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
