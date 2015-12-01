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


def test_game_lookupID():
    # Setup
    log = Log()
    g = Game()
    g.connectDB()

    # This should raise an error
    with pytest.raises(RuntimeError) as excinfo:
        needle = '1996-04-13'
        g.lookupID(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should bring back one record
    needle = {
        'MatchTime': '1996-04-13',
        'HTeamID': 11,
        'ATeamID': 12
    }
    assert g.lookupID(needle, log) is True
    assert g.data['MatchID'] == 10992
