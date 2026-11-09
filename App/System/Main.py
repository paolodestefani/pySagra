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

"""Application startup

This module checks the library versions, sets up Qt and translations, then
runs the login dialog and the main window.

It must stay light at module level: the application modules are imported by
run(), after check_requirements() has confirmed they can work.

"""

# standard library
import logging
import re
import sys
import traceback
import types

# psycopg
from psycopg import __version__ as psycopg_version

# PySide6
from PySide6 import __version__ as pyside6_version
from PySide6.QtCore import QLocale
from PySide6.QtCore import qVersion
from PySide6.QtGui import QIcon
from PySide6.QtNetwork import QHostInfo
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog

# application definitions
from App import APPNAME
from App import APPVERSIONMAJOR
from App import APPVERSIONMINOR
from App import APPVERSIONPATCH
from App import APPVERSIONTAG
from App import MRV_PSYCOPG
from App import MRV_PYSIDE
from App import MRV_QT
from App import ORGANIZATION
from App import WEBSITE
from App import session


# logger
logger = logging.getLogger(__name__)


def log_unhandled_exception(ex_cls: type[BaseException],
                            ex: BaseException,
                            tb: types.TracebackType | None) -> None:
    "Function to get and log unhandled exceptions"
    # Ctrl+C from a terminal: the default behaviour, no error box
    if issubclass(ex_cls, KeyboardInterrupt):
        sys.__excepthook__(ex_cls, ex, tb)
        return
    from App.Widget.MessageBox import MessageBoxCritical
    logger.critical(''.join(traceback.format_tb(tb)))
    logger.critical('%s', ex_cls)
    logger.critical('%s', ex)
    # no QApplication yet: no widget can be shown, the log is all
    if QApplication.instance() is None:
        return
    # normal cursor
    QApplication.restoreOverrideCursor() # good in any case
    MessageBoxCritical(session.get('mainwin'),
                       "Unhandled exception",
                       "Uncaught exception occurred, see details for more information",
                       str(ex),
                       ''.join(traceback.format_tb(tb)))


def check_requirements() -> str | None:
    "Return a description of the first library that is too old, None if all are fine"
    required = (('PySide6', pyside6_version, MRV_PYSIDE),
                ('Qt', qVersion(), MRV_QT),
                ('psycopg', psycopg_version, MRV_PSYCOPG))
    for name, version, minimum in required:
        # leading digits only: pre-releases like 6.12.0a1 or 3.3.4.dev1 are fine
        numbers = tuple(int(m.group()) for m in (re.match(r'\d+', part) for part in version.split('.')[:3]) if m)
        if numbers < minimum:
            return (f"This program requires {name} {'.'.join(map(str, minimum))} "
                    f"or later, detected {version}")
    return None


def run() -> None:
    "Run the application until the user quits, ImportError means a missing library"
    # imported before the translators are installed: messages translated at
    # import time stay in English
    from App.Common.L10n import install_translators
    from App.Common.L10n import system_language
    from App.System.Login import LoginDialog
    from App.System.MainWindow import MainWindow

    ##########################################
    # redirect uncaught exceptions to logger
    sys.excepthook = log_unhandled_exception
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
    session['hostname'] = QHostInfo.localHostName()
    logger.info('Computer hostname has been set to %s', session['hostname'])
    # l10n
    logger.info('Setting up QLocale to system locale')
    lang = system_language()
    # set default locale even if it is not stricly necessary
    session['qlocale'] = QLocale(lang)
    QLocale.setDefault(session['qlocale'])
    # install translators for qt and main application
    logger.info('Installing translators')
    install_translators(lang)
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
