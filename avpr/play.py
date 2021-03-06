#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import sys

from .logger import create_logger, map_loglevel
from .utils import create_dir, run_cmd
from . import __version__

AVPRDIR = os.path.expanduser(os.path.join('~', '.avpr'))
LOGFILE = os.path.join(AVPRDIR, 'play.log')
PIDFILE = os.path.join(AVPRDIR, 'play.pid')

logger = logging.getLogger('play')

def play_loop(filename):
    """Loop video file

    :param filename: file to loop
    """


    if not os.path.isfile(filename):
        logger.critical('Could not open {}'.format(filename))
        sys.exit(1)

    command = "omxplayer -o hdmi --loop --no-osd --no-keys --aspect-mode fill {}".format(filename)

    logger.info('Looping playback of {}'.format(filename))

    pid = run_cmd(command)

    write_pid(pid, PIDFILE)


def open_log(filename):
    """Open log file.

    :param filename: file to append log to
    :returns: file handle
    :raises IOError: if file couldn't be opened
    """

    logfile = filename
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
    pidfile = filename

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
    pidfile = filename

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

    pidfile = PIDFILE

    try:
        with open(pidfile, 'r') as f:
            pid = int(f.readline())
            os.killpg(pid, signal.SIGTERM)
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
    parser.add_argument('--verbosity', '-v', action='count',
                        help='increase log verbosity.')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    create_dir(AVPRDIR)

    create_logger('play', LOGFILE, map_loglevel(args.verbosity))

    if args.kill:
        kill_playback()
        sys.exit(0)

    if not args.file:
        print(('You need to tell me what to play. '
               'See {} -h for help.').format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    play_loop(args.file)
