# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.log import Log
from trapp.compile_game import CompilerGames


def test_compilerGames_init():
    log = Log('test.log')
    compiler = CompilerGames(log)
    assert isinstance(compiler, CompilerGames)
    assert compiler.log.name == 'test.log'


def test_compilerGames_doCompile():
    log = Log('test.log')
    compiler = CompilerGames(log)
    assert compiler.doCompile() is True


def test_compilerGames_setLog():
    log = Log('test.log')
    log2 = Log('test2.log')
    compiler = CompilerGames(log)
    compiler.setLog(log2)
    assert compiler.log.name == 'test2.log'
