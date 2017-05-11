#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import pytest

from avpr.logger import map_loglevel


def test_map_loglevel():
    assert map_loglevel(0) == logging.INFO
    assert map_loglevel(1) == logging.DEBUG
    assert map_loglevel(2) == logging.DEBUG

