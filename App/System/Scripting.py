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
from enum import IntEnum
import zipfile
import logging
from typing import cast

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QDirIterator
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetricsF
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog

# application modules
from App import session
from App.Database.Scripting import load_script
from App.Database.Scripting import get_all_scripts
from App.Database.Company import company_list
from App.Database.Models import ScriptingIndexModel
from App.Database.Models import ScriptingModel
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import GenericDelegate
from App.Ui.ScriptingWidget import Ui_ScriptingWidget
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Core.SyntaxHighlighter import PythonHighlighter


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

class scr(IntEnum):
    ID          = 0 
    CLASS       = 1
    METHOD      = 2
    TRIGGER     = 3
    DESCRIPTION = 4
    NOTE        = 5
    COMPANY     = 6
    ACTIVE      = 7
    SYSTEM      = 8
    SCRIPT      = 9
    USER_INS    = 10
    DATE_INS    = 11
    USER_UPD    = 12
    DATE_UPD    = 13


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
    if not auth[0]: # no read permission
        QMessageBox.warning(
            mw,
            _tr('MessageDialog', "Warning"),
            _tr('CashDesk', 'No access right to this archive')
        )
        return
    sw = ScriptingForm(mw, title, auth)
    sw.applySortFilter()
    mw.addTab(title, sw)
    logging.info('Scripting Form added to main window')


