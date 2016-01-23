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
    p.connectDB()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        p.saveDict(needle, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # New player
    # TODO: Need to make sure this player doesn't already exist
    needle = {
        'FirstName': 'Imported',
        'LastName': 'Player',
        'Position': 'Midfielder',
        'DOB': (1980, 1, 1, 0, 0, 0, 0, 0, 0),
        'Hometown': ''
    }
    assert p.saveDict(needle, log) is True
    assert p.db.warnings() is None


def test_player_saveDict_update():
    log = Log('test.log')
    p = Player()
    p.connectDB()

    # Existing player scenario:
    # 1. Load a known record
    needle = 1
    p.loadByID(needle)

    # 2. Verify the known record
    assert p.data['Hometown'] == 'Bedford Falls, NY'

    # 3. Change one part of the record
    p.data['Hometown'] = 'Paris, France'
    # TODO: Shouldn't need to re-establish DOB here
    p.data['DOB'] = (1980, 1, 1, 0, 0, 0, 0, 0, 0)
    assert p.saveDict(p.data, log) is True

    # 4. Re-load that record
    p.data = ''
    p.loadByID(needle)

    # 5. Confirm the change was recorded
    assert p.data['Hometown'] == 'Paris, France'

    # 6. Change the record back to its original state
    p.data['Hometown'] = 'Bedford Falls, NY'
    # TODO: Shouldn't need to re-establish DOB here
    p.data['DOB'] = (1980, 1, 1, 0, 0, 0, 0, 0, 0)
    p.saveDict(p.data, log)

    # 7. Confirm the change was recorded
    p.data = ''
    p.loadByID(needle)
    assert p.data['Hometown'] == 'Bedford Falls, NY'
