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
        conn = self.loadConnection()
        self.cnx = connector.connect(
            user=conn['dbuser'],
            password=conn['dbpwd'],
            host=conn['dbhost'],
            database=conn['dbschema']
        )
        self.cursor = self.cnx.cursor(buffered=True)

    def disconnect(self):
        self.cursor.close()
        self.cnx.close()

    def convertDate(self, date):
        # This converts a python date object into a MySQL-format date string
        return time.strftime('%Y-%m-%d %H:%M:%S', date)

    def lastInsertID(self):
        rs = self.query('SELECT LAST_INSERT_ID();', ())
        if (rs.with_rows):
            records = rs.fetchall()
        lastID = []
        for value in records:
            lastID.append(value[0])
        return lastID[0]

    def loadConnection(self):
        conn = {}
        conn['dbuser'] = os.getenv('TRAPP_DBUSER', connection.u)
        conn['dbpwd'] = os.getenv('TRAPP_DBPWD', connection.p)
        conn['dbhost'] = os.getenv('TRAPP_DBHOST', connection.h)
        conn['dbschema'] = os.getenv('TRAPP_DBSCHEMA', connection.d)
        return conn

    def query(self, query, params):
        self.cursor.execute(query, params)
        self.cnx.commit()
        return self.cursor

    def warnings(self):
        return self.cursor.fetchwarnings()
