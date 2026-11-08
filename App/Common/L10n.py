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

# standard library
import logging

# PySide6
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QLocale
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon

# application modules
from App import APPNAME
from App import session


# logger
logger = logging.getLogger(__name__)


# translate function

def _tr(context: str, text: str, disambig: str | None = None) -> str:
    return QCoreApplication.translate(context, text, disambig)


def system_language() -> str:
    "Two letters code of the language of the operating system user interface"
    lang = QLocale.system().name()[:2]
    # on macOS the user interface language can differ from the system locale
    if QOperatingSystemVersion.currentType() == QOperatingSystemVersion.OSType.MacOS:
        ui_langs = QLocale().uiLanguages(QLocale.TagSeparator.Underscore)
        if ui_langs:
            lang = ui_langs[0][:2]
    return lang


def install_translators(lang: str) -> None:
    """Replace the Qt and application translators with the ones of a language,
    English needs none: it is the language of the source strings"""
    for name in ('qtbase', APPNAME):
        key = name + '_translator'
        current = session.get(key)
        if current is not None:
            QCoreApplication.removeTranslator(current)
        session[key] = None
        if lang == 'en':
            continue
        translator = QTranslator()
        if not translator.load(f"{name}_{lang}", ":/"):
            logger.warning("No %s translation for language %s", name, lang)
        elif not QCoreApplication.installTranslator(translator):
            logger.error("Error installing the %s translator for language %s", name, lang)
        else:
            session[key] = translator
            logger.info("Installed the %s translator for language %s", name, lang)


def fromCurrency(val: str) -> decimal.Decimal:
    "Returns a decimal value from input (locale aware) string"
    if val:  # value come from spinboxes and model data (QVariant)
        if isinstance(val, str):
            return decimal.Decimal(session['qlocale'].toFloat(val)[0])
        else:
            return decimal.Decimal(val)
    else:
        return decimal.Decimal(0)
    
    
def toCurrency(val: decimal.Decimal | float | int) -> str:
    """Return a localized string representation of a currency value without symbols."""
    # Convert integer cents back to a standard float format strictly for the QLocale formatter
    #float_val = float(val / 100) if isinstance(val, int) else float(val)
    return session['qlocale'].toCurrencyString(float(val), ' ')  # Space character suppresses the currency symbol

def toString(val: decimal.Decimal | float | int) -> str:
    """Return a localized string representatuin of a quantity value"""
    return session['qlocale'].toString(val)


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

