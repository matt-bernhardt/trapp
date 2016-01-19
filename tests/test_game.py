# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.game import Game
from trapp.log import Log


def test_game_init():
    g = Game()
    # object types
    assert isinstance(g, Game)
    assert isinstance(g.data, dict)
    # Default values


def test_game_connect():
    g = Game()
    assert hasattr(g, 'db') is False
    g.connectDB()
    assert hasattr(g, 'db')


def test_game_disconnect():
    g = Game()
    g.connectDB()
    assert hasattr(g, 'db')
    g.disconnectDB()
    assert hasattr(g, 'db') is False


def test_game_loadByID():
    g = Game()
    g.connectDB()

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        g.loadByID(needle)
    assert 'loadByID requires an integer' in str(excinfo.value)

    needle = 1
    g.loadByID(needle)
    assert isinstance(g.data, dict)
    assert g.data['HTeamID'] == 1
    assert g.data['ATeamID'] == 2


def test_game_lookupDuration():
    g = Game()
    g.connectDB()
    log = Log('test_lookupDuration.log')

    # Standard-duration game is 90 minutes
    needle = 1
    assert g.lookupDuration(needle, log) == 90


def test_game_saveDict():
    # Setup
    log = Log('test.log')
    g = Game()
    g.connectDB()

    # This should raise an error
    with pytest.raises(RuntimeError) as excinfo:
        testRecord = "fake player record"
        g.saveDict(testRecord, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # This should work
    sample = {
        'MatchTime': (1980, 1, 1, 19, 30, 0, 0, 0, 0),
        'MatchTypeID': 21,
        'HTeamID': 11,
        'HScore': 0,
        'ATeamID': 12,
        'AScore': 0,
        'VenueID': 1,
    }
    assert g.saveDict(sample, log) is True
    assert g.db.warnings() is None


def test_game_lookupID():
    # Setup
    log = Log('test.log')
    g = Game()
    g.connectDB()

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = '1996-04-13'
        g.lookupID(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should raise a missing-fields error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'MatchTime': '1996-04-13',
            'HTeamID': 11
        }
        g.lookupID(needle, log)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)

    # This should bring back one record
    needle = {
        'MatchTime': (1980, 1, 1, 0, 0, 0, 0, 0, 0),
        'HTeamID': 11,
        'ATeamID': 12
    }
    assert len(g.lookupID(needle, log)) >= 1
