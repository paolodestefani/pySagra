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

"""Scripting

Python scripting management

"""

# standard library
import zipfile
import logging
import re
from typing import cast

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QDirIterator
from PySide6.QtGui import QAction
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetricsF
from PySide6.QtGui import QBrush
from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtGui import QTextCharFormat
from PySide6.QtGui import QTextDocument
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Database.Scripting import load_script
from App.Database.Scripting import get_all_scripts
from App.Database.Company import company_list
from App.Database.Models import ScriptingIndexModel
from App.Database.Models import ScriptingModel
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import HideTextDelegate
from App.Ui.ScriptingWidget import Ui_ScriptingWidget
from App.Core.L10n import _tr
from App.Core.L10n import langCountry
from App.Core.L10n import langCountryFlags


# logger
logger = logging.getLogger(__name__)


SCRIPTABLE = {'CashDeskForm': ['__init__',
                                 'new',
                                 'save',
                                 'delete',
                                 'reload'],

              'PrinterForm': ['__init__',
                               'new',
                               'save',
                               'delete',
                               'reload',
                               'add',
                               'remove',
                               'print'],

              'DepartmentForm': ['__init__',
                                  'new',
                                  'save',
                                  'delete',
                                  'reload',],

              'SeatMapForm': ['__init__',
                             'new',
                             'save',
                             'delete',
                             'deleteAll',
                             'reload',
                             'print',
                             'generateTableNumbers'],

              'ItemForm': ['__init__',
                            'new',
                            'save',
                            'delete',
                            'reload',
                            'copyVariants',
                            'print'],
                            
              'PriceListForm': ['__init__',
                                'new',
                                'save',
                                'delete',
                                'reload',
                                'add',
                                'remove',
                                'duplicate',
                                'print'],

              'EventForm': ['__init__',
                             'new',
                             'save',
                             'delete',
                             'reload',
                             'upload',
                             'download',
                             'removeImage',
                             'print'],
              'OrderForm': ['__init__',
                             'new',
                             'save',
                             'delete',
                             'reload',
                             'print',
                             'reprint'],
              'OrderNumberingForm': ['__init__',
                                     'new',
                                     'save',
                                     'delete',
                                     'reload'],

              'SettingsDialog': ['__init__',
                                 'apply',
                                 'accept']}

(ID, CLASS, METHOD, TRIGGER, DESCRIPTION, NOTE,
 COMPANY, ACTIVE, SCRIPT, 
 USER_INS, DATE_INS, USER_UPD, DATE_UPD) = range(13)

def runOptions() -> list[tuple[str, str]]:
    return [('B', _tr('script', 'Before')),
            ('I', _tr('script', 'Instead')),
            ('A', _tr('script', 'After'))]


