# -*- coding: utf-8 -*-
from __future__ import absolute_import

from trapp.spreadsheet import Spreadsheet


def test_spreadsheet_init(excel):
    s = Spreadsheet(excel)
    assert isinstance(s, Spreadsheet)
    # assert isinstance(s.data, xlrd)


def test_spreadsheet_fields(excel):
    s = Spreadsheet(excel)
    assert s.fields() == ['foo', 'bar']


def test_spreadsheet_recoverDate(excel):
    s = Spreadsheet(excel)
    assert s.recoverDate(35168) == (1996, 4, 13, 0, 0, 0, 0, 0, 0)
