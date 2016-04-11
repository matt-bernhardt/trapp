# -*- coding: utf-8 -*-
from __future__ import absolute_import
import argparse
from trapp.database import Database
from trapp.log import Log
from trapp.check_games import CheckerGames
from trapp.check_minutes import CheckerMinutes
from trapp.compile_game import CompilerGames
from trapp.compile_teammate import CompilerTeammates
from trapp.import_game import ImporterGames
from trapp.import_goal import ImporterGoals
from trapp.import_lineup import ImporterLineups
from trapp.import_player import ImporterPlayers


def checkDB(args):
    print('Checking database connection\n')

    # Load the connection details
    db = Database()
    connection = db.loadConnection()

    # print out credentials in verbose mode
    if (args.verbose):
        print('Credentials:')
        print('dbuser:   ' + str(connection['dbuser']))
        print('dbpwd:    ' + str(connection['dbpwd']))
        print('dbhost:   ' + str(connection['dbhost']))
        print('dbschema: ' + str(connection['dbschema']))
        print('')

    # Try to establish the connection
    db.connect()

    # print result
    print(str(db.cnx))
    if (args.verbose):
        print(str(db.cursor))
        print('Warnings: ' + str(db.warnings()))


def checkGames(args):
    print('Checking game counts\n')

    # Start log
    log = Log('trapp-check-games.log')
    log.message('Started')

    # Output file
    output = Log('trapp-check-games.csv')

    c = CheckerGames(log, output)
    c.checkGames()

    output.end()

    log.end()


def checkMinutes(args):
    print('Checking minute totals\n')

    # Start log
    log = Log('trapp-check-minutes.log')
    log.message('Started')

    # Output file
    output = Log('trapp-check-minutes.csv')

    c = CheckerMinutes(log, output)
    c.checkMinutes()

    output.end()

    log.end()


def compileGames():
    # This is the compiler for game-level summary data
    # This is the first compilation step.
    print('Compiling games data')
    log = Log('trapp-compile-games.log')
    log.message('Compiling games data')
    c = CompilerGames(log)
    c.doCompile()
    log.end()


def compileTeammates():
    # This is the compiler for teammate networks
    # This is the fourth compilation step.
    print('Compiling teammates data')
    log = Log('trapp-compile-teammates.log')
    log.message('Compiling teammates data')
    c = CompilerTeammates(log)
    c.doCompile()
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


def verbCheck(args):
    # Manages all the check-* verbs
    if (args.verb == 'check-db'):
        checkDB(args)
    elif (args.verb == 'check-games'):
        checkGames(args)
    elif (args.verb == 'check-minutes'):
        checkMinutes(args)

    return True


def verbCompile(args):
    # Manages all the compile-* verbs
    if (args.verb == 'compile-games'):
        compileGames()

    elif (args.verb == 'compile-teammates'):
        compileTeammates()

    elif (args.verb == 'compile-years'):
        compileYears()

    return True


def verbImport(args):
    # Manages all the import-* verbs
    if (args.verb == 'import-games'):
        importGames(args.infile)

    elif (args.verb == 'import-goals'):
        importGoals(args.infile)

    elif (args.verb == 'import-players'):
        importPlayers(args.infile)

    elif (args.verb == 'import-lineups'):
        importLineups(args.infile)

    return True


def verbRender(args):
    if (args.verb == 'render'):
        print('Render placeholder')

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
                 'check-games',
                 'check-minutes',
                 'compile-games',
                 'compile-teammates',
                 'compile-years',
                 'import-games',
                 'import-goals',
                 'import-lineups',
                 'import-players',
                 'render',
                 'qa'],
    )
    parser.add_argument(
        'infile',
        nargs='?',
        help='filename submitted along with verb',
        default='trapp/imports/import.xlsx'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='toggle more verbose output, in log and to terminal',
        action="store_true"
    )
    # Need to add an optional filename argument
    args = parser.parse_args()

    if (args.verb[:5] == 'check'):
        # Run check
        verbCheck(args)

    elif (args.verb[:7] == 'compile'):
        # Run compile
        verbCompile(args)

    elif (args.verb[:6] == 'import'):
        # Run import
        verbImport(args)

    elif (args.verb[:6] == 'render'):
        verbRender(args)

    else:
        # qa
        print('Testing...')
