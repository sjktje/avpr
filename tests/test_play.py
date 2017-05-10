#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from avpr.play import main, parse_args, write_pid

def test_parse_args_kill():
    args = parse_args(['--kill'])
    assert args.kill

    args = parse_args(['-k'])
    assert args.kill


def test_write_pid_to_file(tmpdir):
    file = tmpdir.join('play.pid')
    write_pid(1234, file.strpath)
    assert file.read() == '1234'

