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

"""Help

Definition and management of Help and Faq dialogs

"""

# standard library
import logging
from pathlib import Path

# PySide6
from PySide6.QtCore import QUrl
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QEvent
from PySide6.QtGui import QIcon
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtPrintSupport import QPrintPreviewDialog

# application modules
from App import APPNAME
from App import session
from App import currentIcon
from App.Common.L10n import _tr
from App.Ui.HelpDialog import Ui_HelpDialog

# logger
logger = logging.getLogger(__name__)

# the documentation folder: in the project root, or in the data folder of the PyInstaller
# bundle where the App package is too; one subfolder for each language, English is
# used for the languages with no documentation
DOCUMENTATION = Path(__file__).resolve().parents[2] / 'Documentation'
DEFAULT_LANGUAGE = 'en'


def help(action: QAction, checked: bool = False) -> None:
    "Show help dialog"
    logger.info('Starting help dialog')
    dialog = HelpDialog(APPNAME, session['mainwin'].helpLink(), session['mainwin'])
    dialog.show()
    logger.info('Help dialog shown')


def faq(action: QAction, checked: bool = False) -> None:
    "Show FAQ dialog"
    logger.info('Starting faq dialog')
    dialog = HelpDialog(APPNAME, "help/faq.html", session['mainwin'])
    dialog.show()
    logger.info('Faq dialog shown')


class HelpDialog(QDialog):
    "Dialog showing help content"

    def __init__(self, title: str, source: str, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_HelpDialog()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog |
                            Qt.WindowType.WindowMinMaxButtonsHint |
                            Qt.WindowType.WindowCloseButtonHint)
        # set buttons' icons
        self.ui.toolButtonBack.setIcon(currentIcon['edit_previous'] if not currentIcon['edit_previous'].isNull() else QIcon(":/icon/oxygen/edit_previous"))
        self.ui.toolButtonHome.setIcon(currentIcon['edit_home'] if not currentIcon['edit_home'].isNull() else QIcon(":/icon/oxygen/edit_home"))
        self.ui.toolButtonForward.setIcon(currentIcon['edit_next'] if not currentIcon['edit_next'].isNull() else QIcon(":/icon/oxygen/edit_next"))
        self.ui.toolButtonFind.setIcon(currentIcon['edit_find'] if not currentIcon['edit_find'].isNull() else QIcon(":/icon/oxygen/edit_find"))
        self.ui.toolButtonPrint.setIcon(currentIcon['edit_print'] if not currentIcon['edit_print'].isNull() else QIcon(":/icon/oxygen/edit_print"))
        # restore geometry and slider
        st = QSettings()
        if st.value("Help/Geometry"):
            self.restoreGeometry(st.value("Help/Geometry"))
        else:
            self.setGeometry(50, 50, 800, 600)
        self.sliderValue = st.value("Help/SliderTextZoom", 1, type=int) 
        self.ui.horizontalSliderZoom.setValue(self.sliderValue)
        # restore text zoom
        for i in range(self.sliderValue): # type: ignore
            self.ui.textBrowserContent.zoomIn(1)
        # signal/slot
        self.ui.toolButtonBack.clicked.connect(self.ui.textBrowserContent.backward)
        self.ui.toolButtonHome.clicked.connect(self.goToCustomHome)
        self.ui.toolButtonForward.clicked.connect(self.ui.textBrowserContent.forward)
        #self.ui.textBrowserContent.setSource(QUrl(f"qrc:/{source}"))        
        self.setWindowTitle(f"{title}")
        # action for find text
        findDesc = _tr('Help', 'Find')
        self.fa = QAction(f"{findDesc}", self)
        self.fa.setShortcut("F3")
        self.fa.triggered.connect(self.findText)
        self.addAction(self.fa)
        # signal / slot
        self.ui.toolButtonPrint.clicked.connect(self.print)
        self.ui.horizontalSliderZoom.valueChanged.connect(self.sliderChangedValue)
        self.ui.toolButtonFind.clicked.connect(self.findText)
        # start browsing
        self.loadHelpPage(source)
        
    def loadHelpPage(self, page_name: str) -> None:
        """Load a page of the documentation folder of the user language, page_name as
        "help/login.html" or "help/main.html#gui"; the main page if it doesn't exist.
        Links and images are relative to the page, as in a browser"""
        page, _, anchor = page_name.removeprefix('help/').partition('#')
        folder = DOCUMENTATION / session['qlocale'].name()[:2]
        if not folder.is_dir():
            folder = DOCUMENTATION / DEFAULT_LANGUAGE
        path = folder / page
        if not path.is_file():
            path, anchor = folder / 'main.html', ''
        url = QUrl.fromLocalFile(str(path))
        if anchor:
            url.setFragment(anchor)
        self.ui.textBrowserContent.setSource(url)

    def goToCustomHome(self) -> None:
        "Go to the main help page"
        self.loadHelpPage('main.html')
        
    def sliderChangedValue(self, value: int) -> None:
        "Update zoom based on slider"
        if value > self.sliderValue: # type: ignore
            self.ui.textBrowserContent.zoomIn(1)
        else:
            self.ui.textBrowserContent.zoomOut(1)
        self.sliderValue = value

    def print(self) -> None:
        "Print help contents"
        dialog = QPrintPreviewDialog(self)
        dialog.setGeometry(50, 50, 750, 550)
        dialog.setWindowFlags(Qt.WindowType.Dialog | 
                              Qt.WindowType.WindowMinMaxButtonsHint |
                              Qt.WindowType.WindowCloseButtonHint)
        title = _tr('Help', "Print preview of")
        dialog.setWindowTitle(f"{title} {self.windowTitle()}")
        dialog.paintRequested.connect(self.ui.textBrowserContent.print_)
        dialog.exec()

    def findText(self) -> None:
        "Find text"
        self.ui.textBrowserContent.setFocus()
        if not self.ui.textBrowserContent.find(self.ui.lineEditFind.text()):
            QMessageBox.warning(
                self,
                _tr('Help', "Warning"),
                _tr('Help', "Text not found")
            )
            self.ui.textBrowserContent.home()
            cur = self.ui.textBrowserContent.textCursor()
            cur.setPosition(0, QTextCursor.MoveMode.MoveAnchor)
            self.ui.textBrowserContent.setTextCursor(cur)

    def closeEvent(self, event: QEvent) -> None:
        "Save geometry and slider setting on exit"
        st = QSettings()
        st.setValue("Help/Geometry", self.saveGeometry())
        st.setValue("Help/SliderTextZoom", self.sliderValue)
        event.accept()

