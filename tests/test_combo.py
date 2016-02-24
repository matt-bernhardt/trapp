# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.combo import Combo
from trapp.log import Log


def test_combo_init():
    c = Combo()
    # object types
    assert isinstance(c, Combo)
    assert isinstance(c.data, dict)
    # Default values
    assert c.data['ID'] == 0


def test_combo_connect():
    c = Combo()
    assert hasattr(c, 'db') is False
    c.connectDB()
    assert hasattr(c, 'db')


def test_combo_disconnect():
    c = Combo()
    c.connectDB()
    assert hasattr(c, 'db')
    c.disconnectDB()
    assert hasattr(c, 'db') is False


def test_combo_lookupID():
    c = Combo()
    c.connectDB()
    c.data = c.lookupID(1, 2)
    assert len(c.data) == 0
