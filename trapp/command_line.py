# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
import argparse
import trapp
from trapp.log import Log

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
		choices=['import','compile','render','qa'],
	)
	args = parser.parse_args()

	if (args.verb == 'import'):
		print('Importing...')
	elif (args.verb == 'compile'):
		print('Compiling...')
	elif (args.verb == 'render'):
		print('Rendering...')
	else:
		# qa
		print('Testing...')

	l = Log('trapp-' + args.verb + '.log')
	l.message('Does this work?')
	l.message(str(sys.argv))
	l.end()