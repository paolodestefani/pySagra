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

"""Constants

This module define some constants as return values of funcions
used mainly for RelationDelegate

"""

from PySide6.QtGui import QIcon

from App.Core.L10n import _tr


# language and country list

def langCountryFlags() -> list[tuple[QIcon, str, str]]:
    "Returns a list of languages/countries with flag icon"
    # Must use a function because QIcon() can be created only after a QApplication()
    return [#(QIcon(), None, None),
            (QIcon(':/flags/flag_italy'), 'it_IT', "Italiano / Italia"),
            (QIcon(':/flags/flag_usa'), 'en_US', "English / United States"),
            (QIcon(':/flags/flag_uk'), 'en_UK', "English / United Kingdom"),
            (QIcon(':/flags/flag_france'), 'fr_FR', "Français / France"),
            (QIcon(':/flags/flag_germany'), 'de_DE', "Deutsch / Deutschland"),
            (QIcon(':/flags/flag_russia'), 'ru_RU', "русский / Россия"),
            (QIcon(':/flags/flag_china'), 'zh_CN', "中國 / 中國"),
            (QIcon(':/flags/flag_thailand'), 'th_TH', "ไทย / ประเทศไทย")]

def langCountry() -> list[tuple[str, str]]:
    "Returns a list of languages/countries"
    # neew 2 function for use with relationalDelegate
    return [('it_IT', "Italiano / Italia"),
            ('en_US', "English / United States"),
            ('en_UK', "English / United Kingdom"),
            ('fr_FR', "Français / France"),
            ('de_DE', "Deutsch / Deutschland"),
            ('ru_RU', "русский / Россия"),
            ('zh_CN', "中國 / 中國"),
            ('th_TH', "ไทย / ประเทศไทย")]



def itemType() -> list:
    return [('I', _tr('Item', 'Item')),
            ('K', _tr('Item', 'Kit')),
            ('M', _tr('Item', 'Menu'))]
    
    

def deliveryType():
    return [('T', _tr('OrderArchive', 'Table')),
            ('A', _tr('OrderArchive', 'Take Away'))]
    
def orderStatus():
    return [('A', _tr('OrderArchive', 'Acquired')),
            ('I', _tr('OrderArchive', 'In progress')),
            ('P', _tr('OrderArchive', 'Processed'))]

