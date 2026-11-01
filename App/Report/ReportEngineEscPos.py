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

"""Report Engine - generate reports from XML string definition and list of
items/tuples or SQL query for ESC/POS printers

This module is a pure python simple report engine for printing to Esc/Pos printers.
The report definition is an XML document string. The dataset are a python list or
tuple or the result set of an SQL query.

Architecture:
Printing objects are defined of 2 types:
- inline objects (print a list of objects in one line)
- block objects (each object takes up a full line)
A report definition is made of bands. Every band is a collection of printing
block objects (line, barcode, images, row). A row is a container of inline objects printed in one line.
A row con grow in multiple lines and generates the line printing form the included objects.
Every band have a fixed height (but can grow).
In every report we can have this sections:
- a header printed at the beginning of every print job
- group header printed at the beginning of the
  group for each detail group
- details printed for each record of the data source
- group footer printed at the end of the
  group for each detail group
- a footer printed at the end of every print job

Any section can have one or more band.
All sections are optional but a report need at least one detail band.

"""

# standard library
import sys
import collections
import decimal
import itertools
import xml.etree.ElementTree as ET
import operator
import logging
import textwrap
import random
import zlib

from itertools import zip_longest
from typing import Any
from contextlib import contextmanager
from escpos.printer import Dummy, Network, Usb
from escpos.constants import QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q, QR_ECLEVEL_H
from escpos.constants import QR_MODEL_1, QR_MODEL_2, QR_MICRO
import PIL
from io import BytesIO
import base64
import socket

import re
import barcode as pybarcode
import qrcode
from qrcode import constants as qrc


# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QRectF
from PySide6.QtCore import QMarginsF
from PySide6.QtCore import QSizeF
from PySide6.QtCore import QLocale, QPointF
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QFile
from PySide6.QtCore import QIODeviceBase
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal

from PySide6.QtGui import QGuiApplication 
from PySide6.QtGui import QPageLayout 
from PySide6.QtGui import QPaintDevice 
from PySide6.QtGui import QPdfWriter 
from PySide6.QtGui import QPolygonF
from PySide6.QtGui import QCursor
from PySide6.QtGui import QImage

from PySide6.QtWidgets import QApplication
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtPrintSupport import QPrinter

from App.Report.EscposPreview import ReceiptPreview   # absolute import
    
    
# application definitions for special fields
if __name__ != "__main__":
    from App import APPNAME
    from App import APPVERSIONMAJOR
    from App import APPVERSIONMINOR
    from App import APPVERSIONPATCH
    from App import AUTHOR
    from App import EMAIL
    from App import ORGANIZATION
    from App import WEBSITE
    from App import session
    from App.Database.Settings import Settings
    from App.Common.ExceptionHandler import wait_cursor_context
    from App.Report import ReportException
    from App.Report import ReportCreationError
    from App.Report import ReportXMLParseError
    from App.Report import ReportNoDataError
    from App.Report import ReportPrintError

else:
    APPNAME = "Report ESC/POS Engine"
    APPVERSIONMAJOR = 1
    APPVERSIONMINOR = 0
    APPVERSIONPATCH = 0
    APPVERSION = f"{APPVERSIONMAJOR:02}.{APPVERSIONMINOR:02}.{APPVERSIONPATCH:02}"
    AUTHOR = "Paolo De Stefani"
    EMAIL = "info@paolodestefani.it"
    ORGANIZATION = "PDS Software"
    WEBSITE = "https://www.paolodestefani.it"
    session = dict()
    session['qlocale'] = QLocale()
    session['event_description'] = "The over-the-top party in 2026"
    session['event_image'] = QByteArray()
    session['company_description'] = "Local festivities committee"
    session['company_image'] = QByteArray()
    
    @contextmanager
    def wait_cursor_context():
        """
        Simple context manager for wait cursor only, usefull for 
        heavy operation that does not involve the database
        """
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        try:
            yield
        finally:
            QGuiApplication.restoreOverrideCursor()
            
    class ReportException(Exception):               # type: ignore[no-redef]
        pass

    class ReportCreationError(ReportException):     # type: ignore[no-redef]
        pass

    class ReportXMLParseError(ReportException):     # type: ignore[no-redef]
        pass

    class ReportNoDataError(ReportException):       # type: ignore[no-redef]
        pass

    class ReportPrintError(ReportException):        # type: ignore[no-redef]
        pass

   
# report engine version
VERSION = '1.0'



# Default global options

default_options = {
    'printer_profile':       'TM-T20II',
    'charcode':              'AUTO',
    'align':                 'left', # 'left', 'center', 'right'
    'font':                  'a', # 'a' or 'b'
    'bold':                  False,
    'underline':             0, # 0..2
    'normal_textsize':       True,
    'double_height':         False,
    'double_width':          False,
    'width':                 5,
    'height':                1,
    'density':               0, # print density 0..8
    'invert':                False, # True = white on black printing
    'smooth':                False, # True = text smoothing. Effective on 4x4 size text and larger
    'flip':                  False, # True = upside-down printing
    'quantity_decimals':     2,
    'price_decimals':        2,
    'amount_decimals':       2,
    'currency_symbol':       '€'
}


### BASE RENDERER INLINE OBJECTS ###

class BaseInlineRenderer():
    "Base class for all inline tex renderer elements"

    def __init__(self, options: dict, paramdict: dict) -> None:
        self.is_visible = paramdict.get("is_visible", "true") == 'true'
        self.report = options['report_instance']
        # text properties
        self.font = paramdict.get("font", options['font'])
        self.bold = paramdict.get("bold", "false") == 'true'
        self.underline = int(paramdict.get("underline", "0")) # 0..2
        self.normal_textsize = paramdict.get("normal_textsize", "true") == 'true'
        self.double_height = paramdict.get("double_height", "false") == 'true'
        self.double_width = paramdict.get("double_width", "false") == 'true'
        self.density = int(paramdict.get("density", "0")) # 0..8
        self.invert = paramdict.get("invert", "false") == 'true'
        self.flip = paramdict.get("flip", "false") == 'true'
        self.smooth = paramdict.get("smooth", "false") == 'true'
        # other
        self.width = int(paramdict.get("width", "5"))
        self.align = paramdict.get("align", options['align'])
        self.can_grow = paramdict.get("can_grow", "true") == 'true'
        self.quantity_decimals = int(paramdict.get("quantity_decimals", options['quantity_decimals']))
        self.price_decimals = int(paramdict.get("price_decimals", options['price_decimals']))
        self.amount_decimals = int(paramdict.get("amount_decimals", options['amount_decimals']))
        self.currency_symbol = paramdict.get("currency_symbol", options['currency_symbol'])
        self.field_format = paramdict.get("format", "")
        self.value: bool|int|float|decimal.Decimal|str|QDate|QDateTime|QTime|None = None  # current value
    
    def apply_style(self) -> None:
        "Set the text properties of this element on the print buffer"
        self.report.update_text_properties(
            self.font, self.bold, self.underline, self.normal_textsize, self.double_height,
            self.double_width, self.density, self.invert, self.flip, self.smooth)
        
    def render(self) -> str:
        "Print text"
        if not self.is_visible:
            return '' # Row class fill the line in case of invisible elements 
        # create the output string
        text: str = ''
        match (self.value, self.field_format):
            # --- BOOLEAN ---
            case (bool(), _):
                text = 'X' if self.value else 'O'

            # --- NUMBERS WITH SPECIFIC FORMAT ---
            case (int() | float() | decimal.Decimal(), 'currency'):
                raw_formatted = f"{float(self.value or 0.0):,.2f}"
                integer_part, decimal_part = raw_formatted.split('.')
                text = f"{self.currency_symbol} {integer_part.replace(',', self.report.thousand_sep)}{self.report.decimal_sep}{decimal_part}"

            case (int() | float() | decimal.Decimal(), 'amount'):
                raw_formatted = f"{float(self.value or 0.0):,.{self.amount_decimals}f}"
                if self.amount_decimals > 0:
                    integer_part, decimal_part = raw_formatted.split('.')
                    text = f"{integer_part.replace(',', self.report.thousand_sep)}{self.report.decimal_sep}{decimal_part}"
                else:
                    text = raw_formatted.replace(',', self.report.thousand_sep)

            case (int() | float() | decimal.Decimal(), 'price'):
                raw_formatted = f"{float(self.value or 0.0):,.{self.price_decimals}f}"
                if self.price_decimals > 0:
                    integer_part, decimal_part = raw_formatted.split('.')
                    text = f"{integer_part.replace(',', self.report.thousand_sep)}{self.report.decimal_sep}{decimal_part}"
                else:
                    text = raw_formatted.replace(',', self.report.thousand_sep)

            case (int() | float() | decimal.Decimal(), 'quantity'):
                raw_formatted = f"{float(self.value or 0.0):,.{self.quantity_decimals}f}"
                if self.quantity_decimals > 0:
                    integer_part, decimal_part = raw_formatted.split('.')
                    text = f"{integer_part.replace(',', self.report.thousand_sep)}{self.report.decimal_sep}{decimal_part}"
                else:
                    text = raw_formatted.replace(',', self.report.thousand_sep)

            # --- NUMBERS WITH PYTHON STRING FORMAT (ex. '{0:.2f}') ---
            case (int() | float() | decimal.Decimal(), str() as fmt) if fmt:
                text = fmt.format(self.value)

            # --- NUMBERS WITHOUT FORMAT (Fallback QLocale) ---
            case (decimal.Decimal(), _):
                text = session['qlocale'].toString(float(self.value), 'f', 2)
                
            case (int() | float(), _):
                text = session['qlocale'].toString(self.value)

            # --- DATE AND TIME WITH QT FORMAT ---
            case (QDate() | QDateTime() | QTime(), str() as fmt) if fmt:
                text = session['qlocale'].toString(self.value, fmt)

            # --- DATE AND TIME WITHOUT FORMAT ---
            case (QDate() | QDateTime() | QTime(), _):
                text = session['qlocale'].toString(self.value, QLocale.FormatType.ShortFormat)

            # --- GENERAL FALLBACK ---
            case _:
                text = str(self.value or '')
        # render only the available width if can't grow
        if self.can_grow:
            return text
        else:
            return text[:self.width]

