# -*- coding: utf-8 -*-
from __future__ import absolute_import

from trapp.log import Log


def test_log_init():
    l = Log('test.log')
    assert isinstance(l, Log)
    assert isinstance(l.file, file)


def test_log_filename():
    l = Log('test.log')
    assert l.name == 'test.log'


def test_log_write():
    l = Log('test.log')
    msg = 'Hello'
    l.message(msg)
    # assert l.read() == msg


def test_log_end():
    l = Log('test.log')
    l.end()
    assert not(isinstance(l.file, file))
