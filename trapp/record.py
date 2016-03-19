# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


class Record():

    def __init__(self):
        self.data = {}
        self.data["ID"] = 0

    def connectDB(self):
        self.db = Database()
        self.db.connect()

    def disconnectDB(self):
        self.db.disconnect()
        del self.db

    def buildInsertClauses(self, data, fieldList):
        # Loops through sorted dictionary, data
        # Builds the relevant SQL fields and values.

        # Everything comes back in a clauses dictionary
        clauses = {}
        clauses["FieldNames"] = []
        clauses["FieldHolders"] = []
        clauses["FieldData"] = []

        for item in sorted(data):
            if (data[item] != '' and item in fieldList):
                clauses["FieldNames"].append(item)
                clauses["FieldHolders"].append('%s')
                if (item == 'DOB'):
                    clauses["FieldData"].append(
                        self.db.convertDate(data[item])
                    )
                else:
                    clauses["FieldData"].append(
                        data[item]
                    )

        return clauses

    def buildUpdateClauses(self, data, fieldList):
        # Loops through sorted dictionary, data
        # Builds the relevant SQL fields and values.

        # Everything comes back in a clauses dictionary
        clauses = {}
        clauses["FieldNames"] = []
        clauses["FieldData"] = []

        for item in sorted(data):
            if (data[item] != '' and item in fieldList):
                clauses["FieldNames"].append(item + ' = %s')
                if (item == 'DOB'):
                    clauses["FieldData"].append(
                        self.db.convertDate(data[item])
                    )
                else:
                    clauses["FieldData"].append(
                        data[item]
                    )

        return clauses

    def checkData(self, data, required):
        # This checks a submitted data dictionary for required fields.
        # 1) data must be a dictionary
        if not (isinstance(data, dict)):
            raise RuntimeError('lookupID requires a dictionary')

        # 2) data must have certain fields
        missing = []
        for term in required:
            if term not in data:
                missing.append(term)
        if (len(missing) > 0):
            raise RuntimeError(
                'Submitted data is missing the following fields: ' +
                str(missing)
            )
