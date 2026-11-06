#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Author: Paolo De Stefani
# Contact: paolo <at> paolodestefani <dot> it
# Copyright (C) 2026 Paolo De Stefani
# License: GPL v3

# This file is part of pySagra.
#
# pySagra is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pySagra is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pySagra.  If not, see <http://www.gnu.org/licenses/>.

"""pySagra - Application launcher

This module sets up logging, checks the environment and starts the application
that lives in App.Main.

It must import only the standard library at module level and stay readable by
older Python releases: it has to run even when a library is missing or the
Python version is wrong, so that the problem can be reported. print() is not
an option because a graphical application has no console on macOS and Windows.

"""

# standard library
import argparse
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import NoReturn, Optional


# minimum required Python release, it can not live in the App package because
# importing App requires PySide6
MIN_PYTHON = (3, 14)

# log file rotation
LOG_MAX_BYTES = 1_000_000
LOG_BACKUPS = 3

# logger
logger = logging.getLogger(__name__)


def default_log_file() -> str:
    "Return the log file path in the user log folder of the current platform"
    if sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Logs/pySagra.log')
    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
        return os.path.join(base, 'pySagra', 'Logs', 'pySagra.log')
    base = os.environ.get('XDG_STATE_HOME') or os.path.expanduser('~/.local/state')
    return os.path.join(base, 'pySagra', 'pySagra.log')


def open_log_file(logfile: Optional[str]) -> Optional[RotatingFileHandler]:
    "Return a handler for the required log file or, failing that, the default one"
    for path in filter(None, (logfile, default_log_file())):
        try:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            return RotatingFileHandler(path,
                                       maxBytes=LOG_MAX_BYTES,
                                       backupCount=LOG_BACKUPS,
                                       encoding='utf-8')
        except OSError:
            continue
    return None


def setup_logging(level: str, logfile: Optional[str]) -> None:
    "Log to file and, when there is one, to the console"
    handlers: list[logging.Handler] = []
    file_handler = open_log_file(logfile)
    if file_handler is not None:
        handlers.append(file_handler)
    if sys.stderr is not None:  # None in a windowed application
        handlers.append(logging.StreamHandler())
    logging.basicConfig(level=getattr(logging, level),
                        format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=handlers)


def fatal(message: str) -> NoReturn:
    "Log the error, show it to the user whenever possible and exit"
    logger.critical(message)
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.critical(None, 'pySagra', message)
    except ImportError:
        pass  # without Qt the console and the log file are all that is left
    sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    "Return the logging arguments, the others are left to Qt"
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel",
                        default="WARNING",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the required log level")
    parser.add_argument("-f", "--logfile",
                        nargs='?',
                        help="Log to the specified file instead of the default one")
    args, _ = parser.parse_known_args()
    return args


def main() -> None:
    "Start application"
    # set working directory to the executable folder if frozen (= executed from pyinstaller's bundle)
    # mandatory for macos and usefull for windows and linux as well
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    args = parse_arguments()
    setup_logging(args.loglevel, args.logfile)
    if sys.version_info < MIN_PYTHON:
        fatal(f"This program requires Python {'.'.join(map(str, MIN_PYTHON))} or later, "
              f"detected {sys.version.split()[0]}")
    try:
        # App modules are imported here so that a failure can be reported
        from App.Main import check_requirements, run
        problem = check_requirements()
        if problem:
            fatal(problem)
        run()
    except ImportError as er:
        fatal(f"Missing or unusable library: {er.name or er}")
    except Exception as er:  # a library can fail at import time in other ways
        logger.exception("Startup failed")
        fatal(f"Startup failed: {er}")


if __name__ == "__main__":
    main()
