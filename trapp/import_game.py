# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.importer import Importer
from trapp.game import Game


class ImporterGames(Importer):

    def correctValues(self):
        for record in self.records:
            record['MatchTime'] = self.source.recoverDate(record['MatchTime'])

        return True

    def importRecord(self, record):
        self.log.message('Importing game ' + str(record))
        g = Game()
        g.connectDB()

        # Does the record exist?
        found = g.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            g.saveDict(record, self.log)
            self.imported += 1
        elif (len(found) == 1):
            record['MatchID'] = found[0]
            g.saveDict(record, self.log)
            self.imported += 1
        else:
            # Something(s) found, so we skip
            self.processMissingRecord(found, len(found))

        return True
