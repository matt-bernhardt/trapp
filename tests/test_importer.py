# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.log import Log
from trapp.importer import Importer
from trapp.import_game import ImporterGames
from trapp.import_goal import ImporterGoals
from trapp.import_lineup import ImporterLineups
from trapp.import_player import ImporterPlayers


def test_importer_init(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert isinstance(importer, Importer)
    assert importer.log.name == 'test.log'


def test_importer_correctValues(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert importer.correctValues() is True


def test_importer_checkData_sheets(excel_sheets):
    with pytest.raises(RuntimeError) as excinfo:
        log = Log('test.log')
        importer = Importer(excel_sheets, log)
    assert 'more than one worksheet' in str(excinfo.value)


def test_importer_checkFields_empty(excel_empty):
    with pytest.raises(RuntimeError) as excinfo:
        log = Log('test.log')
        importer = Importer(excel_empty, log)
    assert 'nothing to import' in str(excinfo.value)


def test_importer_checkFields(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    requiredFields = (['foo', 'bar'])
    assert importer.checkFields(requiredFields) is True
    with pytest.raises(RuntimeError) as excinfo:
        requiredFields = (['foo', 'none'])
        importer.checkFields(requiredFields)
    assert 'missing the following columns' in str(excinfo.value)


def test_importer_generic_importRecord(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    dummyRecord = 'Dummy Record'
    assert importer.importRecord(dummyRecord) is True


# def test_importer_doImport(excel):
    # log = Log('test.log')
    # importer = Importer(excel, log)
    # assert importer.doImport() is True


def test_importer_lookupPlayerID(excel):
    log = Log('test.log')
    importer = ImporterGoals(excel, log)
    # We don't worry about invalid data formats, as those are caught by player object
    event = {'playername': 'Man', 'TeamID': 2, 'GameID': 1}
    event = importer.lookupPlayerID(event)
    assert event['PlayerID'] == 3
    assert importer.skipped == 0
    event = {'playername': 'Invalid Player', 'TeamID': 2, 'GameID': 1}
    assert importer.lookupPlayerID(event) is False
    assert importer.skipped == 1


def test_importer_lookupTeamID(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    needle = 'Columbus Crew'
    assert importer.lookupTeamID(needle) == 1
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Columbus Magic'
        importer.lookupTeamID(needle)
    assert 'Team not found: ' in str(excinfo.value)
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Duplicate Sample Team'
        importer.lookupTeamID(needle)
    assert 'Ambiguous team name: ' in str(excinfo.value)


def test_importer_parseAssists(excel):
    log = Log('test_parseAssists.log')
    importer = ImporterGoals(excel, log)
    game = 1
    team = 1
    # Test single assist
    record = []
    minute = 78
    assists = 'Player'
    assert importer.parseAssists(record, minute, assists, game, team) == [{'GameID': 1, 'TeamID': 1, 'playername': 'Player', 'MinuteID': 78, 'Event': 2, 'Notes': ''}]
    # Test two assists
    record = []
    assists = 'Player,Potter'
    assert importer.parseAssists(record, minute, assists, game, team) == [{'GameID': 1, 'TeamID': 1, 'playername': 'Player', 'MinuteID': 78, 'Event': 2, 'Notes': ''}, {'GameID': 1, 'TeamID': 1, 'playername': 'Potter', 'MinuteID': 78, 'Event': 3, 'Notes': ''}]
    # Test too many assists
    record = []
    assert importer.skipped == 0
    assists = 'Player,Potter,Rains'
    assert importer.parseAssists(record, minute, assists, game, team) == []
    assert importer.skipped == 1


def test_importer_parseOneGoal(excel):
    log = Log('test.log')
    importer = ImporterGoals(excel, log)
    game = 1
    team = 1
    goals = ""
    # assert importer.parseGoals(goals) == [{}]
    goals = "Player (unassisted) 78"
    assert importer.parseOneGoal(goals, game, team) == [{'playername': 'Player', 'MinuteID': 78, 'Event': 1, 'Notes': '', 'GameID': 1, 'TeamID': 1}]
    goals = "Player (penalty) 78"
    assert importer.parseOneGoal(goals, game, team) == [{'playername': 'Player', 'MinuteID': 78, 'Event': 1, 'Notes': 'penalty kick', 'GameID': 1, 'TeamID': 1}]
    goals = "Player (Potter) 78"
    assert importer.parseOneGoal(goals, game, team) == [{'playername': 'Player', 'MinuteID': 78, 'Event': 1, 'Notes': '', 'GameID': 1, 'TeamID': 1}, {'playername': 'Potter', 'MinuteID': 78, 'Event': 2, 'Notes': '', 'GameID': 1, 'TeamID': 1}]
    goals = "Player (Potter, Rains) 78"
    assert importer.parseOneGoal(goals, game, team) == [{'playername': 'Player', 'MinuteID': 78, 'Event': 1, 'Notes': '', 'GameID': 1, 'TeamID': 1}, {'playername': 'Potter', 'MinuteID': 78, 'Event': 2, 'Notes': '', 'GameID': 1, 'TeamID': 1}, {'playername': 'Rains', 'MinuteID': 78, 'Event': 3, 'Notes': '', 'GameID': 1, 'TeamID': 1}]
    goals = "Player (own goal) 78"
    assert importer.parseOneGoal(goals, game, team) == [{'playername': 'Player', 'MinuteID': 78, 'Event': 6, 'Notes': 'own goal', 'GameID': 1, 'TeamID': 1}]


def test_importer_parseMinuteDoesNothing(excel):
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert importer.parseMinute(15) == 15
    assert importer.parseMinute(unicode(45)) == 45
    assert importer.parseMinute('89') == 89


def test_importer_parseMinuteRemovesSingleQuote(excel):
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert importer.parseMinute("64'") == 64


def test_importer_parseMinuteFixesStoppageTime(excel):
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert importer.parseMinute('46+') == 45
    assert importer.parseMinute('91+') == 89
    assert importer.parseMinute('106+') == 105
    assert importer.parseMinute('122+') == 119


def test_importer_parseLineup(excel, lineup):
    game = 1
    team = 1
    duration = 90
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert hasattr(importer, 'starters') is False
    importer.parseLineup(lineup, game, team, duration)
    assert hasattr(importer, 'starters') is True
    assert len(importer.starters) == 11


def test_importer_parseLineupFailsWhenShort(excel, lineup_short):
    game = 1
    team = 1
    duration = 90
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert importer.errored == 0
    importer.parseLineup(lineup_short, game, team, duration)
    assert importer.errored == 1


def test_importer_parsePlayer(excel, lineup):
    # Need to test parsePlayer's ability to deal with strings of player(s)
    game = 1
    team = 1
    duration = 90
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    player = 'Sample Player'
    result = importer.parsePlayer(player, game, team, duration)
    assert len(result) == 1
    assert result == [{'PlayerID': 15, 'PlayerName': 'Sample Player', 'TimeOn': 0, 'TimeOff': 90, 'Ejected': False, 'GameID': 1, 'TeamID': 1}]
    player = "Sample Player (Substitution 50')"
    result = importer.parsePlayer(player, game, team, duration)
    assert len(result) == 2
    player = 'Sample Player (First Substitution 50 (Second Substitution 76))'
    result = importer.parsePlayer(player, game, team, duration)
    assert len(result) == 3
    player = 'Sample Player (First Substitution 50 (Second Substitution 76 (Third Substitution 92+)))'
    result = importer.parsePlayer(player, game, team, duration)
    assert len(result) == 4
    player = 'Sample Player (First Substitution 50 (Second Substitution 76 (Third Substitution 84 (sent off 88))))'
    result = importer.parsePlayer(player, game, team, duration)
    assert len(result) == 4
    assert result[3]['PlayerName'] == 'Third Substitution'
    assert result[3]['Ejected'] is True
    assert result[3]['TimeOn'] == 84
    assert result[3]['TimeOff'] == 88


def test_importer_parsePlayerRemoveTime(excel, lineup):
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    player = 'Sample Player'
    player = importer.parsePlayerRemoveTime(player)
    assert player == 'Sample Player'
    player = 'Sample Player 56'
    player = importer.parsePlayerRemoveTime(player)
    assert player == 'Sample Player'


def test_importer_parsePlayerSplit(excel):
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    string = 'Player Name'
    assert importer.parsePlayerSplit(string) == ['Player Name']
    string = 'Player Name (Substitute 63)'
    assert importer.parsePlayerSplit(string) == ['Player Name', 'Substitute 63']
    string = 'Sample Player (First Substitution 50 (Second Substitution 76 (Third Substitution 84 (sent off 88))))'
    assert importer.parsePlayerSplit(string) == ['Sample Player', 'First Substitution 50', 'Second Substitution 76', 'Third Substitution 84', 'sent off 88']


def test_importer_processMissingRecords(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert len(importer.missing) == 0
    assert importer.skipped == 0
    importer.processMissingRecord('Missing Record', 0)
    assert len(importer.missing) == 1
    assert importer.skipped == 1
    importer.processMissingRecord('Another Missing Record', 0)
    assert len(importer.missing) == 2
    assert importer.skipped == 2
    importer.processMissingRecord('Missing Record', 0)
    assert len(importer.missing) == 2
    assert importer.skipped == 3


def test_importer_reportStatus(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    # Still working out how best to test this method - all it does is write
    # content out to log files, no calculation
    assert importer.reportStatus() is True
    importer.missing = ['Missing Record']
    assert importer.reportStatus() is True


def test_importer_setLog(excel):
    log = Log('test.log')
    log2 = Log('test2.log')
    importer = Importer(excel, log)
    importer.setLog(log2)
    assert importer.log.name == 'test2.log'


def test_importer_splitGoals(excel):
    log = Log('test.log')
    importer = ImporterGoals(excel, log)
    goals = "Player (Potter, Rains) 78"
    assert importer.splitGoals(goals) == ['Player (Potter, Rains) 78']
    goals = "Player (unassisted) 78; Player (unassisted) 89"
    assert importer.splitGoals(goals) == ['Player (unassisted) 78', 'Player (unassisted) 89']


def test_importerGames(excel_games):
    log = Log('test.log')
    importer = ImporterGames(excel_games, log)
    requiredColumns = ([
        'MatchTime',
        'MatchTypeID',
        'HTeamID',
        'ATeamID',
        'VenueID'
    ])
    assert importer.checkFields(requiredColumns) is True
    assert importer.doImport() is True


def test_importerPlayers(excel_players):
    log = Log('test.log')
    importer = ImporterPlayers(excel_players, log)
    requiredColumns = ([
        'FirstName',
        'LastName',
        'Position',
        'DOB',
        'Hometown'
    ])
    assert importer.checkFields(requiredColumns) is True
    assert importer.doImport() is True
