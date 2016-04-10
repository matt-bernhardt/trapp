# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.log import Log
from trapp.checker import Checker


def test_checker_init():
    log = Log('test.log')
    output = Log('test.csv')
    c = Checker(log, output)
    assert isinstance(c, Checker)
    assert c.log.name == 'test.log'
    assert c.output.name == 'test.csv'
