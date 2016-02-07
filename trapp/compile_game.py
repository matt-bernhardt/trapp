# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.compiler import Compiler
from trapp.gameevent import GameEvent
from trapp.gameminute import GameMinute
from trapp.gamestat import GameStat


class CompilerGames(Compiler):

    def assembleStatLine(self, record):
        # Takes a line in self.appearances and calculates data

        # Looking up event totals
        record = self.getEventSummary(record)

        # Calculating GP/GS/Min
        record['GP'] = 0
        record['GS'] = 0
        record['Min'] = 0
        record['RC'] = record['Ejected']
        if(record['TimeOn'] == 0 and record['TimeOff'] > 0):
            record['GS'] = 1
        if(record['TimeOff'] > 0):
            record['GP'] = 1
        record['Min'] = record['TimeOff'] - record['TimeOn']

        return record

    def doCompile(self):
        # The game stats compiler does the following:

        # 1) Assemble list of player appearances
        self.appearances = self.getAppearanceList()

        # 2) For each appearance, calculate summary statistics
        for item in self.appearances:
            item = self.assembleStatLine(item)

            # 3) Upsert those statistics as GameStat objects
            gs = GameStat()
            gs.connectDB()
            needle = {
                'GameID': item['GameID'],
                'TeamID': item['TeamID'],
                'PlayerID': item['PlayerID']
            }
            statID = gs.lookupID(needle, self.log)
            if len(statID) > 0:
                item['ID'] = statID[0]
            self.log.message(str(item))

            # 4) Goalkeeper stats
            # 5) Calculate plus/minus

            gs.saveDict(item, self.log)

        return True

    def getAppearanceList(self):
        gm = GameMinute()
        gm.connectDB()
        return gm.lookupIDlistByYear()

    def getEventSummary(self, item):
        ge = GameEvent()
        ge.connectDB()
        temp = ge.summarizeEvents(item, self.log)
        if(len(temp) == 0):
            temp = [{'Goals': 0, 'Ast': 0}]
        item = dict(item.items() + temp[0].items())
        return item
