# -*- coding: utf-8 -*-
from __future__ import absolute_import

from database import Database
from log import Log
from spreadsheet import Spreadsheet


def checkData(data):
    log.message('Checking submitted file...')
    # This takes in a spreadsheet and performs needed verification steps

    # 1: Check that data is an xlrd book
    # log.message(str(type(data.data)))
    # if (type(data.data) is 'xlrd.book.Book'):
    #     raise RuntimeError('Submitted data is not a spreadsheet.')

    # 2: Check that data has only one worksheet
    log.message(str(len(data.data.sheets())) + ' sheets')
    if (len(data.data.sheets()) > 1):
        raise RuntimeError('Submitted data has more than one worksheet.')
    sheet = data.data.sheets()[0]

    # 3: Check that data has at least one data row
    if (sheet.nrows < 2):
        raise RuntimeError('Submitted data has nothing to import.')

    # 4: Check for required fields
    data.fields()
    requiredColumns = ([
        'MatchTime',
        'MatchTypeID',
        'HTeamID',
        'ATeamID'
    ])
    missingColumns = []
    for col in requiredColumns:
        if col not in data.fields:
            missingColumns.append(col)
    if (len(missingColumns) > 0):
        raise RuntimeError('Submitted data is missing the following columns: ' + str(missingColumns))

    log.message(str(sheet.nrows) + ' rows')
    log.message(str(sheet.ncols) + ' columns')
    log.message('')
    return sheet


def importGame(game):
    log.message('Importing game...')
    return True


if __name__ == "__main__":

    # Initialize
    log = Log('logs/import_games.log')
    db = Database()
    db.connect()
    log.message('Started')

    # Read in CSV to data frame
    source = Spreadsheet('imports/games.xlsx')

    # Check data for validity
    sheet = checkData(source)

    # Grab field names from first row
    fields = [sheet.cell(0, c).value for c in xrange(sheet.ncols)]

    # Iterate over data, processing each line
    records = []
    for row in xrange(1, sheet.nrows):
        d = {fields[col]: sheet.cell(row, col).value for col in xrange(sheet.ncols)}
        log.message(str(d))
        records.append(d)

    [importGame(game) for game in records]

    log.end()
    db.disconnect()

    print('Finished!')
