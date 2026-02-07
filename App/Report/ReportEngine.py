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
items/tuples or SQL query

This module is a pure PySide6 simple report engine for printing reports.
The report definition is an XML document. The dataset are a python list or
tuple or the result set of an SQL query.

Architecture:
A report definition is made of bands. Every band is a collection of painting
objects (label, fields, lines, images, etc.). Every band have a fixed
height (but can grow). Every object has position relative to the including band.
In every report we can have this sections:
- a page header printed at the beginning of every page
- a report header printed at the beginning of the
  report in the first page after the page header
- group header printed at the beginning of the
  group for each detail group
- details printed for each record of the data source
- group footer printed at the end of the
  group for each detail group
- a report footer printed at the end of the report
  in the last page
- a page footer printed at the end of every page

Any section can have one or more band.
All sections are optional but a report need at least one detail band.


"""

# standard library
import sys
import os
import collections
import decimal
import itertools
import xml.etree.ElementTree as ET
import operator

# PySide6
from PySide6.QtCore import QOperatingSystemVersion
from PySide6.QtCore import QLocale
from PySide6.QtCore import Qt
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QSizeF
from PySide6.QtCore import QRectF
from PySide6.QtCore import QLineF
from PySide6.QtCore import QMarginsF

from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QCursor
from PySide6.QtGui import QFont
from PySide6.QtGui import QImage
from PySide6.QtGui import QColor
from PySide6.QtGui import QPen
from PySide6.QtGui import QBrush
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPicture
from PySide6.QtGui import QPageSize
from PySide6.QtGui import QPageLayout
from PySide6.QtGui import QPaintDevice
from PySide6.QtGui import QPdfWriter
from PySide6.QtWidgets import QApplication
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtPrintSupport import QPrintPreviewDialog


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

else:
    APPNAME = "Report Engine"
    APPVERSIONMAJOR = 1
    APPVERSIONMINOR = 0
    APPVERSIONPATCH = 0
    APPVERSION = f"{APPVERSIONMAJOR:02}.{APPVERSIONMINOR:02}.{APPVERSIONPATCH:02}"
    AUTHOR = "Paolo De Stefani"
    EMAIL = "info@paolodestefani.it"
    ORGANIZATION = "PDS Software"
    WEBSITE = "https:\\www.paolodestefani.it"
    session = dict()
    session['qlocale'] = QLocale()
    session['event_image'] = QByteArray()
   
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


Orientation = {'Portrait':  QPageLayout.Orientation.Portrait, # Default
               'Landscape': QPageLayout.Orientation.Landscape}

Unit = {'Millimeter':   QPageLayout.Unit.Millimeter,
        'Point':        QPageLayout.Unit.Point,  # Default
        'Inch':         QPageLayout.Unit.Inch,
        'Pica':         QPageLayout.Unit.Pica,
        'Didot':        QPageLayout.Unit.Didot,
        'Cicero':       QPageLayout.Unit.Cicero}

PSUnit = {'Millimeter': QPageSize.Unit.Millimeter,
          'Point':      QPageSize.Unit.Point,
          'Inch':       QPageSize.Unit.Inch,
          'Pica':       QPageSize.Unit.Pica,
          'Didot':      QPageSize.Unit.Didot,
          'Cicero':     QPageSize.Unit.Cicero}

PageSize = {'A0':           QPageSize.PageSizeId.A0,
            'A1':           QPageSize.PageSizeId.A1,
            'A2':           QPageSize.PageSizeId.A2,
            'A3':           QPageSize.PageSizeId.A3,
            'A4':           QPageSize.PageSizeId.A4,  # Default
            'A5':           QPageSize.PageSizeId.A5,
            'A6':           QPageSize.PageSizeId.A6,
            'A7':           QPageSize.PageSizeId.A7,
            'A8':           QPageSize.PageSizeId.A8,
            'A9':           QPageSize.PageSizeId.A9,
            'B0':           QPageSize.PageSizeId.B0,
            'B1':           QPageSize.PageSizeId.B1,
            'B2':           QPageSize.PageSizeId.B2,
            'B3':           QPageSize.PageSizeId.B3,
            'B4':           QPageSize.PageSizeId.B4,
            'B5':           QPageSize.PageSizeId.B5,
            'B6':           QPageSize.PageSizeId.B6,
            'B7':           QPageSize.PageSizeId.B7,
            'B8':           QPageSize.PageSizeId.B8,
            'B9':           QPageSize.PageSizeId.B9,
            'B10':          QPageSize.PageSizeId.B10,
            'C5E':          QPageSize.PageSizeId.C5E,
            'Comm10E':      QPageSize.PageSizeId.Comm10E,
            'DLE':          QPageSize.PageSizeId.DLE,
            'Executive':    QPageSize.PageSizeId.Executive,
            'Folio':        QPageSize.PageSizeId.Folio,
            'Ledger':       QPageSize.PageSizeId.Ledger,
            'Legal':        QPageSize.PageSizeId.Legal,
            'Letter':       QPageSize.PageSizeId.Letter,
            'Tabloid':      QPageSize.PageSizeId.Tabloid,
            'Custom':       QPageSize.PageSizeId.Custom}

# standard font properties

FontWeight = {'Thin':       QFont.Weight.Thin,
              'ExtraLight': QFont.Weight.ExtraLight,
              'Light':      QFont.Weight.Light,
              'Normal':     QFont.Weight.Normal, # Default
              'Medium':     QFont.Weight.Medium,
              'DemiBold':   QFont.Weight.DemiBold,
              'Bold':       QFont.Weight.Bold,
              'ExtraBold':  QFont.Weight.ExtraBold,
              'Black':      QFont.Weight.Black}

TextAlign = {'AlignLeft':       Qt.AlignmentFlag.AlignLeft, # Default
             'AlignRight':      Qt.AlignmentFlag.AlignRight,
             'AlignHCenter':    Qt.AlignmentFlag.AlignHCenter,
             'AlignJustify':    Qt.AlignmentFlag.AlignJustify,
             'AlignTop':        Qt.AlignmentFlag.AlignTop,
             'AlignCenter':     Qt.AlignmentFlag.AlignCenter}

# line styles

PenStyle = {'SolidLine':        Qt.PenStyle.SolidLine,
            'DashLine':         Qt.PenStyle.DashLine,
            'DotLine':          Qt.PenStyle.DotLine,
            'DashDotLine':      Qt.PenStyle.DashDotLine,
            'DashDotDotLine':   Qt.PenStyle.DashDotDotLine}

# brush styles

BrushStyle = {'NoBrush':            Qt.BrushStyle.NoBrush,
              'SolidPattern':       Qt.BrushStyle.SolidPattern,
              'Dense1Pattern':      Qt.BrushStyle.Dense1Pattern,
              'Dense2Pattern':      Qt.BrushStyle.Dense2Pattern,
              'Dense3Pattern':      Qt.BrushStyle.Dense3Pattern,
              'Dense4Pattern':      Qt.BrushStyle.Dense4Pattern,
              'Dense5Pattern':      Qt.BrushStyle.Dense5Pattern,
              'Dense6Pattern':      Qt.BrushStyle.Dense6Pattern,
              'Dense7Pattern':      Qt.BrushStyle.Dense7Pattern,
              'HorPattern':         Qt.BrushStyle.HorPattern,
              'VerPattern':         Qt.BrushStyle.VerPattern,
              'CrossPattern':       Qt.BrushStyle.CrossPattern,
              'BDiagPattern':       Qt.BrushStyle.BDiagPattern,
              'FDiagPattern':       Qt.BrushStyle.FDiagPattern,
              'DiagCrossPattern':   Qt.BrushStyle.DiagCrossPattern}

AspectRatio = {'IgnoreAspectRatio':             Qt.AspectRatioMode.IgnoreAspectRatio,
               'KeepAspectRatio':               Qt.AspectRatioMode.KeepAspectRatio,
               'KeepAspectRatioByExpanding':    Qt.AspectRatioMode.KeepAspectRatioByExpanding}

# Default global options

defaultOptions = {'documentName':           'pyReportEngine document',
                  'orientation':            'Portrait',
                  'unit':                   'Point',
                  'pageSize':               'A4',
                  'ignoreWarningOnSetPageLayout': False,
                  'topMargin':              5.0,
                  'bottomMargin':           5.0,
                  'leftMargin':             5.0,
                  'rightMargin':            5.0,
                  'barcodeType':            None,
                  'fontName':               'Arial',
                  'fontSize':               8,
                  'fontItalic':             False,
                  'fontWeight':             'Normal',
                  'textAlign':              'AlignLeft',
                  'color':                  'black',
                  'lineWidth':              1.0,
                  'lineStyle':              'SolidLine',
                  'brushStyle':             'NoBrush',
                  'brushColor':             'Black',
                  'aspectRatio':            'KeepAspectRatio',
                  'opacity':                1.0,
                  'quantityDecimals':       2,
                  'currencySymbol':         '€',
                  'MacOSFontScaleFactor':   120.0, # percent
                  'trueSymbol':             '\u25CF',
                  'falseSymbol':            '\u25CB'
                  }


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



# base elements

class BaseRenderer():
    "Base class for all tex renderer elements"

    def __init__(self, options: dict, paramdict: dict) -> None:
        self.isVisible = 'True' == paramdict.get("isVisible", "True")
        self.isVisibleParameter = paramdict.get("isVisibleParameter")
        self.isNotVisibleParameter = paramdict.get("isNotVisibleParameter")
        self.report = options['reportInstance']
        self.fieldFormat = paramdict.get("format", "")
        self.left = float(paramdict.get("left", 0))
        self.top = float(paramdict.get("top", 0))
        self.width = float(paramdict.get("width", 0))
        self.height = float(paramdict.get("height", 0))
        self.barcode = paramdict.get("barcodeType", options['barcodeType'])
        self.fontName = paramdict.get("fontName", options['fontName'])
        self.fontSize = int(paramdict.get("fontSize", options['fontSize']))
        self.MacOSFontScaleFactor = int(paramdict.get("MacOSFontScaleFactor", options['MacOSFontScaleFactor']))
        self.fontItalic = 'True' == paramdict.get("fontItalic", options['fontItalic'])
        self.fontWeight = FontWeight[paramdict.get("fontWeight", options['fontWeight'])]
        self.textAlign = TextAlign[paramdict.get("textAlign", options['textAlign'])]
        self.color = paramdict.get("color", options['color'])
        self.opacity = float(paramdict.get("opacity", options['opacity']))
        # macOS dark mode and color scheme conflicts workaround
        if self.color in ('black', '#000000'):
            self.color = '???' # an invalid color that Qt interpret as black on any platforms
        self.canGrow = 'True' == paramdict.get("canGrow", "False")
        self.quantityDecimals = int(paramdict.get("quantityDecimals", options['quantityDecimals']))
        self.currencySymbol = paramdict.get("currencySymbol", options['currencySymbol'])
        self.trueSymbol = paramdict.get("trueSymbol", options['trueSymbol'])
        self.falseSymbol = paramdict.get("falseSymbol", options['falseSymbol'])
        self.value: bool|int|float|decimal.Decimal|str|QDate|QDateTime|QTime|None = None  # default value

    def textFormat(self) -> str|None:
        "Format text for check height and painting"
        text = None
        match self.value:
            case bool():
                text = self.trueSymbol if self.value else self.falseSymbol
            case int()|float()|decimal.Decimal():
                if self.fieldFormat:
                    if self.fieldFormat == 'currency':
                        text = session['qlocale'].toCurrencyString(float(self.value),
                                                                   self.currencySymbol) # looks like int/decimal require a float conversion before currency string
                    elif self.fieldFormat == 'decimal2':
                        text = session['qlocale'].toString(float(self.value),
                                                           'f',
                                                           2)
                    elif self.fieldFormat == 'quantity':
                        text = session['qlocale'].toString(float(self.value),
                                                           'f',
                                                           self.quantityDecimals)
                    else:
                        # python string format for numbers f.e. '{0:.2f}'
                        text = self.fieldFormat.format(self.value)
                else:
                    if isinstance(self.value, decimal.Decimal): # decimal without format
                        text = session['qlocale'].toString(float(self.value), 'f', 2)
                    else: # qlocale format for numbers
                        text = session['qlocale'].toString(self.value)
            case QDate()|QDateTime()|QTime():
                if self.fieldFormat: # qt string format f.e. 'dd.MM.yyyy'
                    text = self.value.toString(self.fieldFormat)
                else:
                    text = session['qlocale'].toString(self.value, QLocale.FormatType.ShortFormat)
            case str() if self.barcode == 'Code39':
                text = code39encode(self.value) # None value, not an empty string, for barcode for print nothing 
            case str() if self.barcode == 'Code128':
                text = code128encode(self.value) # None value, not an empty string, for barcode for print nothing               
            case _:
                text = str(self.value or '') # None for string print empty string    
        return text
    
    def checkHeight(self, bandOffset: float, bandHeight:float) -> float:
        "Returns the new band height if band can grow"
        # if an object is not visible don't need to check height
        if not self.isVisible:
            return bandHeight
        painter = self.report.painter
        height = self.height if bandOffset + self.top + self.height <= bandOffset + bandHeight else bandHeight - self.top
        # check image
        if isinstance(self.value, QImage):
            painter.save()
            source = QRectF(self.value.rect())
            if height < self.height and not self.canGrow:
                source.setHeight(height)
            painter.restore()
            return max(source.height(), bandHeight)
        # check text elements
        painter.save()
        # for MacOS font scale factor %
        if QOperatingSystemVersion.currentType() == QOperatingSystemVersion.OSType.MacOS:
            fontSize = int(self.fontSize * self.MacOSFontScaleFactor / 100.0)
        else:
            fontSize = self.fontSize 
        painter.setFont(QFont(self.fontName, fontSize, self.fontWeight, self.fontItalic))
        text = self.textFormat() or ' '  # for painter.boundingRect a string NOT empty is required
        flags = self.textAlign
        if self.canGrow:
            flags |= Qt.TextFlag.TextWordWrap
        rect = painter.boundingRect(QRectF(self.left,
                                           self.top,
                                           self.width,
                                           self.height),
                                    flags,
                                    text)
        painter.restore()
        if rect.height():
            return max(rect.height(), bandHeight)
        return bandHeight

    def render(self, bandOffset:float, bandHeight:float) -> None:
        "Paint an image or text"
        if self.isVisibleParameter:
            self.isVisible = self.report.parameter[self.isVisibleParameter]
        if self.isNotVisibleParameter:
            self.isVisible = not self.report.parameter[self.isNotVisibleParameter]
        if not self.isVisible:  
            return
        painter = self.report.painter
        painter.save()
        pen = QPen()
        pen.setColor(QColor(self.color))
        painter.setPen(pen)
        # for MacOS font scale factor %
        if QOperatingSystemVersion.currentType() == QOperatingSystemVersion.OSType.MacOS:
            fontSize = int(self.fontSize * self.MacOSFontScaleFactor / 100.0)
        else:
            fontSize = self.fontSize
        painter.setFont(QFont(self.fontName, fontSize, self.fontWeight, self.fontItalic))
        # effect
        painter.setOpacity(self.opacity)
        # contain the dimentions into the band boundary
        top = self.top + bandOffset if self.top + bandOffset <= bandOffset + bandHeight else bandOffset + bandHeight
        height = self.height if bandOffset + self.top + self.height <= bandOffset + bandHeight else bandHeight - self.top

        # draw image
        if isinstance(self.value, QImage):
            source = QRectF(self.value.rect())
            if height < self.height and (not self.canGrow):
                source.setHeight(height)
            painter.drawImage(QRectF(self.left,
                                     top,
                                     self.width,
                                     height),
                              self.value,
                              source)
            painter.restore()
            return

        # draw text convertable values
        text = self.textFormat()
        flags = self.textAlign
        if self.canGrow:
            flags |= Qt.TextFlag.TextWordWrap
            height = bandHeight
        # draw text
        painter.drawText(QRectF(self.left,
                                top,
                                self.width,
                                height),
                         flags,
                         text)
        painter.restore()
        return


class Label(BaseRenderer):
    "Label class"

    def __init__(self, options: dict, paramdict: dict, string: str) -> None:
        super().__init__(options, paramdict)
        self.value = string # for labels string is the text


class Field(BaseRenderer):
    "Field class"

    def __init__(self, options: dict, paramdict: dict, fieldName: str) -> None:
        super().__init__(options, paramdict)
        self.value = None
        self.fieldName = fieldName
        self.aspectRatio = AspectRatio[paramdict.get("aspectRatio", options['aspectRatio'])]

    def setValue(self, value: str|int|float|decimal.Decimal|QByteArray) -> None:
        if isinstance(value, QByteArray):
            image = QImage()
            image.loadFromData(value)
            # scale image if necessary
            if image.width != int(self.width) or image.height() != int(self.height):
                self.value = image.scaled(int(self.width), int(self.height), self.aspectRatio, Qt.SmoothTransformation)
            else:
                self.value = image
        else:
            self.value = value


class Summary(BaseRenderer):
    "Class for summaries"

    def __init__(self, options: dict, paramdict: dict, fieldName: str) -> None:
        super().__init__(options, paramdict)
        self.fieldName = fieldName
        self.function = paramdict['function']
        self.onRelatedField = paramdict.get('onRelatedField', None)
        self.lastValue = None
        self.items = 0
        self.summary = 0
        options['reportInstance'].summaries.append(self)  # used for reset all summaries

    def update(self, record: dict) -> None:
        "Update summary value"
        # conditional summary updating based on value change of another field
        if self.onRelatedField:
            if self.lastValue == record[self.onRelatedField]:
                return
            self.lastValue = record[self.onRelatedField]

        if self.function == 'sum':
            self.summary += record[self.fieldName]
        elif self.function == 'count':
            self.summary += 1
        elif self.function == 'min':
            if self.items > 0:
                self.summary = min(record[self.fieldName], self.summary)
            else:
                self.summary = record[self.fieldName]
        elif self.function == 'max':
            if self.items > 0:
                self.summary = max(record[self.fieldName], self.summary)
            else:
                self.summary = record[self.fieldName]
        elif self.function == 'average':
            self.summary += record[self.fieldName]
        else:
            pass
        self.items += 1

    def reset(self) -> None:
        self.lastValue = None
        self.summary = 0
        self.items = 0

    def render(self, bandOffset: float, bandHeight: float) -> None:
        if self.function == 'average':
            if self.items != 0:
                self.value = self.summary / self.items
            else:
                self.value = f"{self.summary}/{self.items}"
        else:
            self.value = self.summary
        super().render(bandOffset, bandHeight)


class Special(BaseRenderer):
    "Class for special fields"

    def __init__(self, options:dict, paramdict: dict, varName: str) -> None:
        super().__init__(options, paramdict)
        self.varName = varName
        self.value = None # band.render() set the field value

    def render(self, bandOffset: float, bandHeight: float) -> None:
        match self.varName:
            case 'pageNumber':
                self.value = self.report.page_num
            case 'printDate':
                self.value = session['qlocale'].toString(QDate.currentDate(), QLocale.FormatType.ShortFormat)
            case 'printDateTime':
                self.value = session['qlocale'].toString(QDateTime.currentDateTime(), QLocale.FormatType.ShortFormat)
            case 'printTime':
                self.value = session['qlocale'].toString(QTime.currentTime(), QLocale.FormatType.ShortFormat)
            case 'recordNumber':
                self.value = self.report.rn
            case 'appName':
                self.value = APPNAME
            case 'appAuthor':
                self.value = AUTHOR
            case 'appEmail':
                self.value = EMAIL
            case 'appOrganization':
                self.value = ORGANIZATION
            case 'appWebsite':
                self.value = WEBSITE
            case 'companyDescription':
                self.value = session['company_description']
            case 'companyImage':
                self.value = QImage()
                self.value.loadFromData = session['company_image']
            case 'eventDescription':
                self.value = session['event_description']
            case 'eventImage':
                self.value = QImage()
                self.value.loadFromData(session['event_image'])
            case _:
                self.value = ''
        super().render(bandOffset, bandHeight)


class Line():
    "Base class for lines"

    def __init__(self, options:dict, paramdict: dict, text: str = '') -> None:  # text is required for generic drawobj
        self.isVisible = True
        self.isVisibleParameter = paramdict.get("isVisibleParameter")
        self.isNotVisibleParameter = paramdict.get("isNotVisibleParameter")
        self.report = options['reportInstance']
        self.x1 = float(paramdict.get("x1", 0))
        self.y1 = float(paramdict.get("y1", 0))
        self.x2 = float(paramdict.get("x2", 0))
        self.y2 = float(paramdict.get("y2", 0))
        self.color = paramdict.get("color", options['color'])
        self.opacity = float(paramdict.get("opacity", options['opacity']))
        self.lineWidth = float(paramdict.get("lineWidth", options['lineWidth']))
        self.style = PenStyle[paramdict.get("style", options['lineStyle'])]

    def render(self, bandOffset: float, bandHeight: float) -> None:
        if self.isVisibleParameter:
            self.isVisible = self.report.parameter[self.isVisibleParameter]
        if self.isNotVisibleParameter:
            self.isVisible = not self.report.parameter[self.isNotVisibleParameter]
        if not self.isVisible:
            return
        painter = self.report.painter
        painter.save()
        pen = QPen()
        pen.setColor(QColor(self.color))
        pen.setWidthF(self.lineWidth)
        pen.setStyle(self.style)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen)
        # effect
        painter.setOpacity(self.opacity)
        # contain the dimentions into the band boundary
        y1 = self.y1 + bandOffset if self.y1 + bandOffset <= bandOffset + bandHeight else bandOffset + bandHeight
        y2 = self.y2 + bandOffset if self.y2 + bandOffset <= bandOffset + bandHeight else bandOffset + bandHeight
        # draw
        painter.drawLine(QLineF(self.x1,
                                y1,
                                self.x2,
                                y2))
        painter.restore()
        return


class Rectangle():
    "Rectangle class"

    def __init__(self, options: dict, paramdict: dict, text: str|None) -> None: # text is required for generic drawobj
        self.isVisible = True
        self.isVisibleParameter = paramdict.get("isVisibleParameter")
        self.isNotVisibleParameter = paramdict.get("isNotVisibleParameter")
        self.report = options['reportInstance']
        self.left = float(paramdict.get("left", 0.0))
        self.top = float(paramdict.get("top", 0.0))
        self.width = float(paramdict.get("width", 0.0))
        self.height = float(paramdict.get("height", 0.0))
        self.xRadius = float(paramdict.get("xRadius", 0.0)) or None
        self.yRadius = float(paramdict.get("yRadius", 0.0)) or None
        self.lineWidth = float(paramdict.get("lineWidth", 0.0))
        self.color = QColor(paramdict.get("color", options['color']))
        self.style = PenStyle[paramdict.get("style", options['lineStyle'])]
        self.brushColor = QColor(paramdict.get("brushColor", options['color']))
        self.brushStyle = BrushStyle[paramdict.get("brushStyle", 'NoBrush')]
        self.opacity = float(paramdict.get("opacity", options['opacity']))

    def render(self, bandOffset: float, bandHeight: float) -> None:
        if self.isVisibleParameter:
            self.isVisible = self.report.parameter[self.isVisibleParameter]
        if self.isNotVisibleParameter:
            self.isVisible = not self.report.parameter[self.isNotVisibleParameter]
        if not self.isVisible:
            return
        painter = self.report.painter
        painter.save()
        # pen for outline, brush for fill
        pen = QPen()
        pen.setColor(self.color)
        pen.setWidthF(self.lineWidth)
        pen.setStyle(self.style)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen)
        if self.brushStyle != Qt.BrushStyle.NoBrush:
            brush = QBrush()
            brush.setStyle(self.brushStyle)
            brush.setColor(self.brushColor)
            painter.setBrush(brush)
        # effect
        painter.setOpacity(self.opacity)
        # contain the dimentions into the band boundary
        top = self.top + bandOffset if self.top + bandOffset <= bandOffset + bandHeight else bandOffset + bandHeight
        height = self.height if bandOffset + self.top + self.height <= bandOffset + bandHeight else bandHeight - self.top

        # draw
        if self.xRadius and self.yRadius:
            # draw a rounded rectangle
            painter.drawRoundedRect(QRectF(self.left,
                                           top,
                                           self.width,
                                           height),
                                    self.xRadius,
                                    self.yRadius)
        else:
            # draw a rectangle
            painter.drawRect(QRectF(self.left,
                                    top,
                                    self.width,
                                    height))
        painter.restore()


class Image():
    "Class for embedded/external images"

    def __init__(self, options: dict, paramdict: dict, text: str = '') -> None: # text is required for generic drawobj
        self.isVisible = 'True' == paramdict.get("isVisible", "True")
        self.isVisibleParameter = paramdict.get("isVisibleParameter")
        self.isNotVisibleParameter = paramdict.get("isNotVisibleParameter")
        #self.canGrow = 'True' == paramdict.get("canGrow", "False")
        self.report = options['reportInstance']
        self.left = float(paramdict.get("left", 0.0))
        self.top = float(paramdict.get("top", 0.0))
        self.width = float(paramdict.get("width", 0.0))
        self.height = float(paramdict.get("height", 0.0))
        self.fromResource = paramdict.get("fromResource")
        self.aspectRatio = AspectRatio[paramdict.get("aspectRatio", options['aspectRatio'])]
        self.opacity = float(paramdict.get("opacity", options['opacity']))
        image = QImage()
        if text:
            image.loadFromData(QByteArray.fromBase64(bytearray(text.encode('utf-8')))) # Image in base64 encoding
        if self.fromResource:
            image.load(f":/{self.fromResource}")  # from resource
        self.image = image.scaled(int(self.width), int(self.height), self.aspectRatio, Qt.TransformationMode.SmoothTransformation)

    def render(self, bandOffset: float, bandHeight: float) -> None:
        "Draw image if necessary"
        if self.isVisibleParameter:
            self.isVisible = self.report.parameter[self.isVisibleParameter]
        if self.isNotVisibleParameter:
            self.isVisible = not self.report.parameter[self.isNotVisibleParameter]
        if not self.isVisible:
            return
        painter = self.report.painter
        painter.save()
        # effect
        painter.setOpacity(self.opacity)
        # contain the dimentions into the band boundary
        top = self.top + bandOffset if self.top + bandOffset <= bandOffset + bandHeight else bandOffset + bandHeight
        height = self.height if bandOffset + self.top + self.height <= bandOffset + bandHeight else bandHeight - self.top
        # draw
        painter.drawImage(QRectF(self.left,
                                 top,
                                 self.width,
                                 height),
                          self.image)
        painter.restore()


# Render object dictionary

drawobj = {"label": Label,
           "field": Field,
           "summary": Summary,
           "special": Special,
           "line": Line,
           "rectangle": Rectangle,
           "image": Image}


# band

class Band(list):
    "Report bands are elements container"

    def __init__(self, options: dict, paramdict: dict) -> None:
        "Every band must have a height"
        self.report = options['reportInstance']
        self.isVisible = 'True' == paramdict.get("isVisible", "True")
        self.isVisibleParameter = paramdict.get("isVisibleParameter")
        self.isNotVisibleParameter = paramdict.get("isNotVisibleParameter")
        self.isPageFooter = False
        self.height = float(paramdict.get("height", 0.0))
        self.canGrow = 'True' == paramdict.get("canGrow", "False")
        self.newPageAfter = 'True' == paramdict.get("newPageAfter", "False")
        self.restartPageNumber = 'True' == paramdict.get("restartPageNumber", "False") # only on new page
        self.executeBefore = None
        self.executeAfter = None

    def render(self, record: dict, prev_record: dict|None = None) -> None:
        "Render the contained objects after setting record value"
        # call newPage if have a pending request
        if self.report.newPageRequest:
            #self.report.newPageRequest = False # must be before newPage because newPage have other bands
            self.report.newPage(record)

        # python scripting
        globalsParameters = {'Qt': Qt,
                             'report': self.report,
                             'band': self,
                             'record': record,
                             'prev_record': prev_record}
        # execute python code before rendering
        if self.executeBefore:
            exec(self.executeBefore, globalsParameters)
        # do nothing (but script) if not visible
        if self.isVisibleParameter:
            self.isVisible = self.report.parameter.get(self.isVisibleParameter)
        if self.isNotVisibleParameter:
            self.isVisible = not self.report.parameter.get(self.isNotVisibleParameter)
        if not self.isVisible:
            return

        newHeight = self.height
        if self.canGrow:
            # adjust the band height to the maximum required by the contained objects
            for element in self:
                if isinstance(element, Field):
                    element.setValue(record[element.fieldName])
                if isinstance(element, BaseRenderer):  # check heigh for fields, labels, summaries, etc.
                    newHeight = element.checkHeight(self.report.offset, newHeight)
        if not self.isPageFooter:
            # start a new page if necessary
            if self.report.offset + newHeight > self.report.page_height - self.report.footer_height:
                self.report.newPage(record)
        # offset must be set after newPage if any
        offset = self.report.offset

        # draw band's elements
        for element in self:
            if isinstance(element, Field):
                element.setValue(record[element.fieldName])
            # if element.isVisible:
            element.render(offset, newHeight)
        # update report offset
        self.report.offset += newHeight
        # execute python code after rendering
        if self.executeAfter:
            exec(self.executeAfter, globalsParameters)
        # restart page numbering if required, must be set before newPage
        if self.restartPageNumber:
            self.report.page_num = 0
        # new page if required
        if self.newPageAfter and self.report.rn < self.report.last_record_num:
            self.report.newPageRequest = True


class Sort(str):
    "Class that adds a reverse boolean value to a string, used for grouping/ordering"

    def __new__(self, text: str, reverse: bool) -> str:
        sg = str.__new__(self, text)
        sg.reverse = True if reverse == 'True' else False
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
    def __init__(self, code: str, description: str, ftype: str) -> None:
        self.code = code
        self.description = description
        self.ftype = ftype


# Report

class Report():
    "Base class for report"

    def __init__(self, xml_string: str|None = None) -> None:
        # report elements
        self.page_background = [] # printed on every page, absolute coordinates, no data
        self.page_header = [] # printed on every page
        self.page_footer = [] # printed on every page
        self.report_header = [] # printed on first page before any group/detail
        self.report_footer = [] # printed on last page after any group/detail
        self.sortings = [] # ordered sorting fields
        self.groups = []  # ordered grouping conditions
        self.group_headers = {} # grouping field: [list of bands]
        self.group_footers = {} # grouping field: [list of bands]
        # self.group_summaries = {}  # grouping field: [list of summary function]
        self.details = [] # must be defined
        self.execute = None # report scripting before starting
        # sql query and field used for generate dataset from sql database
        self.query = None
        self.query_where = None
        self.query_group_by = None
        self.query_order_by = None
        self.conditions = collections.OrderedDict()
        # dataset column definition
        self.column = {} # column aliases
        # data container, overwritten if self.select is not None
        self.data = []
        self.prev_record = None  # pointer to previous rendered record
        # report parameters as a param: value dictionary
        self.parameter = collections.OrderedDict()
        self.summaries = []  # each summary init update this list, must be set before calling setReportDefinition
        #print('Modules:', sys.modules.keys())
        if 'App.Database.Setting' in sys.modules:
            setting = Setting()
            defaultOptions['quantityDecimals'] = setting['quantity_decimal_places']
            defaultOptions['currencySymbol'] = setting['currency_symbol']
        if xml_string:
            self.setReportDefinition(xml_string)

        # report rendering variables
        self.painter = QPainter()
        self.pages = [] # list of pages (QPicture)
        self.offset = 0.0
        self.page_num = 0

    def appendBands(self, childElement: str) -> list:
        outList = []
        for band in childElement.findall('band'):
            b = Band(self.options, band.attrib)
            for sub in band:
                if sub.tag in drawobj:
                    b.append(drawobj[sub.tag](self.options, sub.attrib, sub.text))
                if sub.tag == 'execute':
                    if sub.attrib.get('trigger') == 'Before':
                        b.executeBefore = sub.text
                    if sub.attrib.get('trigger') == 'After':
                        b.executeAfter = sub.text
            outList.append(b)
        return outList

    def setReportDefinition(self, xml_string: str) -> None:
        "Create painting objects and other elements from xml definition"
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as er:
            raise ReportXMLParseError(er)
        self.options = defaultOptions.copy() # Inherit default options
        self.options['reportInstance'] = self  # give reference to report object

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
            val = child.text
            if attr == 'bool':
                self.options[child.tag] = True if val == 'True' else False
            elif attr == 'str':
                self.options[child.tag] = val
            elif attr == 'int':
                self.options[child.tag] = int(val)
            elif attr == 'float':
                self.options[child.tag] = float(val)
            else:
                raise ReportXMLParseError(f"Option with wrong/without type "
                                          f"attribute: <{child.tag}> = {val}")

        # report parameters
        params = root.find('parameters')
        if params is not None:
            for child in params:
                if child.tag == 'parameter':
                    param = child.attrib.get('id')
                    ptype = child.attrib.get('type')
                    value = None
                    items = []
                    referenceList = child.attrib.get('reference')
                    if ptype == 'bool':
                        value = True if child.attrib.get('default') == 'True' else False
                    elif ptype == 'int':
                        value = int(child.attrib.get('default'))
                    elif ptype == 'float':
                        value = float(child.attrib.get('default'))
                    elif ptype == 'str':
                        value = child.attrib.get('default') or ''
                    elif ptype == 'date':
                        value = QDate.fromString(child.attrib.get('default'), 'yyyyMMdd')
                    elif ptype == 'list':
                        value = child.attrib.get('default') or ''
                    if child.attrib.get('items'):
                        items = {}
                        for i in child.attrib.get('items').split('|'):
                            k, v = i.split(":")
                            items[k] = v
                            
                    self.parameter[param] = Parameter(child.text, ptype, value, items, referenceList)

        # report scripting
        execute = root.find('execute')
        if execute is not None:
            self.execute = execute.text

        # query definition
        query = root.find('query')
        if query is not None:
            for child in query:
                if child.tag == 'select':
                    self.query = child.text
                if child.tag == 'where':
                    self.query_where = child.text
                if child.tag == 'groupBy':
                    self.query_group_by = child.text
                if child.tag == 'orderBy':
                    self.query_order_by = child.text
                if child.tag == 'conditions':
                    for cond in child.findall("condition"):
                        self.conditions[cond.text] = SqlField(cond.attrib.get('code'),
                                                              cond.attrib.get('description'),
                                                              cond.attrib.get('type'))

        # columns' names
        columns = root.find('columns')
        if columns is None:
            raise ReportXMLParseError("The mandatory element 'columns' was not found.")
        else:
            for i, c in enumerate(columns.findall("fieldName")):
                self.column[c.text] = i

        # sortings
        sorting = root.find('sorting')
        if sorting is not None:
            for sort in sorting.findall("sort"):
                field = sort.attrib.get('field')
                reverse = sort.attrib.get('reverse')
                self.sortings.append(Sort(field, reverse))

        # groups headers/footers
        groups = root.find('groups')
        if groups is not None:
            for group in groups.findall('group'):
                field = group.attrib.get('field')
                reverse = group.attrib.get('reverse')
                self.groups.append(Sort(field, reverse))
                for child in group:
                    if child.tag == "groupHeader":
                        self.group_headers[field] = self.appendBands(child)
                    if child.tag == "groupFooter":
                        self.group_footers[field] = self.appendBands(child)

        # other render elements
        for child in root:
            if child.tag == "pageBackground":
                for sub in child:
                    self.page_background.append(drawobj[sub.tag](self.options, sub.attrib, sub.text))

            if child.tag == "pageHeader":
                self.page_header = self.appendBands(child)

            if child.tag == "reportHeader":
                self.report_header = self.appendBands(child)

            if child.tag == "details":
                self.details = self.appendBands(child)

            if child.tag == "pageFooter":
                for i in self.appendBands(child):
                    i.isPageFooter = True
                    self.page_footer.append(i)

            if child.tag == "reportFooter":
                self.report_footer = self.appendBands(child)

        if self.details is None:
            raise ReportXMLParseError("The mandatory element 'details' was not found.")

        # set report page layout
        if self.options['pageSize'] == 'Custom':
            pageSize = QPageSize(QSizeF(self.options['pageWidth'],
                                        self.options['pageHeight']),
                                 PSUnit[self.options["unit"]])
        else:
            pageSize = QPageSize(PageSize[self.options['pageSize']])
        self.pageLayout = QPageLayout(pageSize,
                                      Orientation[self.options['orientation']],
                                      QMarginsF(self.options['leftMargin'],
                                                self.options['topMargin'],
                                                self.options['rightMargin'],
                                                self.options['bottomMargin']),
                                      Unit[self.options["unit"]])

    def setData(self, dataSet: list|None = None) -> None:
        self.data = dataSet

    def newPage(self, record: dict) -> None:
        "Add a new page with header/footer if required"
        # reset newPageRequest first
        self.newPageRequest = False
        page = QPicture()
        self.pages.append(page)
        # close last page and start with the new one
        if self.painter.isActive():
            self.painter.end()
        self.painter.begin(page)
        self.page_num += 1
        # set page and footer offset
        self.offset = float(self.options['topMargin'])
        # print page background
        if self.page_background:
            for i in self.page_background:
                if isinstance(i, Field):
                    i.setValue(record[i.fieldName])
                i.render(0.0, self.page_height)
        # print page header
        if self.page_header:
            for b in self.page_header:
                b.render(record)
        # print page footer
        page_offset = self.offset # copy current page offset
        self.offset = self.page_height - self.footer_height # set footer offset
        if self.page_footer:
            for b in self.page_footer:
                b.render(record)
        # restore page offset
        self.offset = page_offset

    def groupGenerate(self, data: list, group_index: int = 0) -> None:
        "Resolve groups recursively"
        grp = self.groups[group_index] if self.groups else None
        for key, group in itertools.groupby(data, lambda x: x[self.column[grp]] if grp else None):  # if no group returns all the dataset
            sub_data = list(group)
            header_record = {k: sub_data[0][v] for k, v in self.column.items()} # first record of the group
            footer_record = {k: sub_data[-1][v] for k, v in self.column.items()} # last record of the group
            
            # group headers
            if self.groups:
                if grp in self.group_headers:
                    for b in self.group_headers[grp]:
                        b.render(header_record, self.prev_record)

            # call recursively this method for nested groups
            if self.groups:
                if group_index < len(self.groups) - 1: # group index must be a local variable, is different from any method call
                    self.groupGenerate(sub_data, group_index + 1)
                    sub_data.clear() # render details only in subgroup

            # details
            for rec in sub_data:
                record = {k: rec[v] for k, v in self.column.items()}
                for b in self.details:
                    b.render(record, self.prev_record)
                # update summaries on group footers and report footers
                # it is require to scroll all the dataset for update summaries so is not possible to put summaries on headers
                if self.groups:
                    for i in self.groups:
                        if self.group_footers.get(i):
                            for b in self.group_footers.get(i):
                                for a in b:
                                    if isinstance(a, Summary):
                                        a.update(record)
                if self.report_footer:
                    for b in self.report_footer:
                        for a in b:
                            if isinstance(a, Summary):
                                a.update(record)
                self.rn += 1  # increase record number only after rendering the previous one
                self.prev_record = record.copy()

            # group footer
            if self.groups:
                if grp in self.group_footers:
                    for b in self.group_footers[grp]:
                        b.render(footer_record, self.prev_record)
                    # reset summaries
                    for b in self.group_footers[grp]:
                        for a in b:
                            if isinstance(a, Summary):
                                a.reset()

    def generate(self) -> None:
        "Generate report"
        if not self.data:  # no data to render
            raise ReportNoDataError
        # clear first
        self.pages.clear()
        self.page_num = 0
        for s in self.summaries:
            s.reset()
        # Calc space available for details bands and all the other bands
        self.page_height = self.pageLayout.fullRect(Unit[self.options["unit"]]).height()
        self.offset = float(self.options['topMargin'])
        # calc footer height
        self.footer_height = float(self.options['bottomMargin'])
        if self.page_footer:
            for b in self.page_footer:
                self.footer_height += b.height

        # sort for required sorting
        for col, rev in [(self.column[i], i.reverse) for i in reversed(self.sortings)]:
            try:
                self.data.sort(key=operator.itemgetter(col), reverse=rev)
            except TypeError: # if a value is None
                try:
                    # sort with None values and strings
                    self.data.sort(key= lambda i: '' if not i[col] else i[col], reverse=rev)
                except TypeError:
                    # sort with None values and numbers
                    self.data.sort(key= lambda i: 0 if not i[col] else i[col], reverse=rev)
                    
        # sort for grouping
        for col, rev in [(self.column[i], i.reverse) for i in reversed(self.groups)]:
            try:
                self.data.sort(key=operator.itemgetter(col), reverse=rev)
            except TypeError: # if a value is None
                try:
                    # sort with None values and strings
                    self.data.sort(key= lambda i: '' if not i[col] else i[col], reverse=rev)
                except TypeError:
                    # sort with None values and numbers
                    self.data.sort(key= lambda i: 0 if not i[col] else i[col], reverse=rev)

        first_record_num = 1
        last_record_num = len(self.data)
        self.last_record_num = last_record_num # reference for bands

        # report scripting, only one time before starting
        if self.execute:
            globalsParameters = {'Qt': Qt,
                                 'report': self}
            exec(self.execute, globalsParameters)

        self.rn = first_record_num

        # begin with new page and report header if required on first record
        first_record = {k: self.data[0][v] for k, v in self.column.items()}
        last_record = {k: self.data[-1][v] for k, v in self.column.items()}

        self.newPageRequest = False # band set this to True when the next band have to call newPage
        self.newPage(first_record)

        if self.report_header:
            for b in self.report_header:
                b.render(first_record)

        # start iterating the dataset
        self.prev_record = {}
        self.groupGenerate(self.data)

        # report footer
        if self.report_footer:
            for b in self.report_footer:
                b.render(last_record)

        self.painter.end() # newPage() do a painter.begin

    def reportName(self) -> str:
        return self.options['documentName']

    def print(self, paintDevice: QPaintDevice) -> None:
        "Print document from generated report"
        if isinstance(paintDevice, QPrinter):
            paintDevice.setDocName(self.options['documentName'])
        elif isinstance(paintDevice, QPdfWriter ): # for PDFWriter
            paintDevice.setTitle(self.options['documentName'])
        # forse printer resolution to platform specific DPI avoiding scaling problems
        if isinstance(paintDevice, QPrinter):
            if QOperatingSystemVersion.currentType() != QOperatingSystemVersion.MacOS:
                paintDevice.setResolution(96)  # Windows and Linux use 96 DPI          
        # force the printer page layout to the report settings
        if not paintDevice.setPageLayout(self.pageLayout):
            w = self.pageLayout.fullRect().size().width()
            h = self.pageLayout.fullRect().size().height()
            u = list(Unit.keys())[list(Unit.values()).index(self.pageLayout.units())]
            if not self.options['ignoreWarningOnSetPageLayout']:
                raise ReportPrintError(f"Unable to set page layout ( {u} {w} x {h} ) to paint device")
        # Coordinate system to selected unit of report definition (converted to Points)
        rect = self.pageLayout.paintRect(self.pageLayout.units()).toRect()
        rect.moveTo(0, 0)
        painter = QPainter(paintDevice)
        painter.setWindow(rect)
        painter.setViewport(0, 0, paintDevice.width(), paintDevice.height())
        
        if isinstance(paintDevice, QPrinter):
            fromPage = paintDevice.fromPage() or 1
            toPage = paintDevice.toPage() or len(self.pages)
        elif isinstance(paintDevice, QPdfWriter): # for PDFWriter
            fromPage = 1
            toPage = len(self.pages)

        for pn, page in enumerate(self.pages, 1):
            if fromPage <= pn <= toPage:
                page.play(painter)
                if pn != toPage: # newPage not on last page
                    paintDevice.newPage()
        painter.end()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    QLocale.setDefault(QLocale.Language.English)
    
    xml_string0 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0">
    <options>
        <topMargin type="float">0.0</topMargin>
        <bottomMargin type="float">0.0</bottomMargin>
        <leftMargin type="float">0.0</leftMargin>
        <rightMargin type="float">0.0</rightMargin>
    </options>
    <columns>
        <fieldName>Empty</fieldName>
    </columns>
    <pageBackground>
        <rectangle color="red" left="0.0" top="0.0" width="595.0" height="842.0" lineWidth="3.0"/>
        <line x1="0.0" y1="0.0" x2="595.0" y2="842.0" lineWidth="1.0"/>
        <line x1="595.0" y1="0.0" x2="0.0" y2="842.0" lineWidth="1.0"/>
    </pageBackground>
    <pageHeader>
        <band height="80.0">
        <label left="0.0" top="10.0" width="595.0" height="80.0" color="blue"
        fontName="Impact" fontWeight="Bold" fontItalic="True" fontSize="32"
        textAlign="AlignHCenter">*** MINIMAL REPORT EXAMPLE ***</label>
        </band>
    </pageHeader>
    <details>
        <band height="100.0" canGrow="True">
            <label left="0.0" top="0.0" width="595.0" height="15.0" textAlign="AlignHCenter">A report must have at least one record, even if it is empty.</label>
            <label left="0.0" top="20.0" width="595.0" height="15.0" textAlign="AlignHCenter">In this example the dataset is one record of one field that is None/Null</label>
            <label left="0.0" top="50.0" width="595.0" height="15.0" textAlign="AlignHCenter">Page size is A4, no margins, page background and one dataset line</label>
        </band>
    </details>
</report>
"""
    xml_string1 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0">
    <options>
        <documentName type="str">Example of a complete report</documentName>
        <orientation type="str">Portrait</orientation>
        <pageSize type="str">A4</pageSize>
        <topMargin type="float">5.0</topMargin>
        <bottomMargin type="float">5.0</bottomMargin>
        <leftMargin type="float">5.0</leftMargin>
        <rightMargin type="float">5.0</rightMargin>
        <fontName type="str">Arial</fontName>
        <fontSize type="int">8</fontSize>
    </options>
    <columns>
        <fieldName>code</fieldName>
        <fieldName>description</fieldName>
        <fieldName>department</fieldName>
        <fieldName>stock_control</fieldName>
        <fieldName>quantity</fieldName>
        <fieldName>date</fieldName>
    </columns>
    <sorting>
        <sort field="department" reverse="False"/>
        <sort field="date" reverse="False"/>
        <sort field="quantity" reverse="True"/>
    </sorting>
    <pageHeader>
        <band height="100.0">
        <image left="0.0" top="0.0" width="48.0" height="48.0" aspectRatio="KeepAspectRatio" opacity="1.0">
        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
        AElFTkSuQmCC</image>
        <label left="0.0" top="20.0" width="550.0" height="38.0" color="blue"
        fontName="Impact" fontWeight="Bold" fontItalic="True" fontSize="24"
        textAlign="AlignHCenter">Example of a complete report</label>
        <rectangle xRadius="3.0" yRadius="3.0" left="0.0" top="72.0" width="585.0" height="15.0" lineWidth="1.0"/>
        <label left="5.0" top="60.0" width="585.0" height="15.0" fontSize="6">A complete report with 2 level of grouping, department and date, and aggregate functions</label>
        <label left="5.0" top="75.0" width="100.0" height="15.0">Code</label>
        <label left="100.0" top="75.0" width="240.0" height="15.0">Description</label>
        <label left="340.0" top="75.0" width="100.0" height="15.0">Department</label>
        <label left="440.0" top="75.0" width="15.0" height="15.0" textAlign="AlignHCenter">SC</label>
        <label left="450.0" top="75.0" width="60.0" height="15.0" textAlign="AlignRight">Quantity</label>
        <label left="510.0" top="75.0" width="65.0" height="15.0" textAlign="AlignRight">Date</label>
    </band>
    </pageHeader>
    <groups>
        <!-- groups are nested -->
        <group field="department" reverse="False">
            <groupHeader>
                <band height="20.0">
                    <label left="5.0" top="0.0" width="100.0" height="18.0" fontWeight="Bold" color="darkblue">Department:</label>
                    <field left="100.0" top="0.0" width="80" height="18.0" fontWeight="Bold" color="darkblue">department</field>
                    <line x1="5.0" y1="15.0" x2="250.0" y2="15.0" lineWidth="1.0" color="darkblue"/>
                </band>
            </groupHeader>
            <groupFooter>
                <band height="30.0" newPageAfter="True">
                    <label left="20.0" top="4.0" width="140.0" height="20" fontWeight="Bold" color="darkblue">Summary for:</label>
                    <field left="120.0" top="4.0" width="80" height="20.0" fontWeight="Bold" color="darkblue">department</field>
                    <label left="200.0" top="4.0" width="30.0" height="20" color="darkblue">Sum:</label>
                    <summary function="sum" left="230.0" top="4.0" width="40.0" height="16" color="darkblue">quantity</summary>
                    <label left="280.0" top="4.0" width="35.0" height="20.0" color="darkblue">Cnt:</label>
                    <summary function="count" left="315.0" top="4.0" width="35.0" height="20.0" color="darkblue">quantity</summary>
                    <label left="350.0" top="4.0" width="35.0" height="20.0" color="darkblue">Min:</label>
                    <summary function="min" left="385.0" top="4.0" width="35" height="20.0" color="darkblue">quantity</summary>
                    <label left="410.0" top="4.0" width="30.0" height="20" color="darkblue">Max:</label>
                    <summary function="max" left="440.0" top="4.0" width="40" height="20" color="darkblue">quantity</summary>
                    <label left="480.0" top="4.0" width="30.0" height="20" color="darkblue">Avg:</label>
                    <summary function="average" left="510.0" top="4.0" width="40" height="20" textAlign="AlignRight" format="{:06.2f}" color="darkblue">quantity</summary>
                    <line x1="20.0" y1="3.0" x2="550.0" y2="3.0" width="1.0" color="darkblue"/>
                </band>
            </groupFooter>
        </group>
        <group field="date" reverse="True">
            <groupHeader>
                <band height="20">
                    <label left="5.0" top="0.0" width="200.0" height="18" color="darkgreen">Date:</label>
                    <field left="60.0" top="0.0" width="80" height="18" color="darkgreen">date</field>
                    <line x1="5.0" y1="15.0" x2="250.0" y2="15.0" lineWidth="1.0" color="darkgreen"/>
                </band>
            </groupHeader>
            <groupFooter>
                <band height="30" isVisible = "True">
                    <label left="20.0" top="4.0" width="140.0" height="20" fontWeight="Bold" color="darkgreen">Summary for:</label>
                    <field left="120.0" top="4.0" width="80" height="20.0" fontWeight="Bold" color="darkgreen">date</field>
                    <label left="200.0" top="4.0" width="30.0" height="20" color="darkgreen">Sum:</label>
                    <summary function="sum" left="230.0" top="4.0" width="40.0" height="16" color="darkgreen">quantity</summary>
                    <label left="280.0" top="4.0" width="35.0" height="20.0" color="darkgreen">Cnt:</label>
                    <summary function="count" left="315.0" top="4.0" width="35.0" height="20.0" color="darkgreen">quantity</summary>
                    <label left="350.0" top="4.0" width="35.0" height="20.0" color="darkgreen">Min:</label>
                    <summary function="min" left="385.0" top="4.0" width="35" height="20.0" color="darkgreen">quantity</summary>
                    <label left="410.0" top="4.0" width="30.0" height="20" color="darkgreen">Max:</label>
                    <summary function="max" left="440.0" top="4.0" width="40" height="20" color="darkgreen">quantity</summary>
                    <label left="480.0" top="4.0" width="30.0" height="20" color="darkgreen">Avg:</label>
                    <summary function="average" left="510.0" top="4.0" width="40" height="20" textAlign="AlignRight" format="{:06.2f}" color="darkgreen">quantity</summary>
                    <line x1="20.0" y1="3.0" x2="550.0" y2="3.0" width="1.0" color="darkgreen"/>
                </band>
            </groupFooter>
        </group>
    </groups>
    <details>
        <band height="20.0" canGrow="True">
            <field left="5.0" top="3" width="100" height="20" fontName="Courier New" textAlign="AlignLeft">code</field>
            <field left="100.0" top="3" width="240.0" height="20.0" canGrow="True">description</field>
            <field left="340.0" top="3" width="100.0" height="20.0">department</field>
            <field left="440.0" top="3" width="15.0" height="20.0" textAlign="AlignHCenter">stock_control</field>
            <field left="450.0" top="3" width="60.0" height="20.0" textAlign="AlignRight">quantity</field>
            <field left="510.0" top="3" width="65.0" height="20.0" format="dd.MM.yy" textAlign="AlignRight">date</field>
        </band>
    </details>
    <reportFooter>
        <band height="60.0">
            <rectangle xRadius="3.0" yRadius="3.0" color="red" left="15.0" top="0.0" width="540.0" height="60.0"
            lineWidth="2.0" brushStyle="DiagCrossPattern" brushColor="lightgrey"/>
            <label left="10.0" top="4.0" width="550.0" height="16" fontItalic="True"
            fontWeight="Bold" textAlign="AlignHCenter">Report summaries of quantity field</label>
            <label left="20.0" top="24.0" width="50.0" height="20" fontWeight="Bold">Sum:</label>
            <summary function="sum" left="60.0" top="24.0" width="50.0" height="16" fontWeight="Bold">quantity</summary>
            <label left="110.0" top="24.0" width="50.0" height="20.0" fontWeight="Bold">Count:</label>
            <summary function="count" left="160.0" top="24.0" width="50" height="20.0" fontWeight="Bold">quantity</summary>
            <label left="210.0" top="24.0" width="50.0" height="20.0" fontWeight="Bold">Min:</label>
            <summary function="min" left="260.0" top="24.0" width="50" height="20.0" fontWeight="Bold">quantity</summary>
            <label left="310.0" top="24.0" width="50.0" height="20" fontWeight="Bold">Max:</label>
            <summary function="max" left="360.0" top="24.0" width="50" height="20" fontWeight="Bold">quantity</summary>
            <label left="410.0" top="24.0" width="50.0" height="20" fontWeight="Bold">Average:</label>
            <summary function="average" left="460.0" top="24.0" width="50" height="20" fontWeight="Bold" format="{:07.2f}">quantity</summary>
        </band>
    </reportFooter>
    <pageFooter>
        <band height="24.0">
            <rectangle xRadius="3.0" yRadius="3.0" left="0.0" top="0.0" width="585.0" height="18.0" brushStyle="Dense3Pattern" brushColor="lightgrey"/>
            <label left="5.0" top="3.0" width="60.0" height="16.0" textAlign="AlignLeft">Print date:</label>
            <special left="60.0" top="3.0" width="70.0" height="16.0" textAlign="AlignLeft">printDate</special>
            <label left="5.0" top="3.0" width="585.0" height="16.0" textAlign="AlignHCenter">Example report</label>
            <label left="520.0" top="3.0" width="50.0" height="16.0" textAlign="AlignLeft">Page:</label>
            <special left="570.0" top="3.0" width="10.0" height="16.0" textAlign="AlignLeft">pageNumber</special>
        </band>
    </pageFooter>
