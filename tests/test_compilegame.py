# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.log import Log
from trapp.compile_game import CompilerGames


def test_compilerGames_init():
    log = Log('test.log')
    compiler = CompilerGames(log)
    assert isinstance(compiler, CompilerGames)
    assert compiler.log.name == 'test.log'


def test_compilerGames_assembleStatLine_starter():
    log = Log('test.log')
    compiler = CompilerGames(log)
    # Started, played whole game
    record = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'TimeOn': 0,
        'TimeOff': 90,
        'Ejected': 0
    }
    result = compiler.assembleStatLine(record)
    assert isinstance(result, dict)
    assert result['GS'] == 1
    assert result['GP'] == 1
    assert result['RC'] == 0


def test_compilerGames_assembleStatLine_ejected_sub():
    log = Log('test.log')
    compiler = CompilerGames(log)
    # Substitute, then ejected
    record = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'TimeOn': 62,
        'TimeOff': 87,
        'Ejected': 1
    }
    result = compiler.assembleStatLine(record)
    assert result['GS'] == 0
    assert result['GP'] == 1
    assert result['RC'] == 1


def test_compilerGames_assembleStatLine_unused_sub():
    log = Log('test.log')
    compiler = CompilerGames(log)
    # Unused substitute
    record = {
        'GameID': 1,
        'TeamID': 1,
        'PlayerID': 1,
        'TimeOn': 0,
        'TimeOff': 0,
        'Ejected': 0
    }
    result = compiler.assembleStatLine(record)
    assert result['GS'] == 0
    assert result['GP'] == 0


# def test_compilerGames_doCompile():
#     log = Log('test.log')
#     compiler = CompilerGames(log)
#     assert compiler.doCompile() is True


def test_compilerGames_setLog():
    log = Log('test.log')
    log2 = Log('test2.log')
    compiler = CompilerGames(log)
    compiler.setLog(log2)
    assert compiler.log.name == 'test2.log'


def test_compilerGames_getAppearanceList():
    log = Log('test.log')
    compiler = CompilerGames(log)
    appList = compiler.getAppearanceList()
    assert isinstance(appList, list)
    assert isinstance(appList[0], dict)
    assert isinstance(appList[0]['GameID'], int)
    assert isinstance(appList[0]['TeamID'], int)
    assert isinstance(appList[0]['PlayerID'], int)


def test_compilerGames_getEventSummary():
    log = Log('test.log')
    compiler = CompilerGames(log)
    needle = {'GameID': 1, 'TeamID': 1, 'PlayerID': 1}
    result = compiler.getEventSummary(needle)
    # Format of response
    assert isinstance(result, dict)
    assert isinstance(result['Goals'], int)
    assert isinstance(result['Ast'], int)
    # Response includes original needle
    assert result['GameID'] == 1
    assert result['TeamID'] == 1
    assert result['PlayerID'] == 1
    # Unfound needles still return zeros
    needle = {'GameID': 184, 'TeamID': 3892, 'PlayerID': 2981}
    result = compiler.getEventSummary(needle)
    assert result['Goals'] == 0
    assert result['Ast'] == 0
