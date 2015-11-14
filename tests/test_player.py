# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.player import Player


def test_player_init():
    p = Player()
    # object types
    assert isinstance(p, Player)
    assert isinstance(p.data, dict)
    # Default values
    assert p.data['ID'] == 0
    assert p.data['FirstName'] == ''
    assert p.data['LastName'] == ''


def test_player_load():
    p = Player()
    p.loadByID(1)
    assert p.data['ID'] == 1
    assert p.data['FirstName'] == 'Matt'
    assert p.data['LastName'] == 'Bernhardt'


def test_player_merge():
    p = Player()
    assert p.merge(1, 2) is False
