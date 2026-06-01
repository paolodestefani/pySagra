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

"""Syntax Highlighter module

This module contains syntax highlighter classes for different languages

"""

# Standard library
import re

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtGui import QTextCharFormat
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QTextDocument
from PySide6.QtGui import QFont
from PySide6.QtGui import QGuiApplication



#
# Syntax Highligter for XML source
#

class XMLHighlighter(QSyntaxHighlighter):

    def __init__(self, parent: QObject) -> None:
        super(XMLHighlighter, self).__init__(parent)
        self._mappings = {}
        # multiline comments
        self.commentFormat = QTextCharFormat()
        self.commentStartExpression = re.compile(r"<!--")
        self.commentEndExpression = re.compile(r"-->")
        # color configuration
        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            # Dark theme
            self.commentFormat.setForeground(QColorConstants.Svg.lime)
            fmt_element = self._create_format(QColorConstants.Svg.deepskyblue)
            fmt_attribute = self._create_format(QColorConstants.Svg.tomato)
            fmt_value = self._create_format(QColorConstants.Svg.violet)
            fmt_text = self._create_format(QColorConstants.Svg.lightcyan, bold=True)
            fmt_entity = self._create_format(QColorConstants.Svg.orange)
        else:
            # Light theme
            self.commentFormat.setForeground(Qt.GlobalColor.darkGreen)
            fmt_element = self._create_format(Qt.GlobalColor.blue)
            fmt_attribute = self._create_format(Qt.GlobalColor.red)
            fmt_value = self._create_format(Qt.GlobalColor.darkMagenta)
            fmt_text = self._create_format(Qt.GlobalColor.black, bold=True)
            fmt_entity = self._create_format(Qt.GlobalColor.darkYellow)
        # Ordered mapping to avoid overwrite conflicts
        self._mappings = {
            r">[^\n]*<": fmt_text,
            r"<[\s]*[/]?[\s]*([^\n]\w*)(?=[\s/>])": fmt_element,
            r"\w+(?=\=)": fmt_attribute,
            r"\"[^\n\"]+\"(?=[\s/>])": fmt_value,
            r"&[a-zA-Z0-9#]+;": fmt_entity  # recognizes &amp;, &lt;, &#123;, ecc.
        }

    def _create_format(self, color, bold=False):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        return fmt

    def highlightBlock(self, text: str) -> None:
        # 1. set standard rules (tag, attributes, strings, entity)
        for pattern, format in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format)
        # 2. special rules for multiline comments overwrite anything else
        self.setCurrentBlockState(0)
        start_index = 0
        # If the previous block ended inside a comment, we look for the end in this block.
        if self.previousBlockState() == 1:
            end_match = self.commentEndExpression.search(text)
            if not end_match:
                # The comment continues across the current line
                self.setCurrentBlockState(1)
                self.setFormat(0, len(text), self.commentFormat)
                return
            else:
                # The comment ends on this line
                end_index = end_match.end()
                self.setFormat(0, end_index, self.commentFormat)
                start_index = end_index
        # Search for new comments starting on the current line
        while start_index < len(text):
            start_match = self.commentStartExpression.search(text, start_index)
            if not start_match:
                break
            start_pos = start_match.start()
            end_match = self.commentEndExpression.search(text, start_pos)
            if not end_match:
                # The comment opens but does not close on this line
                self.setCurrentBlockState(1)
                self.setFormat(start_pos, len(text) - start_pos, self.commentFormat)
                break
            else:
                # The comment opens and closes on the same line
                end_pos = end_match.end()
                self.setFormat(start_pos, end_pos - start_pos, self.commentFormat)
                start_index = end_pos



#
# Syntax Highligter for python script
#

