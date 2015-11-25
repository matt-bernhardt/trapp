# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
from trapp.log import Log
from trapp.importer import Importer


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
        description='Where does this appear?'
    )
    parser.add_argument(
        'verb',
        choices=['import', 'import-games', 'import-players', 'compile', 'render', 'qa'],
    )
    parser.add_argument(
        'infile',
        nargs='?',
        help='filename submitted along with verb',
        default='trapp/imports/import.xlsx'
    )
    # Need to add an optional filename argument
    args = parser.parse_args()

    if (args.verb == 'import'):
        print('Importing...')

    elif (args.verb == 'import-games'):
        print('Importing games from ' + str(args.infile))
        log = Log('trapp-import-games.log')
        # sample trapp/imports/games.xlsx
        importer = Importer(args.infile, log)
        # Check for required fields
        requiredColumns = ([
            'MatchTime',
            'MatchTypeID',
            'HTeamID',
            'ATeamID'
        ])
        importer.checkFields(requiredColumns)
        importer.doImport()
        log.end()

    elif (args.verb == 'import-players'):
        print('Importing players from ' + str(args.infile))
        log = Log('trapp-import-players.log')
        # sample trapp/imports/players.xlsx
        importer = Importer(args.infile, log)
        requiredColumns = ([
            'FirstName',
            'LastName',
            'Position',
            'DOB',
            'Citizenship'
        ])
        importer.checkFields(requiredColumns)
        importer.doImport()
        log.end()

    elif (args.verb == 'compile'):
        print('Compiling...')

    elif (args.verb == 'render'):
        print('Rendering...')

    else:
        # qa
        print('Testing...')
