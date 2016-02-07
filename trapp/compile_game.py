# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.compiler import Compiler
from trapp.gameminute import GameMinute


class CompilerGames(Compiler):

    def doCompile(self):
        self.log.message('Running compile')
        # The game stats compiler does the following:
        # 1) Assemble list of player appearances
        self.appearances = self.getAppearanceList()
        for item in self.appearances:
            self.log.message(str(item))
        # 2) For each appearance, calculate summary statistics
        # 3) Upsert those statistics as GameStat objects
        return True

    def getAppearanceList(self):
        gm = GameMinute()
        gm.connectDB()
        return gm.lookupIDlistByYear()
