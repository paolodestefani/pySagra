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

# check component version modules
from platform import python_version
from psycopg import __version__ as psycopg_version
from PySide6 import __version__ as pyside6_version
from PySide6.QtCore import qVersion

# PySide6
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtCore import Qt
from PySide6.QtCore import QLocale
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialog

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
from App.System.Login import LoginDialog
from App.System.MainWindow import MainWindow


def logUnhandledException(ex_cls: str, ex:str, tb: types.TracebackType) -> None:
    "Function to get and log unhadked exceptions"
    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('%s', ex_cls)
    logging.critical('%s', ex)
    # normal cursor
    QApplication.restoreOverrideCursor()
    # message is html (qt ritch text)
    exs = (str(ex)
           .replace("&", "&amp;")
           .replace("<", "&lt;")
           .replace(">", "&gt;")
           .replace('"', "&quot;"))
    msg = f"""<pre>{''.join(traceback.format_tb(tb))}</pre><b>{exs}</b>"""
    if QMessageBox.critical(session.get('mainwin'),
                            "Unhadled exception",
                            msg,
                            QMessageBox.StandardButton.Ignore | QMessageBox.StandardButton.Abort
                            ) == QMessageBox.StandardButton.Abort:
        sys.exit(0)


# -------------------------------------------------------------------------- #

if __name__ == "__main__":
    "Start application"
    # check client component minimum required version
    # python version
    v1, v2, v3 = python_version().split('.')[:3]
    c1, c2, c3 = MRV_PYTHON.split('.')[:3]
    if f"{v1:0>4}{v2:0>4}{v3:0>4}" < f"{c1:0>4}{c2:0>4}{c3:0>4}":
        print("This program require Python rel. >= {} but detected "
              "rel. {}".format(MRV_PYTHON, python_version()))
        sys.exit(0)
    # psycopg version
    if len(psycopg_version.split('.')) == 3:
        v1, v2, v3 = psycopg_version.split('.')
    else:
        v1, v2 = psycopg_version.split('.')
        v3 = '0'
    c1, c2, c3 = MRV_PSYCOPG.split('.')[:3]
    if f"{v1:0>4}{v2:0>4}{v3:0>4}" < f"{c1:0>4}{c2:0>4}{c3:0>4}":
        print(f"This program require psycopg rel. >= {MRV_PSYCOPG} but detected "
              f"rel. {psycopg_version}")
        sys.exit(0)
    # PySide version
    v1, v2, v3 = pyside6_version.split('.')[:3]
    c1, c2, c3 = MRV_PYSIDE.split('.')[:3]
    if f"{v1:0>4}{v2:0>4}{v3:0>4}" < f"{c1:0>4}{c2:0>4}{c3:0>4}":
        print(f"This program require PySide6 rel. >= {MRV_PYSIDE} but detected "
              f"rel. {pyside6_version}")
        sys.exit(0)
    # Qt version
    v1, v2, v3 = qVersion().split('.')[:3]
    c1, c2, c3 = MRV_QT.split('.')[:3]
    if f"{v1:0>4}{v2:0>4}{v3:0>4}" < f"{c1:0>4}{c2:0>4}{c3:0>4}":
        print(f"This program require Qt rel. >= {MRV_QT} but detected "
              f"rel. {qVersion()}")
        sys.exit(0)
        
    # parse command line arguments for logging
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel",
                        default="CRITICAL",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAl'],
                        help="Set the required log level")
    parser.add_argument("-f", "--logfile",
                        nargs='?',
                        help="Log to a specified log file, default logfile.txt on current working directory")
    parser.add_argument("-c", "--console",
                        action='store_true',
                        help="Log to console if available, overcome logging to a file")  # only if a console is available
    args = parser.parse_args()
    # LOGGING TO TEXT FILEs
    # an empty (None) logfile cause logging to <cwd>\logfile.log
    if args.logfile:
        # check log file access
        try:
            open(args.logfile, 'w')
        except IOError:
            print(f"No write access to {args.logfile}")
            sys.exit(0)
        else:
            logfile = args.logfile
    else:
        logfile = os.path.join(os.getcwd(), 'logfile.log')
    # log to console
    if args.console:
        logfile = None
    # set required log level
    if args.loglevel == 'DEBUG':
        loglevel = logging.DEBUG
    elif args.loglevel == 'INFO':
        loglevel = logging.INFO
    elif args.loglevel == 'WARNING':
        loglevel = logging.WARNING
    elif args.loglevel == 'ERROR':
        loglevel = logging.ERROR
    else:
        loglevel = logging.CRITICAL  # default loglevel
    # start logging
    logging.basicConfig(filename=logfile,
                        level=loglevel,
                        format='%(asctime)s %(levelname)s %(module)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    ##########################################
    # redirect uncaught exceptions to logger
    #sys.excepthook = logUnhandledException
    ##########################################
    # logging information
    logging.info('')
    logging.info('****************************************')
    logging.info('Starting %s version %s.%s.%s %s', APPNAME, APPVERSIONMAJOR, APPVERSIONMINOR, APPVERSIONPATCH, APPVERSIONTAG)
    logging.info('Log level set to %s', logging.getLevelName(logging.getLogger().level))
    logging.info('****************************************')
    logging.info('')
    # start PySide6 Application
    logging.info('Setting up QApplication')
    app = QApplication(sys.argv)
    # l10n
    logging.info('Setting up QLocale to system locale')
    lang = QLocale.system().name()[:2]  # = system language
    # on macos system locale is not correct
    if QOperatingSystemVersion.currentType() == QOperatingSystemVersion.OSType.MacOS:
        lang = QLocale().uiLanguages(QLocale.TagSeparator.Underscore)[-1]
    # install translators for qt and main application
    logging.info('Installing translators')
    for i in ('login', APPNAME):
        t = QTranslator()
        if t.load(i + '_' + lang, ":/"):
            if app.installTranslator(t):
                session[i + '_translator'] = t
    # set basic parameters
    logging.info('Setting QApplication name, version, domain and icon')
    app.setApplicationName(APPNAME)
    app.setApplicationVersion(f'{APPVERSIONMAJOR:02}.{APPVERSIONMINOR:02}.{APPVERSIONPATCH:04}')
    app.setOrganizationName(ORGANIZATION)
    app.setOrganizationDomain(WEBSITE)
    app.setWindowIcon(QIcon(f":/{APPNAME}"))
    # create a db and application connection
    logging.info('Starting the login dialog')
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Rejected:
        sys.exit(0)
    # create a main window
    logging.info('Starting MainWindow')
    session['mainwin'] = MainWindow()
    session['mainwin'].show()
    sys.exit(app.exec())
    