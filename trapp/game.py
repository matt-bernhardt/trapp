# -*- coding: utf-8 -*-
from trapp.record import Record


class Game(Record):

    def loadByID(self, gameID):
        # Verify that gameID is an integer
        if not (isinstance(gameID, int)):
            raise RuntimeError('loadByID requires an integer')

        # Need to check that gameID is a single number
        sql = ('SELECT '
               '  MatchTime, '
               '  MatchTypeID, '
               '  HTeamID, '
               '  HScore, '
               '  ATeamID, '
               '  AScore, '
               '  Duration, '
               '  VenueID, '
               '  Attendance, '
               '  MeanTemperature '
               'FROM tbl_games g '
               'WHERE ID = %s')
        rs = self.db.query(sql, (gameID, ))
        if (rs.with_rows):
            records = rs.fetchall()

        # Assemble final dictionary
        self.data = {}
        for term in records:
            self.data['MatchID'] = gameID
            self.data['MatchTime'] = records[0][0]
            self.data['MatchTypeID'] = records[0][1]
            self.data['HTeamID'] = records[0][2]
            self.data['HScore'] = records[0][3]
            self.data['ATeamID'] = records[0][4]
            self.data['AScore'] = records[0][5]
            self.data['Duration'] = records[0][6]
            self.data['VenueID'] = records[0][7]
            self.data['Attendance'] = records[0][8]
            self.data['MeanTemperature'] = records[0][9]
        return True

    def lookupDuration(self, gameID, log):
        # This looks up a recorded game duration, for use in an importer
        # or possibly a rendering step
        log.message('Looking up duration of game ' + str(gameID))
        duration = 0
        sql = ('SELECT Duration '
               'FROM tbl_games '
               'WHERE ID = %s')
        rs = self.db.query(sql, (
            gameID,
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        for item in records:
            duration = item[0]
        log.message('Game ' + str(gameID) + ' had a duration of ' +
                    str(duration) + ' minutes')
        return duration

    def lookupID(self, data, log):
        # This takes a dictionary and validates it against existing records
        # Do we already have record of these teams playing on this date?
        # data must be a dictionary with the following keys:
        # - MatchTime (MM/DD/YYYY at least, time not needed)
        # - HTeamID (ID needed, not team name - these are too ambiguous)
        # - ATeamID (ID needed, not team name - these are too ambiguous)

        # Check for required parameters
        required = ['MatchTime', 'HTeamID', 'ATeamID']
        self.checkData(data, required)

        # See if any game matches these three terms
        sql = ('SELECT ID '
               'FROM tbl_games '
               'WHERE YEAR(MatchTime) = %s '
               '  AND MONTH(MatchTime) = %s '
               '  AND DAY(MatchTime) = %s '
               '  AND HTeamID = %s '
               '  AND ATeamID = %s')
        rs = self.db.query(sql, (
            data['MatchTime'][0],
            data['MatchTime'][1],
            data['MatchTime'][2],
            data['HTeamID'],
            data['ATeamID'],
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        games = []
        for game in records:
            games.append(game[0])

        # How many games matched this data?
        return games

    def saveDict(self, newData, log):
        # Verify that data is a dictionary
        if not (isinstance(newData, dict)):
            raise RuntimeError('saveDict requires a dictionary')

        # Format check

        # Do we need a sanity check?
        # - Teams don't play >1 game on same day
        # - ??

        # Check if dictionary contains a gameID
        if ('MatchID' in list(newData.keys())):
            # Update
            log.message('MatchID provided')
            sql = ('UPDATE tbl_games SET '
                   'MatchTime = %s, '
                   'MatchTypeID = %s, '
                   'HTeamID = %s, '
                   'ATeamID = %s, '
                   'VenueID = %s '
                   'WHERE ID = %s')
            rs = self.db.query(sql, (
                self.db.convertDate(newData['MatchTime']),
                newData['MatchTypeID'],
                newData['HTeamID'],
                newData['ATeamID'],
                newData['VenueID'],
                newData['MatchID'],
            ))
        else:
            # Insert
            log.message('No MatchID')
            sql = ('INSERT INTO tbl_games '
                   '(MatchTime, MatchTypeID, HTeamID, ATeamID, VenueID)'
                   'VALUES '
                   '(%s, %s, %s, %s, %s)')
            rs = self.db.query(sql, (
                self.db.convertDate(newData['MatchTime']),
                newData['MatchTypeID'],
                newData['HTeamID'],
                #    newData['HScore'],
                newData['ATeamID'],
                #    newData['AScore'],
                #    newData['Duration'],
                newData['VenueID'],
                #    newData['Attendance'],
                #    newData['MeanTemperature'],
            ))

        return True
