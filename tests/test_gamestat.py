# -*- coding: utf-8 -*-
import pytest
from trapp.gamestat import GameStat
from trapp.log import Log


def test_gamestat_init():
    gs = GameStat()
    # object types
    assert isinstance(gs, GameStat)
    assert isinstance(gs.data, dict)
    # Default values


def test_gamestat_connect():
    gs = GameStat()
    assert hasattr(gs, 'db') is False
    gs.connectDB()
    assert hasattr(gs, 'db')


def test_gamestat_disconnect():
    gs = GameStat()
    gs.connectDB()
    assert hasattr(gs, 'db')
    gs.disconnectDB()
    assert hasattr(gs, 'db') is False


def test_gamestat_checkData():
    gs = GameStat()
    required = ['GameID', 'TeamID', 'PlayerID']

    # This should raise a format error
    with pytest.raises(RuntimeError) as excinfo:
        needle = 'Foo'
        gs.checkData(needle, required)
    assert 'lookupID requires a dictionary' in str(excinfo.value)

    # This should raise a field error
    with pytest.raises(RuntimeError) as excinfo:
        needle = {
            'Foo': 'Bar'
        }
        gs.checkData(needle, required)
    assert 'Submitted data is missing the following fields' in str(excinfo.value)


def test_gamestat_lookupID():
    log = Log('test.log')
    gs = GameStat()
    gs.connectDB()

    needle = {
        'GameID': 1,
        'TeamID': 2,
        'PlayerID': 3
    }
    result = gs.lookupID(needle, log)
    assert len(result) == 1

    needle = {
        'GameID': 0,
        'TeamID': 0,
        'PlayerID': 0
    }
    result = gs.lookupID(needle, log)
    assert len(result) == 0


def test_gamestat_saveDict():
    log = Log('test.log')
    gs = GameStat()
    gs.connectDB()

    # Formats
    with pytest.raises(RuntimeError) as excinfo:
        data = 'foo'
        gs.saveDict(data, log)
    assert 'saveDict requires a dictionary' in str(excinfo.value)

    # Inserts
    data = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'Goals': 0,
        'Ast': 0,
        'Shots': 0,
        'SOG': 0,
        'FC': 0,
        'FS': 0,
        'Off': 0,
        'CK': 0,
        'Blk': 0,
        'YC': 0,
        'RC': 0,
        'ShotsFaced': 0,
        'Saves': 0,
        'GA': 0,
        'CP': 0,
        'Plus': 0,
        'Minus': 0
    }
    assert gs.saveDict(data, log) is True
    assert gs.db.warnings() is None

    # Get last ID
    sql = "SELECT Max(ID) FROM tbl_gamestats"
    rs = gs.db.query(sql, (
    ))
    if (rs.with_rows):
        records = rs.fetchall()
    for item in records:
        lastID = item[0]
    log.message(str(lastID))

    # Updates
    data = {
        'ID': lastID,
        'GameID': 2,
        'TeamID': 2,
        'PlayerID': 2,
        'Goals': 0,
        'Ast': 0,
        'Shots': 0,
        'SOG': 0,
        'FC': 0,
        'FS': 0,
        'Off': 0,
        'CK': 0,
        'Blk': 0,
        'YC': 0,
        'RC': 0,
        'ShotsFaced': 0,
        'Saves': 0,
        'GA': 0,
        'CP': 0,
        'Plus': 0,
        'Minus': 0
    }
    assert gs.saveDict(data, log) is True
    assert gs.db.warnings() is None

    # Delete
    rs = gs.db.query("DELETE FROM tbl_gamestats WHERE ID = %s", (
        lastID,
    ))
