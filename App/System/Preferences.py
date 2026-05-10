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

"""Preferences

Preferences allow to set/modify user preferences: ui theme, icon set, font, ecc.

"""

# standard library
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QDirIterator
from PySide6.QtCore import QSysInfo
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QToolBar
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialogButtonBox

from PySide6.QtWidgets import QStyleFactory
from PySide6.QtWidgets import QPushButton

# application modules
from App import APPNAME
from App import session
from App import currentAction
from App import actionDefinition
from App import currentIcon
from App.Core.L10n import _tr
from App.Core.Gui import CS, IT, TBS, TP
from App.Core.Gui import setTheme
from App.Core.Gui import setColorScheme
from App.Core.Gui import setIcon
from App.Database.Exceptions import PyAppDBError
from App.Database.Preferences import load_preferences
from App.Database.Preferences import save_preferences
from App.Ui.PreferencesDialog import Ui_PreferencesDialog


# logger
logger = logging.getLogger(__name__)


def preferences(action: QAction, checked: bool = False) -> None:
    "Launch preferences dialog"
    logger.info('Starting preferences dialog')
    mw = session['mainwin']
    auth = action.data()
    title = action.text()
    icon = action.icon()
    dialog = PreferencesDialog(mw, title, icon, auth)
    dialog.show()
    logger.info('Preferences dialog shown')


class PreferencesDialog(QDialog):
    "Preferences dialog"

    def __init__(self, parent: QTabWidget, title: str, icon: QIcon, auth: str) -> None:
        super().__init__(parent)
        self.ui = Ui_PreferencesDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        self.ui.labelIcon.setPixmap(icon.pixmap(100))
        # setup widgets
        # themes - from platform available qt styles
        self.ui.comboBoxTheme.addItems(QStyleFactory.keys())
        # color scheme for dark mode
        self.ui.comboBoxColorScheme.setItemList([(i[0], i[1][0]) for i in CS.items()])
        # icons - here for translation requirement (a QApplication is require for _tr() to work)
        self.ui.comboBoxIcons.setItemList(IT)
        # tool button style - here for translation requirement (a QApplication is require for _tr() to work)
        self.ui.comboBoxToolButtonStyle.setItemList([(i[0], i[1][0]) for i in TBS.items()])
        # tab position - here for translation requirement (a QApplication is require for _tr() to work)
        self.ui.comboBoxTabPosition.setItemList([(i[0], i[1][0]) for i in TP.items()])
        self.ui.comboBoxFontFamily.setCurrentFont(QFont('Arial'))
        self.ui.spinBoxFontSize.setValue(10)
        # load user preferences
        try:
            theme, color, icon, ffamily, fsize, tbstyle, tabposition  = load_preferences(session['app_user_code'])
        except PyAppDBError as er:
            title = _tr("Preferences", "Error loading user preferences")
            logger.error("On load preferences database error: %s %s", er.code, er.message)
            QMessageBox.critical(self, title, er.message)
            return
        # set widget current value
        self.ui.comboBoxTheme.setCurrentText(theme)
        self.ui.comboBoxColorScheme.modelDataStr = color or 'S'
        self.ui.comboBoxIcons.modelDataStr = icon or 'oxygen'
        if ffamily:
            self.ui.comboBoxFontFamily.setCurrentFont(QFont(ffamily))
        else:
            self.ui.checkBoxDefaultFont.setChecked(True) # Null ffamily = default
        self.ui.spinBoxFontSize.setValue(fsize or QFont().pointSize())
        self.ui.comboBoxToolButtonStyle.modelDataStr = tbstyle or 'I'
        self.ui.comboBoxTabPosition.modelDataStr = tabposition or 'N'
        
        # signal/slot
        self.ui.buttonBox.clicked.connect(self.clicked)

    def clicked(self, button: QPushButton) -> None:
        "Call Apply on clicked"
        if self.ui.buttonBox.standardButton(button) in (QDialogButtonBox.StandardButton.Apply,
                                                        QDialogButtonBox.StandardButton.Ok):
            self.apply()
        if self.ui.buttonBox.standardButton(button) == QDialogButtonBox.StandardButton.RestoreDefaults:
            self.restoreDefault()
            
    def apply(self) -> None:
        "Apply settings variations"
        app = QApplication.instance()
        if app is None or not isinstance(app, QApplication):
            return
        # gui preferences
        theme = self.ui.comboBoxTheme.currentText()
        color = self.ui.comboBoxColorScheme.modelDataStr
        icon = self.ui.comboBoxIcons.modelDataStr
        if self.ui.checkBoxDefaultFont.isChecked():
            font = QFont() # default font
            ffamily = None
        else:
            font = self.ui.comboBoxFontFamily.currentFont()
            ffamily = font.family()
        fsize = self.ui.spinBoxFontSize.value()
        tbstyle = self.ui.comboBoxToolButtonStyle.modelDataStr
        tabposition = self.ui.comboBoxTabPosition.modelDataStr
        # set preferences
        setTheme(theme)
        setColorScheme(color)
        font.setPointSize(fsize)
        setIcon(icon)
        app.setFont(font)
        for i in session['mainwin'].findChildren(QToolBar):
            i.setToolButtonStyle(TBS[tbstyle][1])
        session['mainwin'].tabWidget.setTabPosition(TP[tabposition][1])
        # save new preferences
        try:
            save_preferences(session['app_user_code'], 
                             theme,
                             color,
                             icon,
                             ffamily,
                             fsize,
                             tbstyle,
                             tabposition)
        except PyAppDBError as er:
            title = _tr("Preferences", "Error saving user preferences")
            logger.error("On save preferences database error: %s %s", er.code, er.message)
            QMessageBox.critical(self, title, er.message)

    def restoreDefault(self) -> None:
        "Restore default setings"
        # theme
        match QSysInfo.productType():
            case 'windows':
                theme = 'windows'
            case 'macos':
                theme = 'macOS'
            case _:
                theme = 'fusion'
        self.ui.comboBoxTheme.setCurrentText(theme)
        # font
        font = QFont() # default font
        self.ui.comboBoxFontFamily.setFont(font)
        self.ui.checkBoxDefaultFont.setChecked(True)
        self.ui.spinBoxFontSize.setValue(font.pointSize())
        # color scheme
        self.ui.comboBoxColorScheme.setCurrentIndex(2) # system default
        # tool button style
        self.ui.comboBoxToolButtonStyle.setCurrentIndex(0) # icon only
        # icon theme
        self.ui.comboBoxIcons.setCurrentIndex(0) # oxygen
        # tab position
        self.ui.comboBoxTabPosition.setCurrentIndex(0) # north
        # apply()
        self.apply()
        
    def accept(self) -> None:
        "Apply and exit"
        self.apply()
        QDialog.accept(self)

