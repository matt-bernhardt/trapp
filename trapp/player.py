# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class Player():

    def __init__(self):
        self.data = {}
        self.data["FirstName"] = ''
        self.data["LastName"] = ''
        self.data["ID"] = 0

    def connectDB(self):
        self.db = Database()
        self.db.connect()

    def disconnectDB(self):
        self.db.disconnect()
        del self.db

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
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # check for required fields
        missing = []
        required = ['FirstName', 'LastName', 'Position', 'DOB', 'Hometown']
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError(
                'Submitted data is missing the following fields: '
                + str(missing)
            )

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
