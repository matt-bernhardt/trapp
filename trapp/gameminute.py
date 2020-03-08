# -*- coding: utf-8 -*-
from trapp.record import Record


class GameMinute(Record):

    def loadRecord(self, data, log):
        # Load a specific record of appearance data

        # Check submitted data for format and fields
        required = ['GameID', 'TeamID', 'PlayerID']
        self.checkData(data, required)

        sql = ('SELECT TimeOn, TimeOff, Ejected '
               'FROM tbl_gameminutes '
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
        appearance = []
        for item in records:
            appearance.append(item)
        return appearance

    def lookupID(self, data, log):
        # Do we have a record of player X appearing in game Y for team Z?

        # Check submitted data for format and fields
        required = ['GameID', 'TeamID', 'PlayerID']
        self.checkData(data, required)

        sql = ('SELECT ID '
               'FROM tbl_gameminutes '
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
        appearances = []
        for item in records:
            appearances.append(item[0])

        return appearances

    def lookupIDlistByYear(self):
        # Probably need to check whether year is actually an integer
        sql = ('SELECT gm.ID, gm.GameID, gm.TeamID, gm.PlayerID, '
               'gm.TimeOn, gm.TimeOff, gm.Ejected '
               'FROM tbl_gameminutes gm '
               'INNER JOIN tbl_games g ON gm.GameID = g.ID '
               'ORDER BY g.MatchTime, g.ID ASC')
        rs = self.db.query(sql, ())
        if (rs.with_rows):
            records = rs.fetchall()
        appearances = []
        for item in records:
            record = {}
            # record['ID'] = item[0]
            record['GameID'] = int(item[1])
            record['TeamID'] = int(item[2])
            record['PlayerID'] = int(item[3])
            record['TimeOn'] = item[4]
            record['TimeOff'] = item[5]
            record['Ejected'] = item[6]
            appearances.append(record)

        return appearances

    def saveDict(self, data, log):
        # Verify that data is a dictionary
        if not (isinstance(data, dict)):
            raise RuntimeError('saveDict requires a dictionary')

        if ('ID' in data):
            # Update
            log.message('Record ID provided - we update')
            sql = ('UPDATE tbl_gameminutes SET '
                   'GameID = %s, '
                   'TeamID = %s, '
                   'PlayerID = %s, '
                   'TimeOn = %s, '
                   'TimeOff = %s, '
                   'Ejected = %s '
                   'WHERE ID = %s')
            rs = self.db.query(sql, (
                data['GameID'],
                data['TeamID'],
                data['PlayerID'],
                data['TimeOn'],
                data['TimeOff'],
                data['Ejected'],
                data['ID']
            ))
        else:
            log.message('No Record ID provided - we insert')
            sql = ('INSERT INTO tbl_gameminutes '
                   '(GameID, TeamID, PlayerID, TimeOn, TimeOff, Ejected)'
                   'VALUES '
                   '(%s, %s, %s, %s, %s, %s)')
            rs = self.db.query(sql, (
                data['GameID'],
                data['TeamID'],
                data['PlayerID'],
                data['TimeOn'],
                data['TimeOff'],
                data['Ejected']
            ))
            log.message(str(rs))

        return True
