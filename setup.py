#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = "play",
    packages = ["avpr"],
    entry_points = {
        "console_scripts": ['play = avpr.play:main']
        },
    version = '0.0.1',
    description = 'Play and loop a video file.',
    author = u'Svante Kvarnström',
    author_email = 'sjk@sjk.io',
    setup_requires=['pytest-runner', 'subprocess32'],
    tests_require=['pytest'],
)
