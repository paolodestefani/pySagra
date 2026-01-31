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

# Standard library
import re

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtGui import QTextCharFormat
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QFont
from PySide6.QtGui import QGuiApplication


#
# Syntax Highligter for XML source
#

class XMLHighlighter(QSyntaxHighlighter):

    def __init__(self, parent: QObject) -> None:
        super(XMLHighlighter, self).__init__(parent)
        self._mappings = {}
        # singleline/multiline comment
        #self.commentStartExpression = QRegularExpression("<!--")
        #self.commentEndExpression = QRegularExpression("-->")
        #self.commentFormat = QTextCharFormat()
        # colors
        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            # comment
            xmlCommentFormat = QTextCharFormat()
            xmlCommentFormat.setForeground(QColorConstants.Svg.lime)
            self._mappings.update({r"<!--[\s\S\n]*?-->": xmlCommentFormat})
            # element <Text> </Text>
            xmlElementFormat = QTextCharFormat()
            xmlElementFormat.setForeground(QColorConstants.Svg.deepskyblue)
            # xmlElementFormat.setFontWeight(QFont.Bold)
            self._mappings.update({"<[\\s]*[/]?[\\s]*([^\\n]\\w*)(?=[\\s/>])": xmlElementFormat})
            # attribute < Text= >
            xmlAttributeFormat = QTextCharFormat()
            xmlAttributeFormat.setForeground(QColorConstants.Svg.tomato)
            self._mappings.update({"\\w+(?=\\=)": xmlAttributeFormat})
            # attribute value < text=" " >
            xmlValueAttributeFormat = QTextCharFormat()
            xmlValueAttributeFormat.setForeground(QColorConstants.Svg.violet)
            self._mappings.update({"\"[^\\n\"]+\"(?=[\\s/>])": xmlValueAttributeFormat})
            # element value inline >text<
            xmlValueElementFormat = QTextCharFormat()
            xmlValueElementFormat.setForeground(QColorConstants.Svg.lightcyan)
            xmlValueElementFormat.setFontWeight(QFont.Weight.Bold)
            self._mappings.update({">[^\n]*<": xmlValueElementFormat})
            # singleline/multiline comment
            #self._mappings.update({QColorConstants.Svg.lime)
        else:
            # comment
            xmlCommentFormat = QTextCharFormat()
            xmlCommentFormat.setForeground(Qt.GlobalColor.darkGreen)
            self._mappings.update({r"<!--[\s\S\n]*?-->": xmlCommentFormat})
            # element <Text> </Text>
            xmlElementFormat = QTextCharFormat()
            xmlElementFormat.setForeground(Qt.GlobalColor.blue)
            # xmlElementFormat.setFontWeight(QFont.Bold)
            self._mappings.update({"<[\\s]*[/]?[\\s]*([^\\n]\\w*)(?=[\\s/>])": xmlElementFormat})
            # attribute < Text= >
            xmlAttributeFormat = QTextCharFormat()
            xmlAttributeFormat.setForeground(Qt.GlobalColor.red)
            self._mappings.update({"\\w+(?=\\=)": xmlAttributeFormat})
            # attribute value < text=" " >
            xmlValueAttributeFormat = QTextCharFormat()
            xmlValueAttributeFormat.setForeground(Qt.GlobalColor.darkMagenta)
            self._mappings.update({"\"[^\\n\"]+\"(?=[\\s/>])": xmlValueAttributeFormat})
            # element value inline >text<
            xmlValueElementFormat = QTextCharFormat()
            xmlValueElementFormat.setForeground(Qt.GlobalColor.black)
            xmlValueElementFormat.setFontWeight(QFont.Weight.Bold)
            self._mappings.update({">[^\n]*<": xmlValueElementFormat})
            # singleline/multiline comment
            #self.commentFormat.setForeground(Qt.darkGreen)

    def highlightBlock(self, text: str) -> None:
        for pattern, format in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format)       


#
# Syntax Highligter for python script
#

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    #_color = QColor()
    #_color.setNamedColor(color)

    tcf = QTextCharFormat()
    tcf.setForeground(color)
    if 'bold' in style:
        tcf.setFontWeight(QFont.Weight.Bold)
    if 'italic' in style:
        tcf.setFontItalic(True)
    return tcf


# Syntax styles that can be shared by all languages
STYLES = {
    'keyword': format(QColorConstants.Svg.blue),
    'operator': format(QColorConstants.Svg.red),
    'brace': format(QColorConstants.Svg.darkgray),
    'defclass': format(QColorConstants.Svg.black, 'bold'),
    'string': format(QColorConstants.Svg.magenta),
    'string2': format(QColorConstants.Svg.darkmagenta),
    'comment': format(QColorConstants.Svg.darkgreen, 'italic'),
    'self': format(QColorConstants.Svg.black, 'italic'),
    'numbers': format(QColorConstants.Svg.brown),
}

STYLESDM = {
    'keyword': format(QColorConstants.Svg.deepskyblue),
    'operator': format(QColorConstants.Svg.tomato),
    'brace': format(QColorConstants.Svg.lightgray),
    'defclass': format(QColorConstants.Svg.royalblue, 'bold'),
    'string': format(QColorConstants.Svg.violet),
    'string2': format(QColorConstants.Svg.violet),
    'comment': format(QColorConstants.Svg.lime, 'italic'),
    'self': format(QColorConstants.Svg.slateblue, 'italic'),
    'numbers': format(QColorConstants.Svg.white),
}

class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'case','class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'match', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        r'=',
        # Comparison
        r'==', r'!=', r'<', r'<=', r'>', r'>=',
        # Arithmetic
        r'\+', r'-', r'\*', r'/', r'//', r'\%', r'\*\*',
        # In-place
        r'\+=', r'-=', r'\*=', r'/=', r'\%=',
        # Bitwise
        r'\^', r'\|', r'\&', r'\~', r'>>', r'<<',
    ]

    # Python braces
    braces = [
        r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
    ]

    def __init__(self, document):
        super().__init__(document)
        
        self._mappings = {}

        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            styles = STYLESDM
        else:
            styles = STYLES

        # Keyword, operator, and brace rules
        self._mappings.update({r'\b%s\b' % w: styles['keyword']
            for w in PythonHighlighter.keywords})
        self._mappings.update({r'%s' % o: styles['operator']
            for o in PythonHighlighter.operators})
        self._mappings.update({r'%s' % b: styles['brace']
            for b in PythonHighlighter.braces})

        # All other rules
        # 'self'
        self._mappings.update({r'\bself\b': styles['self']})
        # Double-quoted string, possibly containing escape sequences
        self._mappings.update({r'"[^"\\]*(\\.[^"\\]*)*"': styles['string']})
        # Single-quoted string, possibly containing escape sequences
        self._mappings.update({r"'[^'\\]*(\\.[^'\\]*)*'": styles['string']})
        # 'def' followed by an identifier
        self._mappings.update({r'\bdef\b\s*(\w+)': styles['defclass']})
        # 'class' followed by an identifier
        self._mappings.update({r'\bclass\b\s*(\w+)': styles['defclass']})
        # From '#' until a newline
        self._mappings.update({r'#[^\n]*': styles['comment']})
        # Numeric literals
        self._mappings.update({r'\b[+-]?[0-9]+[lL]?\b': styles['numbers']})
        self._mappings.update({r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b': styles['numbers']})
        self._mappings.update({r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b': styles['numbers']})

    def highlightBlock(self, text):
        for pattern, format in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format)
