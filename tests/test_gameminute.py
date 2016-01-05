# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.gameminute import GameMinute


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
