# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.record import Record


class Season(Record):

    # Seasons are defined as the games that a team plays in a given (calendar)
    # year. They include games from multiple competitions, at least for now.

    def loadAll(self):
        # This loads all available seasons
        sql = ('SELECT t.ID AS TeamID, YEAR(h.MatchTime) AS Season '
               'FROM tbl_teams t '
               'LEFT OUTER JOIN tbl_games h ON t.ID = h.HTeamID '
               'LEFT OUTER JOIN tbl_games a on t.ID = a.ATeamID '
               'WHERE YEAR(h.MatchTime) = YEAR(a.MatchTime) '
               'GROUP BY t.ID, YEAR(h.MatchTime), YEAR(a.MatchTime)')
        rs = self.db.query(sql, ())
        if (rs.with_rows):
            records = rs.fetchall()

        data = []

        for term in records:
            data.append({
                'TeamID': term[0],
                'Season': term[1]
            })

        return data

    def loadPlayerList(self, data):
        # This loads all players to have appeared for a given team in a year

        sql = ('SELECT DISTINCT PlayerID '
               'FROM tbl_gameminutes m '
               'INNER JOIN tbl_games g ON m.GameID = g.ID '
               'WHERE m.TeamID = %s '
               '  AND YEAR(g.MatchTime) = %s '
               'ORDER BY PlayerID ASC')
        rs = self.db.query(sql, (
            data['TeamID'],
            data['Season']
        ))
        if (rs.with_rows):
            records = rs.fetchall()

        data = []

        for player in records:
            data.append(player)

        return data
