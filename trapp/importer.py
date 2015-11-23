# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.spreadsheet import Spreadsheet


class Importer():

    def __init__(self, importFile):
        # This probably needs to check the submitted file type and read in the
        # appropriate shim.
        # For now, though, only Excel spreadsheets are supported.
        self.source = Spreadsheet(importFile)

    def checkFields(self, fields):
        # This checks the imported spreadsheet for a dictionary of required fields
        return True