class Label(BaseInlineRenderer):
    "Label class"

    def __init__(self, options: dict, paramdict: dict, text: str) -> None:
        super().__init__(options, paramdict)
        self.value = text # for labels string is the text
        
    def __repr__(self) -> str:
        return f"Label - '{self.value}'"


class Field(BaseInlineRenderer):
    "Field class"

    def __init__(self, options: dict, paramdict: dict, field_name: str) -> None:
        super().__init__(options, paramdict)
        self.value = None
        self.field_name = field_name
        self.suppress_repeated = paramdict.get("suppress_repeated", "false") == 'true'
        
    def __repr__(self) -> str:
        return f"Field for {self.field_name}"

    def set_value(self, value: bool|int|float|decimal.Decimal|str|QDate|QDateTime|QTime|QImage) -> None:
        self.value = value


class Summary(BaseInlineRenderer):
    "Class for summaries"

    def __init__(self, options: dict, paramdict: dict, field_name: str) -> None:
        super().__init__(options, paramdict)
        self.field_name = field_name
        self.function = paramdict['function']
        self.on_related_field = paramdict.get('on_related_field', None)
        self.last_value = None
        self.items = 0
        self.summary = 0
        options['report_instance'].summaries.append(self)  # used for reset all summaries
        
    def __repr__(self) -> str:
        return f"Summery for {self.field_name} {self.function}"

    def update(self, record: dict) -> None:
        "Update summary value"
        # conditional summary updating based on value change of another field
        if self.on_related_field:
            if self.last_value == record[self.on_related_field]:
                return
            self.last_value = record[self.on_related_field]

        match self.function:
            case 'sum':
                self.summary += record[self.field_name]
            case 'count':
                self.summary += 1
            case 'min':
                if self.items > 0:
                    self.summary = min(record[self.field_name], self.summary)
                else:
                    self.summary = record[self.field_name]
            case 'max':
                if self.items > 0:
                    self.summary = max(record[self.field_name], self.summary)
                else:
                    self.summary = record[self.field_name]
            case 'average':
                self.summary += record[self.field_name]
            case _:
                pass
        self.items += 1

    def reset(self) -> None:
        self.last_value = None
        self.summary = 0
        self.items = 0

    def render(self) -> str:
        if self.function == 'average':
            if self.items != 0:
                self.value = self.summary / self.items
            else:
                self.value = f"{self.summary}/{self.items}"
        else:
            self.value = self.summary
        return super().render()


class Special(BaseInlineRenderer):
    "Class for special fields"

    def __init__(self, options:dict, paramdict: dict, var_name: str) -> None:
        super().__init__(options, paramdict)
        self.var_name = var_name
        self.value = None # row.render() set the field value
        
    def __repr__(self) -> str:
        return f"Special element {self.var_name}"

    def render(self) -> str:
        match self.var_name:
            case 'print_date':
                self.value = session['qlocale'].toString(QDate.currentDate(), QLocale.FormatType.ShortFormat)
            case 'print_date_time':
                self.value = session['qlocale'].toString(QDateTime.currentDateTime(), QLocale.FormatType.ShortFormat)
            case 'print_time':
                self.value = session['qlocale'].toString(QTime.currentTime(), QLocale.FormatType.ShortFormat)
            case 'record_number':
                self.value = self.report.rn
            case 'app_name':
                self.value = APPNAME
            case 'app_author':
                self.value = AUTHOR
            case 'app_email':
                self.value = EMAIL
            case 'app_organization':
                self.value = ORGANIZATION
            case 'app_website':
                self.value = WEBSITE
            case 'company_description':
                self.value = session['company_description']
            # case 'company_image':
            #     self.value = QImage()
            #     self.value.loadFromData(session['company_image'])
            case 'event_description':
                self.value = session['event_description']
            # case 'event_image':
            #     self.value = QImage()
            #     self.value.loadFromData(session['event_image'])
            case _:
                self.value = ''
        return super().render()

 

# BLOCK OBJECTS

class BaseBlockRenderer():
    "Base class for all block renderer elements"

    def __init__(self, options: dict, paramdict: dict) -> None:
        self.is_visible = paramdict.get("is_visible", "true") == 'true'
        self.report = options['report_instance']
   
        
class Line(BaseBlockRenderer):
    "Horizontal line"

    def __init__(self, options:dict, paramdict: dict, text:str) -> None:
        super().__init__(options, paramdict)
        self._max = paramdict.get("width", 'not max') == 'max'
        if self._max:
            self.width = 0
        else:
            self.width = int(paramdict.get("width", options['width']))
        self.align = paramdict.get("align", options['align'])
        
    def __repr__(self) -> str:
        return f"Line block object of {self.width} characters"
        
    def render(self, record) -> None:
        # do nothing (but script) if not visible
        if not self.is_visible:
            return
        rw = self.report.curent_roll_width()
        if self._max:
            text = '-' * rw
        else:
            text = '-' * self.width
        match self.align:
            case 'left':
                text = f"{text:<{rw}}"
            case 'center':
                text = f"{text:^{rw}}"
            case 'right':
                text = f"{text:>{rw}}"
            case _:
                pass
        
        self.report.buffer.text(text + "\n")
        
        
class Feed(BaseBlockRenderer):
    "Print buffer and feed lines"

    def __init__(self, options:dict, paramdict: dict, text:str) -> None:
        super().__init__(options, paramdict)
        self.count = int(paramdict.get("count", "1"))
        
    def __repr__(self) -> str:
        return f"Feed block object of count {self.count}"
        
    def render(self, record) -> None:
        self.report.buffer.print_and_feed(self.count)


