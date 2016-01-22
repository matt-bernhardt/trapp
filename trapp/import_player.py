# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.importer import Importer
from trapp.player import Player


class ImporterPlayers(Importer):

    def correctValues(self):
        for record in self.records:
            record['DOB'] = self.source.recoverDate(record['DOB'])

        return True

    def importRecord(self, record):
        self.log.message('Importing player ' + str(record))
        p = Player()
        p.connectDB()

        # Does the record exist?
        found = p.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            p.saveDict(record, self.log)
            self.imported += 1
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(found) + ' matching players')
            self.skipped += 1

        return True
