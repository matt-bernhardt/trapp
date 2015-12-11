# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.database import Database
import mock


def test_database_init():
    d = Database()
    assert d.cnx == ''
    assert d.cursor == ''


@mock.patch('trapp.database')
def test_database_query(mock_database):
    # Following http://www.toptal.com/python/an-introduction-to-mocking-in-python
    #
    # Questions:
    #
    # Q - Is that article even useful, since it builds on unittest not pytest? Same principle?
    #
    # Q - I'm not setting up a mock _test_, but a mock _method_ right?
    #
    # Q - Curious about how I'd mock a higher-level method (that ultimately depends on Database.query)
    #     Would I mock 'query' differently in each case, standing in for what _would_ come back from the
    #     database?
    d = Database()
    d.connect()
    sql = ('SELECT ID '
           'FROM tbl_players '
           'WHERE FirstName = %s AND LastName = %s')
    params = ('Brian', 'McBride', )
    # Q - the next line came fromm toptal - seems to checking how the mock method was called?
    mock_database.query.assert_called_with(sql, params)
    d.disconnect()
    #
    # Also reading https://pytest.org/latest/monkeypatch.html


def test_database_convertDate():
    d = Database()
    testDate = (1996, 4, 13, 19, 30, 0, 0, 0, 0)
    assert d.convertDate(testDate) == '1996-04-13 19:30:00'
