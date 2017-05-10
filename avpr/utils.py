#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import shlex
import sys

# subprocess32 is a backport of python3's subprocess module. It fixes
# some bugs and adds some features. This requires python-dev to be
# installed.
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess


logger = logging.getLogger('play')


def run_cmd(cmd):
    """Run command, suppress STDOUT and STDERR.

    :param cmd: command to run (string)
    :returns: pid

    """

    logger.debug('running command "{}"'.format(cmd))

    with open(os.devnull, 'wb') as DEVNULL:
        return subprocess.Popen(
            shlex.split(cmd),
            shell=False,
            stderr=subprocess.STDOUT,
            stdout=DEVNULL
        ).pid
