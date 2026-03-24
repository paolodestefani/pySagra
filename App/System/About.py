#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Author: Paolo De Stefani
# Contact: paolo <at> paolodestefani <dot> it
# Copyright (C) 2026 Paolo De Stefani
# License:

"""About

This module define and launch About/SystemInfo dialogs

"""

# standard library
import logging
import platform

# psycopg
import psycopg

# PySide6
from PySide6.QtCore import __version__ as PySide6_version
from PySide6.QtCore import qVersion
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
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
from App import currentAction
from App.Database.Connect import database_information
from App.Core.L10n import _tr
from App.Ui.AboutDialog import Ui_AboutDialog
from App.Ui.SystemInfoDialog import Ui_SystemInfoDialog


# logger
logger = logging.getLogger(__name__)


def about() -> None:
    "About information dialog"
    logger.info('Starting about dialog')
    a = AboutDialog(session['mainwin'])
    a.show()
    logger.info('About dialog shown')


def systemInfo() -> None:
    "System Information action"
    logger.info('Starting system info dialog')
    h = SystemInfoDialog(session['mainwin'])
    h.show()
    logger.info('System info shown')


def aboutQt() -> None:
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
        self.ui.labelIcon.setPixmap(QGuiApplication.windowIcon().pixmap(100))
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog|Qt.WindowType.WindowMinMaxButtonsHint|Qt.WindowType.WindowCloseButtonHint)
        versionLabel = _tr("Help", "Version")
        devDescription = _tr("Help", "Developed with:")
        pythonRef = _tr('Help', 'programming language')
        psycopgRef = _tr('Help', 'PostgreSQL adapter for Python')
        qtRef = _tr('Help', 'cross-platform application and UI framework')
        pySideRef = _tr('Help', 'a set of python bindings for Qt')
        oxygenRef = _tr('Help', 'icon set')
        iconRef = _tr('Help', "pySagra's icon is from DelliOS System Icons by")
        gifRef = _tr('Help', "pySagra's login/version animation was created by")
        licence1 = _tr('Help', """This program is <b>FREE SOFTWARE</b>: you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.""")
        licence2 = _tr('Help', """This program is distributed in the hope that it will be useful,
            but <b>WITHOUT ANY WARRANTY</b>; without even the implied warranty of
            MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
            GNU General Public License for more details.""")
        licence3 = _tr('Help', """You should have received a copy of the GNU General Public License
            along with this program. If not, see 
            <a href="http://www.gnu.org/licenses">http://www.gnu.org/licenses/</a>.""")
        
        text = (f'<b style="font-size: 32pt;">{APPNAME}</b>'
            #f'<p><b>{APPDESC}</b></p>'
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
            f'<li><a href="https://github.com/KDE/oxygen-icons">Oxygen icons</a> {oxygenRef}</li>'
            f'</ul>'
            f'<p>{iconRef} <a href="https://dellustrations.com/ )">Dellustrations</a></p>'
            f'<p>{gifRef} <a href="https://pixabay.com/users/placidplace-25572496/">Placidplace</a></p>'
            f'<p>{licence1}</p>'
            f'<p>{licence2}</p>'
            f'<p>{licence3}</p>'
            f'<hr />'
            f'<p style="font-weight: bold; font-size: 16pt; text-align: center;"><a href="https://www.gnu.org/licenses/gpl-3.0.html">GNU Gpl 3.0</a>')
        
        self.ui.labelAbout.setText(text)
        rect = QPixmap(":/login_gif").rect()
        self.logo = QMovie(":/login_gif")
        if self.logo.isValid():
            self.logo.setScaledSize(QSize(rect.width()//2, rect.height()//2))
            self.ui.labelAnimation.setMovie(self.logo)
            self.logo.start()


class SystemInfoDialog(QDialog):
    "Dialog showing system informations"

    def __init__(self, parent: QWidget) -> None:
        QDialog.__init__(self, parent)
        self.ui = Ui_SystemInfoDialog()
        self.ui.setupUi(self)
        self.ui.labelIcon.setPixmap(currentAction['about_system_info'].icon().pixmap(128))
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog|Qt.WindowType.WindowMinMaxButtonsHint|Qt.WindowType.WindowCloseButtonHint)
        self.ui.lineEditServer.setText(f"{session['server']}:{session['port']}")
        self.ui.lineEditDatabase.setText(session['database'])
        self.ui.lineEditCompany.setText(f"{session['current_company']} {session['company_description']}")
        self.ui.lineEditUser.setText(session['user'])
        self.ui.lineEditProfile.setText(session['profile'])
        text = f"<table>"
        for i in (('Application', APPNAME),
                  #('Description', APPDESC),
                  ('Version', f"{APPVERSIONMAJOR}.{APPVERSIONMINOR}.{APPVERSIONPATCH} {APPVERSIONTAG}"),
                  ('Python', platform.python_version()),
                  ('Psycopg', psycopg.__version__),
                  ('PySide6', PySide6_version),
                  ('Qt', qVersion()),
                  ('Platform', platform.platform()),
                  ('Architecture', platform.architecture()[0])):
            text += f"<tr><td><b>{i[0]}</b></td><td>{i[1]}</td></tr>"
        text += f"<tr><td></td><td></td></tr>"  # empty line
        for i in database_information():
            text += f"<tr><td><b>{i[0]}</b></td><td>{i[1]}</td></tr>"
        text += f"</table>"
        self.ui.textEditInfo.setText(text)
