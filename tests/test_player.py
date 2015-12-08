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


def test_player_load():
    p = Player()
    p.loadByID(1)
    assert p.data['ID'] == 1
    assert p.data['FirstName'] == 'Matt'
    assert p.data['LastName'] == 'Bernhardt'


def test_player_lookupID():
    # Setup
    log = Log('test.log')
    p = Player()

    # Format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Wil'
        p.lookupID(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)


def test_player_merge():
    p = Player()
    assert p.merge(1, 2) is False
