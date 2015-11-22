# -*- coding: utf-8 -*-
from __future__ import absolute_import
import mysql.connector
from trapp.connection import connection
import time


class Database():

    def __init__(self):
        self.cnx = ''
        self.cursor = ''

    def connect(self):
        self.cnx = mysql.connector.connect(user=connection.u, password=connection.p, host=connection.h, database=connection.d)
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
