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

"""Report

This modules manages reports: creation/deletion/modification of sql reports

"""

# standard library
import zipfile
import logging
import re
from typing import cast

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QFileInfo
from PySide6.QtCore import QIODevice
from PySide6.QtCore import QBuffer
from PySide6.QtCore import QByteArray
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetrics
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtGui import QTextCharFormat
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog

# application modules
from App import session
from App import currentAction
from App.Database.Exceptions import PyAppDBError
from App.Database.Report import delete_all_reports
from App.Database.Report import load_report
from App.Database.Report import list_all_reports
from App.Database.Models import ReportModel
from App.Database.Models import ReportIndexModel
from App.Report import REPORT_CLASSES
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Dialog import PrintDialog
from App.Ui.ReportWidget import Ui_ReportWidget
from App.Core.L10n import _tr
from App.Core.L10n import langCountry
from App.Core.L10n import langCountryFlags
from App.Core.SyntaxHighlighter import XMLHighlighter

# logger
logger = logging.getLogger(__name__)


V_ID, V_CODE, V_L10N, V_CLASS, V_DESCRIPTION, V_SYSTEM, V_USER_INS, V_DATE_INS, V_USER_UPD, V_DATE_UPD = range(10)

ID, CODE, L10N, CLASS, DESCRIPTION, XML, SYSTEM, USER_INS, DATE_INS, USER_UPD, DATE_UPD = range(11)



FORM, GRID = range(2)


def report() -> None:
    "Show/Edit reports"
    logger.info('Starting report Form')
    mw = session['mainwin']
    title = currentAction['sys_report'].text()
    auth = currentAction['sys_report'].data()
    cf = ReportForm(mw, title, auth)
    cf.reload()
    mw.addTab(title, cf)
    logger.info('Report Form added to main window')


class ReportForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = ReportModel(self)
        idxModel = ReportIndexModel(self)
        self.setModel(model, idxModel)
        self.tabName = title
        self.helpLink = "help/main.html#gui"
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, False)
        self.ui = Ui_ReportWidget()
        self.ui.setupUi(self)
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('report')
        self.ui.tableView.setItemDelegateForColumn(V_SYSTEM, BooleanDelegate(self))
        self.mapper.addMapping(self.ui.lineEditCode, CODE)
        self.ui.comboBoxL10n.setItemList(langCountryFlags())
        self.mapper.addMapping(self.ui.comboBoxL10n, L10N, b"modelDataStr")
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        self.ui.comboBoxClass.addItems([None] + REPORT_CLASSES)
        self.mapper.addMapping(self.ui.comboBoxClass, CLASS)
        self.mapper.addMapping(self.ui.checkBoxSystem, SYSTEM)
        self.mapper.addMapping(self.ui.textEditXML, XML, b"plainText")
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # set font
        st = QSettings()
        self.editorFont: QFont = cast(QFont, st.value("XMLEditorFont", QFont('Courier', 8), type=QFont))
        self.ui.textEditXML.setFont(self.editorFont)
        self.ui.fontComboBox.setCurrentFont(self.editorFont)
        self.ui.spinBoxFontSize.setValue(self.editorFont.pointSize())
        # set tab spaces
        tabStop = 4
        metrics = QFontMetrics(self.editorFont)
        self.ui.textEditXML.setTabStopDistance(tabStop * metrics.maxWidth())
        # syntax highlighting
        self.highlighter = XMLHighlighter(self.ui.textEditXML.document())
        # signal/slot
        self.ui.pushButtonDeleteAll.clicked.connect(self.deleteAll)
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownloadAll.clicked.connect(self.downloadAll)
        self.ui.pushButtonUploadAll.clicked.connect(self.uploadAll)
        self.ui.fontComboBox.currentFontChanged.connect(self.changeFont)
        self.ui.spinBoxFontSize.valueChanged.connect(self.changeFontSize)
        self.ui.pushButtonInsertImage.clicked.connect(self.insertImage)
        self.ui.lineEditCode.setDisabled(True)
        self.ui.comboBoxL10n.setDisabled(True)

    def mapperIndexChanged(self, row: int) -> None:
        super().mapperIndexChanged(row)
        if self.ui.checkBoxSystem.isChecked():
            self.ui.comboBoxClass.setEditable(True)
            self.ui.lineEditDescription.setReadOnly(True)
            self.ui.textEditXML.setReadOnly(True)
        else:
            self.ui.comboBoxClass.setEditable(False)
            self.ui.lineEditDescription.setReadOnly(False)
            self.ui.textEditXML.setReadOnly(False)

    def new(self) -> None:
        "New report"
        super().new()
        self.ui.lineEditCode.setEnabled(True)
        self.ui.comboBoxL10n.setEnabled(True)
        self.ui.lineEditCode.setFocus()

    def save(self) -> None:
        "Save report edited"
        # check if a '.' is present in code
        if '.' in self.ui.lineEditCode.text():
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Report', "Can't use '.' (dot) in report code"))
            return
        super().save()
        self.ui.lineEditCode.setDisabled(True)
        self.ui.comboBoxL10n.setDisabled(True)

    def delete(self) -> None:
        "Delete current report"
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Report', "It is not possible to "
                                        "delete a system report"))
            return
        msg = _tr('Report', 'Delete current report ?')
        if QMessageBox.question(self,
                                _tr('MessageDialog', 'Question'),
                                f"{msg}\n{self.ui.lineEditCode.text()}",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    def changeFont(self, font: QFont) -> None:
        "Change editor font"
        self.ui.textEditXML.setFont(font)
        # save font properties
        st = QSettings()
        st.setValue("XMLEditorFont", font)

    def changeFontSize(self, size: int) -> None:
        "Change editor font size"
        font = self.ui.textEditXML.font()
        font.setPointSize(size)
        self.ui.textEditXML.setFont(font)
        # save font properties
        st = QSettings()
        st.setValue("XMLEditorFont", font)

    def insertImage(self, checked: bool) -> None:
        "Load an image file as base64 string data to clipboard"
        st = QSettings()
        path = st.value("PathImagesReports", QDir.current().path(), type = str)
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr('Report', "Select the image to insert into clipboard"),
                                           str(path),
                                           _tr('Report', "Portable Network Graphics (*.png);;All files (*.*)"))

        if f == "":
            return
        pix = QPixmap(f)
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODevice.OpenModeFlag.WriteOnly)
        pix.save(buf, "PNG")
        #txt = str(ba.toBase64().data(), encoding='utf8')
        txt = bytes(ba.toBase64().data()).decode('utf-8')
        cb = QApplication.clipboard()
        cb.setText(f"""<image left="0.0" top="0.0" width="45.0" height="48.0" aspectRatio="KeepAspectRatio">{txt}</image>""")
        st.setValue("PathImagesReports", QFileInfo(f).path())
        
    def deleteAll(self) -> None:
        "Delete all reports"
        msg = _tr('Report', 'Delete ALL reports ?')
        if QMessageBox.question(self,
                                _tr('MessageDialog', 'Question'),
                                msg,
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        delete_all_reports()
        self.reload()        

    def download(self) -> None:
        "Dowload current report to file"
        st = QSettings()
        path = st.value("PathReports", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Report', "Select the directory"),
                                                     str(path))
        if directory == "":
            return
        row = self.mapper.currentIndex()
        # looks like zipfile accept qt file path with / so no need to use os.path.join
        fileName = (f"{directory}"
                    f"/{self.model.index(row, CODE).data()}"
                    f"_{self.model.index(row, L10N).data()}"
                    f".rpt.zip")
        try:
            with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr('code', self.model.data(self.model.index(row, CODE)))
                zf.writestr('l10n', self.model.data(self.model.index(row, L10N)))
                zf.writestr('class', self.model.data(self.model.index(row, CLASS)))
                zf.writestr('system', str(self.model.data(self.model.index(row, SYSTEM))))
                zf.writestr('description', self.model.data(self.model.index(row, DESCRIPTION)))
                zf.writestr('xml', self.model.data(self.model.index(row, XML)))
        except Exception as er:
            msg = _tr('Report', "Error on saving current report to file")
            QMessageBox.critical(self,
                                 _tr('Report', "Download current report"),
                                 f"{msg}\n{er}")
        else:
            msg = _tr('Report', "Current report saved to file:")
            QMessageBox.information(self,
                                    _tr('Report', "Download current report"),
                                    f"<p>{msg}</p><p><b>{fileName}</b></p>")
            # update settings
            st.setValue("PathReports", directory)

    def downloadAll(self) -> None:
        "Save all report definition to a directory, one file per report"
        st = QSettings()
        path = str(st.value("PathReports", QDir.current().path()))
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Report', "Select the directory"),
                                                     path)
        if directory == "":
            return
        try:
            for i, (cod, lcn, cls, sys, dsc, xml) in enumerate(list_all_reports(), 1):
                fileName = (f"{directory}"
                            f"/{i:02d}"
                            f"_{cod}"
                            f"_{lcn}"
                            f".rpt.zip")
                with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr('code', cod)
                    zf.writestr('l10n', lcn)
                    zf.writestr('class', cls)
                    zf.writestr('system', str(sys))
                    zf.writestr('description', dsc)
                    zf.writestr('xml', xml)
        except Exception as er:
            msg = _tr('Report', "Error on saving all reports to file")
            QMessageBox.critical(self,
                                _tr('Report', "Download all reports"),
                                f"{msg}\n{er}")
        else:
            msg = _tr('Report', "All reports saved to directory")
            QMessageBox.information(self,
                                    _tr('Report', "Download all reports"),
                                    f"<p>{msg}</p><p><b>{directory}</b></p>")
        # update settings
        st.setValue("PathReports", directory)

    def upload(self) -> None:
        "Upload one report file from directory"
        st = QSettings()
        path = str(st.value("PathReports", QDir.currentPath()))
        fileName, t = QFileDialog.getOpenFileName(self,
                                                  _tr('Report', "Select the file to import"),
                                                  path,
                                                  "*.rpt.zip")
        if fileName == "":
            return
        try:
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                cod = zf.read('code').decode('utf-8')
                lcn = zf.read('l10n').decode('utf-8')
                cls = zf.read('class').decode('utf-8')
                sys = zf.read('system').decode('utf-8')
                dsc = zf.read('description').decode('utf-8')
                xml = zf.read('xml').decode('utf-8')
        except Exception as er:
            msg = _tr('Report', "Error on opening a report file")
            QMessageBox.critical(self,
                                 _tr('Report', "Upload current report"),
                                 f"{msg}\n{er}")
        else:
            sysb: bool = sys == 'True'
            try:
                load_report(cod, lcn, cls, sysb, dsc, xml)
            except PyAppDBError as er:
                QMessageBox.critical(self,
                                     _tr("MessageDialog", "Critical"),
                                     f"<p>Database error: {er.code}</p><p><b>{er.message}</b></p>")
            else:
                self.reload()
                QMessageBox.information(self,
                                        _tr('MessageDialog', "information"),
                                        _tr('Report', "Report file imported to database"))

    def uploadAll(self) -> None:
        "Upload all reports from directory"
        st = QSettings()
        path = str(st.value("PathReports", QDir.currentPath()))
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Report', "Select the directory"),
                                                     path)
        if directory == "":
            return
        error = False
        for f in QDir(directory).entryInfoList(QDir.Filter.NoFilter, QDir.SortFlag.Name):
            if f.isFile() and f.completeSuffix() == 'rpt.zip':
                fileName = f.absoluteFilePath()
                try:
                    with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                        cod = zf.read('code').decode('utf-8')
                        lcn = zf.read('l10n').decode('utf-8')
                        cls = zf.read('class').decode('utf-8')
                        sys = zf.read('system').decode('utf-8')                    
                        dsc = zf.read('description').decode('utf-8')
                        xml = zf.read('xml').decode('utf-8')
                except Exception as er:
                    msg = _tr('Report', "Error on opening report file:")
                    QMessageBox.critical(self,
                                         _tr('Report', "Upload all reports"),
                                         f"{msg}\n{fileName}\n{er}")
                    error = True
                else:
                    sysb: bool = sys == 'True'
                    try:
                        load_report(cod, lcn, cls, sysb, dsc, xml)
                    except PyAppDBError as er:
                        error = True
                        QMessageBox.critical(self,
                                             _tr("MessageDialog", "Critical"),
                                             f"<p>Database error: {er.code}</p><p><b>{er.message}</b></p>")
        self.reload()
        if error:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Error"),
                                 _tr('Report', "Reports imported to database with errors"))
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "information"),
                                    _tr('Report', "All reports imported to database"))

    def print(self) -> None:
        rid: int = self.model.data(self.model.index(self.mapper.currentIndex(), ID))
        lcn: str = self.model.data(self.model.index(self.mapper.currentIndex(), L10N))
        dialog = PrintDialog(self, reportId=rid, l10n=lcn)
        dialog.show()

