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
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QProxyStyle
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QStyleFactory
from PySide6.QtWidgets import QTabWidget

# application modules
from App import APPNAME
from App import currentIcon
from App import session
from App import currentAction
from App import actionDefinition
from App.Core.L10n import _tr



# colors for color combo box
COLORS = [('#950606', _tr('Item', 'Dark red')),
          ('#FF0000', _tr('Item', 'Red')),
          ('#FF7700', _tr('Item', 'Orange')),
          ('#FFFF00', _tr('Item', 'Yellow')),
          ('#006400', _tr('Item', 'Dark green')),
          ('#008000', _tr('Item', 'Green')),
          ('#90EE90', _tr('Item', 'Light green')),
          ('#000077', _tr('Item', 'Dark blue')),
          ('#0000FF', _tr('Item', 'Blue')),
          ('#4141C5', _tr('Item', 'Light blue')),
          ('#00FFFF', _tr('Item', 'Cyan/Aqua')),
          ('#FF00FF', _tr('Item', 'Magenta / Fuchsia')),
          ('#A52A2A', _tr('Item', 'Brown')),
          ('#000000', _tr('Item', 'Black')),
          ('#808080', _tr('Item', 'Gray')),
          ('#D3D3D3', _tr('Item', 'Light gray')),
          ('#FFFFFF', _tr('Item', 'White'))]

# color scheme
CS = {'L': (_tr('Preferences', "Light"), Qt.ColorScheme.Light),
      'D': (_tr('Preferences', "Dark"), Qt.ColorScheme.Dark),
      'S': (_tr('Preferences', "System default"), Qt.ColorScheme.Unknown)}

# icon theme
IT = [('oxygen', _tr('Preferences', 'Oxygen')),
      ('crystal_clear', _tr('Preferences', 'Crystal Clear')),
      ('fluentui', _tr('Preferences', 'Fluent UI')),
      ('flatwoken', _tr('Preferences', 'Flatwoken'))]

# toolbutton style dictionary
TBS = {'I': (_tr('Preferences', 'Icon only'), Qt.ToolButtonIconOnly), 
       'T': (_tr('Preferences', 'Text only'), Qt.ToolButtonTextOnly),
       'B': (_tr('Preferences', 'Text beside icon'), Qt.ToolButtonTextBesideIcon),
       'U': (_tr('Preferences', 'Text under icon'), Qt.ToolButtonTextUnderIcon),
       'S': (_tr('Preferences', 'Follow style'), Qt.ToolButtonFollowStyle)}

# tab position dictionary
TP = {'N': (_tr('Preferences', "Tabs above the pages"), QTabWidget.North), 
      'S': (_tr('Preferences', "Tabs below the pages"), QTabWidget.South),
      'W': (_tr('Preferences', "Tabs to the left of the pages"), QTabWidget.West),
      'E': (_tr('Preferences', "Tabs to the right of the pages"), QTabWidget.East)} 


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
    
    
def setColorScheme(color: str|None) -> None:
    "Set the application color scheme"
    if not color:
        color = 'S'
    QApplication.styleHints().setColorScheme(CS[color][1])
    
    
def setIconTheme(theme: str|None) -> None: # used in login, currentIcon created before currentAction
    "Fill currentIcon dictionary"
    if not theme:
        theme = 'oxygen'
    # application icon
    currentIcon[APPNAME] = QIcon(f":/{APPNAME}")
    it = QDirIterator(f":/icon/{theme}", QDirIterator.IteratorFlag.NoIteratorFlags)
    # in resource.qrc an alias is mandatory, the it.fileName() is the alias
    while it.hasNext():
        it.next()
        if it.fileInfo().isFile(): # QDirIterator returns 'icons' directory too (probably current directory) that i don't use
            pix = QPixmap(it.filePath())
            currentIcon[it.fileName()] = QIcon(pix)


def setIcon(theme: str|None) -> None:
    "Set action's icon"
    if not theme:
        theme = 'oxygen'
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