class Image(BaseBlockRenderer):
    "Class for rendering embedded/external images"

    def __init__(self, options: dict, paramdict: dict, text:str) -> None: # text is base64 data of the image or field name or file resourse
        super().__init__(options, paramdict)
        self.type = paramdict.get("type", None)
        if not self.type:
            raise ReportCreationError("Image type not specified")
        self.img_source = paramdict.get("file_name", None)
        self.high_density_vertical = paramdict.get("high_density_vertical", "true") == 'true'
        self.high_density_horizontal = paramdict.get("high_density_horizontal", "true") == 'true'
        self.impl = paramdict.get("impl", "bitImageRaster")
        self.fragment_height = paramdict.get("fragment_height", 960) # Images larger than this will be split into multiple fragments
        self.center = paramdict.get("center", "true") == 'true'
        # create image for in report defined image
        self.image = None
        self.field_name = None
        match self.type:
            case 'field':
                self.field_name = text
            case 'embedded':
                self.image = PIL.Image.open(BytesIO(base64.b64decode(text)))
            case 'file':
                pass
            case 'resource':
                image_res = QFile(f":/{text}")
                image_res.open(QIODeviceBase.OpenModeFlag.ReadOnly)
                raw_bytes = image_res.readAll().data() 
                self.image = PIL.Image.open(BytesIO(raw_bytes))
                self.image.load()
            case _:
                raise ReportCreationError("Unknown image type")
                
    def __repr__(self) -> str:
        return f"Image block object of type: {self.type}"
                
    def render(self, record) -> None:
        "Draw image if necessary"
        if not self.is_visible:
            return
        if self.type == 'field':
            # create the image
            field_data = record[self.field_name]
            if not isinstance(field_data, QByteArray):
                raise ReportPrintError("Field IS NOT an image")
            raw_bytes = field_data.data()
            image = PIL.Image.open(BytesIO(raw_bytes))
            image.load()
        else:
            image = self.image
        # remove transparency if any
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGBA')
            alpha = image.split()[-1]
            bg = PIL.Image.new("RGBA", image.size, (255, 255, 255, 255))
            bg.paste(image, mask=alpha)
            image = bg.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Optional: Dithering (Recommended for PHOTOS/GRADIENTS)
        # image = image.convert("1")
        # Optional: Sharp black and white (Recommended for crisp LOGOS/TEXT)
        # image = image.convert("L").point(lambda x: 0 if x < 128 else 255, '1')
        
        self.report.buffer.image(img_source=self.image or self.img_source,
                                 high_density_vertical=self.high_density_vertical,
                                 high_density_horizontal=self.high_density_horizontal,
                                 impl=self.impl,
                                 fragment_height=self.fragment_height,
                                 center=self.center)
        
        
class QRCode(BaseBlockRenderer):
    "QRCode class manager"
    
    def __init__(self, options:dict, paramdict: dict, text:str) -> None:
        super().__init__(options, paramdict)
        self.type = paramdict.get("type", None)
        if not self.type:
            raise ReportCreationError("QRCode type not specified")
        self.ec_level = {'QR_ECLEVEL_L': QR_ECLEVEL_L, 
                         'QR_ECLEVEL_M': QR_ECLEVEL_M,
                         'QR_ECLEVEL_Q': QR_ECLEVEL_Q,
                         'QR_ECLEVEL_H': QR_ECLEVEL_H}.get(paramdict.get("ec_level", 'QR_ECLEVEL_L'))
        self.size = int(paramdict.get("size", '3')) # 1..16
        self.model = {'QR_MODEL_1':QR_MODEL_1,
                      'QR_MODEL_2': QR_MODEL_2,
                      'QR_MICRO': QR_MICRO}.get(paramdict.get("model", 'QR_MODEL_2'))
        self.native = paramdict.get("native", "true") == 'true'
        self.center = paramdict.get("center", "false") == 'true' # for hw qrc center is unavailable
        self.impl = paramdict.get("impl", "bitImageRaster") # bitImageRaster | graphics | bitImageColumn
        
        self.content = None
        self.field_name = None
        match self.type:
            case 'field':
                self.field_name = text
            case 'embedded':
                self.content = text
            case _:
                raise ReportCreationError("Unknown QRCode type")
                 
    def __repr__(self) -> str:
        return f"QRCode block object of type: {self.type}"
        
    def render(self, record) -> None:
        "Print the QR Code"
        if not self.is_visible:
            return
        if self.type == 'field':
            content = record[self.field_name]
        elif self.type == 'embedded':
            content = self.content
        else:
            pass
        self.report.buffer.qr(content,
                              ec=self.ec_level,
                              size=self.size,
                              model=self.model,
                              native=self.native,
                              center=self.center,
                              impl=self.impl,
                              image_arguments=None)
    
    
class Barcode(BaseBlockRenderer):
    "Barcode class manager"
    
    def __init__(self, options: dict, paramdict: dict, text:str) -> None: # text is required for generic drawobj
        super().__init__(options, paramdict)
        self.type = paramdict.get("type", None)
        if not self.type:
            raise ReportCreationError("Barcode type not specified")
        self.bc = paramdict.get("barcode_type", 'CODE128').upper()
        self.height = int(paramdict.get("height", '64')) # 1..255
        self.width = int(paramdict.get("width", '3')) # 2..6
        self.text_position = paramdict.get("text_position", 'BELOW') # ABOVE, BELOW, BOTH, OFF)
        self.font = paramdict.get("font", 'A') # A | B
        self.center = paramdict.get("center", "true") == 'true'
        
        self.code = None
        self.field_name = None
        match self.type:
            case 'field':
                self.field_name = text
            case 'embedded':
                self.code = text
            case _:
                raise ReportCreationError("Unknown Barcode type")
        
    def __repr__(self) -> str:
        return f"Barcode block object of type: {self.type}"
        
    def render(self, record):
        "Print the Barcode"
        if not self.is_visible:
            return
        if self.type == 'field':
            code = record[self.field_name]
        elif self.type == 'embedded':
            code = self.code
        else:
            pass
        if self.bc == 'CODE128':
            code = '{B' + code
        self.report.buffer.barcode(code, 
                                   bc=self.bc, 
                                   height=self.height, 
                                   width=self.width, 
                                   pos=self.text_position,
                                   font=self.font,
                                   align_ct=self.center,
                                   function_type=None,
                                   check=True,
                                   force_software=False)
    
    
class Cut(BaseBlockRenderer):
    "Cut the paper with a full or partial cut"

    def __init__(self, options:dict, paramdict: dict, text: str) -> None:
        super().__init__(options, paramdict)
        self.mode: str = paramdict.get("mode", "FULL") # "FULL" or "PART" (str)
        self.feed: bool = paramdict.get("feed", "true") == "true" # print and feed before cutting
        
    def __repr__(self) -> str:
        return f"Cut the paper with a {self.mode} cut, feed is {self.feed}"
        
    def render(self, record) -> None:
        self.report.buffer.cut(self.mode, self.feed)

# Render object dictionaries

inlineobj = {"label": Label,
             "field": Field,
             "summary": Summary,
             "special": Special}

blockobj = {"line": Line,
            "feed": Feed,
            "image": Image,
            "qrcode": QRCode,
            "barcode": Barcode,
            "cut": Cut}


# CONTAINER OBJECTS

# ROW - Inline objects container

class Row(list):
    """
    Row class, inline element container that print a line (or more) on print_device
    This container of inline objects print a line of text generated by inline objects
    """

    def __init__(self, options:dict, paramdict: dict) -> None:
        self.is_visible = paramdict.get("is_visible", "true") == 'true'
        self.report = options['report_instance']
        #raw_param = paramdict.get("is_visible_parameter", "").strip()
        #if raw_param:
        #    # it recognizes "not" only if it is a standalone word at the beginning
        #    self.parameter_negated = raw_param.startswith("not ") or raw_param.startswith("not\t")
        #    # if "not" is present, it takes everything after the space; otherwise, it takes the entire string.
        #    self.is_visible_parameter = raw_param[4:].lstrip() if self.parameter_negated else raw_param
        #else:
        #    self.is_visible_parameter = None
        #    self.parameter_negated = None
        
    def __repr__(self) -> str:
        return f"Row object with {len(self)} elements"
        
    def render(self, record) -> None:
        "Print a line of text on print device"
        # draw row's elements
        text_columns = []
        # 1. We ask each inline object for its clean text and split it using textwrap.
        for element in self:
            if isinstance(element, Field):
                value = record[element.field_name]
                if element.suppress_repeated:
                    if self.report.last_printed_values.get(element.field_name) == value:
                        value = None
                    else:
                        self.report.last_printed_values[element.field_name] = value
                element.set_value(value)
            if element.is_visible:         
                lines = textwrap.wrap(element.render(), width=element.width)
            else:
                lines = [""] #[' ' * element.width]
            if not lines:
                lines = [""]
            text_columns.append(lines)
        # 2. Synchronize the columns vertically using zip_longest
        phisical_lines = list(zip_longest(*text_columns, fillvalue=""))
        
        # 3. Composizione stringa e invio fisico alla stampante
        for line in phisical_lines:
            stringa_finale_linea = "\n"
            
            for i, pezzo_testo in enumerate(line):
                elem = self[i]
                
                # Gestione dinamica del grassetto inline: 
                # Diciamo al report engine di impostare il grassetto solo se l'elemento lo richiede
                #report_engine.imposta_formato(bold=elem.bold, font_style=self.font_style)
                
                # Applichiamo il padding in base all'allineamento dell'elemento inline
                if elem.align == 'right':
                    pezzo_formattato = pezzo_testo[:elem.width].rjust(elem.width)
                elif elem.align == 'left':
                    pezzo_formattato = pezzo_testo[:elem.width].ljust(elem.width)
                else: # center
                    pezzo_formattato = pezzo_testo[:elem.width].center(elem.width)
                
                elem.apply_style()
                self.report.buffer.text(pezzo_formattato)
            
            # Invio della riga fisica al buffer/stampante
            self.report.buffer.text(stringa_finale_linea)


