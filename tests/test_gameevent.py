# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.gameevent import GameEvent
from trapp.log import Log


def test_gameevent_init():
    ge = GameEvent()
    # object types
    assert isinstance(ge, GameEvent)
    assert isinstance(ge.data, dict)
    # Default values


def test_gameevent_connect():
    ge = GameEvent()
    assert hasattr(ge, 'db') is False
    ge.connectDB()
    assert hasattr(ge, 'db')


def test_gameevent_disconnect():
    ge = GameEvent()
    ge.connectDB()
    assert hasattr(ge, 'db')
    ge.disconnectDB()
    assert hasattr(ge, 'db') is False


def test_gameevent_checkData():
    ge = GameEvent()
    required = ['GameID', 'TeamID', 'PlayerID', 'MinuteID']

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        ge.checkData(needle, required)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should raise a field error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'Foo': 'Bar'
        }
        ge.checkData(needle, required)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)


def test_gameevent_lookupID():
    log = Log('test.log')
    ge = GameEvent()
    ge.connectDB()

    needle = {
        'GameID': 1,
        'TeamID': 2,
        'PlayerID': 3,
        'MinuteID': 4,
    }
    result = ge.lookupID(needle, log)
    assert len(result) == 1

    needle = {
        'GameID': -1,
        'TeamID': -1,
        'PlayerID': -1,
        'MinuteID': -1,
    }
    result = ge.lookupID(needle, log)
    assert len(result) == 0


def test_gameevent_saveDict():
    log = Log('test.log')
    ge = GameEvent()
    ge.connectDB()

    # Formats
    with pytest.raises(RuntimeError) as excinfo:
        data = 'foo'
        ge.saveDict(data, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # Insert dummy data
    data = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'MinuteID': 1,
        'Event': 1,
        'Notes': 'DeleteMe'
    }
    assert ge.saveDict(data, log) is True
    assert ge.db.warnings() is None

    # Updates
    data = {
        'ID': 2,
        'GameID': 0,
        'TeamID': 0,
        'PlayerID': 0,
        'MinuteID': 0,
        'Event': 0,
        'Notes': 'EditMe'
    }
    assert ge.saveDict(data, log) is True
    assert ge.db.warnings() is None

    # Delete dummy data
    sql = "DELETE FROM tbl_gameevents WHERE Notes = 'DeleteMe'"
    ge.db.query(sql, ())
