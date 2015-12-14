# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.log import Log
from trapp.importer import Importer, ImporterGames, ImporterPlayers


def test_importer_init(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert isinstance(importer, Importer)
    assert importer.log.name == 'test.log'


def test_importer_correctValues(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert importer.correctValues() is True


def test_importer_checkData_sheets(excel_sheets):
    with pytest.raises(RuntimeError) as excinfo:
        log = Log('test.log')
        importer = Importer(excel_sheets, log)
    assert 'more than one worksheet' in str(excinfo.value)


def test_importer_checkFields_empty(excel_empty):
    with pytest.raises(RuntimeError) as excinfo:
        log = Log('test.log')
        importer = Importer(excel_empty, log)
    assert 'nothing to import' in str(excinfo.value)


def test_importer_checkFields(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    requiredFields = (['foo', 'bar'])
    assert importer.checkFields(requiredFields) is True


def test_importer_checkFields_fail(excel):
    with pytest.raises(RuntimeError) as excinfo:
        log = Log('test.log')
        importer = Importer(excel, log)
        requiredFields = (['foo', 'none'])
        importer.checkFields(requiredFields)
    assert 'missing the following columns' in str(excinfo.value)


# def test_importer_doImport(excel):
    # log = Log('test.log')
    # importer = Importer(excel, log)
    # assert importer.doImport() is True


def test_importer_setLog(excel):
    log = Log('test.log')
    log2 = Log('test2.log')
    importer = Importer(excel, log)
    importer.setLog(log2)
    assert importer.log.name == 'test2.log'


def test_importerGames(excel_games):
    log = Log('test.log')
    importer = ImporterGames(excel_games, log)
    requiredColumns = ([
        'MatchTime',
        'MatchTypeID',
        'HTeamID',
        'ATeamID'
    ])
    assert importer.checkFields(requiredColumns) is True
    assert importer.doImport() is True


def test_importerPlayers(excel_players):
    log = Log('test.log')
    importer = ImporterPlayers(excel_players, log)
    requiredColumns = ([
        'FirstName',
        'LastName',
        'Position',
        'DOB',
        'Hometown'
    ])
    assert importer.checkFields(requiredColumns) is True
    assert importer.doImport() is True