class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language"""
    
    keywords = [
        'and', 'assert', 'break', 'case','class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'match', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    operators = [
        r'=', '==', '!=', '<', '<=', '>', '>=',
        r'\+', r'-', r'\*', r'/', r'//', r'\%', r'\*\*',
        r'\+=', r'-=', r'\*=', r'/=', r'\%=',
        r'\^', r'\|', r'\&', r'\~', '>>', '<<',
    ]

    braces = [
        r'\{', r'\}', r'\(', r'\)', r'\[', r'\]',
    ]

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)
        def format(color: QBrush|QColor, style: str = '') -> QTextCharFormat:
            """Return a QTextCharFormat with the given attributes."""
            tcf = QTextCharFormat()
            tcf.setForeground(color)
            if 'bold' in style:
                tcf.setFontWeight(QFont.Weight.Bold)
            if 'italic' in style:
                tcf.setFontItalic(True)
            return tcf
        
        self._mappings = {}
        # Specific mapping for code inside f-strings/t-strings
        self._inner_mappings = {}

        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark:
            styles =  {
                        'keyword': format(QColorConstants.Svg.deepskyblue),
                        'operator': format(QColorConstants.Svg.tomato),
                        'brace': format(QColorConstants.Svg.lightgray),
                        'defclass': format(QColorConstants.Svg.royalblue, 'bold'),
                        'string': format(QColorConstants.Svg.violet),
                        'string2': format(QColorConstants.Svg.violet),       
                        'comment': format(QColorConstants.Svg.lime, 'italic'),
                        'self': format(QColorConstants.Svg.slateblue, 'italic'),
                        'numbers': format(QColorConstants.Svg.white),
                        'decorator': format(QColorConstants.Svg.gold),
                        'interpolation_brace': format(QColorConstants.Svg.orange, 'bold'),     # color for  { and }
                    }
        else:
            styles = {
                        'keyword': format(QColorConstants.Svg.blue),
                        'operator': format(QColorConstants.Svg.red),
                        'brace': format(QColorConstants.Svg.darkgray),
                        'defclass': format(QColorConstants.Svg.black, 'bold'),
                        'string': format(QColorConstants.Svg.magenta),
                        'string2': format(QColorConstants.Svg.darkmagenta), 
                        'comment': format(QColorConstants.Svg.darkgreen, 'italic'),
                        'self': format(QColorConstants.Svg.black, 'italic'),
                        'numbers': format(QColorConstants.Svg.brown),
                        'decorator': format(QColorConstants.Svg.darkcyan),
                        'interpolation_brace': format(QColorConstants.Svg.darkorange, 'bold'), # color for  { and }
                    }

        self.multilineStringFormat = styles['string2']
        self.braceFormat = styles['interpolation_brace']
        
        # Find expressions between braces that do not contain other braces nested on the line.
        self.interpolationExpression = re.compile(r"\{([^{}\n]+)\}")
        
        self.trippleDoubleExpression = re.compile(r'[fFrRbBuUtT]?"""')
        self.trippleSingleExpression = re.compile(r"[fFrRbBuUtT]?'''")

        # 1. Configuring standard global rules
        self._mappings.update({r'\b%s\b' % w: styles['keyword'] for w in PythonHighlighter.keywords})
        self._mappings.update({r'%s' % o: styles['operator'] for o in PythonHighlighter.operators})
        self._mappings.update({r'%s' % b: styles['brace'] for b in PythonHighlighter.braces})
        self._mappings.update({r'\bself\b': styles['self']})
        self._mappings.update({r'[fFrRbBuUtT]?"[^"\\]*(\\.[^"\\]*)*"': styles['string']})
        self._mappings.update({r"[fFrRbBuUtT]?'[^'\\]*(\\.[^'\\]*)*'": styles['string']})
        self._mappings.update({r'@[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*': styles['decorator']})
        self._mappings.update({r'\bdef\b\s*(\w+)': styles['defclass']})
        self._mappings.update({r'\bclass\b\s*(\w+)': styles['defclass']})
        self._mappings.update({r'#[^\n]*': styles['comment']})
        
        # Numbers
        num_patterns = [
            r'\b[+-]?[0-9]+[lL]?\b',
            r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b',
            r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b'
        ]
        for p in num_patterns:
            self._mappings.update({p: styles['numbers']})

        # 2. Configuring internal rules for code inside braces {...}
        # We include keywords, numbers, operators, and self (we exclude comments and external strings)
        self._inner_mappings.update({r'\b%s\b' % w: styles['keyword'] for w in PythonHighlighter.keywords})
        self._inner_mappings.update({r'\bself\b': styles['self']})
        self._inner_mappings.update({r'%s' % o: styles['operator'] for o in PythonHighlighter.operators})
        for p in num_patterns:
            self._inner_mappings.update({p: styles['numbers']})

    def highlightBlock(self, text: str) -> None:
        # STEP 1: Apply standard syntax rules line by line
        for pattern, format_style in self._mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format_style)

        # STEP 2: Special handling for multiline strings
        self.setCurrentBlockState(0)
        start_index = 0
        
        if self.previousBlockState() == 1:
            start_index = self._process_multiline_end(text, self.trippleDoubleExpression, 1)
        elif self.previousBlockState() == 2:
            start_index = self._process_multiline_end(text, self.trippleSingleExpression, 2)

        if self.currentBlockState() == 0:
            while start_index < len(text):
                match_double = self.trippleDoubleExpression.search(text, start_index)
                match_single = self.trippleSingleExpression.search(text, start_index)
                
                pos_double = match_double.start() if match_double else -1
                pos_single = match_single.start() if match_single else -1
                
                if pos_double == -1 and pos_single == -1:
                    break
                    
                if pos_single == -1 or (pos_double != -1 and pos_double < pos_single):
                    start_index = self._process_multiline_start(text, match_double, self.trippleDoubleExpression, 1)
                else:
                    start_index = self._process_multiline_start(text, match_single, self.trippleSingleExpression, 2)
                    
                if self.currentBlockState() != 0:
                    break

        # STEP 3: Parsing and re-highlighting the code inside the curly braces of the f/t-strings
        comment_index = text.find('#')
        for match in self.interpolationExpression.finditer(text):
            start, end = match.span()
            
            # Skip if the brace occurs after a standard '#' comment.
            if comment_index != -1 and start > comment_index:
                continue
                
            # 1. Color the outer brackets { and } orange.
            self.setFormat(start, 1, self.braceFormat)
            self.setFormat(end - 1, 1, self.braceFormat)
            
            # 2. Extract only the internal code (excluding the { and } characters)
            inner_code = match.group(1)
            inner_start_pos = start + 1
            
            # Temporarily resets the background/text to neutral for the internal code
            # (Removes the surrounding string color before re-parsing it)
            neutral_format = QTextCharFormat() 
            self.setFormat(inner_start_pos, len(inner_code), neutral_format)
            
            # 3. Selectively apply Python rules on the extracted internal code
            for pattern, format_style in self._inner_mappings.items():
                for inner_match in re.finditer(pattern, inner_code):
                    i_start, i_end = inner_match.span()
                    # Calculates the actual offset from the total document row
                    real_start = inner_start_pos + i_start
                    self.setFormat(real_start, i_end - i_start, format_style)

    def _process_multiline_start(self, text: str, match: re.Match, expression: re.Pattern, state: int) -> int:
        start_pos = match.start()
        match_len = match.end() - start_pos
        
        end_match = expression.search(text, start_pos + match_len)
        if not end_match:
            self.setCurrentBlockState(state)
            self.setFormat(start_pos, len(text) - start_pos, self.multilineStringFormat)
            return len(text)
        else:
            end_pos = end_match.end()
            self.setFormat(start_pos, end_pos - start_pos, self.multilineStringFormat)
            return end_pos
    
    def _process_multiline_end(self, text: str, expression: re.Pattern, state: int) -> int:
        end_match = expression.search(text)
        if not end_match:
            self.setCurrentBlockState(state)
            self.setFormat(0, len(text), self.multilineStringFormat)
            return len(text)
        else:
            end_index = end_match.end()
            self.setFormat(0, end_index, self.multilineStringFormat)
            return end_index
