# -*- coding: utf-8 -*-
import xlrd
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


def test_spreadsheet_buildRecords(excel):
    s = Spreadsheet(excel)
    s.fields()
    s.buildRecords()
    assert isinstance(s.records, list)

def test_spreadsheet_buildSheet(excel):
    s = Spreadsheet(excel)
    s.buildSheet()
    assert isinstance(s.sheet, xlrd.sheet.Sheet)
