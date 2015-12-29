# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database
import os


def test_database_init():
    d = Database()
    assert d.cnx == ''
    assert d.cursor == ''
    assert d.conn == {}


"""
def test_database_lookupConnection():
    d = Database()
    # os.environ['trapp.dbuser'] = 'foo'
    # os.environ['trapp.dbpwd'] = 'bar'
    # os.environ['trapp.dbhost'] = 'baz'
    # os.environ['trapp.dbschema'] = 'none'
    d.lookupConnection()
    assert d.conn['user'] == 'foo'
    assert d.conn['pwd'] == 'bar'
    assert d.conn['host'] == 'baz'
    assert d.conn['schema'] == 'none'
    os.environ.clear('trapp.dbuser')
    os.environ.clear('trapp.dbpwd')
    os.environ.clear('trapp.dbhost')
    os.environ.clear('trapp.dbschema')
    d.lookupConnection()
    assert d.conn['user'] == 'travis'
    assert d.conn['pwd'] == ''
    assert d.conn['host'] == 'localhost'
    assert d.conn['schema'] == 'trapp'
"""


def test_database_query():
    d = Database()
    d.connect()
    # Inserts
    sql = ('INSERT INTO tbl_players '
           '(FirstName, LastName) '
           'VALUES '
           '(%s, %s)')
    params = ('Delete', 'Me', )
    rs = d.query(sql, params)
    assert d.warnings() is None
    # Updates
    sql = ('UPDATE tbl_players '
           'SET Position = %s '
           'WHERE FirstName = %s AND LastName = %s')
    rs = d.query(sql, ('Defender', 'Delete', 'Me', ))
    assert d.warnings() is None
    # Selects
    sql = ('SELECT ID '
           'FROM tbl_players '
           'WHERE FirstName = %s AND LastName = %s')
    rs = d.query(sql, params)
    if (rs.with_rows):
        records = rs.fetchall()
    for term in records:
        needleID = records[0][0]
    assert needleID > 0
    assert d.warnings() is None
    d.disconnect()


def test_database_convertDate():
    d = Database()
    testDate = (1996, 4, 13, 19, 30, 0, 0, 0, 0)
    assert d.convertDate(testDate) == '1996-04-13 19:30:00'
