#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from avpr.play import main, parse_args

def test_parse_args_kill():
    args = parse_args(['--kill'])
    assert args.kill

    args = parse_args(['-k'])
    assert args.kill
