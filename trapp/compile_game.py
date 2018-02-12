# -*- coding: utf-8 -*-
import time
from trapp.compiler import Compiler
from trapp.gameevent import GameEvent
from trapp.gameminute import GameMinute
from trapp.gamestat import GameStat


class CompilerGames(Compiler):

    def assemblePlusMinus(self, record):
        # Looks up plus/minus data for this appearance

        # Get eligible goals for this player in this game
        ge = GameEvent()
        ge.connectDB()
        impact = ge.summarizeRelevantGoals(record, self.log)

        # Transfer impact information to record
        record = dict(record, **impact[0])

        ge.disconnectDB()
        del ge

        return record

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
        print(("Processing " + str(len(self.appearances)) + " records"))
        self.log.message(str(len(self.appearances)) + " records\n")

        # 2) For each appearance:
        for item in self.appearances:

            # 3) Look up ID for this statline
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

            # 4) Calculate summary statistics
            item = self.assembleStatLine(item)

            # 5) Goalkeeper stats

            # 6) Calculate plus/minus
            item = self.assemblePlusMinus(item)

            # Save record in the log
            self.log.message(str(item))

            # 7) Upsert those statistics as GameStat objects
            gs.saveDict(item, self.log)

            self.log.message('')

            # Trying a delay to prevent buffer space problems
            time.sleep(0.01)

            gs.disconnectDB()
            del gs

        return True

    def getAppearanceList(self):
        gm = GameMinute()
        gm.connectDB()
        result = gm.lookupIDlistByYear()
        gm.disconnectDB()
        del gm
        return result

    def getEventSummary(self, item):
        ge = GameEvent()
        ge.connectDB()
        temp = ge.summarizeEvents(item, self.log)
        if(len(temp) == 0):
            temp = [{'Goals': 0, 'Ast': 0}]
        item = dict(list(item.items()) + list(temp[0].items()))
        ge.disconnectDB()
        del ge
        return item
