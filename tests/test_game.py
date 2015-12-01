# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.game import Game


def test_game_init():
    g = Game()
    # object types
    assert isinstance(g, Game)
    assert isinstance(g.data, dict)
    # Default values


def test_game_lookupID():
    g = Game()
    g.connectDB()
    # This should raise an error
    needle = '1996-04-13'

    needle = {
        'MatchTime': '1996-04-13',
        'HTeamID': 11,
        'ATeamID': 12
    }
    g.lookupID(needle)
    assert g.data['MatchID'] == 10992
