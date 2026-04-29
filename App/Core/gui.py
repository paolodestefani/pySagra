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

"""Localization functions and utilities

This module contains functions to manage localization, translations
and currency formatting

"""

# standard library
import decimal

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QDirIterator
from PySide6.QtGui import QFont
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QProxyStyle
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QStyleFactory

# application modules
from App import APPNAME
from App import currentIcon
from App import session
from App import currentAction
from App import actionDefinition

# color scheme
color_scheme = {
    'L': Qt.ColorScheme.Light,
    'D': Qt.ColorScheme.Dark,
    'S': Qt.ColorScheme.Unknown} # system default



class CenteredProxyStyle(QProxyStyle):
    "Proxy style to center checkboxes in item views"

    def subElementRect(self, element, option, widget=None):
        # get the standard rectangle from the underlying style engine
        rect = super().subElementRect(element, option, widget)
        if element == QStyle.SubElement.SE_ItemViewItemCheckIndicator:
            # center the checkbox rectangle relative to the entire cell
            rect.moveCenter(option.rect.center())
        return rect


def setTheme(theme: str) -> None:
    "Set the application theme"
    app = QApplication.instance()
    if app is not None and isinstance(app, QApplication):
        base_style = QStyleFactory.create(theme) 
        proxy_style = CenteredProxyStyle(base_style)
        app.setStyle(proxy_style)
        app.processEvents()
    
def setColorScheme(color: str) -> None:
    "Set the application color scheme"
    QApplication.styleHints().setColorScheme(color_scheme.get(color, Qt.ColorScheme.Unknown))
    
def setIconTheme(theme: str) -> None: # used in login, currentIcon created before currentAction
    "Fill currentIcon dictionary"
    # application icon
    currentIcon[APPNAME] = QIcon(f":/{APPNAME}")
    it = QDirIterator(f":/icon/{theme or 'oxygen'}", QDirIterator.IteratorFlag.NoIteratorFlags)
    # in resource.qrc an alias is mandatory, the it.fileName() is the alias
    while it.hasNext():
        it.next()
        if it.fileInfo().isFile(): # QDirIterator returns 'icons' directory too (probably current directory) that i don't use
            pix = QPixmap(it.filePath())
            currentIcon[it.fileName()] = QIcon(pix)

def setIcon(theme: str) -> None:
    "Set action's icon"
    currentIcon.clear()
    setIconTheme(theme)
    # updte current action's icons
    for action in currentAction:
        currentAction[action].setIcon(currentIcon[actionDefinition[action][3]])

def setFont(ffamily: str|None = None, fsize: int = 10):
    "Set font family and font size"
    app = QApplication.instance()
    if app is None or not isinstance(app, QApplication):
        return
    if ffamily is None:
        font = QFont()
    else:
        font = QFont(ffamily,
                     fsize,
                     QFont.Weight.Normal)
    app.setFont(font)
