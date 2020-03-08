# -*- coding: utf-8 -*-
from trapp.log import Log
from trapp.compile_teammate import CompilerTeammates


def test_compilerTeammates_init():
    log = Log('test.log')
    compiler = CompilerTeammates(log)
    assert isinstance(compiler, CompilerTeammates)
    assert compiler.log.name == 'test.log'


def test_compilerTeammates_assembleCombos():
    log = Log('test.log')
    compiler = CompilerTeammates(log)
    players = [(1,), (2,)]
    combos = compiler.assembleCombos(players)
    assert len(combos) == 1
    players = [(1,), (2,), (3,)]
    combos = compiler.assembleCombos(players)
    assert len(combos) == 3