# BAND block objects container

class Band(list):
    "Report bands are block object container"

    def __init__(self, options: dict, paramdict: dict) -> None:
        "Every band must have a height"
        self.report = options['report_instance']
        self.is_visible = paramdict.get("is_visible", "true") == 'true'
        self.is_page_footer = False
        self.execute_before: str|None = None
        self.execute_after: str|None = None
        raw_param = paramdict.get("is_visible_parameter", "").strip()
        if raw_param:
            # it recognizes "not" only if it is a standalone word at the beginning
            self.parameter_negated = raw_param.startswith("not ") or raw_param.startswith("not\t")
            # if "not" is present, it takes everything after the space; otherwise, it takes the entire string.
            self.is_visible_parameter = raw_param[4:].lstrip() if self.parameter_negated else raw_param
        else:
            self.is_visible_parameter = None
            self.parameter_negated = None
        
    def __repr__(self) -> str:
        return f"Band object with {len(self)} elements"

    def render(self, record: dict) -> None:
        "Render the contained objects after setting record value"
        # # python scripting
        # global_parameters = {'report': self.report,
        #                      'band': self,
        #                      'record': record}
        # # execute python code before rendering
        # if self.execute_before:
        #     exec(self.execute_before, global_parameters)
        if self.execute_before:
            # 1. Definiamo il contesto globale (in sola lettura per lo script)
            exec_globals = {
                '__builtins__': __builtins__ # Mantiene le funzioni standard di Python (len, str, ecc.)
            }
            
            # 2. Definiamo le variabili locali su cui lo script può operare direttamente
            exec_locals = {
                'report': self.report,
                'band': self,
                'record': record
            }
            # 3. Eseguiamo isolando i contesti
            exec(self.execute_before, exec_globals, exec_locals)
        # do nothing (but execute before) if not visible
        # if self.is_visible_parameter:
        #     self.is_visible = (not self.report.parameter.get(self.is_visible_parameter) if self.parameter_negated 
        #                         else self.report.parameter.get(self.is_visible_parameter))
        # 2. Se c'è un parametro dell'operatore, valuta il suo stato attuale a runtime
        if not self.is_visible:
                    return
                
        if self.is_visible_parameter:
            param_value = bool(self.report.parameter.get(self.is_visible_parameter))
            # Se la condizione (considerando il 'not') è falsa, salta il record corrente
            if not (param_value ^ self.parameter_negated):
                return
            
        # call band's row elements
        for element in self:
            if element.is_visible:
                element.render(record)
                
        # execute python code after rendering
        if self.execute_after:
            exec(self.execute_after, exec_globals, exec_locals)
            

class Sort(str):
    "Class that adds a reverse boolean value to a string, used for grouping/ordering"

    def __new__(self, text: str|None, reverse: bool) -> str: # type: ignore
        sg = str.__new__(self, text)
        sg.reverse = reverse # type: ignore
        return sg


class Parameter():
    "Class for store parameters settings"

    def __init__(self, description: str, ptype: str, value=None, items=[], referenceList=None) -> None:
        self.description = description
        self.ptype = ptype
        self.value = value
        self.items = items
        self.referenceList = referenceList


class SqlField():
    def __init__(self, code: str|None, description: str|None, ftype: str|None, reference: str|None = None) -> None:
        self.code = code
        self.description = description
        self.ftype = ftype
        self.referenceList = reference # use in report dialog for reference list selection


# Print over Network or USB using a thread

class PrinterSenderThread(QThread):
    # Segnali per la UI
    job_completed = Signal()
    print_error   = Signal(str)

    def __init__(self, pd: Network | Usb, raw_bytes: bytes):
        super().__init__()
        self.raw_bytes = raw_bytes
        self.pd = pd
        
        # default parameters initialization
        # network printer
        self.host: str = ''
        self.port: int = 9100
        self.net_timeout: int | float = 4.0
        # usb printer
        self.id_vendor: int | None = None
        self.id_product: int | None = None
        self.usb_timeout: int | float = 0
        self.in_ep: int = 0x82
        self.out_ep: int = 0x01
        
        match pd:
            case Network() as net_dev:
                self.host = net_dev.host
                self.port = net_dev.port
                self.net_timeout = net_dev.timeout if net_dev.timeout else 4.0
            case Usb() as usb_dev:
                self.id_vendor = usb_dev.idVendor
                self.id_product = usb_dev.product_id if hasattr(usb_dev, 'product_id') else usb_dev.idProduct
                self.usb_timeout = usb_dev.timeout
                self.in_ep = usb_dev.in_ep
                self.out_ep = usb_dev.out_ep

    def run(self):
        match self.pd:
            case Network():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.net_timeout)
                try:
                    s.connect((self.host, self.port))
                    s.sendall(self.raw_bytes)
                    self.job_completed.emit()
                except socket.timeout:
                    self.print_error.emit(f"Timeout: the printer {self.host} is not responding.")
                except socket.error as e:
                    self.print_error.emit(f"Network error: {str(e)}")
                finally:
                    s.close()
                    
            case Usb() as usb_dev:
                try:
                    usb_dev.open()
                    usb_dev._raw(self.raw_bytes)
                    self.job_completed.emit()
                except Exception as e:
                    self.print_error.emit(f"USB error: {str(e)}")
                finally:
                    try:
                        usb_dev.close()
                    except:
                        pass
            
         
# Dummy subclass for store preview operations
from escpos.printer import Dummy

def _default_style() -> dict:
    return dict(font='a', bold=False, underline=0, invert=False,
                align='left', wm=1, hm=1)   # wm/hm = moltiplicatori larghezza/altezza

class DummyDevice(Dummy):
    "Dummy that records styled operations for a graphical/textual preview"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = self.profile.profile_data['fonts'].get('0')['columns']
        self.ops: list[tuple] = []
        self.style = _default_style()

    def _track(self, kw: dict) -> None:
        s = self.style
        for k in ('align', 'font', 'bold', 'underline', 'invert'):
            if kw.get(k) is not None:
                s[k] = kw[k]
        if kw.get('normal_textsize'):
            s['wm'] = s['hm'] = 1
        if kw.get('double_width') is not None:
            s['wm'] = 2 if kw['double_width'] else 1
        if kw.get('double_height') is not None:
            s['hm'] = 2 if kw['double_height'] else 1
        if kw.get('custom_size'):
            s['wm'], s['hm'] = kw.get('width', 1), kw.get('height', 1)

    def set(self, *args, **kwargs) -> None:
        super().set(*args, **kwargs)
        self._track(kwargs)

    def set_with_default(self, *args, **kwargs) -> None:
        super().set_with_default(*args, **kwargs)
        self.style = _default_style()
        self._track(kwargs)

    def text(self, txt: str) -> None:
        if txt:
            self.ops.append(('text', txt, dict(self.style)))
        super().text(txt)

    def block(self, txt: str, *args, **kwargs) -> None:
        if txt:
            self.ops.append(('text', txt, dict(self.style)))
        super().block(txt, *args, **kwargs)

    def image(self, *args, **kwargs) -> None:
        self.ops.append(('box', 'IMAGE'))
        super().image(*args, **kwargs)
        
    def qr(self, content, *args, **kwargs) -> None:
        ec = kwargs.get('ec', args[0] if len(args) > 0 else 0)
        size = kwargs.get('size', args[1] if len(args) > 1 else 3)
        self.ops.append(('qr', content, ec, size))
        super().qr(content, *args, **kwargs)

    def barcode(self, code, bc, *args, **kwargs) -> None:
        self.ops.append(('barcode', code, bc,
                        kwargs.get('height', 64), kwargs.get('width', 3),
                        str(kwargs.get('pos', 'BELOW')).upper()))
        super().barcode(code, bc, *args, **kwargs)

    def print_and_feed(self, n: int = 1, *args, **kwargs) -> None:
        self.ops.append(('feed', n))
        super().print_and_feed(n, *args, **kwargs)

    def cut(self, mode: str = 'FULL', feed: bool = True, *args, **kwargs) -> None:
        super().cut(mode, feed, *args, **kwargs)   # il feed interno è già registrato
        self.ops.append(('cut', mode))

    def clear_preview(self) -> None:
        self.ops.clear()
        self.style = _default_style()
        self.clear()          # Dummy.clear(): svuota anche i byte
        
    
