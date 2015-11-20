from __future__ import absolute_import
from database import Database


class Game():

    def __init__(self):
        self.data = {}
        self.db = Database()
        self.db.connect()

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

    def saveDict(self, newData):
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
            print('MatchID provided')
        else:
            # Insert
            print('No MatchID')

        return True
