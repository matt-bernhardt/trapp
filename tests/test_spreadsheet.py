# -*- coding: utf-8 -*-
from __future__ import absolute_import

from trapp.spreadsheet import Spreadsheet


def test_spreadsheet_init():
    s = Spreadsheet('test.xlsx')
    assert isinstance(s, Spreadsheet)
    assert isinstance(s.data, xlrd)