# Report

class ReportEscpos():
    "Base class for report"

    def __init__(self, xml_string: str|None = None) -> None:
        # report output buffer created after parsing XML
        self.buffer: DummyDevice
        # text properties default
        self._current_text_property: dict = {}
        self._current_text_property['font'] = 'a' # 'a' or 'b'
        self._current_text_property['bold'] = False
        self._current_text_property['underline'] = 0 # 0..2
        self._current_text_property['normal_textsize'] = True
        self._current_text_property['double_height'] = False
        self._current_text_property['double_width'] = False
        self._current_text_property['density'] = 0 # 0..8
        self._current_text_property['invert'] = False
        self._current_text_property['flip'] = False
        self._current_text_property['smooth'] = False
        # report elements
        self.header: list = [] # printed on beginning
        self.footer: list = [] # printed on ending
        self.sortings: list = [] # ordered sorting fields
        self.groups: list = []  # ordered grouping conditions
        self.group_headers: dict = {} # grouping field: [list of bands]
        self.group_headers_repeat: dict = {} # grouping field: [list of bands]
        self.group_footers: dict = {} # grouping field: [list of bands]
        self.current_group_index: int|None = None # current group index for render time optimization
        # self.group_summaries = {}  # grouping field: [list of summary function]
        self.details: list = [] # must be defined
        self.execute: str|None = None # report scripting before starting
        # sql query and field used for generate dataset from sql database
        self.query: str|None = None
        self.query_where: str|None = None
        self.query_group_by: str|None = None
        self.query_order_by: str|None = None
        self.conditions: collections.OrderedDict = collections.OrderedDict()
        # dataset column definition
        self.column: dict = {} # column aliases
        # data container, overwritten if self.select is not None
        self.data: list[Any]|tuple[Any]|None = []
        self.prev_record: dict|None = None  # pointer to previous rendered record
        # report parameters as a param: value dictionary
        self.parameter: collections.OrderedDict = collections.OrderedDict()
        self.summaries: list = []  # each summary init update this list, must be set before calling setReportDefinition
        self.last_printed_values: dict = {} # for suppressRepeated fields
        
        if 'App.Database.Settings' in sys.modules:
            setting = Settings()
            default_options['quantity_decimals'] = setting['quantity_decimal_places']
            default_options['price_decimals'] = setting['price_decimal_places']
            default_options['amount_decimals'] = setting['amount_decimal_places']
            default_options['currency_symbol'] = setting['currency_symbol']
        self.thousand_sep = session['qlocale'].groupSeparator()
        self.decimal_sep = session['qlocale'].decimalPoint()
        if xml_string:
            self.set_report_definition(xml_string)
        self.buffer = DummyDevice(self.options.get('printer_profile', default_options['printer_profile']))
        # 'codePages', 'colors', 'features', 'fonts', 'media', 'name', 'notes', 'vendor'

    def append_bands(self, child_element: ET.Element) -> list:
        out_list = []
        for band in child_element.findall('band'):
            # create a band
            b = Band(self.options, band.attrib)
            for blk in band:
                # create a block object
                if blk.tag == "row":
                    bo = Row(self.options, blk.attrib)
                    # create an inline object
                    for inl in blk:
                        if inl.tag in inlineobj:
                            ilo = inlineobj[inl.tag](self.options, inl.attrib, inl.text)
                            bo.append(ilo)
                    b.append(bo)
                if blk.tag in blockobj:
                    bo = blockobj[blk.tag](self.options, blk.attrib, blk.text)
                    b.append(bo)
                if blk.tag == 'execute':
                    if blk.attrib.get('trigger') == 'before':
                        b.execute_before = blk.text
                    if blk.attrib.get('trigger') == 'after':
                        b.execute_after = blk.text
            out_list.append(b)
        return out_list

    def set_report_definition(self, xml_string: str) -> None:
        "Create printing objects and other elements from xml definition"
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as er:
            raise ReportXMLParseError(er)
        self.options = default_options.copy() # Inherit default options
        self.options['report_instance'] = self  # give a reference to report object

        # sanity check
        if root.tag != 'report':
            raise ReportXMLParseError("The mandatory element 'report' was not found.")
        if root.attrib.get('version') != VERSION:
            raise ReportXMLParseError(f"Wrong report engine version: "
                                      f"{root.attrib.get('version')}")

        # Get options from report definition when different from default
        opt = root.find('options')
        if opt is None:
            raise ReportXMLParseError("The mandatory element 'options' was not found.")
        for child in opt:
            attr = child.attrib.get('type')
            val = child.text or '0' # for numeric and boolean options text must be not empty,
                                    # for string options can be empty but not None
            match attr:
                case 'bool':
                    self.options[child.tag] = True if val == 'true' else False
                case 'str':
                    self.options[child.tag] = val
                case 'int':
                    self.options[child.tag] = int(val)
                case 'float':
                    self.options[child.tag] = float(val)
                case _:
                    raise ReportXMLParseError(f"Option with wrong/without type attribute: <{child.tag}> = {val}")

        # report parameters
        params = root.find('parameters')
        if params is not None:
            for child in params:
                if child.tag == 'parameter':
                    param = child.attrib.get('id')
                    ptype = child.attrib.get('type')
                    value: bool|int|float|QDate|str|None = None
                    items: dict = {}
                    referenceList = child.attrib.get('reference')
                    df = child.attrib.get('default')
                    if not df:
                        raise ReportXMLParseError(f"Parameter with empty default value: <parameter id='{param}'>")
                    match ptype:
                        case 'bool':
                            value = True if df == 'true' else False
                        case 'int':
                            value = int(df)
                        case 'float':
                            value = float(df)
                        case 'str':
                            value = df or ''
                        case 'date':
                            value = QDate.fromString(df, 'yyyyMMdd')
                            if not value.isValid():
                                value = QDate.fromString('19000101', 'yyyyMMdd') # fallback to a default date if parsing failed
                        case 'list':
                            value = df
                        case _:
                            raise ReportXMLParseError(f"Parameter with wrong/without type "
                                                    f"attribute: <parameter id='{param}'> with type '{ptype}'")
                            
                    if child.attrib.get('items'):
                        items = {}
                        for i in child.attrib.get('items').split('|'): # type: ignore
                            k, v = i.split(":")
                            items[k] = v
                            
                    self.parameter[param] = Parameter(child.text, ptype, value, items, referenceList) # type: ignore

        # report scripting
        execute = root.find('execute')
        if execute is not None:
            self.execute = execute.text

        # query definition
        query = root.find('query')
        if query is not None:
            for child in query:
                match child.tag:
                    case 'select':
                        self.query = child.text
                    case 'where':
                        self.query_where = child.text
                    case 'groupBy':
                        self.query_group_by = child.text
                    case 'orderBy':
                        self.query_order_by = child.text
                    case 'conditions':
                        for cond in child.findall("condition"):
                            self.conditions[cond.text] = SqlField(cond.attrib.get('code'),
                                                                  cond.attrib.get('description'),
                                                                  cond.attrib.get('type'),
                                                                  cond.attrib.get('reference'))
                    case _:
                        raise ReportXMLParseError(f"Query child tag unknown {child.tag}")

        # columns' names
        columns = root.find('columns')
        if columns is None:
            raise ReportXMLParseError("The mandatory element 'columns' was not found.")
        else:
            for i, c in enumerate(columns.findall("field_name")):
                self.column[c.text] = i

        # sortings
        sorting = root.find('sorting')
        if sorting is not None:
            for sort in sorting.findall("sort"):
                field = sort.attrib.get('field')
                reverse = bool(sort.attrib.get('reverse'))
                self.sortings.append(Sort(field, reverse))

        # groups headers/footers
        groups = root.find('groups')
        if groups is not None:
            for group in groups.findall('group'):
                field = group.attrib.get('field')
                reverse = 'true' == group.attrib.get('reverse', 'false')
                self.groups.append(Sort(field, reverse))
                for child in group:
                    if child.tag == "group_header":
                        self.group_headers[field] = self.append_bands(child)
                    if child.tag == "group_footer":
                        self.group_footers[field] = self.append_bands(child)

        # other render elements
        for child in root:
            match child.tag:
                case 'options'|'parameters'|'execute'|'query'|'columns'|'sorting'|'groups':
                    pass
                case "header":
                    self.header = self.append_bands(child)
                case "details":
                    self.details = self.append_bands(child)
                case "footer":
                    for i in self.append_bands(child):
                        i.is_page_footer = True
                        self.footer.append(i)
                case _:
                    raise ReportXMLParseError(f"Root child tag unknown {child.tag}")

        if self.details is None:
            raise ReportXMLParseError("The mandatory element 'details' was not found.")

    def set_data(self, data_set: list[Any]|tuple[Any]|None = None) -> None:
        self.data = data_set
        
    def curent_roll_width(self) -> int:
        "Return the current roll width in characters base on the font in use and printer profile"
        if not self.buffer:
            return 0
        font_id = {'a': '0', 'b': '1'}.get(self._current_text_property['font'], '0')
        width = self.buffer.profile.profile_data['fonts'].get(font_id, '0')['columns'] # in case of obly one font supported
        return width
        
    def update_text_properties(self, 
                               font: str, 
                               bold: bool, 
                               underline: int, 
                               normal_textsize: bool,
                               double_height: bool,
                               double_width: bool, 
                               density: int, 
                               invert: bool, 
                               flip: bool, 
                               smooth: bool) -> None:
        "Set text properties only if different from current value"
        if not self.buffer:
            return
        for p, v in (('font', font),
                     ('bold', bold),
                     ('underline', underline),
                     ('normal_textsize', normal_textsize),
                     ('double_height', double_height),
                     ('double_width', double_width),
                     ('density', density),
                     ('invert', invert),
                     ('flip', flip),
                     ('smooth', smooth)):
            if self._current_text_property.get(p, None) != v:
                match p:
                    case 'font':
                        self.buffer.set(font=v)
                    case 'bold':
                        self.buffer.set(bold=v)
                    case 'underline':
                        self.buffer.set(underline=v)
                    case 'normal_textsize':
                        self.buffer.set(normal_textsize=v)
                    case 'double_height':
                        self.buffer.set(double_height=v)
                    case 'double_width':
                        self.buffer.set(double_width=v)
                    case 'density':
                        self.buffer.set(density=v)
                    case 'invert':
                        self.buffer.set(invert=v)
                    case 'smooth':
                        self.buffer.set(smooth=v)
                    case 'flip':
                        self.buffer.set(flip=v)
                    case _:
                        pass
                self._current_text_property[p] = v
                #print('Text property dict ', self._current_text_property)

    def group_generate(self, data: list[Any]|tuple[Any], group_index: int = 0) -> None:
        "Resolve groups recursively"
        grp = self.groups[group_index] if self.groups else None
        for key, group in itertools.groupby(data, lambda x: x[self.column[grp]] if grp else None):  # if no group returns all the dataset
            sub_data = list(group)
            header_record = {k: sub_data[0][v] for k, v in self.column.items()} # first record of the group
            footer_record = {k: sub_data[-1][v] for k, v in self.column.items()} # last record of the group
            
            # set current group index for render group headers on new page
            self.current_group_index = group_index
                    
            # group headers
            if self.groups:
                if grp in self.group_headers:
                    for b in self.group_headers[grp]:
                        b.render(header_record)

            # call recursively this method for nested groups
            if self.groups:
                if group_index < len(self.groups) - 1: # group index must be a local variable, is different from any method call
                    self.group_generate(sub_data, group_index + 1)
                    sub_data.clear() # render details only in subgroup

            # details
            for rec in sub_data:
                record = {k: rec[v] for k, v in self.column.items()}
                for b in self.details:
                    b.render(record)
                # update summaries on group footers and report footers
                # it is require to scroll all the dataset for update summaries so is not possible to put summaries on headers
                if self.groups:
                    for i in self.groups:
                        if self.group_footers.get(i):
                            for b in self.group_footers.get(i): # type: ignore band
                                for r in b: # row
                                    if isinstance(r, Row):
                                        for ilo in r: # summary
                                            if isinstance(ilo, Summary):
                                                ilo.update(record)
                self.rn += 1  # increase record number only after rendering the previous one
                self.prev_record = record.copy()

            # group footer
            if self.groups:
                if grp in self.group_footers:
                    for b in self.group_footers[grp]:
                        b.render(footer_record)
                    # reset summaries
                    for b in self.group_footers[grp]:
                        for r in b:
                            if isinstance(r, Row):
                                for ilo in r: # summary
                                    if isinstance(ilo, Summary):
                                        ilo.reset()

    def generate(self) -> None:
        "Generate report"
        if not self.data:  # no data to render
            raise ReportNoDataError
        
        self.buffer.clear_preview()
         
        # clear everything first
        self.current_group_index = 0
        for s in self.summaries:
            s.reset()
        self.last_printed_values.clear()
        
        # report scripting, only one time before starting
        if self.execute:
            global_parameters = {'Qt': Qt,
                                 'Sort': Sort,
                                 'Parameter': Parameter,
                                 'SqlField': SqlField,
                                 'report': self}
            exec(self.execute, global_parameters)

        # sort for required sorting
        for col, rev in [(self.column[i], i.reverse) for i in reversed(self.sortings)]:
            try:
                self.data.sort(key=operator.itemgetter(col), reverse=rev) #type: ignore
            except TypeError: # if a value is None
                try:
                    # sort with None values and strings
                    self.data.sort(key= lambda i: '' if not i[col] else i[col], reverse=rev) #type: ignore
                except TypeError:
                    # sort with None values and numbers
                    self.data.sort(key= lambda i: 0 if not i[col] else i[col], reverse=rev) #type: ignore
      
        # sort for grouping
        for col, rev in [(self.column[i], i.reverse) for i in reversed(self.groups)]:
            try:
                self.data.sort(key=operator.itemgetter(col), reverse=rev) #type: ignore
            except TypeError: # if a value is None
                try:
                    # sort with None values and strings
                    self.data.sort(key= lambda i: '' if not i[col] else i[col], reverse=rev) #type: ignore
                except TypeError:
                    # sort with None values and numbers
                    self.data.sort(key= lambda i: 0 if not i[col] else i[col], reverse=rev) #type: ignore
                    
        self.rn = 1 # record number, start from 1 for compatibility with report definition functions
        self.last_record_num = len(self.data) # reference for bands

        first_record = {k: self.data[0][v] for k, v in self.column.items()}
        last_record = {k: self.data[-1][v] for k, v in self.column.items()}

        # header
        if self.header:
            for b in self.header:
                b.render(first_record)

        # start iterating the dataset
        self.prev_record = {}
        self.group_generate(self.data)

        # footer
        if self.footer:
            for b in self.footer:
                b.render(last_record)

        # final cut managed by report
        #self.buffer.cut() 
        
        #print(self.buffer.output)

    def _on_print_success(self):
        "Successful printing"
        print("Everything OK")
        self.printer_thread = None  
    
    def _on_print_error(self, error_message):
        "Show print error"
        print(error_message)
        self.printer_thread = None
        
    
    def print(self, pd: Network | Usb | QPaintDevice) -> None:
        "Print the generated receipt on a raw device, a text preview or a paint device (preview dialog, printer, PDF)"
        match pd:
            case Network() | Usb():
                self.printer_thread = PrinterSenderThread(pd, raw_bytes=self.buffer.output)
                self.printer_thread.job_completed.connect(self._on_print_success)
                self.printer_thread.print_error.connect(self._on_print_error)
                self.printer_thread.start()
            case QPaintDevice():          # QPrinter (anche dalla dialog), QPdfWriter
                self._print_graphic(pd)
            case _:
                pass
                
    def receipt_page_layout(self, paper_width_mm: float = 80.0) -> QPageLayout:
        return ReceiptPreview(self.buffer, paper_width_mm).page_layout()

    def _print_graphic(self, device: QPaintDevice, paper_width_mm: float = 80.0) -> None:
        preview = ReceiptPreview(self.buffer, paper_width_mm)
        if isinstance(device, QPrinter):
            device.setDocName(self.options.get('documentName', 'Receipt'))
        elif isinstance(device, QPdfWriter):
            device.setTitle(self.options.get('documentName', 'Receipt'))
            device.setPageLayout(preview.page_layout())
        preview.paint(device)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QLocale.setDefault(QLocale.Language.English)
    
    xml_string0 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0" print_method="ESC/POS">
    <options>
        <printer_profile type="str">TM-T20II</printer_profile>
        <charcode type="str">AUTO</charcode>
        <font type="str">a</font> <!-- default Font A -->
    </options>
    <columns>
        <field_name>id</field_name>
        <field_name>number</field_name>
        <field_name>date</field_name>
        <field_name>time</field_name>
        <field_name>table</field_name>
        <field_name>customer</field_name>
        <field_name>item</field_name>
        <field_name>quantity</field_name>
        <field_name>price</field_name>
        <field_name>amount</field_name>
    </columns>
    <header>
    </header>
    <groups>
        <group field="id" reverse="false">
            <group_header>
                <band>
                <barcode type="embedded" barcode_type="CODE128">123456789</barcode>
                    <row>
                        <label width="48" font="a">****** EXAMPLE OF AVAILABLE OPTIONS ******</label>
                    </row>
                    <line width="max"/>
                </band>
                <band>
                    <row>
                        <label width="48" align="left">-- STYLE TEST --</label>
                    </row>
                    <row>
                        <label width="48" underline="1">Underline 1 (sottile)</label>
                    </row>
                    <row>
                        <label width="48" underline="2">Underline 2 (spesso)</label>
                    </row>
                    <row>
                        <label width="48" invert="true">Invert: bianco su nero</label>
                    </row>
                    <row>
                        <label width="24" double_width="true">Doppia larghezza</label>
                    </row>
                    <row>
                        <label width="48" double_height="true">Doppia altezza</label>
                    </row>
                    <row>
                        <label width="24" double_width="true" double_height="true">Doppia W+H</label>
                    </row>
                    <row>
                        <label width="24" align="center" double_width="true" bold="true">CENTRATO</label>
                    </row>
                    <row>
                        <label width="24" align="right" font="b">Font B a destra</label>
                    </row>
                </band>
            </group_header>
            <group_footer>
                <band>
                    <qrcode type="embedded">ABCDCBA</qrcode>
                    <feed count="1"/>
                    <cut mode="PART" feed="true"/>
                </band>
            </group_footer>
        </group>
    </groups>
    <details>
    </details>
