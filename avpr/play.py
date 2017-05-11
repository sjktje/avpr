#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys

from .logger import create_logger
from .utils import run_cmd

__version__ = '0.0.1'

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

    command = "omxplayer -o hdmi --loop --no-osd --no-keys {}".format(filename)

    logger.info('Looping playback of {}'.format(filename))

    pid = run_cmd(command)

    write_pid(pid, PIDFILE)


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

    :returns: nothing

    """

    pidfile = os.path.expanduser(PIDFILE)

    try:
        with open(pidfile, 'r') as f:
            pid = int(f.readline())
            os.kill(pid, signal.SIGTERM)
    except IOError as e:
        logger.debug(
            ('Could not open pid file {}: {} ({}) -- '
             'perhaps there is no player running?'
             ).format(pidfile, e.strerror, e.errno))

    except OSError as e:
        logger.debug('Could not kill playback: {} ({})'.format(e.strerror,
            e.errno))
    else:
        logger.info('Killed playback (pid {})'.format(str(pid)))
        os.remove(pidfile)



def parse_args(args):
    parser = argparse.ArgumentParser(description='Loop play video files.')

    parser.add_argument('file', nargs='?', help='file to loop')
    parser.add_argument('--version', '-V', action='version',
                        version='%(prog)s {}'.format(__version__))
    parser.add_argument('--kill', '-k', action='store_true', 
            help='kill video playback')

    return parser.parse_args(args)


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
