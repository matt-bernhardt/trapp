# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.competition import Competition
from trapp.log import Log


def test_competition_init():
    c = Competition()
    # object types
    assert isinstance(c, Competition)
    assert isinstance(c.data, dict)
    # Default values


def test_competition_connect():
    c = Competition()
    assert hasattr(c, 'db') is False
    c.connectDB()
    assert hasattr(c, 'db')


def test_competition_disconnect():
    c = Competition()
    c.connectDB()
    assert hasattr(c, 'db')
    c.disconnectDB()
    assert hasattr(c, 'db') is False


def test_competition_loadAll():
    c = Competition()
    c.connectDB()

    result = c.loadAll()
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert len(result) == 4
    item = result[0]
    assert item['CompetitionID'] == 3
    assert item['Competition'] == 'MLS Cup'
    assert item['CompetitionType'] == 'Playoffs'
    assert item['Official'] == 1
