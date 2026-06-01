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

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QDirIterator
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QFont
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QProxyStyle
from PySide6.QtWidgets import QStyle
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
COLORS = [(QColorConstants.Svg.darkred,  _tr('Item', 'Dark red')),
          (QColorConstants.Svg.red, _tr('Item', 'Red')),
          (QColorConstants.Svg.coral, _tr('Item', 'Coral')),
          (QColorConstants.Svg.orange, _tr('Item', 'Orange')),
          (QColorConstants.Svg.gold, _tr('Item', 'Gold')),
          (QColorConstants.Svg.yellow, _tr('Item', 'Yellow')),
          (QColorConstants.Svg.darkgreen, _tr('Item', 'Dark green')),
          (QColorConstants.Svg.green, _tr('Item', 'Green')),
          (QColorConstants.Svg.greenyellow, _tr('Item', 'Green yellow')),
          (QColorConstants.Svg.lightgreen, _tr('Item', 'Light green')),
          (QColorConstants.Svg.darkblue, _tr('Item', 'Dark blue')),
          (QColorConstants.Svg.blue, _tr('Item', 'Blue')),
          (QColorConstants.Svg.royalblue, _tr('Item', 'Royal blue')),
          (QColorConstants.Svg.skyblue, _tr('Item', 'Sky blue')),
          (QColorConstants.Svg.cyan, _tr('Item', 'Cyan/Aqua')),
          (QColorConstants.Svg.magenta, _tr('Item', 'Magenta / Fuchsia')),
          (QColorConstants.Svg.purple, _tr('Item', 'Purple')),
          (QColorConstants.Svg.black, _tr('Item', 'Black')),
          (QColorConstants.Svg.gray, _tr('Item', 'Gray')),
          (QColorConstants.Svg.lightgray, _tr('Item', 'Light gray')),
          (QColorConstants.Svg.white, _tr('Item', 'White'))]

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
TBS = {'I': (_tr('Preferences', 'Icon only'), Qt.ToolButtonStyle.ToolButtonIconOnly), 
       'T': (_tr('Preferences', 'Text only'), Qt.ToolButtonStyle.ToolButtonTextOnly),
       'B': (_tr('Preferences', 'Text beside icon'), Qt.ToolButtonStyle.ToolButtonTextBesideIcon),
       'U': (_tr('Preferences', 'Text under icon'), Qt.ToolButtonStyle.ToolButtonTextUnderIcon),
       'S': (_tr('Preferences', 'Follow style'), Qt.ToolButtonStyle.ToolButtonFollowStyle)}

# tab position dictionary
TP = {'N': (_tr('Preferences', "Tabs above the pages"), QTabWidget.TabPosition.North), 
      'S': (_tr('Preferences', "Tabs below the pages"), QTabWidget.TabPosition.South),
      'W': (_tr('Preferences', "Tabs to the left of the pages"), QTabWidget.TabPosition.West),
      'E': (_tr('Preferences', "Tabs to the right of the pages"), QTabWidget.TabPosition.East)} 


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
