from xlrd import open_workbook, xldate_as_tuple

class Spreadsheet():

    def __init__(self, file):
        self.data = open_workbook(file)

    def recoverDate(self, number):
        # This implements xlrd's 'xldate_as_tuple' method, which is then 
        # rebuilt as a 9-item tuple rather than 6. Because reasons.
        temp = xldate_as_tuple(number, 0)
        temp = (
            temp[0],
            temp[1],
            temp[2],
            temp[3],
            temp[4],
            temp[5],
            0,
            0,
            0
        )
        return temp

    def fields(self):
        # This assumes only one worksheet.
        # It returns a list of the values across the top of the first worksheet.
        self.fields = []
        sheet = self.data.sheets()[0]
        for col in range(sheet.ncols):
            self.fields.append(sheet.cell(0, col).value)
        return self.fields
