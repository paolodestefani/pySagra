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

This module is a pure python simple report engine for printing to EscPos printers.
The report definition is an XML document string. The dataset are a python list or
tuple or the result set of an SQL query.

Architecture:
Printing objects are defined of 2 types:
- inline objects (print a string)
- block objects (prints a line)
A report definition is made of bands. Every band is a collection of printing
block objects (line, barcode, images, row). A row is a container of inline objects.
A row con grow in multiple lines and generates the line printing form the included objects
Every band have a fixed height (but can grow). Every object has position relative to the including band.
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
from itertools import zip_longest
from typing import Any
from contextlib import contextmanager
from escpos.printer import Dummy
from escpos.escpos import Escpos

# PySide6
# from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtCore import QLocale
from PySide6.QtCore import Qt
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime

from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QCursor
from PySide6.QtGui import QImage

from PySide6.QtWidgets import QApplication


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
    from App.Database.Setting import Setting
    from App.Core.ExceptionHandler import wait_cursor_context

else:
    APPNAME = "Report ESCPOS Engine"
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
    session['event_description'] = "Sagra Dimostrativa 2026"
    session['event_image'] = QByteArray()
    session['company_description'] = "Comitato Festeggiamenti Dimostrativo"
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

   
# report engine version
VERSION = '1.0'

class ReportException(Exception):
    pass

class ReportCreationError(ReportException):
    pass

class ReportXMLParseError(ReportException):
    pass

class ReportNoDataError(ReportException):
    pass

class ReportPrintError(ReportException):
    pass



# Default global options

default_options = {
    'printer_profile':       'TM-T20II',
    'charcode':              'AUTO',
    'roll_width_chars':      42,
    'align':                 'left', # 'left', 'center', 'right'
    'font':                  'a', # 'a' or 'b'
    'bold':                  False,
    'underline':             0, # 0..2
    'normal_textsize':       True,
    'double_height':         False,
    'double_width':          False,
    'custom_size':           False,
    'width':                 1, # for custom_size=True width 1..8
    'height':                1, # for custom_size=True height 1..8
    'density':               0, # print density 0..8
    'invert':                False, # True = white on black printing
    'smooth':                False, # True = text smoothing. Effective on 4x4 size text and larger
    'flip':                  False, # True = upside-down printing
    'quantity_decimals':     2,
    'price_decimals':        2,
    'amount_decimals':       2,
    'currency_symbol':       '€'
}



### CODE 39 BARCODE ENCODING FUNCTION ###

# code39 barcode characters
CODE39CHRS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%'

def code39encode(text: str, checksum: bool = False) -> str|None:
    "Calculate code39 barcode string with optional checksum"
    # sanity check
    if not text:
        return None
    chkchar = ''
    # sanity checks
    for i in text:
        if i not in CODE39CHRS:
            raise ReportException('Not valid code39 chars')
    # calc checksum if required
    if checksum:
        chknum = 0
        for i in text:
            try:
                chknum += CODE39CHRS.index(i)
            except ValueError:
                raise ReportException('Not valid code39 chars')
        chkchar = CODE39CHRS[chknum % 43]
    return '*' + text + chkchar + '*'


### CODE 128 BARCODE ENCODING FUNCTION ###

# Source - https://stackoverflow.com/a
# Posted by Mark Ransom, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-03, License - CC BY-SA 4.0

def code128encode(s: str) -> str|None:
    ''' Code 128 conversion for a font as described at
        https://en.wikipedia.org/wiki/Code_128 and downloaded
        from http://www.barcodelink.net/barcode-font.php
        Only encodes ASCII characters, does not take advantage of
        FNC4 for bytes with the upper bit set.
        It does not attempt to optimize the length of the string,
        Code B is the default to prefer lower case over control characters.
        Coded for https://stackoverflow.com/q/52710760/5987
    '''
    # sanity check
    if not s:
        return None
    s = s.encode('ascii').decode('ascii')
    if s.isdigit() and len(s) % 2 == 0:
        # use Code 128C, pairs of digits
        codes = [105]
        for i in range(0, len(s), 2):
            codes.append(int(s[i:i+2], 10))
    else:
        # use Code 128B and shift for Code 128A
        mapping = dict((chr(c), [98, c + 64] if c < 32 else [c - 32]) for c in range(128))
        codes = [104]
        for c in s:
            codes.extend(mapping[c])
    check_digit = (codes[0] + sum(i * x for i,x in enumerate(codes))) % 103
    codes.append(check_digit)
    codes.append(106) # stop code
    chars = (b'\xd4' + bytes(range(33,126+1)) + bytes(range(200,211+1))).decode('latin-1')
    return ''.join(chars[x] for x in codes)