class ScriptingForm(FormIndexManager):
    "Form for python scripting management"

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
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
        self.mapper.addMapping(self.ui.comboBoxClass, scr.CLASS)
        self.mapper.addMapping(self.ui.comboBoxMethod, scr.METHOD)
        self.ui.comboBoxTrigger.setItemList(runOptions())
        self.mapper.addMapping(self.ui.comboBoxTrigger, scr.TRIGGER)#, b"modelDataStr")
        self.mapper.addMapping(self.ui.lineEditDescription, scr.DESCRIPTION)
        self.mapper.addMapping(self.ui.plainTextEditNote, scr.NOTE)
        self.mapper.addMapping(self.ui.comboBoxCompany, scr.COMPANY, b"modelDataInt")#, b"modelDataStr")
        self.mapper.addMapping(self.ui.checkBoxActive, scr.ACTIVE)
        self.mapper.addMapping(self.ui.textEditScript, scr.SCRIPT)#, b"plainText")
        self.mapper.addMapping(self.ui.checkBoxSystem, scr.SYSTEM)
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # set font
        st = QSettings()
        self.editorFont: QFont = cast(QFont, st.value("Scripting/EditorFont", QFont('Courier New', 8), type=QFont))
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

    def mapperIndexChanged(self, index):
        # disable save option for system profiles
        super().mapperIndexChanged(index)
        if self.ui.checkBoxSystem.isChecked():
            self.write_perm = False
        else:
            self.write_perm = True
            
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
            QMessageBox.warning(
                self,
                _tr('MessageDialog', 'information'),
                msg
            )

    def delete(self) -> None:
        "Delete current script"
        msg = _tr('Scripting', 'Delete current script ?')
        if QMessageBox.question(
            self,
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
        directory = QFileDialog.getExistingDirectory(
            self,
            _tr('Scripting', "Select the directory"),
            str(path)
            )
        if directory == "":
            return

        row = self.mapper.currentIndex()
        # looks like zipfile accept qt file path with / so no need to use os.path.join
        fileName = (f"{directory}/"
                    f"{self.model.index(row, scr.COMPANY).data()}"
                    f"_{self.model.index(row, scr.CLASS).data()}"
                    f"_{self.model.index(row, scr.METHOD).data()}"
                    f"_{self.model.index(row, scr.TRIGGER).data()}"
                    f".scp.zip")
        with gui_exception_context(self,
                                   _tr('Scripting', "Saving current script to file")):
            with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr('class', self.model.index(row, scr.CLASS).data())
                zf.writestr('method', self.model.index(row, scr.METHOD).data())
                zf.writestr('trigger', self.model.index(row, scr.TRIGGER).data())
                zf.writestr('company', str(self.model.index(row, scr.COMPANY).data()))
                zf.writestr('active', str(self.model.index(row, scr.ACTIVE).data()))
                zf.writestr('description', str(self.model.index(row, scr.DESCRIPTION).data()))
                zf.writestr('pyscript', self.model.index(row, scr.SCRIPT).data())
                zf.writestr('note', str(self.model.index(row, scr.NOTE).data()))
                zf.writestr('system', str(self.model.index(row, scr.SYSTEM).data()))
        
            msg = _tr('Scripting', "Current script saved to file:")
            QMessageBox.information(
                self,
                _tr('Scripting', "Download current script"),
                f"<p>{msg}</p><p><b>{fileName}</b></p>"
            )
            # update settings
            st.setValue("Scripting/PathScripts", directory)

    def downloadAll(self) -> None:
        "Save all scripts to a directory, one file per script"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(
            self,
            _tr('Scripting', "Select the directory"),
            str(path)
            )
        if directory == "":
            return
        with gui_exception_context(self, _tr('Scripting', "Saving all scripts to files")):
            for cls, mth, trg, cmp, act, des, pys, nte, sys in get_all_scripts():
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
                    zf.writestr('company', str(cmp))
                    zf.writestr('active', str(act))
                    zf.writestr('description', des)
                    zf.writestr('pyscript', pys)
                    zf.writestr('note', nte or '')
                    zf.writestr('system', str(sys))
                    
            msg = _tr('Scripting', "All scripts saved to directory:")
            QMessageBox.information(
                self,
                _tr('Scripting', "Download all script"),
                f"<p>{msg}</p><p><b>{directory}</b></p>"
            )
            # update settings
            st.setValue("Scripting/PathScripts", directory)

    def upload(self) -> None:
        "Upload one script file from directory"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            _tr('Scripts', "Select the file to import"),
            str(path),
            "*.scp.zip"
            )
        if fileName == "":
            return
        
        with gui_exception_context(self, _tr('Scripting', "Uploading script file")):
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                cls = zf.read('class').decode('utf-8')
                mth = zf.read('method').decode('utf-8')
                trg = zf.read('trigger').decode('utf-8')
                cmp = zf.read('company').decode('utf-8')
                act = zf.read('active').decode('utf-8')
                des = zf.read('description').decode('utf-8')
                pys = zf.read('pyscript').decode('utf-8')
                nte = zf.read('note').decode('utf-8')
                sys = zf.read('system').decode('utf-8')
            with gui_exception_context(self, _tr('Scripting', "Saving script file to database")):
                load_script(cls, 
                            mth,
                            trg,
                            int(cmp),
                            True if act == 'True' else False,
                            des,
                            pys,
                            nte or None,
                            True if sys == 'True' else False)
                self.reload()
                QMessageBox.information(
                    self,
                    _tr('MessageDialog', "information"),
                    _tr('Scripting', "Script file imported to database")
                )

    def uploadAll(self) -> None:
        "Upload all scripts from directory"
        st = QSettings()
        path = st.value("Scripting/PathScripts", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(
            self,
            _tr('Scripting', "Select the directory"),
            str(path)
            )
        if directory == "":
            return
        
        it = QDirIterator(QDir(directory), QDirIterator.IteratorFlag.NoIteratorFlags)
        imported_count = 0  # Contatore invece di un semplice boolean

        while it.hasNext():
            it.next()
            if it.fileInfo().isFile() and it.fileInfo().completeSuffix() == 'scp.zip':
                fileName = it.fileInfo().absoluteFilePath()
                with gui_exception_context(self, _tr('Scripting', "Uploading script file")):
                    with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                        cls = zf.read('class').decode('utf-8')
                        mth = zf.read('method').decode('utf-8')
                        trg = zf.read('trigger').decode('utf-8')
                        cmp = zf.read('company').decode('utf-8')
                        act = zf.read('active').decode('utf-8')
                        des = zf.read('description').decode('utf-8')
                        pys = zf.read('pyscript').decode('utf-8')
                        nte = zf.read('note').decode('utf-8')
                        sys = zf.read('system').decode('utf-8')
                        
                    with gui_exception_context(self, _tr('Scripting', f"Saving script file {fileName} to database")):
                        load_script(cls, 
                                    mth,
                                    trg,
                                    int(cmp),
                                    True if act == 'True' else False,
                                    des,
                                    pys,
                                    nte or None,
                                    True if sys == 'True' else False)
                    imported_count += 1 # Incrementa per ogni file salvato

        # Il controllo va FUORI dal ciclo while
        if imported_count > 0:        
            QMessageBox.information(
                self,
                _tr("MessageDialog", "information"),
                _tr('Scripting', "All files imported successfully")
            )
        else:
            QMessageBox.warning(
                self,
                _tr("MessageDialog", "warning"),
                _tr('Scripting', "No valid .scp.zip files found")
            )
         
        self.reload()
        
