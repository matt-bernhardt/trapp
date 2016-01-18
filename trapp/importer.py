# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.spreadsheet import Spreadsheet
from trapp.game import Game
from trapp.gameminute import GameMinute
from trapp.gameevent import GameEvent
from trapp.player import Player
from trapp.team import Team


class Importer():

    def __init__(self, importFile, logFile):
        # Counters for reporting outcomes
        self.imported = 0
        self.skipped = 0
        self.errored = 0
        # This probably needs to check the submitted file type and read in the
        # appropriate shim.
        # For now, though, only Excel spreadsheets are supported.
        self.source = Spreadsheet(importFile)
        self.fields = self.source.fields()
        self.checkData()
        self.setLog(logFile)

    def adjustStoppageTime(self, minute):
        # Remove +, cast to integer for numeric comparison
        minute = int(minute.replace('+', ''))

        # Correct to last break:
        # - A minute before the end of a game/extra time
        # - The exact minute for midpoints (45, 105)
        if (minute > 120):
            return 119
        elif (minute > 105):
            return 105
        elif (minute > 90):
            return 89

        return 45

    def checkFields(self, fields):
        # This checks the imported spreadsheet for a dictionary of required
        # fields
        missingFields = []

        for col in fields:
            if col not in self.fields:
                missingFields.append(col)
        if (len(missingFields) > 0):
            raise RuntimeError(
                'Submitted data is missing the following columns: ' +
                str(missingFields)
            )

        return True

    def checkData(self):
        # This performs basic integrity checks on the data to be imported

        # Check for one worksheet
        if (len(self.source.data.sheets()) > 1):
            raise RuntimeError('Submitted data has more than one worksheet.')
        self.sheet = self.source.data.sheets()[0]

        # Check for at least one data row
        if (self.sheet.nrows < 2):
            raise RuntimeError('Submitted data has nothing to import.')

        return True

    def correctValues(self):
        # This is overwritten in child objects depending on the corrective
        # steps needed with the data.
        return True

    def doImport(self):
        # Prepare records
        self.records = self.source.buildRecords()

        # Correct values
        self.correctValues()

        # Iterate over records
        [self.importRecord(record) for record in self.records]

        self.reportStatus()

        return True

    def importRecord(self, record):
        # This is overwritten in child objects
        print('Importing record ' + str(record))
        g = Game()
        g.connectDB()
        # Look up whether the record already exists
        found = g.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            g.saveDict(record, self.log)
        else:
            # Some other number of games was found
            print('Found ' + str(found) + ' games already exist')
        return True

    def lookupTeamID(self, teamname):
        team = Team()
        team.connectDB()
        teamID = team.lookupID({'teamname': teamname}, self.log)
        if (len(teamID) > 1):
            raise RuntimeError('Ambiguous team name: ' + str(teamname))
        elif (len(teamID) == 0):
            raise RuntimeError('Team not found: ' + str(teamname))
        # At this point we know teamID is a list of length 1, so we return
        # the first value only
        return teamID[0]

    def parseMinute(self, minute):
        # This reads in a string representing a minute denotation, and
        # adjusts it for format:
        # - removes ' characters
        # - detects + notations, and reduces value to the end of that period
        # It returns an integer

        # Cast to string so the next two steps don't fail
        minute = str(minute)

        # Remove ' if found
        minute = minute.replace("'", "")

        # Correct stoppage time back to end of that period
        # This assumes 45 minute halves, and 15 minute extra time periods
        # (those may not be valid assumptions)
        if (minute.find('+') > 0):
            minute = self.adjustStoppageTime(minute)

        # Cast back to integer
        minute = int(minute)
        return minute

    def setLog(self, log):
        self.log = log
        self.log.message('Log transferred')
        return True

    def reportStatus(self):
        self.log.message('\nImport results:')
        self.log.message(str(self.imported) + ' imported')
        self.log.message(str(self.skipped) + ' skipped')
        self.log.message(str(self.errored) + ' errored')
        print(str(self.imported) + ' imported')
        print(str(self.skipped) + ' skipped')
        print(str(self.errored) + ' errored')
        return True


