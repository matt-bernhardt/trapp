# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.compiler import Compiler


class CompilerGames(Compiler):

    def doCompile(self):
        self.log.message('Running compile')
        # The game stats compiler does the following:
        # 1) Assemble list of player appearances
        # 2) For each appearance, calculate summary statistics
        # 3) Upsert those statistics as GameStat objects
        return True
