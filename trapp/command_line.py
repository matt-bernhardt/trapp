# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
from trapp.database import Database
from trapp.log import Log
from trapp.importer import (
    ImporterGoals,
    ImporterLineups
)
from trapp.import_game import ImporterGames
from trapp.import_player import ImporterPlayers


def checkDB():
    print('Checking database connection\n')
    # Read and output the connection details
    db = Database()
    connection = db.loadConnection()
    print('Current credentials:')
    print('dbuser:   ' + str(connection['dbuser']))
    print('dbpwd:    ' + str(connection['dbpwd']))
    print('dbhost:   ' + str(connection['dbhost']))
    print('dbschema: ' + str(connection['dbschema']))
    print('')
    # Try to establish the connection
    print('Testing connection:')
    db.connect()
    print(str(db.cnx))
    print(str(db.cursor))
    print('Warnings: ' + str(db.warnings()))


def importGames(infile):
    # Feedback, setup
    print('Importing games from ' + str(infile))
    log = Log('trapp-import-games.log')
    importer = ImporterGames(infile, log)

    # Check for required fields
    requiredColumns = ([
        'MatchTime',
        'MatchTypeID',
        'HTeamID',
        'ATeamID',
        'VenueID'
    ])
    importer.checkFields(requiredColumns)

    # Do the import
    importer.doImport()

    # Shutdown
    log.end()

    return True


def importGoals(infile):
    # Feedback, setup
    print('Importing goals from ' + str(infile))
    log = Log('trapp-import-goals.log')
    importer = ImporterGoals(infile, log)

    # Check for required fields
    requiredColumns = ([
        'Code',
        'Date',
        'H/A',
        'Opponent',
        'Score',
        'Goals',
    ])
    importer.checkFields(requiredColumns)
    log.message('Required fields checked')

    # Do the import
    importer.doImport()
    log.message('Import done')

    # Shutdown
    log.end()


def importLineups(infile):
    # TODO: Lookup teams in a specified league and year?
    # TODO: Iterate over team list, with separate Importer for each?
    # Feedback, setup
    print('Importing lineups from ' + str(infile))
    log = Log('trapp-import-lineups.log')
    importer = ImporterLineups(infile, log)

    # Check for required fields
    requiredColumns = ([
        'Code',
        'Date',
        'H/A',
        'Opponent',
        'Score',
        'WDL',
        'Record',
        'Goals',
        'Lineup',
    ])
    importer.checkFields(requiredColumns)

    # Do the import
    importer.doImport()

    # Shutdown
    log.end()

    return True


def importPlayers(infile):
    # Feedback, setup
    print('Importing players from ' + str(infile))
    log = Log('trapp-import-players.log')
    importer = ImporterPlayers(infile, log)

    # Check for required fields
    requiredColumns = ([
        'FirstName',
        'LastName',
        'Position',
        'DOB',
        'Hometown'
    ])
    importer.checkFields(requiredColumns)

    # Do the import
    importer.doImport()

    # Shutdown
    log.end()

    return True


def main():
    # I'm imagining a few different verbs:
    # import: harvest data out of supplied files
    # - games
    # - lineups
    # - players
    # - ...etc
    #
    # compile: internal database operations, building summary tables and other
    #          calculated values
    # - summary statistics (GP, GS, Min, G, A, etc)
    # - plus/minus data (or other combinations)
    # - ...etc
    #
    # render: generate csv files, excel spreadsheets, or other images based on
    #         stored data
    # - ...etc
    #
    # qa: consistency checks
    #

    # Initialize argument parser
    parser = argparse.ArgumentParser(
        description=('Trapp is a Python library for linking, analyzing, '
                     'and extending soccer data. '
                     'https://github.com/matt-bernhardt/trapp')
    )
    parser.add_argument(
        'verb',
        choices=['check-db',
                 'import-games',
                 'import-goals',
                 'import-lineups',
                 'import-players',
                 'compile',
                 'render',
                 'qa'],
    )
    parser.add_argument(
        'infile',
        nargs='?',
        help='filename submitted along with verb',
        default='trapp/imports/import.xlsx'
    )
    # Need to add an optional filename argument
    args = parser.parse_args()

    if (args.verb == 'check-db'):
        checkDB()

    elif (args.verb == 'import-games'):
        importGames(args.infile)

    elif (args.verb == 'import-goals'):
        importGoals(args.infile)

    elif (args.verb == 'import-players'):
        importPlayers(args.infile)

    elif (args.verb == 'import-lineups'):
        importLineups(args.infile)

    elif (args.verb == 'compile'):
        print('Compiling...')

    elif (args.verb == 'render'):
        print('Rendering...')

    else:
        # qa
        print('Testing...')
