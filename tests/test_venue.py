# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.venue import Venue
from trapp.log import Log
import trapp.connection as connection


def test_venue_init():
    v = Venue()
    # object types
    assert isinstance(v, Venue)
    assert isinstance(v.data, dict)
    # Default values
    assert v.data['ID'] == 0


def test_venue_connect():
    v = Venue()
    assert hasattr(v, 'db') is False
    v.connectDB()
    assert hasattr(v, 'db')


def test_venue_disconnect():
    v = Venue()
    v.connectDB()
    assert hasattr(v, 'db')
    v.disconnectDB()
    assert hasattr(v, 'db') is False


def test_venue_lookupID(data_teams):
    # Setup
    log = Log('test.log')
    v = Venue()
    v.connectDB()

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'My favorite venue'
        v.lookupID(needle, log)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should raise a missing-fields error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'Venue': 'Columbus Crew Stadium'
        }
        v.lookupID(needle, log)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)

    # This should bring back one record
    needle = {
        'VenueName': 'MAPFRE Stadium'
    }
    assert len(v.lookupID(needle, log)) >= 1
