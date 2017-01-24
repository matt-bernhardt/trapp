# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.checker import Checker
from trapp.competition import Competition


class CheckerGames(Checker):

    def reviewCompetition(self, competition, year):
        self.log.message('Reviewing competition ' + str(competition))

        # Get years this competition was held
        sql = ("SELECT DISTINCT(YEAR(MatchTime)) AS MatchYear, "
               "  COUNT(ID) AS Games "
               "FROM tbl_games "
               "WHERE MatchTypeID = %s AND YEAR(MatchTime) >= %s "
               "GROUP BY YEAR(MatchTime) "
               "ORDER BY MatchYear ASC")
        rs = self.db.query(sql, (competition, year, ))

        if (rs.with_rows):
            records = rs.fetchall()

        for index, item in enumerate(records):
            self.output.message(str(competition) + ',' +
                                str(item[0]) + ',' +
                                str(item[1]))

    def checkGames(self):
        # What year are we starting our checks
        startYear = 1990

        # Label Columns
        self.output.message('Competition,Year,Games')

        # Get Competitions list
        c = Competition()
        c.connectDB()
        competitions = c.loadAll()

        # Do work
        [self.reviewCompetition(record['CompetitionID'], startYear)
         for record
         in competitions]