class ImporterGames(Importer):

    def correctValues(self):
        for record in self.records:
            record['MatchTime'] = self.source.recoverDate(record['MatchTime'])

        return True

    def importRecord(self, record):
        self.log.message('Importing game ' + str(record))
        g = Game()
        g.connectDB()

        # Does the record exist?
        found = g.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            g.saveDict(record, self.log)
            self.imported += 1
        elif (len(found) == 1):
            record['MatchID'] = found[0]
            g.saveDict(record, self.log)
            self.imported += 1
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(len(found)) + ' matching games: ' +
                             str(found))
            self.skipped += 1

        return True


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
            record['NewEvents'] = []
            # record['Events'] is now a list of strings. We now need to parse
            # each individual string into a dictionary.
            for item in record['Events']:
                item = self.parseOneGoal(item, game, teamID)
                for subitem in item:
                    record['NewEvents'].append(self.lookupPlayerID(subitem))

            # Log the corrected record for later inspection
            self.log.message('  Outcome:\n  ' + str(record))

        return True

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
            self.imported += 1

        return True

    def lookupPlayerID(self, event):
        self.log.message('Looking up PlayerID for event:\n' + str(event))

        p = Player()
        p.connectDB()

        PlayerID = p.lookupIDbyGoal(event, self.log)

        if (len(PlayerID) != 1):
            self.log.message('Found wrong number of players with name ' +
                             '_' + str(event['playername']) + '_: ' +
                             str(PlayerID))
            self.skipped += 1
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
        begin = inputString.find('(')
        end = inputString.rfind(')')

        # If there's no parenthesis, then increment skipped and head back
        if not (inputString.find('(')):
            self.skipped += 1
            return records

        # Isolate player name and substitute
        playerName = inputString[:begin - 1].strip()

        # Isolate substitute name
        assistName = inputString[begin + 1:end].strip()

        notes = ''
        if assistName == 'penalty':
            notes = 'penalty kick'

        # Isolate minute
        minute = self.parseEventTime(inputString)

        records.append({
            'GameID': gameID,
            'TeamID': teamID,
            'MinuteID': minute,
            'Event': 1,
            'playername': playerName,
            'Notes': notes
        })

        if (assistName != 'penalty' and assistName != 'unassisted'):
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


