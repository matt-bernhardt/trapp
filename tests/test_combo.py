# -*- coding: utf-8 -*-
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


def test_combo_lookupCombos_needsDict():
    c = Combo()
    c.connectDB()
    with pytest.raises(RuntimeError) as excinfo:
        needle1 = 1
        needle2 = 'Foo'
        c.data = c.lookupCombos(needle1, needle2)
    assert 'lookupID requires two integers' in str(excinfo.value)


def test_combo_lookupCombos():
    c = Combo()
    c.connectDB()
    c.data = c.lookupCombos(1, 2)
    assert len(c.data) == 4
