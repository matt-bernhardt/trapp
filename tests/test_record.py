# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.record import Record


def test_record_init():
    r = Record()
    # object types
    assert isinstance(r, Record)
    assert isinstance(r.data, dict)
    # Default values
    assert r.data['ID'] == 0


def test_record_connect():
    r = Record()
    assert hasattr(r, 'db') is False
    r.connectDB()
    assert hasattr(r, 'db')


def test_record_disconnect():
    r = Record()
    r.connectDB()
    assert hasattr(r, 'db')
    r.disconnectDB()
    assert hasattr(r, 'db') is False


def test_record_buildUpdateClauses_empty():
    r = Record()
    data = []
    fieldList = []
    clauses = r.buildUpdateClauses(data, fieldList)
    assert clauses == {
        'FieldData': [],
        'FieldNames': []
    }


def test_record_buildUpdateClauses_simple():
    r = Record()
    data = {'Name':'Foo'}
    fieldList = ['Name']
    clauses = r.buildUpdateClauses(data, fieldList)
    assert clauses['FieldNames'] == ['Name = %s']
    assert clauses['FieldData'] == ['Foo']


def test_record_buildUpdateClauses_two():
    r = Record()
    data = {'Foo':'one','Bar':'two'}
    fieldList = ['Foo','Bar']
    clauses = r.buildUpdateClauses(data, fieldList)
    assert clauses['FieldNames'] == ['Bar = %s','Foo = %s']
    assert clauses['FieldData'] == ['two','one']