</report>
"""
    xml_string2 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0">
    <options>
        <documentName type="str">Test report Barcode</documentName>
        <orientation type="str">Portrait</orientation>
        <unit type="str">Point</unit>
        <pageSize type="str">A4</pageSize>
        <topMargin type="float">5.0</topMargin>
        <bottomMargin type="float">5.0</bottomMargin>
        <leftMargin type="float">5.0</leftMargin>
        <rightMargin type="float">5.0</rightMargin>
        <fontName type="str">Arial</fontName>
        <fontSize type="int">8</fontSize>
    </options>
    <columns><!-- Must have a columnNumber/fieldName for every column of the dataset -->
        <fieldName>code</fieldName>
        <fieldName>description</fieldName>
        <fieldName>department</fieldName>
        <fieldName>stock_control</fieldName>
        <fieldName>quantity</fieldName>
        <fieldName>date</fieldName>
    </columns>
    <parameters>
        <parameter type="bool" id="booleanExample" default="True">Boolena parameter example</parameter>
        <parameter type="int" id="intExample" default="1" items="1:a|5:b|7:c|22:d|29:e">Integer parameter example</parameter>
        <parameter type="float" id="floatExample" default="123456.789" items="1.2:a|1.3:b|2.1:c">Float parameter example</parameter>
        <parameter type="date" id="dateExample" default="20180101" items="20180101:a|20180201:b|20171231:c|20160630:d">Date (QDate) parameter example</parameter>
        <parameter type="str" id="stringExample">String parameter example</parameter>
        <parameter type="str" id="stringSecondExample" items="First:First|Second:Second|Tirth:Tirth">Second string parameter example</parameter>
    </parameters>
    <sorting>
        <sort field="department" reverse="False"/>
        <sort field="date" reverse="False"/>
        <sort field="quantity" reverse="True"/>
    </sorting>
    <pageBackground>
        <image left="0.0" top="0.0" width="590.0" height="837.0" aspectRatio="KeepAspectRatio"
        opacity="0.3">
        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
        AElFTkSuQmCC</image>
    </pageBackground>
    <pageHeader>
        <band height="120.0">
            <label left="0.0" top="0.0" width="585.0" height="50.0" fontName="Archon Code 39 Barcode" fontSize="36" textAlign="AlignLeft" barcodeType="Code39">ABCD12345</label>
            <label left="0.0" top="0.0" width="585.0" height="50.0" fontName="Code 128" fontSize="36" textAlign="AlignRight" barcodeType="Code128">ABCD12345</label>
            <label left="0.0" top="50.0" width="585.0" height="40.0" color="blue" fontName="Impact" fontWeight="Bold" fontItalic="True" fontSize="24" textAlign="AlignHCenter">Test report Barcode</label>
            <label left="0.0" top="90.0" width="28.0" height="15.0" fontWeight="Bold">R.N.</label>
            <label left="30.0" top="90.0" width="110.0" height="15.0" fontWeight="Bold">Code128</label>
            <label left="140.0" top="90.0" width="110.0" height="15.0" fontWeight="Bold">Code39</label>
            <label left="250.0" top="90.0" width="60.0" height="15.0" fontWeight="Bold">Code</label>
            <label left="310.0" top="90.0" width="150.0" height="15.0" fontWeight="Bold">Description</label>
            <label left="460.0" top="90.0" width="60.0" height="15.0" textAlign="AlignRight" fontWeight="Bold">Quantity</label>
            <label left="525.0" top="90.0" width="60.0" height="15.0" textAlign="AlignRight" fontWeight="Bold">Date</label>
            <line x1="0.0" y1="110.0" x2="585.0" y2="110.0" lineWidth="2.0"/>
        </band>
    </pageHeader>
    <details>
        <band height="35.0" canGrow="True">
            <special left="2.0" top="3.0" width="28.0" height="30.0" textAlign="AlignLeft" color="red" format="{:0>3d}">recordNumber</special>
            <field left="30.0" top="3" width="110" height="30.0" fontName="Code 128" fontSize="20" textAlign="AlignLeft" barcodeType="Code128">code</field>
            <field left="140.0" top="3" width="110" height="30.0" fontName="Archon Code 39 Barcode" fontSize="20" textAlign="AlignLeft" barcodeType="Code39">code</field>
            <field left="250.0" top="3" width="60" height="30.0">code</field>
            <field left="310.0" top="3" width="150.0" height="30.0" canGrow="True">description</field>
            <field left="460.0" top="3" width="60.0" height="30.0" textAlign="AlignRight">quantity</field>
            <field left="525.0" top="3" width="60.0" height="30.0" textAlign="AlignRight">date</field>
        </band>
    </details>
    <pageFooter>
        <band height="45.0">
            <line x1="0.0" y1="0.0" x2="585.0" y2="0.0" width="1.0" style="SolidLine"/>
            <label left="240.0" top="4.0" width="50.0" height="16.0">Page:</label>
            <special left="0.0" top="4.0" width="550.0" height="16.0" textAlign="AlignHCenter">pageNumber</special>
        </band>
    </pageFooter>
</report>
"""
    xml_string3 = """<?xml version="1.0" encoding="UTF-8"?>
<report version="1.0">
    <options>
        <documentName type="str">Test report in millimeters</documentName>
        <orientation type="str">Portrait</orientation>
        <unit type="str">Millimeter</unit>
        <pageSize type="str">A4</pageSize>
        <topMargin type="float">0.0</topMargin>
        <bottomMargin type="float">0.0</bottomMargin>
        <leftMargin type="float">0.0</leftMargin>
        <rightMargin type="float">0.0</rightMargin>
        <fontName type="str">Arial</fontName>
        <fontSize type="int">4</fontSize>
    </options>
    <columns>
        <fieldName>code</fieldName>
        <fieldName>description</fieldName>
        <fieldName>department</fieldName>
        <fieldName>stock_control</fieldName>
        <fieldName>quantity</fieldName>
        <fieldName>date</fieldName>
    </columns>
    <sorting>
        <sort field="department" reverse="False"/>
        <sort field="date" reverse="False"/>
        <sort field="quantity" reverse="True"/>
    </sorting>
    <pageBackground>
        <rectangle color="red" left="0" top="0" width="210" height="297" lineWidth="1"/>
    </pageBackground>
    <pageHeader>
        <band height="30">
            <label left="0" top="0" width="210" height="20" color="blue"
            fontName="Impact" fontWeight="Bold" fontItalic="True" fontSize="8"
            textAlign="AlignHCenter">Test report in millimeters</label>
            <label left="2" top="20" width="13" height="8" fontSize="4" fontWeight="Bold">R.N.</label>
            <label left="15" top="20" width="30" height="8" fontSize="4" fontWeight="Bold">Code</label>
            <label left="45" top="20" width="65" height="8" fontSize="4" fontWeight="Bold">Description</label>
            <label left="110" top="20" width="30" height="8" fontSize="4" fontWeight="Bold">Department</label>
            <label left="140" top="20" width="10" height="8" fontSize="4" textAlign="AlignHCenter" fontWeight="Bold">S.C.</label>
            <label left="150" top="20" width="25" height="8" fontSize="4" textAlign="AlignRight" fontWeight="Bold">Quantity</label>
            <label left="175" top="20" width="30" height="8" fontSize="4" textAlign="AlignRight" fontWeight="Bold">Date</label>
            <line x1="0" y1="26" x2="210" y2="26" lineWidth="1.0"/> 
        </band>
    </pageHeader>
    <details>
        <band height="8" canGrow="True">
            <special left="2" top="2" width="13" height="6" fontSize="3" textAlign="AlignLeft" color="green" format="{:0>3d}">recordNumber</special>
            <field left="15" top="2" width="30" height="6" fontSize="3" textAlign="AlignLeft">code</field>
            <field left="45" top="2" width="65" height="6" fontSize="3" canGrow="True">description</field>
            <field left="110" top="2" width="30" height="6" fontSize="3">department</field>
            <field left="140" top="2" width="10" height="6" fontSize="3" textAlign="AlignHCenter">stock_control</field>
            <field left="150" top="2" width="25" height="6" fontSize="3" format="" textAlign="AlignRight">quantity</field>
            <field left="175" top="2" width="30" height="6" fontSize="3" format="" textAlign="AlignRight">date</field>
        </band>
    </details>
    <pageFooter>
        <band height="20.0">
            <line x1="0" y1="0" x2="210" y2="0" lineWidth="0.5" style="SolidLine"/>
            <special left="0" top="4.0" width="210" height="20" textAlign="AlignHCenter">pageNumber</special>
        </band>
    </pageFooter>
</report>
"""
    for i in (
              xml_string0,
              xml_string1,
              xml_string2,
              xml_string3,
                 ):
        r = Report(i)
        r.setData([
                ('AAAAA', 'description 1 that is very long so it could be wrapped', 'Research', True, 22, QDate(2018, 1, 1)),
                ('BBBBB', 'description 2', 'Production', True, 25, QDate(2018, 2, 2)),
                ('CCCCC', 'description 3', 'Accounting', False, 1, QDate(2018, 3, 3)),
                ('DDDDD', 'description 4', 'Research', False, 23, QDate(2018, 1, 2)),
                ('EEEEE', 'description 5', 'Production', True, 25, QDate(2018, 2, 2)),
                ('FFFFF', 'description 6', 'Accounting', True, 10, QDate(2018, 3, 3)),
                ('GGGGG', 'description 7', 'Research', True, 23, QDate(2018, 1, 3)),
                ('HHHHH', 'description 8', 'Production', False, 25, QDate(2018, 2, 2)),
                ('IIIII', 'description 9', 'Accounting', False, 0, QDate(2018, 3, 3)),
                ('JJJJJ', 'description 10', 'Research', True, 23, QDate(2018, 1, 4)),
                ('KKKKK', 'description 11', 'Production', True, 25, QDate(2018, 2, 3)),
                ('LLLLL', 'description 12', 'Accounting', True, 2250, QDate(2018, 3, 3)),
                ('MMMMM', 'description 13', 'Research', True, 11, QDate(2018, 1, 5)),
                ('NNNNN', 'description 14', 'Production', False, 25, QDate(2018, 2, 2)),
                ('OOOOO', 'description 15', 'Accounting', False, 0, QDate(2018, 3, 3)),
                ('PPPPP', 'description 16', 'Research', True, 23, QDate(2018, 2, 1)),
                ('QQQQQ', 'description 17', 'Production', True, 25, QDate(2018, 2, 3)),
                ('RRRRR', 'description 18', 'Accounting', False, 110, QDate(2018, 3, 3)),
                ('SSSSS', 'description 19', 'Research', True, 11, QDate(2018, 1, 1)),
                ('TTTTT', 'description 20', 'Production', True, 25, QDate(2018, 2, 2)),
                ('UUUUU', 'description 21', 'Accounting', False, 0, QDate(2018, 3, 3)),
                ('VVVVV', 'description 22', 'Research', True, 23, QDate(2018, 1, 1)),
                ('WWWWW', 'description 23', 'Production', True, 25, QDate(2018, 2, 2)),
                ('XXXXX', 'description 24 description - description - accounting description | very large description only for testing', 'Accounting', False, 7, QDate(2018, 3, 3)),
                ('YYYYY', 'description 25', 'Research', True, 23, QDate(2018, 1, 1)),
                ('ZZZZZ', 'description 26', 'Production', True, 25, QDate(2018, 2, 2)),
                ('11111', 'description 27', 'Accounting', False, 0, QDate(2018, 3, 3)),
                ('22222', 'description 28', 'Research', True, 23, QDate(2018, 1, 1)),
                ('33333', 'description 29', 'Production', True, 25, QDate(2018, 2, 2)),
                ('44444', 'description 30', 'Accounting', False, 0, QDate(2018, 3, 3)),
                ('55555', 'description 31', 'Research', True, 33, QDate(2018, 1, 1)),
                ('66666', 'description 32', 'Production', True, 9991, QDate(2018, 2, 2)),
                ('77777', 'description 33', 'Accounting', False, 0, QDate(2018, 3, 3)),
                ('88888', 'description 34', 'Research', True, 23, QDate(2018, 1, 1)),
                ('99999', 'description 35', 'Production', True, 26, QDate(2018, 2, 2)),
                ('00000', 'description 36', 'Production', True, 26, QDate(2018, 2, 2)),
                ('A', 'description 37', 'Production', True, 1225, QDate(2018, 2, 2)),
                ('AA', 'description 38', 'Production', True, 26, QDate(2018, 2, 2)),
                ('AAA', 'description 39', 'Production', True, 27, QDate(2018, 2, 2)),
                ('AAAA', 'description 40 go to 2 lines description *', 'Production', True, 28, QDate(2018, 2, 2)),
                ('AAAAA', 'description 41', 'Production', True, 29, QDate(2018, 2, 2)),
                ('AAAAAA', 'description 42', 'Production', True, 30, QDate(2018, 2, 2)),
                ('AAAAAAA', 'description 43', 'Production', True, 31, QDate(2018, 2, 2)),
                ('AAAAAAAA', 'description 44', 'Accounting', False, 0, QDate(2018, 3, 3))])
        if i == xml_string0:
            r.setData([('', 'One line recordset test', 'Accounting', False, 0, QDate(2018, 3, 3))])
            r.setData([(None,)])  # test empty dataset
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        r.generate()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()
        # print preview
        dialog = QPrintPreviewDialog()
        dialog.setWindowFlags(Qt.WindowType.Dialog|Qt.WindowType.WindowMinMaxButtonsHint|Qt.WindowType.WindowCloseButtonHint)
        dialog.setWindowTitle("Print preview")
        dialog.paintRequested.connect(r.print)
        dialog.exec()
