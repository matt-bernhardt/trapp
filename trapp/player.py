# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.record import Record


class Player(Record):

    # def __init__(self):
    #     self.data = {}
    #     self.data["FirstName"] = ''
    #     self.data["LastName"] = ''
    #     self.data["ID"] = 0

    def loadByID(self, playerID):
        if not (isinstance(playerID, int)):
            raise RuntimeError('loadByID requires an integer')

        sql = ('SELECT FirstName, '
               '  LastName, '
               '  Position, '
               '  RosterNumber, '
               '  Height_Feet, '
               '  Height_Inches, '
               '  Weight, '
               '  Birthplace, '
               '  Hometown, '
               '  Citizenship, '
               '  DOB '
               'FROM tbl_players p '
               'WHERE ID = %s')
        rs = self.db.query(sql, (playerID, ))
        if (rs.with_rows):
            records = rs.fetchall()

        # Assemble final dictionary
        self.data = {}
        for term in records:
            self.data['PlayerID'] = playerID
            self.data['FirstName'] = records[0][0]
            self.data['LastName'] = records[0][1]
            self.data['Position'] = records[0][2]
            self.data['RosterNumber'] = records[0][3]
            self.data['Height_Feet'] = records[0][4]
            self.data['Height_Inches'] = records[0][5]
            self.data['Weight'] = records[0][6]
            self.data['Birthplace'] = records[0][7]
            self.data['Hometown'] = records[0][8]
            self.data['Citizenship'] = records[0][9]
            self.data['DOB'] = records[0][10]

        return True

    def lookupID(self, data, log):
        # This takes a dictionary and validates it against existing records
        # Do we already have record of this player?
        # data must be a dictionary with the following keys:
        # - FirstName (string - may be blank for players with one name)
        # - LastName (string - players with one name use this)
        # - Position (string -
        #   'Goalkeeper', 'Defender', 'Midfielder', 'Forward')
        # - DOB (date object)
        # - Hometown ('City, ST' for US/Canada, 'City, Country' otherwise)
        required = ['FirstName', 'LastName', 'Position', 'DOB', 'Hometown']
        self.checkData(data, required)

        # See if any game matches these three terms
        sql = ('SELECT ID '
               'FROM tbl_players '
               'WHERE FirstName = %s '
               '  AND LastName = %s '
               '  AND Position = %s '
               '  AND YEAR(DOB) = %s '
               '  AND MONTH(DOB) = %s '
               '  AND DAY(DOB) = %s '
               '  AND Hometown = %s')
        rs = self.db.query(sql, (
            data['FirstName'],
            data['LastName'],
            data['Position'],
            data['DOB'][0],
            data['DOB'][1],
            data['DOB'][2],
            data['Hometown'],
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        players = []
        for player in records:
            players.append(player[0])

        # How many games matched this data?
        return players

    def lookupIDbyName(self, data, log):
        # This takes in a player's name and looks up player ID based on that
        # alone
        required = ['PlayerName']
        self.checkData(data, required)

        # See if any game matches these three terms
        sql = ('SELECT ID '
               'FROM tbl_players '
               'WHERE TRIM(CONCAT(FirstName," ",LastName)) = %s')
        rs = self.db.query(sql, (
            data['PlayerName'],
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        players = []
        for player in records:
            players.append(player[0])

        return players

    def lookupIDbyGoal(self, data, log):
        # This is meant for goalscorers. It takes in a player's last name,
        # GameID, and TeamID, minute and returns the ID of the player on the
        # field at that moment.

        required = ['playername', 'TeamID', 'GameID']
        self.checkData(data, required)

        # Perform lookup
        sql = ('SELECT p.ID '
               'FROM tbl_players p '
               'INNER JOIN tbl_gameminutes m ON p.ID = m.PlayerID '
               'WHERE p.LastName = %s '
               '  AND m.GameID = %s '
               '  AND m.TeamID = %s ')
        rs = self.db.query(sql, (
            data['playername'],
            data['GameID'],
            data['TeamID']
        ))
        if (rs.with_rows):
            records = rs.fetchall()
        players = []
        for player in records:
            players.append(player[0])
        return players

    def merge(self, fromID, intoID):
        # This merges one player record into another.
        # It includes all related tables.
        return False

    def saveDict(self, newData, log):
        if not (isinstance(newData, dict)):
            raise RuntimeError('saveDict requires a dictionary')
        log.message('Saving player record to database')

        if ('PlayerID' in newData.keys()):
            # Update
            log.message('  ...Updating')
            sql = ('')
        else:
            # Insert
            log.message('  ...Inserting')
            sql = ('INSERT INTO tbl_players '
                   '(FirstName, LastName, Position, DOB, Hometown) '
                   'VALUES '
                   '(%s, %s, %s, %s, %s)')
            rs = self.db.query(sql, (
                newData['FirstName'],
                newData['LastName'],
                newData['Position'],
                self.db.convertDate(newData['DOB']),
                newData['Hometown'],
            ))

        return True
