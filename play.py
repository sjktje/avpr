#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

LOGFILE = '~/Code/avpr/play.log'

def play_loop(filename):
    """Loop video file

    :param filename: TODO
    :returns: TODO

    :raises:
        FileNotFoundError if filename does not exist
    """

    filename = os.path.expanduser(filename)

    if not os.path.isfile(filename):
        raise IOError("Could not open {}".format(filename))

    command = ("omxplayer "
               "-o hdmi "
               "--loop "
               "--no-osd "
               "--no-keys "
               "{}".format(filename))

    p = subprocess.Popen(shlex.split(command))

    print("Pid: {}".format(p.pid))


def main():
    play_loop("test/instagramloop_avp_3.mp4")

if __name__ == "__main__":
    main()
