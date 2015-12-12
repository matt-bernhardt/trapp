# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database


def test_database_init():
    d = Database()
    assert d.cnx == ''
    assert d.cursor == ''


def test_database_query():
    d = Database()
    d.connect()
    # Inserts
    sql = ('INSERT INTO tbl_players '
           '(FirstName, LastName) '
           'VALUES '
           '(%s, %s)')
    params = ('Brian', 'McBride', )
    rs = d.query(sql, params)
    assert d.warnings() is None
    # Updates
    sql = ('UPDATE tbl_players '
           'SET Position = %s '
           'WHERE FirstName = %s AND LastName = %s')
    rs = d.query(sql, ('Forward', 'Brian', 'McBride', ))
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
    assert needleID == 1
    assert d.warnings() is None
    d.disconnect()


def test_database_convertDate():
    d = Database()
    testDate = (1996, 4, 13, 19, 30, 0, 0, 0, 0)
    assert d.convertDate(testDate) == '1996-04-13 19:30:00'