</report>"""

    xml_string1 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0" print_method="ESC/POS">
    <options>
        <printer_profile type="str">TM-T20II</printer_profile>
        <charcode type="str">AUTO</charcode>
        <font type="str">a</font> <!-- Font A -->
    </options>
    <columns>
        <field_name>id</field_name>
        <field_name>number</field_name>
        <field_name>date</field_name>
        <field_name>time</field_name>
        <field_name>table</field_name>
        <field_name>customer</field_name>
        <field_name>item</field_name>
        <field_name>quantity</field_name>
        <field_name>price</field_name>
        <field_name>amount</field_name>
    </columns>
    <header>
    </header>
    <groups>
        <group field="id" reverse="false">
            <group_header>
                <band>
                <barcode type="embedded" barcode_type="CODE128">123456789</barcode>
                    <image type="embedded">
                        iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABHNCSVQICAgIfAhkiAAAAAlw
                        SFlzAAAFMQAABTEBt+0oUgAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoA
                        AApISURBVHja1Zp7jB1Xfcc/vzOP+753H/Y+jF+xnZCHG4TlhDg0jU2kkrRRGxWCEOLVVqJp
                        ICpBBdQ/Wtv9o1UrtVWS0opWFY9ihdYUKQ8DAUwegAIsCU5C7UCcONhbr73rvfu4e18zc86v
                        a3ajyV15N1l7pTg/6auZOTN35vc5v/P7nTOzK6rKm9kMb3LzYeVNZu2FbxDmwlIRoBnVZrb8
                        DhGq+qaIwKlHyPdMZf6xa9WHRyu9HxjtquU/N/YoBZm1iz4CR78pmUo1/Ou4W+7MFgcw4mNL
                        7o/9k2Hr2BeiPwdaF3EExFTa4Vttjk8GxW0Eb1mHv6aPsHwdcY47g4p/NYi5aAGOH6DiZjhg
                        w8AULn8v1pye1Rlyl92GhjnxZ+TB4UfouigBDu+X0BvzPhMVZG1l/UfRUgTWzanYpLThj4hK
                        pt8fCf+KwxJeZAAiFS/f5wLv02H+SoKNlyNWZwWvyN94CWFpG3HIXcNPZtaDyEUDMPIwOcaT
                        fXEgXmnLbajWUKsdws5Q2vy7xL4Yte7+098mf5EAiImqbG1n9YbSqp2Y3hw4d06Zike5/2bi
                        nGxvnvSuAzFvOMChL1LWhn9/bAIpbd6JxG0k0UWUUNy0AzUZaMlXDu+n640F2C9hue59spU1
                        m1avvw2yFnUsKcKYnkv+gNnfDGRHvT2PfVGybwzAY+IfO831sW/+Mle+ksIl28BasO41ldtw
                        FYWebUSB+cT6GjfzbxJwnras1ej+/eKtHSbsDskbZZeq/2VX6sltvOFuJNNmWZZkOf7Df0En
                        TkaC3HFa44fzGeq1EaKduzVZAQCRw3sJkk0EzhL4U2QysEOtf5f1uD7KSNaYgI077sIvZ4Dl
                        F0Y7o7z0o/uwUZ0w1tiPedqp/IeW4ocn67RdTNyfI9pXJd69W91rAjy2V/zSIGFoyZgafYHx
                        /szBLvVYH3uSSzwRgN6126iseyfZVRvATQA2veNyIFQQfzXRxDDTJ57i9LEnAMVz4FttG8eo
                        ce7HzcDdYxOez+VoNX3a2/+ERGctBdgr5gd9VLqngvcb4+5whsvagck6AT8IqAxcQWn1lWTy
                        vfiVVRg/QJPp1Flh+QC6sBjnUTyS6TO0a1Ua1ReojvycuDmDKISJxr7TE6rsG8/Z+04NUL39
                        drWiezBDAVtznv9EM5AKvmHVuquo9F1Nprwav9QPNkKTGoginU6fH4QucqzpvpgiGuSx9TGi
                        qVFmqi8xNvw0cb1BLtZW4pLfP7qZg/LoHoo9oX8kKmTXbtp2K/mBqxArcw4DSKpXH6cgSzgv
                        y3CcFEABtFPi5X4NFE8N8/LPHsaNHp9stZMNfhOMc5r1wgy5ci/Up1EAObdksR6V12hXgNcH
                        IDp/qKRQUR3adTLdW/HDb9OyampZxPQN0jQJX5qpTjEzMgTOzknPLZ0XZ0W6XVS6yDW6cJvu
                        K+kzOmQCovovOXP8KJLof69p0RRV5eDfSm9XZI42Q7/r6hveRZC/HHl1z5vFI9I5lJadA2kP
                        K2m7Iz3nXrlG0HI/h/bvJWzG0zWSzbv2MG4AboqYaDfdTtOyyfM//QHODqPqfi1YuBaYk8yL
                        85E4YJH7pc/skOl6C784+M/QiBJLsmsnVHXWDAC71UU5/jdU+5FmtaUvPfs4UO0YMp2hn2/H
                        wkJJ536qpa/Vs1pk6ElpDcPP/BdTJ06pb+wfHjrJc2d97lgLnZ2+Zzy+nkfvOf1ileNHvgtm
                        GnEWoxZ5RXRu0TlHhAV6PW1pxyxoT7emMMjYsW/x4o+fJo/eV1e+9rHPa7xwJn71bFzMWfOF
                        yUjee+k1g6zZdBNIBklzoSMnxCxeamHpypOqs+Iw37cms5bq6BMceuggPRl9cKTpPvh7f6e1
                        JddCMmvf+Szlgm8eqEZy49bfWkf/uhsR/HnnUwDpgFkikWVh4i4iB3gV0Cxu4mVGRh7k8JNN
                        egs6NH7avfvWf2VSZ20JgJTikbvpLhfN4+N12brjPVdQyG9HTAdACrIkxNIzLg7AA38AaYxj
                        zzyFGx2iFng89UPozumxdt1du/MfGCd1dimAFOIbn6a/4JujrhgW3nHrO/FYAwJ4qeMpzPIA
                        xOtG4hauPYE2RtDqEBq3wYLzhEPP+0RnbFSvu0tvvZcTqOryvsypav19Mpbb4t5fH40eGj76
                        LOsv60XUB0AWOJpq4TkBUwRNwNaRpImLqrjaAxBNgwO1gAHxQAVGGh7V45ZK3t1Z7OEkqnre
                        LzT7Py7FgR7zyNgk19/yp9fguS3gCXgeahQj82VQEkQsSAKAaB1sHXU1NPoVuHrnxOTgHNUZ
                        QuH73zNkrP6iPumuveVenb6wb6NjRLbC4STi+mh0iLA5hPge+Ip4Cc4D/Pne8wADYkBfXanm
                        2tOK4wCXRkolzXPnCVELwoDhmVPEK/JxV9XVXWJQZL6XHWIAb06SQsAr7TIPAyBpmeyYiNMF
                        IqogCk4gaipqaNQL6AUDTHSjPULDWbAKmE5JCtEJZDoTWkgB1AE27XU0lXqQtECLtPtLKwDQ
                        PoGhzFprFd8XSBZApI6nUfBIAdNKlA4dCwoAae87UANGwGRBreufOYW5YICBIsY5NosPfqDQ
                        BpHOMipmQRT8BVGAdJ1vQQVE5iFc59wSoFRWG+w0g2PgrcR3Ic8mDJb7DIECcg6ZVGlOzEmC
                        VPidcJJGKU3+WKkMCkkk3T54F54D4GUT6epdC9pUUltY+xfJCQNImrxKmgsIqUgjlckrUZtC
                        MViBIWQbmDgiV+gGFynik5pybiCzYChJWuclrT6p6LxnmIV2m2CmtgIRCPOIjdULMoADdBFB
                        R2ZOT3q88IzSasEV7xB6ByzqSG2JFannQ9xWaSfIBQO0EiQXYzwfcGkZFAdoZ1uz7fHLIeXI
                        0/Dcjyy1GiQOwgC2/IZw9XXC228UKgULjvS3Ssex70PUQgK7AgCuhUl8xPNJnbeAB2pBPGiI
                        x8gx+P79jtETSq6H6JINHMuH3NdsMt5W/qJxRt/66H9q5if/Azs/4HH5dij6Nn1Bc3NbdeCF
                        ELURfyUAAJIYmTWI02rjAmEm8Bgdhif3JURt6FrD/23czKcmz3DQG6eZz9I+AOwY5oEuj2xP
                        P2/L9vL5oa/ZS4e+gvzmRzzWXiaU8w5puvRN0whxBHYlABKHzeW9OHJhqANKFMDEJLz0JDx3
                        IKHUhVvVzzPNBnc0n+NIaQ2Nj39dLfN2OwA0z2qvyBOF32Zbd4XBnnV87ucH7Lse/3f8DW83
                        vO1mn+5VkHFKPFWkUKrpzKi1FwxQCGllPPesqVyz/VsPDDF8qIEAfQNMrN/CvuNH+BsbMzXy
                        EK3dqo4lbP58HZEX/2kHt9kSpc2X8iE77e7+zj1uTaOBrNpQ4LqPbadc+t7xsVO0LvzvAyLy
                        5Zvo6dta+FJ9srFBjB6JW/z9yAhHp1bT2LOfWGeN87S9u8TPxeRWd7G6MsinwLs2X86OnT5Z
                        /8TLX+VXc9DnC5AyyL23EGZ8vHaCveubrPw/bojI3qsIymU8vwv3ep/x/7X90Ba5k+pnAAAA
                        AElFTkSuQmCC
                    </image>
                    <row>
                        <label width="48" font="a">****** EXAMPLE OF A CUSTOMER COPY RECEIPT ******</label>
                    </row>
                    <row>
                        <label width="12">Order Num.:</label>
                        <field width="10" align="left">number</field>
                        <label width="6">Time:</label>
                        <field width="8" align="left">time</field>
                        <label width="7">Table:</label>
                        <field width="5" align="right">table</field> <!-- total 48 chaars -->
                    </row>
                    <row>
                        <label width="25" align="left" bold="true">ITEM</label>
                        <label width="5" align="right" bold="true">Q.TY</label>
                        <label width="8" align="right" bold="true">PRICE</label>
                        <label width="10" align="right" bold="true">AMOUNT</label> <!-- total 48 chars-->
                    </row>
                    <line width="max"/>
                </band>
            </group_header>
            <group_footer>
                <band>
                    <line width="20" align="right"/>
                    <row>
                        <label width="38" align="right">TOTAL:</label>
                        <summary function="sum" width="10" align="right">amount</summary>
                    </row>
                    <feed count="1"/>
                    <row>
                        <label width="48" align="center">THANKS AND GOODBYE</label>
                    </row>
                    <feed count="1"/>
                    <row>
                        <label width="6" align="left" font="b">Date:</label>
                        <special width="15" align="left" font="b">print_date_time</special>
                        <label width="12" align="left" font="b">- pySagra -</label>
                        <special width="30" align="left" font="b">app_email</special>
                    </row>
                    <qrcode type="embedded">ABCDCBA</qrcode>
                    <feed count="1"/>
                    <cut mode="PART" feed="true"/>
                </band>
            </group_footer>
        </group>
    </groups>
    <details>
        <band is_visible="true">
            <row>
                <field width="25" align="left">item</field>
                <field width="5" align="right">quantity</field>
                <field width="8" align="right">price</field>
                <field width="10" align="right">amount</field> <!-- total 48 chars-->
            </row>
        </band>
    </details>
</report>
"""
    
    for i in (xml_string0, xml_string1):
        report = ReportEscpos(i)
        report.set_data([# id, number, date, time, table, customer name, item, quantity, price, amount
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'GNOCCHI', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'PENNE amatriciana', 3, decimal.Decimal(5.5), decimal.Decimal(16.5)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'SALSICCE con 2 fette di polenta', 1, decimal.Decimal(6.5), decimal.Decimal(6.5)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'COSTICINE', 2, decimal.Decimal(6.5), decimal.Decimal(13.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BRACIOLA', 2, decimal.Decimal(7.5), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'PATATE FRITTE', 4, decimal.Decimal(3.0), decimal.Decimal(12.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'GNOCCHI', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'PENNE amatriciana', 3, decimal.Decimal(5.5), decimal.Decimal(16.5)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'SALSICCE con 2 fette di polenta', 1, decimal.Decimal(6.5), decimal.Decimal(6.5)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'COSTICINE', 2, decimal.Decimal(6.5), decimal.Decimal(13.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BRACIOLA', 2, decimal.Decimal(7.5), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'PATATE FRITTE', 4, decimal.Decimal(3.0), decimal.Decimal(12.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),                                                    
            (110, 36, QDate(2018, 1, 1), QTime(19, 15, 35), '198A', None, 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
            (110, 36, QDate(2018, 1, 1), QTime(19, 15, 35), '198A', None, 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0))
            ])
        with wait_cursor_context():
            report.generate()
        dialog = QPrintPreviewDialog()
        dialog.setWindowTitle("Print preview")
        printer = dialog.printer()
        printer.setPageSize(report.receipt_page_layout(80.0).pageSize())
        printer.setFullPage(True)
        dialog.paintRequested.connect(report.print)
        dialog.exec()


