# -*- coding: utf-8 -*-
from __future__ import absolute_import
import datetime
from trapp.database import Database


def test_database_init():
    d = Database()
    assert d.cnx == ''
    assert d.cursor == ''


def test_database_convertDate():
    d = Database()
    testDate = (1996, 4, 13, 19, 30, 0, 0, 0, 0)
    assert d.convertDate(testDate) == '1996-04-13 19:30:00'
