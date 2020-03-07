# -*- coding: utf-8 -*-
import pytest
from trapp.team import Team
from trapp.log import Log


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
        'teamname': 'Columbus Crew'
    }
    assert len(t.lookupID(needle, log)) >= 1
