# -*- coding: utf-8 -*-
from xlrd import open_workbook


class Spreadsheet():

    def __init__(self, file):
        self.data = open_workbook(file)

    def fields(self):
        # This assumes only one worksheet.
        # It returns a list of the values across the top of the first worksheet.
        self.fields = []
        sheet = self.data.sheets()[0]
        for col in range(sheet.ncols):
            self.fields.append(sheet.cell(0, col).value)
        return self.fields
