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
from PySide6.QtCore import QDir
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


# functions are required for the correct work of _tr() wich need
# the translations made after the module import

# colors for color combo box
def get_colors()-> list[tuple]:
    """Returns the list of colors for combo boxes, translated at runtime"""
    return [
        (QColorConstants.Svg.darkred,  _tr('Color', 'Dark red')),
        (QColorConstants.Svg.red, _tr('Color', 'Red')),
        (QColorConstants.Svg.coral, _tr('Color', 'Coral')),
        (QColorConstants.Svg.orange, _tr('Color', 'Orange')),
        (QColorConstants.Svg.gold, _tr('Color', 'Gold')),
        (QColorConstants.Svg.yellow, _tr('Color', 'Yellow')),
        (QColorConstants.Svg.darkgreen, _tr('Color', 'Dark green')),
        (QColorConstants.Svg.green, _tr('Color', 'Green')),
        (QColorConstants.Svg.greenyellow, _tr('Color', 'Green yellow')),
        (QColorConstants.Svg.lightgreen, _tr('Color', 'Light green')),
        (QColorConstants.Svg.darkblue, _tr('Color', 'Dark blue')),
        (QColorConstants.Svg.blue, _tr('Color', 'Blue')),
        (QColorConstants.Svg.royalblue, _tr('Color', 'Royal blue')),
        (QColorConstants.Svg.skyblue, _tr('Color', 'Sky blue')),
        (QColorConstants.Svg.cyan, _tr('Color', 'Cyan / Aqua')),
        (QColorConstants.Svg.magenta, _tr('Color', 'Magenta / Fuchsia')),
        (QColorConstants.Svg.purple, _tr('Color', 'Purple')),
        (QColorConstants.Svg.black, _tr('Color', 'Black')),
        (QColorConstants.Svg.gray, _tr('Color', 'Gray')),
        (QColorConstants.Svg.lightgray, _tr('Color', 'Light gray')),
        (QColorConstants.Svg.white, _tr('Color', 'White'))
    ]

# color scheme
def get_color_scheme() -> dict[str, tuple]:
    """Returns the color scheme dictionary, translated at runtime"""
    return {
        'L': (_tr('ColorScheme', "Light"), Qt.ColorScheme.Light),
        'D': (_tr('ColorScheme', "Dark"), Qt.ColorScheme.Dark),
        'S': (_tr('ColorScheme', "System default"), Qt.ColorScheme.Unknown)
    }

# icon theme
def get_icon_themes() -> list[tuple[str, str]]:
    """Returns the available icon themes, translated at runtime"""
    return [
        ('oxygen', _tr('IconSet', 'Oxygen')),
        ('crystal_clear', _tr('IconSet', 'Crystal Clear')),
        ('fluentui', _tr('IconSet', 'Fluent UI')),
        ('flatwoken', _tr('IconSet', 'Flatwoken'))
    ]

# toolbutton style dictionary
def get_toolbutton_styles() -> dict[str, tuple]:
    """Returns the toolbutton styles, translated at runtime"""
    return {
        'I': (_tr('ToolButtonStyle', 'Icon only'), Qt.ToolButtonStyle.ToolButtonIconOnly), 
        'T': (_tr('ToolButtonStyle', 'Text only'), Qt.ToolButtonStyle.ToolButtonTextOnly),
        'B': (_tr('ToolButtonStyle', 'Text beside icon'), Qt.ToolButtonStyle.ToolButtonTextBesideIcon),
        'U': (_tr('ToolButtonStyle', 'Text under icon'), Qt.ToolButtonStyle.ToolButtonTextUnderIcon),
        'S': (_tr('ToolButtonStyle', 'Follow style'), Qt.ToolButtonStyle.ToolButtonFollowStyle)
    }

# tab position dictionary
def get_tab_positions() -> dict[str, tuple]:
    """Returns the positions of the QTabWidget tabs, translated at runtime"""
    return {
        'N': (_tr('TabPosition', "Tabs above the pages"), QTabWidget.TabPosition.North), 
        'S': (_tr('TabPosition', "Tabs below the pages"), QTabWidget.TabPosition.South),
        'W': (_tr('TabPosition', "Tabs to the left of the pages"), QTabWidget.TabPosition.West),
        'E': (_tr('TabPosition', "Tabs to the right of the pages"), QTabWidget.TabPosition.East)
    }


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
    QApplication.styleHints().setColorScheme(get_color_scheme()[color][1])
    
    
def setIconTheme(theme: str|None) -> None: # used in login, currentIcon created before currentAction
    "Fill currentIcon dictionary"
    if not theme:
        theme = 'oxygen'
    # application icon
    currentIcon[APPNAME] = QIcon(f":/{APPNAME}")
    it = QDirIterator(f":/icon/{theme}", QDir.Filter.Files, QDirIterator.IteratorFlag.NoIteratorFlags)
    # in resource.qrc an alias is mandatory, the it.fileName() is the alias
    while it.hasNext():
        it.next()
        #if it.fileInfo().isFile(): # QDirIterator returns 'icons' directory too (probably current directory) that i don't use
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
