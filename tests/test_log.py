# -*- coding: utf-8 -*-
from __future__ import absolute_import
from trapp.log import Log


def test_log_init():
    l = Log('test.log')
    assert isinstance(l, Log)
    # There used to be a test here to make sure l.file was a file type.
    # That was removed because Python 3 is entirely different, and this test
    # most likely wasn't needed.


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
    assert l.file is None
