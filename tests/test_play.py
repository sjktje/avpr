#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from avpr.play import main, parse_args, write_pid, read_pid

def test_parse_args_kill():
    args = parse_args(['--kill'])
    assert args.kill

    args = parse_args(['-k'])
    assert args.kill


def test_parse_args_verbosity():
    args = parse_args(['--verbosity', '--verbosity'])
    assert args.verbosity == 2
    
    args = parse_args(['-v', '-v'])
    assert args.verbosity == 2


def test_write_pid_to_file(tmpdir):
    file = tmpdir.join('play.pid')
    write_pid(1234, file.strpath)
    assert file.read() == '1234'


def test_read_pid(tmpdir):
    pidfile = tmpdir.join('play.pid')
    with open(pidfile.strpath, 'w') as p:
        p.write('1234')

    pid = read_pid(pidfile.strpath)
    assert pid == '1234'


def test_read_pid_raises_ioerror():
    with pytest.raises(IOError):
        read_pid('nonexistent_file_name.pid')
