# -*- coding: utf-8 -*-
from __future__ import absolute_import

from database import Database
from log import Log
from spreadsheet import Spreadsheet


def checkFields(fields):
    log.message('Checking for required fields...')
    # These columns are required:
    requiredColumns = ([
        'MatchTime',
        'MatchTypeID',
        'HTeamID',
        'ATeamID'
    ])
    missingColumns = []

    for col in requiredColumns:
        if col not in fields:
            missingColumns.append(col)
    if (len(missingColumns) > 0):
        raise RuntimeError('Submitted data is missing the following columns: ' + str(missingColumns))

    return True


def prepareData(data, log):
    log.message('Preparing submitted data...')
    # Check that file has one worksheet
    log.message(str(len(data.data.sheets())) + ' sheets')
    if (len(source.data.sheets()) > 1):
        raise RuntimeError('Submitted data has more than one worksheet.')
    sheet = data.data.sheets()[0]

    # Check that file has at least one data row
    if (sheet.nrows < 2):
        raise RuntimeError('Submitted data has nothing to import.')

    # Summarize data size in the log
    log.message(str(sheet.nrows) + ' rows')
    log.message(str(sheet.ncols) + ' columns')

    return sheet


def importGame():
    return True


if __name__ == "__main__":

    # Initialize
    log = Log('logs/import_games.log')
    db = Database()
    db.connect()
    log.message('Started')

    # Read in CSV to data frame
    source = Spreadsheet('imports/games.xlsx')
    sheet = prepareData(source, log)

    # Check for validity of import - right fields?
    fields = source.fields()
    checkFields(fields)

    # Iterate over data, processing each line
    importGame()

    log.end()
    db.disconnect()

    print('Finished!')
