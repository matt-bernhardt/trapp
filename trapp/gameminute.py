# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class GameMinute():

    def __init__(self):
        self.data = {}

    def connectDB(self):
        self.db = Database()
        self.db.connect()

    def disconnectDB(self):
        self.db.disconnect()
        del self.db

    def lookupID(self, data, log):
        # Do we have a record of player X appearing in game Y for team Z?
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # Check data for required fields
        missing = []
        required = ['GameID', 'TeamID', 'PlayerID']
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError(
                'Submitted data is missing the following fields: ' +
                str(missing)
            )

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