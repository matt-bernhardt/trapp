# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.log import Log
from trapp.importer import Importer


def test_importer_init(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert isinstance(importer, Importer)
    assert importer.log.name == 'test.log'


def test_importer_checkFields(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    requiredFields = (['foo', 'bar'])
    assert importer.checkFields(requiredFields) is True


def test_importer_doImport(excel):
    log = Log('test.log')
    importer = Importer(excel, log)
    assert importer.doImport() is True


def test_importer_setLog(excel):
    log = Log('test.log')
    log2 = Log('test2.log')
    importer = Importer(excel, log)
    importer.setLog(log2)
    assert importer.log.name == 'test2.log'
