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
from PySide6.QtCore import QSysInfo
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QToolBar
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QStyleFactory
from PySide6.QtWidgets import QPushButton

# application modules
from App import APPNAME
from App import session
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Core.Gui import get_color_scheme
from App.Core.Gui import get_icon_themes
from App.Core.Gui import get_toolbutton_styles
from App.Core.Gui import get_tab_positions
from App.Core.Gui import setTheme
from App.Core.Gui import setColorScheme
from App.Core.Gui import setIcon
from App.Database.Preferences import load_preferences
from App.Database.Preferences import save_preferences
from App.System.Help import HelpDialog
from App.Ui.PreferencesDialog import Ui_PreferencesDialog


# logger
logger = logging.getLogger(__name__)


def preferences(action: QAction, checked: bool = False) -> None:
    "Launch preferences dialog"
    logger.info('Starting preferences dialog')
    mw = session['mainwin']
    title = action.text()
    icon = action.icon()
    auth = action.data()
    if not auth[2]: # no execute permission
        QMessageBox.warning(
            mw,
            _tr('MessageDialog', "Warning"),
            _tr('MessageDialog', 'No access right to this function')
        )
        return
    dialog = PreferencesDialog(mw, title, icon)
    dialog.show()
    logger.info('Preferences dialog shown')


class PreferencesDialog(QDialog):
    "Preferences dialog"

    def __init__(self, parent: QTabWidget, title: str, icon: QIcon) -> None:
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
        self.ui.comboBoxColorScheme.setItemList([(i[0], i[1][0]) for i in get_color_scheme().items()])
        # icons - here for translation requirement (a QApplication is require for _tr() to work)
        self.ui.comboBoxIcons.setItemList(get_icon_themes())
        # tool button style - here for translation requirement (a QApplication is require for _tr() to work)
        self.ui.comboBoxToolButtonStyle.setItemList([(i[0], i[1][0]) for i in get_toolbutton_styles().items()])
        # tab position - here for translation requirement (a QApplication is require for _tr() to work)
        self.ui.comboBoxTabPosition.setItemList([(i[0], i[1][0]) for i in get_tab_positions().items()])
        self.ui.comboBoxFontFamily.setCurrentFont(QFont('Arial'))
        self.ui.spinBoxFontSize.setValue(10)
        # load user preferences
        success = False
        with gui_exception_context(self, _tr('Preferences', 'Load user preferences')):
            theme, color, icon, ffamily, fsize, tbstyle, tabposition  = load_preferences(session['app_user_code'])
            success = True
        if not success:
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
        # help request
        self.ui.buttonBox.helpRequested.connect(self.showHelp)
        
    def showHelp(self) -> None:
        "Open help dialog for contextual help"
        dialog = HelpDialog(APPNAME, "help/preferences.html" , self)
        dialog.show()

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
            i.setToolButtonStyle(get_toolbutton_styles()[tbstyle][1])
        session['mainwin'].tabWidget.setTabPosition(get_tab_positions()[tabposition][1])
        # save new preferences
        with gui_exception_context(self, _tr('Preferences', 'Save user preferences')):
            save_preferences(session['app_user_code'], 
                             theme,
                             color,
                             icon,
                             ffamily,
                             fsize,
                             tbstyle,
                             tabposition)

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

