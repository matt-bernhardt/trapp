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


def test_gameminute_saveDict():
    log = Log('test.log')
    gm = GameMinute()
    gm.connectDB()

    # Formats
    with pytest.raises(RuntimeError) as excinfo:
        data = 'foo'
        gm.saveDict(data, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # Inserts
    data = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'TimeOn': 0,
        'TimeOff': 90,
        'Ejected': 0
    }
    assert gm.saveDict(data, log) is True
    assert gm.db.warnings() is None

    # Updates
    data = {
        'ID': 1,
        'GameID': 2,
        'TeamID': 2,
        'PlayerID': 2,
        'TimeOn': 0,
        'TimeOff': 89,
        'Ejected': 1
    }
    assert gm.saveDict(data, log) is True
    assert gm.db.warnings() is None
