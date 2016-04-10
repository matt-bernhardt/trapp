# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class Checker():

    def __init__(self, logFile, outputFile):
        # set log file
        self.setLog(logFile)
        # set output file
        self.setOutput(outputFile)
        # set database connection
        self.db = Database()
        self.db.connect()

    def setLog(self, log):
        self.log = log
        self.log.message('Log transferred')

    def setOutput(self, output):
        self.output = output
