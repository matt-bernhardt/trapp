# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class Player():

    def __init__(self):
        self.data = {}
        self.data["FirstName"] = ''
        self.data["LastName"] = ''
        self.data["ID"] = 0

    def loadByID(self, playerID):
        if not (isinstance(playerID, int)):
            raise RuntimeError('loadByID requires an integer')

        # This loads a player record by ID from a database.
        record = {"ID": 1, "FirstName": "Matt", "LastName": "Bernhardt"}
        self.data = record
        return True

    def lookupID(self, data, log):
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # check for required fields
        missing = []
        required = ['FirstName', 'LastName', 'DOB', 'Hometown']
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError('Submitted data is missing the following fields: ' + str(missing))

        # See if any game matches these three terms
        sql = ('SELECT ID '
               'FROM tbl_players '
               'WHERE FirstName = %s AND LastName = %s AND YEAR(DOB) = %s AND MONTH(DOB) = %s AND DAY(DOB) = %s AND Hometown = %s')
        rs = self.db.query(sql, (data['FirstName'], data['LastName'], data['DOB'][0], data['DOB'][1], data['DOB'][2], data['Hometown'], ))
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

        return True
