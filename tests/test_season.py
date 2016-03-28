# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.season import Season
from trapp.log import Log


def test_season_init():
    s = Season()
    # object types
    assert isinstance(s, Season)
    assert isinstance(s.data, dict)
    # Default values
    assert s.data['ID'] == 0


def test_season_connect():
    s = Season()
    assert hasattr(s, 'db') is False
    s.connectDB()
    assert hasattr(s, 'db')


def test_season_disconnect():
    s = Season()
    s.connectDB()
    assert hasattr(s, 'db')
    s.disconnectDB()
    assert hasattr(s, 'db') is False


def test_season_loadAll():
    s = Season()
    s.connectDB()
    s.data = s.loadAll()
    assert len(s.data) == 2


def test_season_loadGameList():
    s = Season()
    s.connectDB()
    needle = {
        'TeamID': 1,
        'Season': 1894
    }
    s.data = s.loadGameList(needle)
    assert len(s.data) == 0
    needle = {
        'TeamID': 1,
        'Season': 1980
    }
    s.data = s.loadGameList(needle)
    assert len(s.data) == 2
    s.disconnectDB()


def test_season_loadPlayerList():
    s = Season()
    s.connectDB()
    needle = {
        'TeamID': 1,
        'Season': 1894
    }
    s.data = s.loadPlayerList(needle)
    assert len(s.data) == 0
    needle = {
        'TeamID': 2,
        'Season': 1980
    }
    s.data = s.loadPlayerList(needle)
    assert len(s.data) == 2