# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
from trapp.database import Database
from trapp.log import Log
from trapp.import_game import ImporterGames
from trapp.import_goal import ImporterGoals
from trapp.import_lineup import ImporterLineups
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


def compileGames():
    # This is the compiler for game-level summary data
    # This is the first compilation step.
    print('Compiling games data')
    log = Log('trapp-compile-games.log')
    log.message('Compiling games data')
    log.end()


def compileImpacts():
    # This is the compiler for plus/minus or impact data
    # This is the second compilation step.
    print('Compiling impacts data')
    log = Log('trapp-compile-impacts.log')
    log.message('Compiling impacts data')
    log.end()


def compileTeammates():
    # This is the compiler for teammate networks
    # This is the fourth compilation step.
    print('Compiling teammates data')
    log = Log('trapp-compile-teammates.log')
    log.message('Compiling teammates data')
    log.end()


def compileYears():
    # This is the compiler for year-level summary data
    # This is the third compilation step.
    print('Compiling years data')
    log = Log('trapp-compile-years.log')
    log.message('Compiling years data')
    log.end()


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
                 'compile-games',
                 'compile-impacts',
                 'compile-teammates',
                 'compile-years',
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

    elif (args.verb == 'compile'):
        compileGames()
        compileImpacts()
        compileYears()
        compileTeammates()

    elif (args.verb == 'compile-games'):
        compileGames()

    elif (args.verb == 'compile-impacts'):
        compileImpacts()

    elif (args.verb == 'compile-teammates'):
        compileTeammates()

    elif (args.verb == 'compile-years'):
        compileYears()

    elif (args.verb == 'import-games'):
        importGames(args.infile)

    elif (args.verb == 'import-goals'):
        importGoals(args.infile)

    elif (args.verb == 'import-players'):
        importPlayers(args.infile)

    elif (args.verb == 'import-lineups'):
        importLineups(args.infile)

    elif (args.verb == 'render'):
        print('Rendering...')

    else:
        # qa
        print('Testing...')
