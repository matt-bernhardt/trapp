# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.log import Log
from trapp.check_minutes import CheckerMinutes


def test_checkerGames_init():
    log = Log('test.log')
    output = Log('test.csv')
    c = CheckerMinutes(log, output)
    assert isinstance(c, CheckerMinutes)
