#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from avpr.utils import create_dir


def test_create_dir_creates_dir(tmpdir):
    basedir = tmpdir.mkdir('basedir')
    testdir = os.path.join(basedir.strpath, 'testdir')
    create_dir(testdir)
    assert os.path.isdir(testdir)


def test_create_dir_fails_silently_with_duplicate_dirs(tmpdir):
    basedir = tmpdir.mkdir('basedir')
    testdir = os.path.join(basedir.strpath, 'testdir')
    create_dir(testdir)
    create_dir(testdir)
