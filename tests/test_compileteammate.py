# -*- coding: utf-8 -*-
from trapp.log import Log
from trapp.compile_teammate import CompilerTeammates


def test_compilerTeammates_init():
    log = Log('test.log')
    compiler = CompilerTeammates(log)
    assert isinstance(compiler, CompilerTeammates)
    assert compiler.log.name == 'test.log'


