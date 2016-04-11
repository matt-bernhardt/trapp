# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from trapp.log import Log
from trapp.check_games import CheckerGames


def test_checkerGames_init():
    log = Log('test.log')
    output = Log('test.csv')
    c = CheckerGames(log, output)
    assert isinstance(c, CheckerGames)


def test_checkerGames_checkGames():
    log = Log('test.log')
    output = Log('test.csv')
    c = CheckerGames(log, output)
    c.checkGames()
    # Re-open output in read mode
    output.file = open('test.csv', 'r')
    # Default start year is 2012, but sample games are in 1980.
    # This is by design, to give a negative test.
    assert output.file.readline() == ''


def test_checkerGames_reviewCompetition():
    log = Log('test.log')
    output = Log('test.csv')
    c = CheckerGames(log, output)
    c.reviewCompetition(1, 1980)
    # Re-open output in read mode
    output.file = open('test.csv', 'r')
    # Two games in the sample dataset for 1980
    assert output.file.readline() == '1,1980,2\n'