### BASE RENDER INLINE OBJECTS ###

class BaseInlineRenderer():
    "Base class for all inline tex renderer elements"

    def __init__(self, options: dict, paramdict: dict) -> None:
        self.is_visible = 'True' == paramdict.get("is_visible", "True")
        self.is_visible_parameter = None
        self.report = options['report_instance']
        # text properties
        self.font = paramdict.get("font", options['font'])
        self.bold = 'True' == paramdict.get("bold", "True")
        self.underline = int(paramdict.get("underline", "0")) # 0..2
        self.normal_textsize = 'True' == paramdict.get("normal_textsize", "True")
        self.double_height = 'True' == paramdict.get("double_height", "True")
        self.double_width = 'True' == paramdict.get("double_width", "True")
        self.density = int(paramdict.get("density", "0")) # 0..8
        self.invert = paramdict.get("font", options['font'])
        self.flip = paramdict.get("font", options['font'])
        # other
        self.width = int(paramdict.get("width", "5"))
        self.align = paramdict.get("align", options['align'])
        self.quantity_decimals = int(paramdict.get("quantity_decimals", options['quantity_decimals']))
        self.price_decimals = int(paramdict.get("price_decimals", options['price_decimals']))
        self.amount_decimals = int(paramdict.get("amount_decimals", options['amount_decimals']))
        self.currency_symbol = paramdict.get("currency_symbol", options['currency_symbol'])
        self.value: bool|int|float|decimal.Decimal|str|QDate|QDateTime|QTime|QImage|None = None  # current value
    
    def render(self) -> str:
        "Print text"
        out_text: str = ''
        match self.value:
            case bool():
                out_text = 'X' if self.value else 'O'
            case int():
                out_text = str(self.value)
            case float():
                out_text = str(self.value)
            case decimal.Decimal():
                q_locale = session['qlocale']
                thousand_sep = q_locale.groupSeparator()
                decimal_sep = q_locale.decimalPoint()
                raw_formatted = f"{float(self.value or 0.0):,.2f}"
                out_text = raw_formatted.replace(",", "X").replace(".", decimal_sep).replace("X", thousand_sep)
            case str():
                out_text = self.value
            case QDate() | QDateTime() | QTime():
                out_text = session['qlocale'].toString(self.value, QLocale.FormatType.ShortFormat)
            case _:
                oou_text = str(self.value) if self.value is not None else ""
        return out_text


class Label(BaseInlineRenderer):
    "Label class"

    def __init__(self, options: dict, paramdict: dict, text: str) -> None:
        super().__init__(options, paramdict)
        self.value = text # for labels string is the text


class Field(BaseInlineRenderer):
    "Field class"

    def __init__(self, options: dict, paramdict: dict, field_name: str) -> None:
        super().__init__(options, paramdict)
        self.value = None
        self.field_name = field_name
        self.suppress_repeated = 'True' == paramdict.get("suppress_repeated", "False") 

    def set_value(self, value: bool|int|float|decimal.Decimal|str|QDate|QDateTime|QTime|QImage) -> None:
        # if self.value is not None and self.value != '':
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
            case 'company_image':
                self.value = QImage()
                self.value.loadFromData(session['company_image'])
            case 'event_description':
                self.value = session['event_description']
            case 'event_image':
                self.value = QImage()
                self.value.loadFromData(session['event_image'])
            case _:
                self.value = ''
        return super().render()

# BLOCK OBJECTS
 
# ROW - Inline objects container


class Row(list):
    """Row class, inline element container that print a line (or more) on print_device
    
    This container of inline objects print a line of text 
    """

    def __init__(self, options:dict, paramdict: dict) -> None:
        self.is_visible = True
        self.is_visible_parameter = None
        self.parameter_negated = False
        self.report = options['report_instance']
        
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
                element.set_value(value)
            if element.is_visible:         
                lines = textwrap.wrap(element.render(), width=element.width)
            else:
                lines = [' ' * element.width]
            if not lines:
                lines = [""]
            text_columns.append(lines)
        # 2. Synchronize the columns vertically using zip_longest
        phisical_lines = list(zip_longest(*text_columns, fillvalue=""))
        
        # 3. Composizione stringa e invio fisico alla stampante
        for line in phisical_lines:
            stringa_finale_linea = ""
            
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
                    
                self.report.buffer.text(pezzo_formattato)
                print(pezzo_formattato, end='')
            
            # Invio della riga fisica al buffer/stampante
            self.report.buffer.text("\n")
            print(stringa_finale_linea)


