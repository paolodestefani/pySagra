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

This module startup the application, login to database server and start
the main window

"""

# standard library
import sys
import os
import traceback
import types
import logging
import argparse
from typing import Any

# check component version modules
from sys import version_info
from typing import Any
from psycopg import __version__ as psycopg_version
from PySide6 import __version__ as pyside6_version
from PySide6.QtCore import qVersion 

# PySide6
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtCore import QLocale
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtNetwork import QHostInfo

# minimum required version of application components
from App import MRV_PYTHON
from App import MRV_PYSIDE
from App import MRV_QT
from App import MRV_PSYCOPG

# application definitions
from App import APPNAME
from App import APPVERSIONMAJOR
from App import APPVERSIONMINOR
from App import APPVERSIONPATCH
from App import APPVERSIONTAG
from App import ORGANIZATION
from App import WEBSITE
from App import session

# application modules
from App.Widget.Dialog import MessageBoxCritical
from App.System.Login import LoginDialog
from App.System.MainWindow import MainWindow
    

# logger
logger = logging.getLogger(__name__)


def logUnhandledException(ex_cls: type[BaseException], ex: BaseException, tb: types.TracebackType | None) -> None:
    "Function to get and log unhandled exceptions"
    logger.critical(''.join(traceback.format_tb(tb)))
    logger.critical('%s', ex_cls)
    logger.critical('%s', ex)
    # normal cursor
    QApplication.restoreOverrideCursor() # good in any case
    MessageBoxCritical(session.get('mainwin'),
                       "Unhandled exception",
                       "Uncaught exception occurred, see details for more information",
                       str(ex),
                       ''.join(traceback.format_tb(tb)))


# -------------------------------------------------------------------------- #

if __name__ == "__main__":
    "Start application"
    # set working directory to the executable folder if frozen (= execut from pyinstaller bundle)
    # mandatory for macos and usefull for windows and linux as well
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
            
    # parse command line arguments for logging
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel",
                        default="CRITICAL",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Set the required log level")
    parser.add_argument("-f", "--logfile",
                        nargs='?',
                        help="Log to a specified log file, default logfile.txt on current working directory")
    parser.add_argument("-c", "--console",
                        action='store_true',
                        help="Log to console if available, overcome logging to a file")  # only if a console is available
    args, unknown = parser.parse_known_args()
    loglevel = getattr(logging, args.loglevel.upper(), logging.CRITICAL)
    logfile = None
    # logging to console if available, otherwise to a file
    if args.console:
        logfile = None  # Console
    elif args.logfile:
        try:
            with open(args.logfile, 'a', encoding="utf-8") as f:
                pass
            logfile = args.logfile
        except IOError:
            # not able to write to the specified file, fallback to default
            logfile = os.path.join(os.getcwd(), 'logfile.log')
    else:
        # default behavior
        # save log file to system folder on MacOS, to current working directory on other platforms
        if sys.platform == 'darwin':
            log_dir = os.path.expanduser("~/Library/Logs")
            os.makedirs(log_dir, exist_ok=True)
            logfile = os.path.join(log_dir, "pySagra.log")
        else:
            logfile = os.path.join(os.getcwd(), 'logfile.log')
            
    log_config: dict[str, Any] = {
        "level": loglevel,
        "format": '%(asctime)s %(levelname)s %(module)s: %(message)s',
        "datefmt": '%Y-%m-%d %H:%M:%S'
    }
    # if logfile is None, basicConfig write automatically to sys.stderr (Console)
    if logfile:
        log_config["filename"] = logfile
        log_config["encoding"] = "utf-8"

    logging.basicConfig(**log_config)
    
    # check client component minimum required version
    # python version
    pyv = (version_info.major, version_info.minor, version_info.micro)
    if pyv < MRV_PYTHON:
        logger.critical(f"This program require Python rel. >= {MRV_PYTHON} but detected rel. {pyv}")
        sys.exit(0)
    # PySide version
    psv = tuple(map(int, pyside6_version.split('.')[:3]))
    if psv < MRV_PYSIDE:
        logger.critical(f"This program require PySide6 rel. >= {MRV_PYSIDE} but detected rel. {psv}")
        sys.exit(0)
    # Qt version
    qtv = tuple(map(int, qVersion().split('.')[:3]))
    if qtv < MRV_QT:
        logger.critical(f"This program require Qt rel. >= {MRV_QT} but detected rel. {qtv}")
        sys.exit(0)
    # psycopg version
    ppv = tuple(map(int, psycopg_version.split('.')[:3]))
    if ppv < MRV_PSYCOPG:
        logger.critical(f"This program require psycopg rel. >= {MRV_PSYCOPG} but detected rel. {ppv}")
        sys.exit(0)
    
    ##########################################
    # redirect uncaught exceptions to logger
    sys.excepthook = logUnhandledException
    ##########################################
    # logging information
    logger.info('')
    logger.info('****************************************')
    logger.info('Starting %s version %s.%s.%s %s', APPNAME, APPVERSIONMAJOR, APPVERSIONMINOR, APPVERSIONPATCH, APPVERSIONTAG)
    logger.info('Log level set to %s', logging.getLevelName(logging.getLogger().level))
    logger.info('****************************************')
    logger.info('')
    # start PySide6 Application
    logger.info('Setting up QApplication')
    app = QApplication(sys.argv)
    # host name
    session['computer_name'] = QHostInfo.localHostName()
    logger.info('Computer name has been set to %s', session['computer_name'])
    # l10n
    logger.info('Setting up QLocale to system locale')
    # set system language
    lang = QLocale.system().name()[:2]
    # different behaviour on macOS
    if QOperatingSystemVersion.currentType() == QOperatingSystemVersion.OSType.MacOS:
        ui_langs = QLocale().uiLanguages(QLocale.TagSeparator.Underscore)
        if ui_langs:
            lang = ui_langs[0][:2]
    # set default locale even if it is not stricly necessary
    session['qlocale'] = QLocale(lang)
    QLocale.setDefault(session['qlocale'])
    # install translators for qt and main application
    logger.info('Installing translators')
    for i in ('qtbase', APPNAME):
        tr_key = i + '_translator'
        session[tr_key] = QTranslator()
        if session[tr_key].load(f"{i}_{lang}", ":/"):
            if app.installTranslator(session[tr_key]):
                logger.info("Successfully installed translator for %s", i)
            else:
                logger.error("Error installing application translator for %s", i)
                session[tr_key] = None
        else:
            logger.error("Error loading application translator for %s", i)
            session[tr_key] = None
    # set basic parameters
    logger.info('Setting QApplication name, version, domain and icon')
    app.setApplicationName(APPNAME)
    app.setApplicationVersion(f'{APPVERSIONMAJOR:02}.{APPVERSIONMINOR:02}.{APPVERSIONPATCH:04}')
    app.setOrganizationName(ORGANIZATION)
    app.setOrganizationDomain(WEBSITE)
    app.setWindowIcon(QIcon(f":/{APPNAME}"))
    # create a db and application connection
    logger.info('Starting the login dialog')
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Rejected:
        sys.exit(0)
    # create a main window
    logger.info('Starting MainWindow')
    session['mainwin'] = MainWindow()
    session['mainwin'].show()
    sys.exit(app.exec())
    