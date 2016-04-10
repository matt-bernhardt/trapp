# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.checker import Checker


class CheckerGames(Checker):

    def reviewCompetition(self, competition, year):
        log.message('Reviewing competition ' + str(competition))

        # Get years this competition was held
        sql = ("SELECT DISTINCT(YEAR(MatchTime)) AS MatchYear, COUNT(ID) AS Games "
               "FROM tbl_games "
               "WHERE MatchTypeID = %s AND YEAR(MatchTime) >= %s "
               "GROUP BY YEAR(MatchTime) "
               "ORDER BY MatchYear ASC")
        # log.message(sql)
        rs = database.query(sql, (competition, year, ))

        if (rs.with_rows):
            records = rs.fetchall()

        for index, item in enumerate(records):
            output.message(str(competition) + ',' + str(item[0]) + ',' + str(item[1]))

    def checkGames(self):
        # What year are we starting our checks
        startYear = 2012

        # competitions key:
        # 21 - MLS League
        # 4, 5 - MLS Playoffs, MLS Cup
        # 14, 22 - US Open Cup, qualifiers
        # 23, 24, 25 - CONCACAF
        # 26 - Canadian Championship
        # 28, 29, 30 - NASL league, playoffs, final
        competitionlist = [21, 4, 5, 14, 22, 23, 24, 25, 26, 28, 29, 30]

        # Teams key is too long to summarize - look in tbl_teams
        teamlist = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 42, 43, 44, 45, 174, 175, 340, 341, 427, 463, 479, 506, 547]
        