class Line():
    "Horizontal line"

    def __init__(self, options:dict, paramdict: dict) -> None:
        self.is_visible = True
        self.is_visible_parameter = None
        self.parameter_negated = False
        self.width = int(paramdict.get("width", options['width']))
        self.align = paramdict.get("align", options['align'])
        self.roll_width_chars = options['roll_width_chars']
        self.report = options['report_instance']
        
    def __repr__(self) -> str:
        return f"Line block object"
        
    def render(self, record) -> None:
        # do nothing (but script) if not visible
        text = '-' * self.width
        match self.align:
            case 'left':
                text = f"{text:<{self.roll_width_chars}}"
            case 'center':
                text = f"{text:^{self.roll_width_chars}}"
            case 'right':
                text = f"{text:>{self.roll_width_chars}}"
            case _:
                pass
        
        self.report.buffer.text(text + "\n")
        print(text)
        
        
class NewLine():
    "New empty line CR-LF"

    def __init__(self, options:dict, paramdict: dict) -> None:
        self.is_visible = True
        self.is_visible_parameter = None
        self.parameter_negated = False
        self.count = int(paramdict.get("count", "1"))
        self.report = options['report_instance']
        
    def __repr__(self) -> str:
        return f"New line block object of count {self.count}"
        
    def render(self, record) -> None:
        text = "\n" * self.count
        self.report.buffer.text(text)
        print(text, end='')


class Image():
    "Class for embedded/external images"

    def __init__(self, options: dict, paramdict: dict, text: str = '') -> None: # text is required for generic drawobj
        self.from_resource = paramdict.get("from_resource")
        image = QImage()
        if text:
            image.loadFromData(QByteArray.fromBase64(bytearray(text.encode('utf-8')))) # Image in base64 encoding
        if self.from_resource:
            image.load(f":/{self.from_resource}")  # from resource
        if not image.isNull():
            self.image = image.scaled(int(self.width), int(self.height), Qt.TransformationMode.SmoothTransformation)
        else:
            self.image = QImage()
        if paramdict.get("is_visible_parameter"):
            t = paramdict.get("is_visible_parameter", "").split(' ')
            if t[0] == "Not":
                self.parameter_negated = True
                self.is_visible_parameter = t[1]
            else:
                self.parameter_negated = False
                self.is_visible_parameter = t[0]
                
    def __repr__(self) -> str:
        return f"Image block object"
                
    def render(self, pd: Escpos) -> None:
        "Draw image if necessary"
        # do nothing (but script) if not visible
        if self.is_visible_parameter:
            self.is_visible = (not self.report.parameter.get(self.is_visible_parameter) if self.parameter_negated 
                              else self.report.parameter.get(self.is_visible_parameter))
        if not self.is_visible:
            return
        

# Render object dictionary

inlineobj = {"label": Label,
             "field": Field,
             "summary": Summary,
             "special": Special}

blockobj = {"line": Line,
            "new_line": NewLine,
            "image": Image}

# band

class Band(list):
    "Report bands are block object container"

    def __init__(self, options: dict, paramdict: dict) -> None:
        "Every band must have a height"
        self.report = options['report_instance']
        self.is_visible = 'True' == paramdict.get("is_visible", "True")
        self.is_visible_parameter = None
        self.parameter_negated = False
        self.is_page_footer = False
        self.execute_before: str|None = None
        self.execute_after: str|None = None
        
    def __repr__(self) -> str:
        return f"Band object with {len(self)} elements"

    def render(self, record: dict) -> None:
        "Render the contained objects after setting record value"
        # python scripting
        global_parameters = {'report': self.report,
                             'band': self,
                             'record': record}
        # execute python code before rendering
        if self.execute_before:
            exec(self.execute_before, global_parameters)
        # do nothing (but script) if not visible
        if self.is_visible_parameter:
            self.is_visible = (not self.report.parameter.get(self.is_visible_parameter) if self.parameter_negated 
                              else self.report.parameter.get(self.is_visible_parameter))
        if not self.is_visible:
            return

        # call band's row elements
        for element in self:
            if element.is_visible:
                element.render(record)
        # execute python code after rendering
        if self.execute_after:
            exec(self.execute_after, global_parameters)
            

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

# Report

