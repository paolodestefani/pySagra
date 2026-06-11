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

"""About

Definition and management of About and SystemInfo dialogs

"""

# standard library
import logging
import platform

# psycopg
import psycopg

# PySide6
from PySide6 import __version__ as PySide6_version
from PySide6.QtCore import qVersion
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QMovie
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox

# application modules
from App import APPNAME
from App import APPVERSIONMAJOR 
from App import APPVERSIONMINOR 
from App import APPVERSIONPATCH
from App import APPVERSIONTAG
from App import AUTHOR
from App import EMAIL
from App import WEBSITE
from App import session
#from App import currentAction
from App.Database.Connect import database_information
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Ui.AboutDialog import Ui_AboutDialog
from App.Ui.SystemInfoDialog import Ui_SystemInfoDialog


# logger
logger = logging.getLogger(__name__)


def about(action: QAction, checked: bool = False) -> None:
    "About information dialog"
    logger.info('Starting about dialog')
    a = AboutDialog(session['mainwin'])
    a.show()
    logger.info('About dialog shown')


def systemInfo(action: QAction, checked: bool = False) -> None:
    "System Information action"
    logger.info('Starting system info dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[2]: # no execute permission
        QMessageBox.warning(
            mw,
            _tr('MessageDialog', "Warning"),
            _tr('CashDesk', 'No access right to this function')
        )
        return
    h = SystemInfoDialog(session['mainwin'], action.icon())
    h.show()
    logger.info('System info shown')


def aboutQt(action: QAction, checked: bool = False) -> None:
    "About Qt"
    logger.info('Starting about qt dialog')
    QMessageBox.aboutQt(session['mainwin'])
    logger.info('About qt dialog shown')



class AboutDialog(QDialog):
    "Dialog showing About informations"

    def __init__(self, parent: QWidget) -> None:
        QDialog.__init__(self, parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.labelIcon.setPixmap(QGuiApplication.windowIcon().pixmap(128))
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog | 
                            Qt.WindowType.WindowMinMaxButtonsHint |
                            Qt.WindowType.WindowCloseButtonHint)
        appDescription = _tr("About", "A small program to manage a food stand")
        versionLabel = _tr("About", "Version")
        devDescription = _tr("About", "Developed with:")
        pythonRef = _tr('About', 'programming language')
        psycopgRef = _tr('About', 'PostgreSQL adapter for Python')
        qtRef = _tr('About', 'cross-platform application and UI framework')
        pySideRef = _tr('About', 'a set of python bindings for Qt')
        oxygenRef = _tr('About', 'icon set and others from')
        iconRef = _tr('About', "pySagra's icon is from DelliOS System Icons by")
        gifRef = _tr('About', "pySagra's login/version animation was created by")
        licence1 = _tr('About', """This program is <b>FREE SOFTWARE</b>: you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.""")
        licence2 = _tr('About', """This program is distributed in the hope that it will be useful,
            but <b>WITHOUT ANY WARRANTY</b>; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU General Public License for more details.""")
        licence3 = _tr('About', """You should have received a copy of the GNU General Public License
            along with this program. If not, see 
            <a href="http://www.gnu.org/licenses">http://www.gnu.org/licenses/</a>.""")
        
        text = (f'<b style="font-size: 32pt;">{APPNAME}</b>'
            f'<p><b style="font-size: 16pt;">{appDescription}</b></p>'
            f'<p><b style="font-size: 16pt;">{versionLabel} {APPVERSIONMAJOR}.{APPVERSIONMINOR}.{APPVERSIONPATCH} {APPVERSIONTAG}</b></p>'
            f'<p>Copyright &copy; 2026 {AUTHOR}</p>'
            f'<p><a href="mailto:{EMAIL}">{EMAIL}</a> - <a href="{WEBSITE}">{WEBSITE}</a><p>'
            #f'<p>{appDescription}</p>'
            f'<p>{devDescription}</p>'
            f'<ul>'
            f'<li><a href="https://www.python.org">Python</a> {pythonRef}</li>'
            f'<li><a href="https://www.psycopg.org/">Psycopg</a> {psycopgRef}</li>'
            f'<li><a href="https://www.qt.io/">Qt</a> {qtRef}</li>'
            f'<li><a href="https://doc.qt.io/qtforpython-6/">Qt for Python</a> {pySideRef}</li>'
            f'<li><a href="https://github.com/KDE/oxygen-icons">Oxygen icons</a> {oxygenRef} <a href="https://www.iconarchive.com/">Icon Archive</a></li>'
            f'</ul>'
            f'<p>{iconRef} <a href="https://dellustrations.com">Dellustrations</a></p>'
            f'<p>{gifRef} <a href="https://pixabay.com/users/placidplace-25572496/">Placidplace</a></p>'
            f'<p>{licence1}</p>'
            f'<p>{licence2}</p>'
            f'<p>{licence3}</p>'
            f'<hr />'
            f'<p style="font-weight: bold; font-size: 16pt; text-align: center;">'
            '<a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU Gpl 3.0</a>')
        
        self.ui.labelAbout.setText(text)
        rect = QPixmap(":/login_gif").rect()
        self.logo = QMovie(":/login_gif")
        if self.logo.isValid():
            self.logo.setScaledSize(QSize(rect.width()//2, rect.height()//2))
            self.ui.labelAnimation.setMovie(self.logo)
            self.logo.start()


class SystemInfoDialog(QDialog):
    "Dialog showing system informations"

    def __init__(self, parent: QWidget, icon: QIcon) -> None:
        QDialog.__init__(self, parent)
        self.ui = Ui_SystemInfoDialog()
        self.ui.setupUi(self)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog | 
                            Qt.WindowType.WindowMinMaxButtonsHint |
                            Qt.WindowType.WindowCloseButtonHint)
        self.ui.lineEditServer.setText(f"{session['server']}:{session['port']}")
        self.ui.lineEditDatabase.setText(session['database'])
        self.ui.lineEditCompany.setText(f"{session['current_company']} {session['company_description']}")
        self.ui.lineEditUser.setText(session['user'])
        self.ui.lineEditProfile.setText(session['profile'])
        text = f"<table>"
        for i in (('Application', APPNAME),
                  ('Version', f"{APPVERSIONMAJOR}.{APPVERSIONMINOR}.{APPVERSIONPATCH} {APPVERSIONTAG}"),
                  ('Python', platform.python_version()),
                  ('Psycopg', psycopg.__version__),
                  ('PySide6', PySide6_version),
                  ('Qt', qVersion()),
                  ('Platform', platform.platform()),
                  ('Architecture', platform.architecture()[0])):
            text += f"<tr><td><b>{i[0]}</b></td><td>{i[1]}</td></tr>"
        text += f"<tr><td></td><td></td></tr>"  # empty line
        with gui_exception_context(self, _tr('SystemInfo', 'System info database information')):
            for i in database_information():
                text += f"<tr><td><b>{i[0]}</b></td><td>{i[1]}</td></tr>"
            text += f"</table>"
        self.ui.textEditInfo.setText(text)
