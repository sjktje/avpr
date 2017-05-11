#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

def get_version():
    """Get version string

    Got this from the pytest project's setup.py

    :returns: version string in format x.y.z, for example 0.0.1
    :license: MIT

    """
    path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'avpr',
            '__init__.py'
            )
    with open(path, 'r') as file:
        for line in file.readlines():
            if '__version__' in line:
                return line.strip().split('=')[-1].strip(" '")
    raise ValueError('Could not read version from avpr/__init__.py')


setup(
    name = "avpr",
    packages = ["avpr"],
    entry_points = {
        "console_scripts": ['avprplay = avpr.play:main']
        },
    version = get_version(),
    description = 'Play and loop a video file.',
    author = u'Svante Kvarnström',
    author_email = 'sjk@sjk.io',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=['subprocess32']
)
