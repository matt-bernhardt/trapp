# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.checker import Checker


class CheckerMinutes(Checker):

    def checkMinutes(self):
        self.log.message('Starting work...')