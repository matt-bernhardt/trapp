# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.team import Team
from trapp.log import Log
import trapp.connection as connection


def test_team_init():
    t = Team()
    # object types
    assert isinstance(t, Team)
    assert isinstance(t.data, dict)
    # Default values
    assert t.data['ID'] == 0


def test_team_connect():
    t = Team()
    assert hasattr(t, 'db') is False
    t.connectDB()
    assert hasattr(t, 'db')


def test_team_disconnect():
    t = Team()
    t.connectDB()
    assert hasattr(t, 'db')
    t.disconnectDB()
    assert hasattr(t, 'db') is False


def test_game_lookupID(data_teams):
    # Setup
    log = Log('test.log')
    t = Team()
    t.connectDB()

    # Populate table for later querying
    # TODO do this via setup/teardown?
    sql = 'INSERT INTO tbl_teams (teamname) VALUES ("Sample Team")'
    t.db.query(sql, ())

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'My favorite team'
        t.lookupID(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should raise a missing-fields error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'FirstName': 'Harvey'
        }
        t.lookupID(needle, log)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)

    # This should bring back one record
    needle = {
        'teamname': 'Sample Team'
    }
    assert len(t.lookupID(needle, log)) >= 1
