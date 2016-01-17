# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class GameEvent():

    def __init__(self):
        self.data = {}

    def connectDB(self):
        self.db = Database()
        self.db.connect()

    def disconnectDB(self):
        self.db.disconnect()
        del self.db

    def checkData(self, data, required):
        # This checks a submitted data dictionary for required fields.
        # 1) data must be a dictionary
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # 2) data must have certain fields
        missing = []
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError(
                'Submitted data is missing the following fields: ' +
                str(missing)
            )

    def lookupID(self, data, log):
        # Do we have a record of player X appearing in game Y for team Z?

        # Check submitted data for format and fields
        required = ['GameID', 'TeamID', 'PlayerID', 'MinuteID']
        self.checkData(data, required)

        sql = ('SELECT ID '
               'FROM tbl_gameevents '
               'WHERE GameID = %s '
               '  AND TeamID = %s '
               '  AND PlayerID = %s '
               '  AND MinuteID = %s')
        rs = self.db.query(sql, (
            data['GameID'],
            data['TeamID'],
            data['PlayerID'],
            data['MinuteID']
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        events = []
        for item in records:
            events.append(item[0])

        return events

    def saveDict(self, data, log):
        # Verify that data is a dictionary
        if not (isinstance(data, dict)):
            raise RuntimeError('saveDict requires a dictionary')

        if ('ID' in data):
            # Update
            log.message('Record ID provided - we update')
            sql = ('UPDATE tbl_gameevents SET '
                   'GameID = %s, '
                   'TeamID = %s, '
                   'PlayerID = %s, '
                   'MinuteID = %s, '
                   'Event = %s, '
                   'Notes = %s '
                   'WHERE ID = %s')
            rs = self.db.query(sql, (
                data['GameID'],
                data['TeamID'],
                data['PlayerID'],
                data['MinuteID'],
                data['Event'],
                data['Notes'],
                data['ID']
            ))
        else:
            log.message('No Record ID provided - we insert')
            sql = ('INSERT INTO tbl_gameevents '
                   '(GameID, TeamID, PlayerID, MinuteID, Event, Notes)'
                   'VALUES '
                   '(%s, %s, %s, %s, %s, %s)')
            rs = self.db.query(sql, (
                data['GameID'],
                data['TeamID'],
                data['PlayerID'],
                data['MinuteID'],
                data['Event'],
                data['Notes']
            ))
            log.message(str(rs))

        return True
