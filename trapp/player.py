from __future__ import absolute_import
# from trapp.database import Database


class Player():

    def __init__(self):
        self.data = {}
        self.data["FirstName"] = ''
        self.data["LastName"] = ''
        self.data["ID"] = 0

    def loadByID(self, playerID):
        # This loads a player record by ID from a database.
        record = {"ID": 1, "FirstName": "Matt", "LastName": "Bernhardt"}
        self.data = record
        return True

    def merge(self, fromID, intoID):
        # This merges one player record into another.
        # It includes all related tables.
        return False
