# -*- coding: utf-8 -*-
from __future__ import absolute_import


class Compiler():

    def __init__(self, logFile):
        self.setLog(logFile)

    def setLog(self, log):
        self.log = log
        self.log.message('Log transferred')