class Report():
    "Base class for report"

    def __init__(self, xml_string: str|None = None) -> None:
        # report output buffer
        self.buffer = Dummy()
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
        
        if 'App.Database.Setting' in sys.modules:
            setting = Setting()
            default_options['quantity_decimals'] = setting['quantity_decimal_places']
            default_options['price_decimals'] = setting['price_decimal_places']
            default_options['amount_decimals'] = setting['amount_decimal_places']
            default_options['currency_symbol'] = setting['currency_symbol']
        self.thousand_sep = session['qlocale'].groupSeparator()
        self.decimal_sep = session['qlocale'].decimalPoint()
        if xml_string:
            self.set_report_definition(xml_string)
        
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
                else:
                    bo = blockobj[blk.tag](self.options, blk.attrib)
                b.append(bo)
                if blk.tag == 'execute':
                    if blk.attrib.get('trigger') == 'Before':
                        b.execute_before = blk.text
                    if blk.attrib.get('trigger') == 'After':
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
                    self.options[child.tag] = True if val == 'True' else False
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
                            value = True if df == 'True' else False
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
                reverse = 'True' == group.attrib.get('reverse', 'False')
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

        # final cut
        self.buffer.cut() 
        
        print(self.buffer.output)

    def print(self, pd: Escpos) -> None:
        "Print document from generated report in the actual print device"
        pass

   
if __name__ == "__main__":
    app = QApplication(sys.argv)
    QLocale.setDefault(QLocale.Language.English)
    
    xml_string0 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0" print_method="ESCPOS">
    <options>
        <printer_profile type="str">TM-T20II</printer_profile>
        <charcode type="str">AUTO</charcode>
        <roll_width_chars type="int">42</roll_width_chars>
        <font type="str">a</font>
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
        <group field="id" reverse="False">
            <group_header>
                <band>
                    <row>
                        <label width="42">*** EXAMPLE OF A NON-FISCAL RECEIPT ***</label>
                    </row>
                    <row>
                        <label width="9">Order N.</label>
                        <field width="4">number</field>
                        <label width="9">Time</label>
                        <field width="6">time</field>
                        <label width="6">Table</label>
                        <field width="4">table</field>
                    </row>
                    <row>
                        <label width="20" align="left">ITEM</label>
                        <label width="5" align="right">Q.TY</label>
                        <label width="7" align="right">PRICE</label>
                        <label width="10" align="right">AMOUNT</label>
                    </row>
                    <line width="42"/>
                </band>
            </group_header>
            <group_footer>
                <band>
                    <line width="20" align="right"/>
                    <row>
                        <label width="34" align="right">TOTAL:</label>
                        <summary function="sum" width="8" align="right">amount</summary>
                    </row>
                    <new_line count="1"/>
                    <row>
                        <label width="42" align="right">THANKS AND GOODBYE</label>
                    </row>
                    <new_line count="1"/>
                    <row>
                        <label width="42" align="center">- pySagra -</label>
                    </row>
                    <new_line count="1"/>
                </band>
            </group_footer>
        </group>
    </groups>
    <details>
        <band is_visible="True">
            <row>
                <field width="20" align="left">item</field>
                <field width="5" align="right">quantity</field>
                <field width="7" align="right">price</field>
                <field width="10" align="right">amount</field>
            </row>
        </band>
    </details>
    <footer>
        <band>
            <row>
                <special>priont_date_time</special>
            </row>
        </band>
    </footer>
</report>
"""
    
    for i in (
              xml_string0,
                 ):
        r = Report(i)
        r.set_data([# id, number, date, time, table, customer name, item, quantity, prise, amount
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'GNOCCHI', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'PENNE amatriciana', 3, decimal.Decimal(5.5), decimal.Decimal(16.5)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'SALSICCE con 2 fette di polenta', 1, decimal.Decimal(6.5), decimal.Decimal(6.5)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'COSTICINE', 2, decimal.Decimal(6.5), decimal.Decimal(13.0)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BRACIOLA', 2, decimal.Decimal(7.5), decimal.Decimal(15.0)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'PATATE FRITTE', 4, decimal.Decimal(3.0), decimal.Decimal(12.0)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'FAGIOLI con cipolla', 1, decimal.Decimal(3.0), decimal.Decimal(3.0)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
                (100, 35, QDate(2018, 1, 1), QTime(19, 12, 35), '54B', 'Pippo Baudo', 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0)),
                (110, 36, QDate(2018, 1, 1), QTime(19, 15, 35), '198A', None, 'BIRRA BIONDA', 3, decimal.Decimal(5.0), decimal.Decimal(15.0)),
                (110, 36, QDate(2018, 1, 1), QTime(19, 15, 35), '198A', None, 'BIRRA ROSSA', 2, decimal.Decimal(5.5), decimal.Decimal(11.0))
                ])
        with wait_cursor_context():
            r.generate()
