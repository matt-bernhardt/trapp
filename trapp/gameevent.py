# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.record import Record


class GameEvent(Record):

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

    def summarizeEvents(self, data, log):
        # Build a summary of events for a player in a game (for a team)

        # Check submitted data for format and fields
        required = ['GameID', 'TeamID', 'PlayerID']
        self.checkData(data, required)

        sql = ('SELECT SUM(IF(Event=1,1,0)) AS Goals, '
               '  SUM(IF(Event IN (2,3),1,0)) AS Ast '
               'FROM tbl_gameevents '
               'WHERE GameID = %s '
               '  AND TeamID = %s '
               '  AND PlayerID = %s '
               'GROUP BY GameID, TeamID, PlayerID')
        rs = self.db.query(sql, (
            data['GameID'],
            data['TeamID'],
            data['PlayerID']
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        events = []
        for item in records:
            record = {}
            record['Goals'] = int(item[0])
            record['Ast'] = int(item[1])
            events.append(record)

        return events

    def summarizeRelevantGoals(self, data, log):
        # Build a summary of goals that occurred during a player's time on the
        # field

        # Check submitted data for format and fields
        required = ['GameID', 'TimeOn', 'TimeOff']
        self.checkData(data, required)

        sql = ('SELECT '
               '  SUM(IF((TeamID = %s AND Event = 1) OR '
               '     (TeamID <> %s AND Event = 6), 1, 0)) AS Plus, '
               '  SUM(IF((TeamID <> %s AND Event = 1) OR '
               '     (TeamID = %s AND Event = 6), 1, 0)) AS Minus '
               'FROM tbl_gameevents '
               'WHERE GameID = %s '
               '  AND MinuteID >= %s '
               '  AND MinuteID < %s'
               '  AND (Event = 1 OR Event = 6) '
               'ORDER BY MinuteID ASC')
        rs = self.db.query(sql, (
            data['TeamID'],
            data['TeamID'],
            data['TeamID'],
            data['TeamID'],
            data['GameID'],
            data['TimeOn'],
            data['TimeOff']
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        events = []
        for item in records:
            record = {}
            record['Plus'] = 0 if item[0] is None else int(item[0])
            record['Minus'] = 0 if item[1] is None else int(item[1])
            events.append(record)

        return events
