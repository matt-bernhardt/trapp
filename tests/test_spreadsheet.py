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
