#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
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

    :param filename: file to loop
    """

    filename = os.path.expanduser(filename)
    try:
        log = open_log(LOGFILE)
    except IOError:
        sys.exit(1)

    if not os.path.isfile(filename):
        print("Could not open {}".format(filename))
        sys.exit(1)

    command = ("omxplayer "
               "-o hdmi "
               "--loop "
               "--no-osd "
               "--no-keys "
               "{}".format(filename))

    p = subprocess.Popen(shlex.split(command), shell=False, stderr=log,
                         stdout=log)

    print("Pid: {}".format(p.pid))


def open_log(filename):
    """Open log file.

    :param filename: file to append log to
    :returns: file handle
    :raises: IOError if file couldn't be opened
    """

    logfile = os.path.expanduser(filename)
    try:
        return open(logfile, 'a')
    except IOError as e:
        print("Could not open {}: {} ({})".format(logfile, e.strerror, e.errno))
        raise


def parse_args(args):
    parser = argparse.ArgumentParser(description='Loop play video files.')

    parser.add_argument('file', nargs='?', help='file to loop')
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s 0.0.1')

    return parser.parse_args()


def main():
    args = parse_args(sys.argv[1:])

    if not args.file:
        print("You need to tell me what to play.")
        sys.exit(1)

    play_loop(args.file)
def main():
    play_loop("test/instagramloop_avp_3.mp4")

if __name__ == "__main__":
    main()
