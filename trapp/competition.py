# -*- coding: utf-8 -*-
from trapp.record import Record


class Competition(Record):

    # Competitions are also referred to as Match Types, especially in the
    # database table names and fields.

    def loadAll(self):
        # This loads all available competitions
        sql = ('SELECT t.ID AS CompetitionID, t.MatchType, '
               't.CompetitionType, t.Official '
               'FROM lkp_matchtypes t '
               'ORDER BY MatchType')
        rs = self.db.query(sql, ())
        if (rs.with_rows):
            records = rs.fetchall()

        data = []

        for term in records:
            data.append({
                'CompetitionID': term[0],
                'Competition': term[1],
                'CompetitionType': term[2],
                'Official': term[3]
            })

        return data
