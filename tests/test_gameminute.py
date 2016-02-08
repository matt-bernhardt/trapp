# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.gameminute import GameMinute
from trapp.log import Log


def test_gameminute_init():
    gm = GameMinute()
    # object types
    assert isinstance(gm, GameMinute)
    assert isinstance(gm.data, dict)
    # Default values


def test_gameminute_connect():
    gm = GameMinute()
    assert hasattr(gm, 'db') is False
    gm.connectDB()
    assert hasattr(gm, 'db')


def test_gameminute_disconnect():
    gm = GameMinute()
    gm.connectDB()
    assert hasattr(gm, 'db')
    gm.disconnectDB()
    assert hasattr(gm, 'db') is False


def test_gameminute_checkData():
    gm = GameMinute()
    required = ['GameID', 'TeamID', 'PlayerID']

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        gm.checkData(needle, required)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should raise a field error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'Foo': 'Bar'
        }
        gm.checkData(needle, required)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)


def test_gameminute_lookupID():
    log = Log('test.log')
    gm = GameMinute()
    gm.connectDB()

    needle = {
        'GameID': 1,
        'TeamID': 2,
        'PlayerID': 3
    }
    result = gm.lookupID(needle, log)
    assert len(result) == 1

    needle = {
        'GameID': -1,
        'TeamID': -1,
        'PlayerID': -1
    }
    result = gm.lookupID(needle, log)
    assert len(result) == 0


def test_gameminute_saveDict():
    log = Log('test.log')
    gm = GameMinute()
    gm.connectDB()

    # Formats
    with pytest.raises(RuntimeError) as excinfo:
        data = 'foo'
        gm.saveDict(data, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # Insert dummy data
    data = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'TimeOn': 0,
        'TimeOff': 90,
        'Ejected': 314
    }
    assert gm.saveDict(data, log) is True
    assert gm.db.warnings() is None

    # Updates
    data = {
        'ID': 2,
        'GameID': 0,
        'TeamID': 0,
        'PlayerID': 0,
        'TimeOn': 0,
        'TimeOff': 0,
        'Ejected': 0
    }
    assert gm.saveDict(data, log) is True
    assert gm.db.warnings() is None

    # Delete dummy data
    sql = 'DELETE FROM tbl_gameminutes WHERE Ejected = 314'
    gm.db.query(sql, ())
