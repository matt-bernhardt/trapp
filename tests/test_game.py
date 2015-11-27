# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.game import Game


def test_game_init():
    g = Game()
    # object types
    assert isinstance(g, Game)
    assert isinstance(g.data, dict)
    # Default values
    assert g.data['ID'] == 0
