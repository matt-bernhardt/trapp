# -*- coding: utf-8 -*-
from __future__ import absolute_import
from mysql import connector
import trapp.connection as connection
import time
import os


class Database():

    def __init__(self):
        self.cnx = ''
        self.cursor = ''
        self.conn = {}

    def connect(self):
        self.lookupConnection()
        self.cnx = connector.connect(user=self.conn['user'], password=self.conn['pwd'], host=self.conn['host'], database=self.conn['schema'])
        self.cursor = self.cnx.cursor(buffered=True)

    def disconnect(self):
        self.cursor.close()
        self.cnx.close()

    def convertDate(self, date):
        # This converts a python date object into a MySQL-format date string
        return time.strftime('%Y-%m-%d %H:%M:%S', date)

    def lookupConnection(self):
        try:
            self.conn['user'] = os.environ['trapp.dbuser']
            self.conn['pwd'] = os.environ['trapp.dbpwd']
            self.conn['host'] = os.environ['trapp.dbhost']
            self.conn['schema'] = os.environ['trapp.dbschema']
        except KeyError:
            self.conn['user'] = connection.u
            self.conn['pwd'] = connection.p
            self.conn['host'] = connection.h
            self.conn['schema'] = connection.d
        print(str(self.conn))
        return True

    def query(self, query, params):
        self.cursor.execute(query, params)
        self.cnx.commit()
        return self.cursor

    def warnings(self):
        return self.cursor.fetchwarnings()
