# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.player import Player
from trapp.log import Log


def test_player_init():
    p = Player()
    # object types
    assert isinstance(p, Player)
    assert isinstance(p.data, dict)
    # Default values
    assert p.data['ID'] == 0
    assert p.data['FirstName'] == ''
    assert p.data['LastName'] == ''


def test_player_connect():
    p = Player()
    # Assert DB connection not present
    p.connectDB()
    # Assert DB connection exists


def test_player_disconnect():
    p = Player()
    p.connectDB()
    # Assert DB connection exists
    p.disconnectDB()
    # Assert DB connection not present


def test_player_load():
    p = Player()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        p.loadByID(needle)
    assert 'loadByID requires an integer' in str(excinfo.value)

    p.connectDB()

    # Actual lookup
    needle = 2
    p.loadByID(needle)
    assert p.data['PlayerID'] == 2
    assert p.data['FirstName'] == 'Bryheem'
    assert p.data['LastName'] == 'Hancock'
    assert p.data['DOB'] == '1980-03-01'

    p.disconnectDB()


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
