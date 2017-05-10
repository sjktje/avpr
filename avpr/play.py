#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
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

from .logger import create_logger

LOGFILE = '~/Code/avpr/play.log'
PIDFILE = '~/Code/avpr/play.pid'

logger = logging.getLogger('play')

def play_loop(filename):
    """Loop video file

    :param filename: file to loop
    """


    if not os.path.isfile(filename):
        logger.critical('Could not open {}'.format(filename))
        sys.exit(1)

    command = ("./omxplayer "
               "-o hdmi "
               "--loop "
               "--no-osd "
               "--no-keys "
               "{}".format(filename))

    logger.info('Looping playback of {}'.format(filename))
    logger.debug(command)

    p = subprocess.Popen(shlex.split(command), shell=False, stderr=None, stdout=None)

    write_pid(p.pid, PIDFILE)


def open_log(filename):
    """Open log file.

    :param filename: file to append log to
    :returns: file handle
    :raises IOError: if file couldn't be opened
    """

    logfile = os.path.expanduser(filename)
    try:
        return open(logfile, 'a')
    except IOError as e:
        print("Could not open {}: {} ({})".format(logfile, e.strerror, e.errno))
        raise


def write_pid(pid, filename):
    """Write pid to file

    This function will exit(1) unless the pid file was written.

    :param pid: pid number to write
    :param filename: path to and name of file to write to. Expands ~.
    :returns: nothing

    """
    pidfile = os.path.expanduser(filename)

    try:
        with open(pidfile, 'w') as f:
            f.write(str(pid))

    except IOError as e:
        print("Could not open pidfile {}: {} ({})".format(logfile,
            e.strerror, e.errno))
        exit(1)


def read_pid(filename):
    """Read pid from file

    :param filename: file containing pid
    :returns: pid
    :raises IOError: if pid file couldn't be opened

    """
    pidfile = os.path.expanduser(filename)

    try:
        with open(pidfile, 'r') as f:
            return f.readline()
    except IOError as e:
        logger.critical('Could not open pid file {}: {} ({})'.format(
            pidfile, e.strerror, e.errno))
        raise


def kill_playback():
    """Kill playback
    :returns: TODO

    """
    print("Killing playback")


def parse_args(args):
    parser = argparse.ArgumentParser(description='Loop play video files.')

    parser.add_argument('file', nargs='?', help='file to loop')
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s 0.0.1')
    parser.add_argument('--kill', '-k', action='store_true', 
            help='kill video playback')

    return parser.parse_args()


def main():
    args = parse_args(sys.argv[1:])

    create_logger('play', LOGFILE, logging.DEBUG)

    if args.kill:
        kill_playback()
        sys.exit(0)

    if not args.file:
        print("You need to tell me what to play.")
        sys.exit(1)


    play_loop(args.file)
