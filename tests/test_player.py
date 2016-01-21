# -*- coding: utf-8 -*-
from __future__ import absolute_import
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


def test_player_lookupIDbyGame():
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

    needle = {
        'PlayerName': 'asdf',
    }
    assert p.lookupIDbyName(needle, log) == []

    needle = {
        'PlayerName': 'Sample Player',
    }
    assert len(p.lookupIDbyName(needle, log)) == 1


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