class ImporterLineups(Importer):

    def adjustTimeOff(self, result, lastOff):
        sentOff = False

        # Need to track backwards through list, transferring timeoff
        for x in reversed(result):
            x['TimeOff'] = lastOff
            if (sentOff is True):
                x['Ejected'] = True
                sentOff = False
            if (x['PlayerName'] == 'sent off' or x['PlayerName'] == 'ejected'):
                result.remove(x)
                sentOff = True
            lastOff = x['TimeOn']

        return result

    def correctValues(self):
        for record in self.records:
            record['Date'] = self.source.recoverDate(record['Date'])
        return True

    def importPlayer(self, player):
        self.log.message(str(player))
        gm = GameMinute()
        gm.connectDB()
        appearanceID = gm.lookupID(player, self.log)
        if (len(appearanceID) > 1):
            # We have more than one record of this player/team/game.
            # This is a problem.
            self.errored += 1
        elif (len(appearanceID) == 1):
            # We already have a record of this player/team/game.
            # We add that appearanceID, to ensure an update operation.
            player['ID'] = appearanceID[0]
            gm.saveDict(player, self.log)
            self.imported += 1
        else:
            gm.saveDict(player, self.log)
            self.imported += 1
        return True

    def importRecord(self, record):
        self.log.message('Importing lineup ' + str(record))
        # Need to identify gameID
        g = Game()
        g.connectDB()

        # Team and Opponent ID
        teamID = self.lookupTeamID(record['Team'])
        opponentID = self.lookupTeamID(record['Opponent'])

        # Sort home/away teams
        if (record['H/A'] == 'H'):
            homeID = teamID
            awayID = opponentID
        elif (record['H/A'] == 'A'):
            homeID = opponentID
            awayID = teamID

        # Lookup this gameID
        needle = {
            'MatchTime': record['Date'],
            'HTeamID': homeID,
            'ATeamID': awayID,
        }
        game = g.lookupID(needle, self.log)

        self.log.message('Found games: ' + str(game))

        if (len(game) != 1):
            self.log.message('Found wrong number of games: ' + str(len(game)))
            self.skipped += 1
            # If we didn't find one gameID, then we abort processing this game
            return False

        # Need to convert gameID from a list of 1 number to an integer
        game = game[0]

        # Parse lineup string
        self.parseLineup(record['Lineup'], game, teamID)

        # At this point we have self.players - but need to store them
        [self.importPlayer(player) for player in self.players]

        return True

    def parseLineup(self, lineup, game, teamID):
        # Parses a long string of starters and substitutes, populating
        # self.players with records for each player who appeared in the
        # game.
        self.log.message(str(lineup))
        self.starters = lineup.split(',')
        if (len(self.starters) != 11):
            # We don't raise an error for a short lineup, as the records
            # can still be safely parsed and stored - just log for inspection
            # later.
            self.log.message('ERROR: Wrong number of starters')
            self.errored += 1

        # self.starters has strings for every starter, combined with any
        # substitutes or sendings off. These need to be split into separate
        # records for every player, which is done in parsePlayer
        self.players = []
        for starter in self.starters:
            batch = self.parsePlayer(starter, game, teamID)
            for item in batch:
                self.players.append(item)
        self.log.message(str(self.players))

        # This method returns nothing, as its work is recorded in
        # self.starters and self.players.

    def parsePlayerTimeOn(self, string):
        # This splits off the last word/blob in a player string, and parses
        # it as a time denotation. If it passes, this is the time the player
        # entered the game. If it is not a time, then it is the player's last
        # name, and they started the game.
        candidate = string[string.rfind(' '):].strip()
        try:
            timeon = self.parseMinute(candidate)
        except ValueError:
            timeon = 0
        return timeon

    def parsePlayerRemoveTime(self, string):
        # This strips away a time designation from a player string, and
        # returns only the player name.
        time = self.parsePlayerTimeOn(string)
        if (time > 0):
            return str(string[:string.rfind(' ')])
        return string

    def parsePlayer(self, starter, gameID, teamID):
        result = []
        timeoff = 90

        # Split the player string into a list
        result = self.parsePlayerSplit(starter)

        augmented = []
        # parse each member of the list
        for string in result:
            # Split time from player name
            timeon = self.parsePlayerTimeOn(string)
            player = self.parsePlayerRemoveTime(string).strip()

            # Look up playerID
            playerID = [0]
            if (player != 'sent off' and player != 'ejected'):
                p = Player()
                p.connectDB()
                needle = {
                    'PlayerName': player,
                }
                playerID = p.lookupIDbyName(needle, self.log)

            if (len(playerID) == 1):
                playerID = playerID[0]
                augmented.append({
                    'PlayerID': playerID,
                    'PlayerName': player,
                    'TimeOn': timeon,
                    'TimeOff': timeoff,
                    'Ejected': False,
                    'GameID': gameID,
                    'TeamID': teamID
                })
            else:
                self.skipped += 1
                self.log.message('_' + str(player) + '_ returned ' +
                                 str(len(playerID)) + ' matches')

        # Transfer timeon values to previous player's timeoff
        result = self.adjustTimeOff(augmented, timeoff)

        return result

    def parsePlayerSplit(self, inputString):
        # This takes in a string and splits it into a list. For example:
        # "Player Name" -> ["Player Name"]
        # "Player Name (Substitute 63)" -> ["Player Name", "Substitute 65"]
        # ... and so fort
        result = []

        while (inputString.find('(') > 0):
            # Find boundaries to split
            begin = inputString.find('(')
            end = inputString.rfind(')')
            # Perform the split
            outer = inputString[:begin - 1]
            inputString = inputString[begin + 1:end]
            # Append results
            result.append(outer)

        # Do stuff
        result.append(inputString)

        return result


class ImporterPlayers(Importer):

    def correctValues(self):
        for record in self.records:
            record['DOB'] = self.source.recoverDate(record['DOB'])

        return True

    def importRecord(self, record):
        self.log.message('Importing player ' + str(record))
        p = Player()
        p.connectDB()

        # Does the record exist?
        found = p.lookupID(record, self.log)
        if (len(found) == 0):
            # Nothing found, so we import
            p.saveDict(record, self.log)
            self.imported += 1
        else:
            # Something(s) found, so we skip
            self.log.message('Found ' + str(found) + ' matching players')
            self.skipped += 1

        return True
