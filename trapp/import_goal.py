# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.importer import Importer
from trapp.game import Game
from trapp.gameevent import GameEvent
from trapp.player import Player


class ImporterGoals(Importer):

    def correctValues(self):
        # This takes in all rows of the imported spreadsheet, and performs
        # any needed repairs / adjustments

        # We can re-use the same Game object inside the loop
        g = Game()
        g.connectDB()

        self.log.message('Correcting values...')
        for record in self.records:

            # Log the record when we begin
            self.log.message('\nParsing game record:')
            # self.log.message('  ' + str(record) + '\n')

            # NewEvents holds the rebuilt event records - we create it this
            # early because the next step skips this record when no goals
            # are scored - and it still needs to be present.
            record['NewEvents'] = []

            # Games with no goals get skipped
            if (record['Goals'] == ''):
                continue

            # 1. TeamID lookup
            teamID = self.lookupTeamID(record['Team'])

            # 2. OpponentID lookup
            opponentID = self.lookupTeamID(record['Opponent'])

            # 3. Home or Away
            if (record['H/A'] == 'H'):
                homeID = teamID
                awayID = opponentID
            elif (record['H/A'] == 'A'):
                homeID = opponentID
                awayID = teamID

            # 4. The game date needs to be converted
            record['Date'] = self.source.recoverDate(record['Date'])

            # Use home/away ID and game date to look up the game ID
            needle = {
                'MatchTime': record['Date'],
                'HTeamID': homeID,
                'ATeamID': awayID,
            }
            self.log.message('  Looking up needle: ' + str(needle))
            game = g.lookupID(needle, self.log)

            self.log.message('  Found games: ' + str(game) + '\n')

            if (len(game) != 1):
                self.log.message('Found wrong number of games: ' +
                                 str(len(game)))
                self.skipped += 1
                # If we didn't find one gameID, then we abort processing this
                # game
                return False

            # Need to convert gameID from a list of 1 number to an integer
            game = game[0]

            # 5. The goalscorers string needs to be expanded
            record['Events'] = self.splitGoals(record['Goals'])
            # record['Events'] is now a list of strings. We now need to parse
            # each individual string into a dictionary.
            for item in record['Events']:
                item = self.parseOneGoal(item, game, teamID)
                for subitem in item:
                    record['NewEvents'].append(self.lookupPlayerID(subitem))

            # Log the corrected record for later inspection
            self.log.message('  Outcome:\n  ' + str(record))

        return True

    def disambiguatePlayers(self, record, result):
        # Ask user to provide player ID
        print('\nPlayerID lookup of _' + str(record['playername']) + '_' +
              ' failed with ' + str(len(result)) + ' records\n')
        print(str(record))
        newID = int(raw_input('Player ID - provide null or 0 to skip: '))

        return newID

    def importRecord(self, record):
        self.log.message('\nImporting record:\n  ' + str(record))

        for item in record['NewEvents']:
            self.log.message(str(item))

            # Skip over items
            if item is False:
                self.log.message('Skipping FALSE item')
                continue

            e = GameEvent()
            e.connectDB()

            eventID = e.lookupID(item, self.log)

            if (len(eventID) > 1):
                # We have more than one record of this player/team/game/minute.
                # This is a problem.
                self.errored += 1
            elif (len(eventID) == 1):
                # We already have a record of this event.
                # We add that eventID to ensure an update.
                item['ID'] = eventID[0]
                e.saveDict(item, self.log)
                self.updated += 1
            else:
                e.saveDict(item, self.log)
                self.imported += 1

        return True

    def lookupPlayerID(self, event):
        self.log.message('Looking up PlayerID for event:\n' + str(event))

        p = Player()
        p.connectDB()

        PlayerID = p.lookupIDbyGoal(event, self.log)

        if (len(PlayerID) != 1):
            # First step is to ask the user to disambiguate
            newID = self.disambiguatePlayers(event, PlayerID)
            PlayerID = []
            PlayerID.append(newID)

        if (PlayerID[0] == 0):
            # If PlayerID is still zero, mark it as missing
            self.processMissingRecord(event['playername'], len(PlayerID))
            return False

        event['PlayerID'] = PlayerID[0]
        return event

    def parseAssists(self, recordList, minute, assists, gameID, teamID):
        # This adds records to a list according to the assists in a string
        # describing a goal.

        # Split into a list, test its length
        test = assists.split(',')
        if (len(test) > 2):
            self.skipped += 1
            self.log.message('Found too many assists: ' +
                             str(test) + ' has ' + str(len(test)))
            return recordList

        # Parse each element in the list
        eventID = 2
        for item in test:
            item = item.strip()
            recordList.append({
                'GameID': gameID,
                'TeamID': teamID,
                'MinuteID': minute,
                'Event': eventID,
                'playername': item,
                'Notes': ''
            })
            eventID += 1

        return recordList

    def parseEventTime(self, inputString):
        candidate = inputString[inputString.rfind(' '):].strip()
        try:
            time = self.parseMinute(candidate)
        except ValueError:
            time = 0

        return time

    def parseOneGoal(self, inputString, gameID, teamID):
        # This takes in a string describing a single goal.
        # It returns a list of dictionaries, one for the goal and then up to
        # two for the assists.

        # Need to check format. Expects:
        # Lastname (Assist, Assist) Minute
        # If no assist, then:
        # Lastname (unassisted) Minute
        # If a penalty, then:
        # Lastname (penalty) Minute

        records = []

        # If there's no parenthesis, then increment skipped and head back
        if not (inputString.find('(')):
            self.skipped += 1
            return records

        begin = inputString.find('(')
        end = inputString.rfind(')')

        # Isolate player name and substitute
        playerName = inputString[:begin - 1].strip()

        # Isolate substitute name
        assistName = inputString[begin + 1:end].strip()

        event = 1
        notes = ''
        if assistName == 'penalty':
            notes = 'penalty kick'

        if assistName == 'own goal':
            notes = 'own goal'
            event = 6

        # Isolate minute
        minute = self.parseEventTime(inputString)

        records.append({
            'GameID': gameID,
            'TeamID': teamID,
            'MinuteID': minute,
            'Event': event,
            'playername': playerName,
            'Notes': notes
        })

        if (
            assistName != 'penalty' and
            assistName != 'unassisted' and
            assistName != 'own goal'
        ):
            records = self.parseAssists(
                records, minute, assistName, gameID, teamID
            )

        return records

    def splitGoals(self, inputString):
        # This takes ina string listing all goals scored in a game.
        # It returns a list, with each goal separated.
        # Downstream steps will perform additional parsing.
        self.log.message('  Parsing goal string: ' + str(inputString))
        events = []
        for goal in inputString.split(';'):
            events.append(goal.strip())
        self.log.message('  ' + str(events) + '\n')
        return events
