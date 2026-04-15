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

This modules manages python scripting

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
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetricsF
#from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtGui import QTextCharFormat
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog

# application modules
from App import session
from App import currentAction
from App.Database.Exceptions import PyAppDBError
from App.Database.Scripting import load_script
from App.Database.Company import company_list
from App.Database.Models import ScriptingIndexModel
from App.Database.Models import ScriptingModel
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import HideTextDelegate
#from App.Widgets.Dialogs import PrintReportDialog
from App.Ui.ScriptingWidget import Ui_ScriptingWidget
from App.Core.L10n import _tr
from App.Core.L10n import langCountry
from App.Core.L10n import langCountryFlags
from App.Core.SyntaxHighlighter import PythonHighlighter


SCRIPTABLE = {'PrintersForm': ['__init__',
                               'new',
                               'save',
                               'delete',
                               'reload',
                               'add',
                               'remove',
                               'print_'],

              'DepartmentsForm': ['__init__',
                                  'new',
                                  'save',
                                  'delete',
                                  'reload',],

              'TablesForm': ['__init__',
                             'new',
                             'save',
                             'delete',
                             'deleteAll',
                             'reload',
                             'generateTables'],

              'ItemsForm': ['__init__',
                            'new',
                            'save',
                            'delete',
                            'reload',
                            'copyVariants',
                            'print_'],
              'PriceListForm': ['__init__',
                                'new',
                                'save',
                                'delete',
                                'reload',
                                'add',
                                'remove',
                                'duplicate',
                                'print_'],
              'EventsForm': ['__init__',
                             'new',
                             'save',
                             'delete',
                             'reload',
                             'upload',
                             'download',
                             'removeImage',
                             'print_'],
              'WebOrdersForm': ['__init__',
                                'reload',
                                'deleteOrders',
                                'recalcTotals'],
              'OrdersForm': ['__init__',
                             'new',
                             'save',
                             'delete',
                             'reload',
                             'print_',
                             'reprint'],
              'SettingsDialog': ['__init__',
                                 'apply',
                                 'accept']}

(ID, CLASS, METHOD, TRIGGER, COMPANY, ACTIVE, SCRIPT,
 USER_INS, DATE_INS, USER_UPD, DATE_UPD) = range(11)

def runOptions() -> list[tuple[str, str]]:
    return [('B', _tr('script', 'Before')),
            ('I', _tr('script', 'Instead')),
            ('A', _tr('script', 'After'))]


def scripting() -> None:
    "Show/Edit python script"
    logging.info('Starting scripting Form')
    mw = session['mainwin']
    title = currentAction['sys_scripting'].text()
    auth = currentAction['sys_scripting'].data()
    sw = ScriptingForm(mw, title, auth)
    sw.reload()
    mw.addTab(title, sw)
    logging.info('Scripting Form added to main window')


class ScriptingForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = ScriptingModel(self)
        idxModel = ScriptingIndexModel(self)
        self.setModel(model, idxModel)
        self.tabName = title
        self.helpLink = "help/main.html#gui"
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, False, False)
        self.ui = Ui_ScriptingWidget()
        self.ui.setupUi(self)
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('scripting')
        self.ui.tableView.setItemDelegateForColumn(TRIGGER, RelationDelegate(self, runOptions))
        self.ui.tableView.setItemDelegateForColumn(ACTIVE, BooleanDelegate(self))
        # fill classcombobox, methodcombobox and companycombobox
        self.ui.comboBoxClass.currentIndexChanged.connect(self.fillMethods)
        self.ui.comboBoxClass.addItems(list(SCRIPTABLE.keys()))
        self.ui.comboBoxCompany.setItemList(company_list() + [(None, _tr('script', 'All'))])
        # field mapping
        self.mapper.addMapping(self.ui.comboBoxClass, CLASS)
        self.mapper.addMapping(self.ui.comboBoxMethod, METHOD)
        self.ui.comboBoxTrigger.setItemList(runOptions())
        self.mapper.addMapping(self.ui.comboBoxTrigger, TRIGGER, b"modelDataStr")
        self.mapper.addMapping(self.ui.comboBoxCompany, COMPANY, b"modelDataStr")
        self.mapper.addMapping(self.ui.checkBoxActive, ACTIVE)
        self.mapper.addMapping(self.ui.textEditScript, SCRIPT, b"plainText")
        #self.ui.textEditScript.textChanged.connect(self.textChanged)
        # set font
        st = QSettings()
        self.editorFont: QFont = cast(QFont, st.value("ScriptEditorFont", QFont('Courier', 8), type=QFont))
        self.ui.textEditScript.setFont(self.editorFont)
        self.ui.fontComboBox.setCurrentFont(self.editorFont)
        self.ui.spinBoxFontSize.setValue(self.editorFont.pointSize())
        # set tab spaces
        tabStop = 4
        metrics = QFontMetricsF(self.editorFont)
        self.ui.textEditScript.setTabStopDistance(tabStop * metrics.maxWidth())
        # syntax highlighting
        self.highlighter = PythonHighlighter(self.ui.textEditScript.document())
        # self.ui.textEditScript.show()
        # signal/slot
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownloadAll.clicked.connect(self.downloadAll)
        self.ui.pushButtonUploadAll.clicked.connect(self.uploadAll)
        self.ui.fontComboBox.currentFontChanged.connect(self.changeFont)
        self.ui.spinBoxFontSize.valueChanged.connect(self.changeFontSize)
        # initial status
        self.ui.comboBoxClass.setDisabled(True)
        self.ui.comboBoxMethod.setDisabled(True)
        self.ui.comboBoxTrigger.setDisabled(True)

    def fillMethods(self, text: str) -> None:
        self.ui.comboBoxMethod.clear()
        self.ui.comboBoxMethod.addItems(SCRIPTABLE.get(self.ui.comboBoxClass.currentText()) or [])  # on New text is empty

    def new(self) -> None:
        "New script"
        super().new()
        self.ui.comboBoxClass.setEnabled(True)
        self.ui.comboBoxMethod.setEnabled(True)
        self.ui.comboBoxTrigger.setEnabled(True)
        self.ui.comboBoxClass.setCurrentIndex(-1)
        self.ui.comboBoxTrigger.setCurrentIndex(-1)
        self.ui.comboBoxClass.setFocus()

    def save(self) -> None:
        super().save()
        self.ui.comboBoxClass.setDisabled(True)
        self.ui.comboBoxMethod.setDisabled(True)
        self.ui.comboBoxTrigger.setDisabled(True)
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
        super().reload()
        self.ui.comboBoxClass.setDisabled(True)
        self.ui.comboBoxMethod.setDisabled(True)
        self.ui.comboBoxTrigger.setDisabled(True)

    def changeFont(self, font: QFont) -> None:
        "Change editor font"
        self.ui.textEditScript.setFont(font)
        # save font properties
        st = QSettings()
        st.setValue("ScriptEditorFont", font)

    def changeFontSize(self, size: int) -> None:
        "Change editor font size"
        font = self.ui.textEditScript.font()
        font.setPointSize(size)
        self.ui.textEditScript.setFont(font)
        # save font properties
        st = QSettings()
        st.setValue("ScriptEditorFont", font)

    def download(self) -> None:
        "Dowload current script to a file"
        st = QSettings()
        path = st.value("PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Scripting', "Select the directory"),
                                                     str(path))
        if directory == "":
            return

        row = self.mapper.currentIndex()
        # looks like zipfile accept qt file path with / so no need to use os.path.join
        fileName = (f"{directory}"
                    f"/{self.model.index(row, CLASS).data()}"
                    f"_{self.model.index(row, METHOD).data()}"
                    f"_{self.model.index(row, TRIGGER).data()}"
                    f".scp.zip")
        try:
            with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr('class', self.model.index(row, CLASS).data())
                zf.writestr('method', self.model.index(row, METHOD).data())
                zf.writestr('trigger', self.model.index(row, TRIGGER).data())
                zf.writestr('active', str(self.model.index(row, ACTIVE).data()))
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
            st.setValue("PathScripts", directory)

    def downloadAll(self) -> None:
        "Save all scripts to a directory, one file per script"
        st = QSettings()
        path = st.value("PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Scripting', "Select the directory"),
                                                     str(path))
        if directory == "":
            return
        # avoid active filters
        if hasattr(self.model, 'filterCondition'):
            self.model.filterCondition.clear()
        if hasattr(self.model, 'whereConditions'):
            self.model.whereConditions.clear()
        self.reload()
        try:
            for row in range(self.model.rowCount()):
                # looks like zipfile accept qt file path with / so no need to use os.path.join
                fileName = (f"{directory}"
                            f"/{self.model.index(row, CLASS).data()}"
                            f"_{self.model.index(row, METHOD).data()}"
                            f"_{self.model.index(row, TRIGGER).data()}"
                            f".scp.zip")
                with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr('class', self.model.index(row, CLASS).data())
                    zf.writestr('method', self.model.index(row, METHOD).data())
                    zf.writestr('trigger', self.model.index(row, TRIGGER).data())
                    zf.writestr('active', str(self.model.index(row, ACTIVE).data()))
                    zf.writestr('pyscript', self.model.index(row, SCRIPT).data())
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
            st.setValue("PathScripts", directory)


    def upload(self) -> None:
        "Upload one script file from directory"
        st = QSettings()
        path = st.value("PathScripts", QDir.current().path())
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
                pys = zf.read('pyscript').decode('utf-8')
        except Exception as er:
            msg = _tr('Scripting', "Error on opening a script file")
            QMessageBox.critical(self,
                                 _tr('Scripting', "Upload current script"),
                                 f"{msg}\n{er}")
        else:
            try:
                load_script(cls, mth, trg, pys, True if act == 'True' else False)
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
        path = st.value("PathScripts", QDir.current().path())
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
                        pys = zf.read('pyscript').decode('utf-8')
                except Exception as er:
                    msg = _tr('Scripting', "Error on uploading script file:")
                    QMessageBox.critical(self,
                                         _tr('Scripting', "Upload all scripts"),
                                         f"{msg}\n{fileName}\n{er}")
                    error = True
                else:
                    try:
                        load_script(cls, mth, trg, pys, True if act == 'True' else False)
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


