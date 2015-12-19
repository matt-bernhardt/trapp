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

    def connect(self):
        try:
            dbuser = os.environ['trapp.dbuser']
            dbpwd = os.environ['trapp.dbpwd']
            dbhost = os.environ['trapp.dbhost']
            dbschema = os.environ['trapp.dbschema']
        except KeyError:
            dbuser = connection.u
            dbpwd = connection.p
            dbhost = connection.h
            dbschema = connection.d
        self.cnx = connector.connect(user=dbuser, password=dbpwd, host=dbhost, database=dbschema)
        self.cursor = self.cnx.cursor(buffered=True)

    def disconnect(self):
        self.cursor.close()
        self.cnx.close()

    def convertDate(self, date):
        # This converts a python date object into a MySQL-format date string
        return time.strftime('%Y-%m-%d %H:%M:%S', date)

    def query(self, query, params):
        self.cursor.execute(query, params)
        self.cnx.commit()
        return self.cursor

    def warnings(self):
        return self.cursor.fetchwarnings()
