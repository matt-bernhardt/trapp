# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class Game():

    def __init__(self):
        self.data = {}

    def connectDB(self):
        self.db = Database()
        self.db.connect()

    def disconnectDB(self):
        self.db.disconnect()
        self.db = None

    def loadByID(self, gameID):
        # Need to check that gameID is a single number
        sql = ('SELECT MatchTime, MatchTypeID, HTeamID, HScore, ATeamID, AScore, Duration, VenueID, Attendance, MeanTemperature '
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

    def saveDict(self, newData, log):
        # Verify that data is a dictionary
        if not (isinstance(newData, dict)):
            raise RuntimeError('saveDict requires a dictionary')

        # Format check

        # Do we need a sanity check?
        # - Teams don't play >1 game on same day
        # - ??

        # Check if dictionary contains a gameID
        if ('MatchID' in newData.keys()):
            # Update
            log.message('MatchID provided')
            sql = ('UPDATE tbl_games ')
        else:
            # Insert
            log.message('No MatchID')
            sql = ('INSERT INTO tbl_games '
                   '(MatchTime, MatchTypeID, HTeamID, ATeamID)'
                   'VALUES '
                   '(%s, %s, %s, %s)')
            rs = self.db.query(sql, (
                self.db.convertDate(newData['MatchTime']),
                newData['MatchTypeID'],
                newData['HTeamID'],
            #    newData['HScore'],
                newData['ATeamID'],
            #    newData['AScore'],
            #    newData['Duration'],
            #    newData['VenueID'],
            #    newData['Attendance'],
            #    newData['MeanTemperature'],
            ))

        return True

    def lookupID(self, data, log):
        # This takes a dictionary and validates it against existing records
        # Do we already have record of these teams playing on this date?
        # data must be a dictionary with the following keys:
        # - MatchTime (MM/DD/YYYY at least, time not needed)
        # - HTeamID (ID needed, not team name - these are too ambiguous)
        # - ATeamID (ID needed, not team name - these are too ambiguous)
        if not (isinstance(data, dict)):
            raise RuntimeError('saveDict requires a dictionary')

        # Check data for required fields
        missing = []
        required = ['MatchTime', 'HTeamID', 'ATeamID']
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError('Submitted data is missing the following fields: ' + str(missing))

        # See if any game matches these three terms
        sql = ('SELECT ID '
               'FROM tbl_games '
               'WHERE MatchTime = %s AND HTeamID = %s AND ATeamID = %s')
        rs = self.db.query(sql, (data, ))
        if (rs.with_rows):
            records = rs.fetchall()
        games = []
        for game in records:
            games.append(game['ID'])

        # How many games matched this data?
        if (len(games) == 1):
            self.data['MatchID'] = games[0]
            return True
        elif (len(games) > 1):
            # Found more than one game
            return False
        else:
            # Found no games that match
            return False
