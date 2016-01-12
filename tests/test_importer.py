# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.log import Log
from trapp.importer import (
    Importer,
    ImporterGames,
    ImporterGoals,
    ImporterPlayers,
    ImporterLineups
)


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


# def test_importer_doImport(excel):
    # log = Log('test.log')
    # importer = Importer(excel, log)
    # assert importer.doImport() is True


def test_importer_parseGoals(excel):
    log = Log('test_parseGoals.log')
    importer = ImporterGoals(excel, log)
    goals = ""
    # assert importer.parseGoals(goals) == [{}]
    goals = "Player (unassisted) 78"
    assert importer.parseGoals(goals) == [{'playername': 'Player', 'minute': 78, 'eventID': 1}]
    goals = "Player (Potter) 78"
    assert importer.parseGoals(goals) == [{'playername': 'Player', 'minute': 78, 'eventID': 1}, {'playername': 'Potter', 'minute': 78, 'eventID': 2}]
    goals = "Player (Potter, Rains) 78"
    assert importer.parseGoals(goals) == [{'playername': 'Player', 'minute': 78, 'eventID': 1}, {'playername': 'Potter', 'minute': 78, 'eventID': 2}, {'playername': 'Potter', 'minute': 78, 'eventID': 3}]
    goals = "Player (unassisted) 78; Player (unassisted) 89"
    assert importer.parseGoals(goals) == [{'playername': 'Player', 'minute': 78, 'eventID': 1}, {'playername': 'Player', 'minute': 89, 'eventID': 1}]


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
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert hasattr(importer, 'starters') is False
    importer.parseLineup(lineup, game, team)
    assert hasattr(importer, 'starters') is True
    assert len(importer.starters) == 11


def test_importer_parseLineupFailsWhenShort(excel, lineup_short):
    game = 1
    team = 1
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    assert importer.errored == 0
    importer.parseLineup(lineup_short, game, team)
    assert importer.errored == 1


def test_importer_parsePlayer(excel, lineup):
    # Need to test parsePlayer's ability to deal with strings of player(s)
    game = 1
    team = 1
    log = Log('test.log')
    importer = ImporterLineups(excel, log)
    player = 'Sample Player'
    result = importer.parsePlayer(player, game, team)
    assert len(result) == 1
    assert result == [{'PlayerID': 15, 'PlayerName': 'Sample Player', 'TimeOn': 0, 'TimeOff': 90, 'Ejected': False, 'GameID': 1, 'TeamID': 1}]
    player = "Sample Player (Substitution 50')"
    result = importer.parsePlayer(player, game, team)
    assert len(result) == 2
    player = 'Sample Player (First Substitution 50 (Second Substitution 76))'
    result = importer.parsePlayer(player, game, team)
    assert len(result) == 3
    player = 'Sample Player (First Substitution 50 (Second Substitution 76 (Third Substitution 92+)))'
    result = importer.parsePlayer(player, game, team)
    assert len(result) == 4
    player = 'Sample Player (First Substitution 50 (Second Substitution 76 (Third Substitution 84 (sent off 88))))'
    result = importer.parsePlayer(player, game, team)
    assert len(result) == 4
    assert result[3]['PlayerName'] == 'Third Substitution'
    assert result[3]['Ejected'] is True
    assert result[3]['TimeOn'] == 84
    assert result[3]['TimeOff'] == 88

    # starter = 'Sample Player'
    # gameID = 1
    # teamID = 1
    # importer.parsePlayer(starter, gameID, teamID)


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


def test_importer_setLog(excel):
    log = Log('test.log')
    log2 = Log('test2.log')
    importer = Importer(excel, log)
    importer.setLog(log2)
    assert importer.log.name == 'test2.log'


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
