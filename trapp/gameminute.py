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
