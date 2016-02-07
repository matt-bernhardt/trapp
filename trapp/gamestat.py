# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.record import Record


class GameStat(Record):

    def lookupID(self, data, log):
        # Do we have a record of player X appearing in game Y for team Z?

        # Check submitted data for format and fields
        required = ['GameID', 'TeamID', 'PlayerID']
        self.checkData(data, required)

        sql = ('SELECT ID '
               'FROM tbl_gamestats '
               'WHERE GameID = %s '
               '  AND TeamID = %s '
               '  AND PlayerID = %s')
        rs = self.db.query(sql, (
            data['GameID'],
            data['TeamID'],
            data['PlayerID']
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        stats = []
        for item in records:
            stats.append(item[0])

        return stats

    def saveDict(self, data, log):
        # Verify that data is a dictionary
        if not (isinstance(data, dict)):
            raise RuntimeError('saveDict requires a dictionary')

        if ('ID' in data):
            # Update
            log.message('Record ID provided - we update')
            sql = ('UPDATE tbl_gamestats SET '
                   'GameID = %s, '
                   'TeamID = %s, '
                   'PlayerID = %s, '
                   'Goals = %s, '
                   'Ast = %s, '
                   'RC = %s '
                   'WHERE ID = %s')
            rs = self.db.query(sql, (
                data['GameID'],
                data['TeamID'],
                data['PlayerID'],
                data['Goals'],
                data['Ast'],
                data['RC'],
                data['ID']
            ))
        else:
            log.message('No Record ID provided - we insert')
            sql = ('INSERT INTO tbl_gamestats '
                   '(GameID, TeamID, PlayerID, Goals, Ast, RC) '
                   'VALUES '
                   '(%s, %s, %s, %s, %s, %s)')
            log.message(str(sql))
            log.message(str(data))
            rs = self.db.query(sql, (
                data['GameID'],
                data['TeamID'],
                data['PlayerID'],
                data['Goals'],
                data['Ast'],
                data['RC']
            ))
            log.message(str(rs))

        return True
