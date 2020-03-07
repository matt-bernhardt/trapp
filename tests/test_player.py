# -*- coding: utf-8 -*-
import pytest
from trapp.player import Player
from trapp.log import Log
import datetime


def test_player_init():
    p = Player()
    # object types
    assert isinstance(p, Player)
    assert isinstance(p.data, dict)
    # Default values
    assert p.data['ID'] == 0


def test_player_connect():
    p = Player()
    assert hasattr(p, 'db') is False
    p.connectDB()
    assert hasattr(p, 'db')


def test_player_disconnect():
    p = Player()
    p.connectDB()
    assert hasattr(p, 'db')
    p.disconnectDB()
    assert hasattr(p, 'db') is False


def test_player_load():
    p = Player()
    p.connectDB()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        p.loadByID(needle)
    assert 'loadByID requires an integer' in str(excinfo.value)

    # Actual lookup
    needle = 1
    p.loadByID(needle)
    assert isinstance(p.data, dict)
    assert p.data['FirstName'] == 'Harvey'
    assert p.data['LastName'] == 'the Rabbit'
    assert isinstance(p.data['DOB'], datetime.date)


def test_player_lookupID():
    # Setup
    log = Log('test.log')
    p = Player()
    p.connectDB()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Wil'
        p.lookupID(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # Missing fields error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'FirstName': 'Wil',
            'LastName': 'Trapp'
        }
        p.lookupID(needle, log)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)

    # Need a test of successful lookups
    needle = {
        'FirstName': 'Sample',
        'LastName': 'Player',
        'Position': 'Midfielder',
        'DOB': (1980, 1, 1, 0, 0, 0, 0, 0, 0,),
        'Hometown': 'Oneonta, NY'
    }
    assert p.lookupID(needle, log) == [15]


def test_player_lookupIDbyGoal():
    # Setup
    log = Log('test.log')
    p = Player()
    p.connectDB()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Wil'
        p.lookupIDbyGoal(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # Missing fields error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'FirstName': 'Wil',
            'LastName': 'Trapp'
        }
        p.lookupIDbyGoal(needle, log)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)

    # TODO: Need to actually look something up...
    needle = {
        'playername': 'Man',
        'TeamID': 2,
        'GameID': 1,
    }
    assert p.lookupIDbyGoal(needle, log) == [3]


def test_player_lookupIDbyName():
    # Setup
    log = Log('test.log')
    p = Player()
    p.connectDB()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Wil'
        p.lookupIDbyName(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # Missing fields error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'FirstName': 'Wil',
            'LastName': 'Trapp'
        }
        p.lookupIDbyName(needle, log)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)

    # Look up a player we know doesn't exist.
    needle = {
        'PlayerName': 'asdf',
    }
    assert p.lookupIDbyName(needle, log) == []

    # Look up a known player in the test dataset.
    needle = {
        'PlayerName': 'Sample Player',
    }
    assert p.lookupIDbyName(needle, log) == [15]


def test_player_merge():
    p = Player()
    assert p.merge(1, 2) is False


def test_player_saveDict():
    log = Log('test.log')
    p = Player()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        p.saveDict(needle, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # TODO: Need to actually save something
