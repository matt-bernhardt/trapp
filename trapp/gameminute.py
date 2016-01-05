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
                data['MatchID'],
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
                data['MatchID'],
                data['TeamID'],
                data['PlayerID'],
                data['TimeOn'],
                data['TimeOff'],
                data['Ejected']
            ))
            log.message(str(rs))

        return True
