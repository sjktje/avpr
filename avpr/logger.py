#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

def create_logger(name, logfile, level):
    """Create and setup logger.

    :param name: name of logger
    :param logfile: file to write log to
    :param level:
        logging level defined in the logging module. See
        https://docs.python.org/2/howto/logging.html#logging-levels for
        details.
    :returns: nothing

    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fh = logging.FileHandler(os.path.expanduser(logfile))
    fh.setLevel(level)

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    fh.setFormatter(formatter)

    logger.addHandler(fh)