def scripting(action: QAction, checked: bool = False) -> None:
    "Show/Edit python script"
    logging.info('Starting scripting Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    sw = ScriptingForm(mw, title, auth)
    sw.applySortFilter()
    mw.addTab(title, sw)
    logging.info('Scripting Form added to main window')


class ScriptingForm(FormIndexManager):
    "Form for python scripting management"

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = ScriptingModel(self)
        idxModel = ScriptingIndexModel(self)
        self.setModel(model, idxModel)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, False, False)
        self.ui = Ui_ScriptingWidget()
        self.ui.setupUi(self)
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('ScriptingIndex')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        # fill classcombobox, methodcombobox and companycombobox
        self.ui.comboBoxClass.currentIndexChanged.connect(self.fillMethods)
        self.ui.comboBoxClass.addItems(list(SCRIPTABLE.keys()))
        self.ui.comboBoxCompany.setItemList(company_list())
        # field mapping
        self.mapper.addMapping(self.ui.comboBoxClass, CLASS)
        self.mapper.addMapping(self.ui.comboBoxMethod, METHOD)
        self.ui.comboBoxTrigger.setItemList(runOptions())
        self.mapper.addMapping(self.ui.comboBoxTrigger, TRIGGER)#, b"modelDataStr")
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        self.mapper.addMapping(self.ui.plainTextEditNote, NOTE)
        self.mapper.addMapping(self.ui.comboBoxCompany, COMPANY, b"modelDataInt")#, b"modelDataStr")
        self.mapper.addMapping(self.ui.checkBoxActive, ACTIVE)
        self.mapper.addMapping(self.ui.textEditScript, SCRIPT)#, b"plainText")
        # set font
        st = QSettings()
        self.editorFont: QFont = cast(QFont, st.value("Scripting/EditorFont", QFont('Courier', 8), type=QFont))
        self.ui.textEditScript.setFont(self.editorFont)
        self.ui.fontComboBox.setCurrentFont(self.editorFont)
        self.ui.spinBoxFontSize.setValue(self.editorFont.pointSize())
        # set tab spaces
        tabStop = 4
        metrics = QFontMetricsF(self.editorFont)
        self.ui.textEditScript.setTabStopDistance(tabStop * metrics.maxWidth())
        # syntax highlighting
        self.highlighter = PythonHighlighter(self.ui.textEditScript.document())
        # signal/slot
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownloadAll.clicked.connect(self.downloadAll)
        self.ui.pushButtonUploadAll.clicked.connect(self.uploadAll)
        self.ui.fontComboBox.currentFontChanged.connect(self.changeFont)
        self.ui.spinBoxFontSize.valueChanged.connect(self.changeFontSize)

    def fillMethods(self, text: str) -> None:
        "fill available methods"
        self.ui.comboBoxMethod.clear()
        self.ui.comboBoxMethod.addItems(SCRIPTABLE.get(self.ui.comboBoxClass.currentText()) or [])  # on New text is empty

    def new(self) -> None:
        "New script"
        super().new()
        self.ui.comboBoxClass.setCurrentIndex(-1)
        self.ui.comboBoxTrigger.setCurrentIndex(-1)
        self.ui.comboBoxClass.setFocus()

    def save(self) -> None:
        "Save current script"
        super().save()
        if (self.ui.comboBoxMethod.currentText() == '__init__' and
                self.ui.comboBoxTrigger.currentData() == 'B'):
            msg = _tr('Scripting', "Warning: script linked to an __init__ "
                      "method will be executed only if trigger is set to 'after'")
            QMessageBox.warning(self,
                                _tr('MessageDialog', 'information'),
                                msg)

    def delete(self) -> None:
        "Delete current script"
        msg = _tr('Scripting', 'Delete current script ?')
        if QMessageBox.question(self,
                                _tr('MessageDialog', 'Question'),
                                f"{msg}",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    def reload(self) -> None:
        "reload form"
        super().reload()

    def changeFont(self, font: QFont) -> None:
        "Change editor font"
        self.ui.textEditScript.setFont(font)
        # save font properties
        st = QSettings()
        st.setValue("Scripting/EditorFont", font)

    def changeFontSize(self, size: int) -> None:
        "Change editor font size"
        font = self.ui.textEditScript.font()
        font.setPointSize(size)
        self.ui.textEditScript.setFont(font)
        # save font properties
        st = QSettings()
        st.setValue("Scripting/EditorFont", font)

    def download(self) -> None:
        "Dowload current script to a file"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Scripting', "Select the directory"),
                                                     str(path))
        if directory == "":
            return

        row = self.mapper.currentIndex()
        # looks like zipfile accept qt file path with / so no need to use os.path.join
        fileName = (f"{directory}/"
                    f"{self.model.index(row, COMPANY).data()}"
                    f"_{self.model.index(row, CLASS).data()}"
                    f"_{self.model.index(row, METHOD).data()}"
                    f"_{self.model.index(row, TRIGGER).data()}"
                    f".scp.zip")
        try:
            with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr('class', self.model.index(row, CLASS).data())
                zf.writestr('method', self.model.index(row, METHOD).data())
                zf.writestr('trigger', self.model.index(row, TRIGGER).data())
                zf.writestr('active', str(self.model.index(row, ACTIVE).data()))
                zf.writestr('company', str(self.model.index(row, COMPANY).data()))
                zf.writestr('pyscript', self.model.index(row, SCRIPT).data())
        except Exception as er:
            msg = _tr('Scripting', "Error on saving current script to file")
            QMessageBox.critical(self,
                                 _tr('Scripting', "Download current script"),
                                 f"{msg}\n{er}")
        else:
            msg = _tr('Scripting', "Current script saved to file:")
            QMessageBox.information(self,
                                    _tr('Scripting', "Download current script"),
                                    f"<p>{msg}</p><p><b>{fileName}</b></p>")
            # update settings
            st.setValue("Scripting/PathScripts", directory)

    def downloadAll(self) -> None:
        "Save all scripts to a directory, one file per script"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Scripting', "Select the directory"),
                                                     str(path))
        if directory == "":
            return
        try:
            for cls, mth, trg, act, cmp, pys in get_all_scripts():
                # looks like zipfile accept qt file path with / so no need to use os.path.join
                fileName = (f"{directory}/"
                            f"{cmp}"
                            f"_{cls}"
                            f"_{mth}"
                            f"_{trg}"
                            f".scp.zip")
                with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr('class', cls)
                    zf.writestr('method', mth)
                    zf.writestr('trigger', trg)
                    zf.writestr('active', str(act))
                    zf.writestr('company', str(cmp))
                    zf.writestr('pyscript', pys)
        except Exception as er:
            msg = _tr('Scripting', "Error on saving script to file")
            QMessageBox.critical(self,
                                 _tr('Scripting', "Download all script"),
                                 f"{msg}\n{er}")
        else:
            msg = _tr('Scripting', "All scripts saved to directory:")
            QMessageBox.information(self,
                                    _tr('Scripting', "Download all script"),
                                    f"<p>{msg}</p><p><b>{directory}</b></p>")
            # update settings
            st.setValue("Scripting/PathScripts", directory)


    def upload(self) -> None:
        "Upload one script file from directory"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        fileName, t = QFileDialog.getOpenFileName(self,
                                                  _tr('Scripts', "Select the file to import"),
                                                  str(path),
                                                  "*.scp.zip")
        if fileName == "":
            return

        try:
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                cls = zf.read('class').decode('utf-8')
                mth = zf.read('method').decode('utf-8')
                trg = zf.read('trigger').decode('utf-8')
                act = zf.read('active').decode('utf-8')
                cmp = zf.read('company').decode('utf-8')
                pys = zf.read('pyscript').decode('utf-8')
        except Exception as er:
            msg = _tr('Scripting', "Error on opening a script file")
            QMessageBox.critical(self,
                                 _tr('Scripting', "Upload current script"),
                                 f"{msg}\n{er}")
        else:
            try:
                load_script(cls, mth, trg, True if act == 'True' else False, int(cmp), pys)
            except PyAppDBError as er:
                QMessageBox.critical(self,
                                     _tr("MessageDialog", "Critical"),
                                     f"<p>Database error: {er.code}</p><p><b>{er.message}</b></p>")
            else:
                self.reload()
                QMessageBox.information(self,
                                        _tr('MessageDialog', "information"),
                                        _tr('Scripting', "Script file imported to database"))

    def uploadAll(self) -> None:
        "Upload all scripts from directory"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Scripting', "Select the directory"),
                                                     str(path))
        if directory == "":
            return

        error = False
        it = QDirIterator(QDir(directory), QDirIterator.IteratorFlag.NoIteratorFlags)
        while it.hasNext():
            it.next()
            if it.fileInfo().isFile() and it.fileInfo().completeSuffix() == 'scp.zip':
                fileName = it.fileInfo().absoluteFilePath()
                try:
                    with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                        cls = zf.read('class').decode('utf-8')
                        mth = zf.read('method').decode('utf-8')
                        trg = zf.read('trigger').decode('utf-8')
                        act = zf.read('active').decode('utf-8')
                        cmp = zf.read('company').decode('utf-8')
                        pys = zf.read('pyscript').decode('utf-8')
                except Exception as er:
                    msg = _tr('Scripting', "Error on uploading script file:")
                    QMessageBox.critical(self,
                                         _tr('Scripting', "Upload all scripts"),
                                         f"{msg}\n{fileName}\n{er}")
                    error = True
                else:
                    try:
                        load_script(cls, mth, trg, True if act == 'True' else False, int(cmp), pys)
                    except PyAppDBError as er:
                        error = True
                        QMessageBox.critical(self,
                                             _tr("MessageDialog", "Critical"),
                                             f"<p>Database error: {er.code}</p><p><b>{er.message}</b></p>")
        self.reload()
        if error:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Error"),
                                 _tr('Scripting', "Scripts imported with errors"))
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "information"),
                                    _tr('Scripting', "All files imported successfully"))


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
