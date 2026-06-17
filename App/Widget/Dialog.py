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

"""Dialogs

This module contains general custom dialogs


"""

# standard library
from enum import IntEnum
import sys
from typing import cast, Any

# PySide6
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSettings
from PySide6.QtCore import QFile
from PySide6.QtCore import QUrl
from PySide6.QtCore import QDir
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtCore import QMimeDatabase
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QIODevice
from PySide6.QtCore import QBuffer
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime

from PySide6.QtPrintSupport import QPrinter
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtPrintSupport import QPrintPreviewWidget
from PySide6.QtPrintSupport import QPrinterInfo
from PySide6.QtPrintSupport import QPrintDialog
from PySide6.QtGui import QCursor
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QDesktopServices
from PySide6.QtGui import QPdfWriter
from PySide6.QtGui import QPagedPaintDevice
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QDoubleSpinBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QDateEdit
from PySide6.QtWidgets import QDateTimeEdit
from PySide6.QtWidgets import QTimeEdit
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPushButton

# application modules
from App import session
from App import currentIcon
from App.Core.L10n import _tr
from App.Ui.MessageDialog import Ui_MessageDialog
from App.Ui.SelectImageDialog import Ui_SelectImageDialog
from App.Ui.PrintDialog import Ui_PrintDialog
from App.Ui.SortFilterDialog import Ui_SortFilterDialog
from App.Ui.EventFilterDialog import Ui_EventFilterDialog
from App.Ui.DateTimeInputDialog import Ui_DateTimeInputDialog
from App.Database.AbstractModels.TableModel import QueryModel
from App.Database.AbstractModels.TableModel import TableModel
from App.Database.Report import report_class_adapt_list
from App.Database.Report import get_report_list
from App.Database.Report import report_xml
from App.Database.Report import get_report_from_adapt
from App.Database.Report import report_query
from App.Database.Adaptation import set_adapt_setting
from App.Database.Adaptation import get_adapt_setting
from App.Database.Adaptation import delete_adaptation
from App.Database.Adaptation import create_adaptation
from App.Database.Adaptation import get_adapt_sorting
from App.Database.Adaptation import set_adapt_sorting
from App.Database.Adaptation import is_system_object
from App.Database.Report import report_description
from App.Database.Lookup import event_lookup
from App.Database.Lookup import item_lookup
from App.Database.Lookup import get_list
from App.Database.Adaptation import create_adaptation
from App.Database.Adaptation import delete_adaptation
from App.Database.Adaptation import list_adaptation
from App.Database.Adaptation import get_adapt_limit
from App.Database.Adaptation import set_adapt_limit
from App.Database.Adaptation import get_adapt_setting
from App.Database.Adaptation import set_adapt_setting
from App.Database.Adaptation import get_adapt_sorting
from App.Database.Adaptation import set_adapt_sorting
from App.Database.Adaptation import get_adapt_default
from App.Database.Adaptation import get_adapt_class_default
from App.Database.Adaptation import set_adapt_class_default
from App.Database.Adaptation import get_adapt_user_default
from App.Database.Adaptation import set_adapt_user_default
from App.Database.Event import get_event_data
from App.Database.Exceptions import PyAppDBError
from App.Report.ReportEngine import Report
from App.Report.ReportEngine import ReportException, ReportPrintError
from App.Widget.Control import RelationalComboBox
from App.Widget.Control import CheckableComboBox


# filter rows
FILTER_ROWS = 30

# sort tab index
class sti(IntEnum):
    FILTER      = 0
    SORT        = 1
    CUSTOMIZE   = 2

# filter fields
class ff(IntEnum):
    FIELD       = 0
    NEGATE      = 1
    OPERATOR    = 2 
    OPERAND     = 3

# sort fields
class sf(IntEnum):
    SORTFIELD   = 0
    SORTORDER   = 1

# print tab index
class pti(IntEnum):
    PARAMS      = 0
    FILTER      = 1
    OPTION      = 2
    CUSTIMIZE   = 3


referenceList = {'eventList': event_lookup,
                 'itemList': item_lookup}


class MessageBox(QDialog):
    "Custom message expanding dialog"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MessageDialog()
        self.ui.setupUi(self)
        app = cast(QApplication, QCoreApplication.instance())
        if not app:
            return
        sty = app.style()
        icon = sty.standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        self.ui.labelIcon.setPixmap(icon.pixmap(icon.actualSize(QSize(32, 32))))
        
def MessageBoxCritical(parent, 
                       title: str|None = None,
                       ercode: str|None = None,
                       text: str|None = None, 
                       detail: str|None = None
                       ) -> None:
    "Show a critical message dialog with optional detail message"
    dlg = MessageBox(parent)
    dlg.setWindowTitle(title or _tr('Dialog', "Critical error"),)
    dlg.ui.labelErrorCode.setText(ercode or '')
    dlg.ui.labelMessage.setText(text or _tr('Dialog', "Unidentified critical error"),)
    if detail:
        detail = f"""
```python
{detail.strip()}
```
"""
    dlg.ui.textEditDetailMessage.setMarkdown(detail or "")
    ret = dlg.exec()
    # clicking on Abort should be equal to dialog.rejected
    if ret == QDialog.DialogCode.Rejected:
        sys.exit(0)
        

class SelectImageDialog(QDialog):
    "Select Image Dialog"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_SelectImageDialog()
        self.ui.setupUi(self)
        self.image: QPixmap|None = None
        # actions
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownload.clicked.connect(self.download)

    def upload(self) -> None:
        "Upload an image file"
        path = QDir.currentPath()
        f, fi = QFileDialog.getOpenFileName(
            self,
            _tr('Dialog', "Select the image file to upload"),
            path,
            _tr('Dialog', "Portable Network Graphics (*.png);;All files (*.*)")
        )
        if f == "":
            return
        pix = QPixmap()
        if not pix.load(f):
            MessageBoxCritical(self,
                                 _tr("MessageDialog", "Critical"),
                                 _tr("Dialog", "Unable to load the file {}").format(f))
            return
        db = QMimeDatabase()
        ft = db.mimeTypeForFile(f).name()
        self.ui.lineEditImageFormat.setEnabled(True)
        self.ui.lineEditImageFormat.setText(ft)
        self.setImage(pix)

    def download(self) -> None:
        "Save an image to a file"
        if not self.image:
            return
        path = QDir.currentPath()
        f, fi = QFileDialog.getSaveFileName(
            self,
            _tr("SelectImageDialod", "Select the image file name"),
            path,
            _tr("SelectImageDialod","Portable Network Graphics (*.png);;Tutti i files (*.*)")
        )
        if self.image:
            self.image.save(f)

    def getImage(self) -> QPixmap|None:
        return self.image

    def setImage(self, pix: QPixmap) -> None:
        self.image = pix
        # preview
        if pix.width() > 200 or pix.height() > 200:
            pix = pix.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.ui.labelImage.setPixmap(pix)
        self.ui.pushButtonDownload.setEnabled(True)
        # pixmap information
        self.ui.lineEditWidth.setEnabled(True)
        self.ui.lineEditWidth.setText(str(self.image.width()))
        self.ui.lineEditHeight.setEnabled(True)
        self.ui.lineEditHeight.setText(str(self.image.height()))
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODevice.OpenModeFlag.WriteOnly)
        self.image.save(buf, "PNG")
        self.ui.spinBoxPixmapSize.setEnabled(True)
        self.ui.spinBoxPixmapSize.setValue(ba.size()/1024)


class RowComboBox(QComboBox):
    "Custom combo box for store row number"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.row: int|None = None
        
        
class RowCheckBox(QCheckBox):
    "Custom checkbox for storeing row number"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.row: int|None = None
        
        
class SpacerWidget(QWidget):
    "Custom widget for storeing field type"


class LineEditStrings(QLineEdit):
    "Custom line edit for list of string values separated by comma"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)

    def value(self) -> list:
        "Return the list of values separated by comma for ues in SQL ILIKE ANY(%s) operator"
        return [f'%{v.strip()}%' for v in self.text().split(',') if v.strip()]
    
    
class LineEditInts(QLineEdit):
    "Custom line edit for list of int values separated by comma"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)

    def value(self) -> list:
        "Return the list of values separated by comma"
        return [int(v.strip()) for v in self.text().split(',') if v.strip()]
    
class LineEditDecimals(QLineEdit):
    "Custom line edit for list of decimal values separated by comma"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)

    def value(self) -> list:
        "Return the list of values separated by comma"
        return [float(v.strip()) for v in self.text().split(',') if v.strip()]
    

class SortFilterDialog(QDialog):
    "Sort and filter Dialog for Forms"

    def __init__(self, 
                 sortfilterClass: str,
                 model: QueryModel|TableModel,
                 parent: QWidget
                 ) -> None:
        super().__init__(parent)
        self.ui = Ui_SortFilterDialog()
        self.ui.setupUi(self)
        # can't be class variables for translation requirements
        # object type (operator, operator description, format, widget)
        # format:
        # 0 = require operand argument (field operator %s - args)
        # 1 = no require operand (field operator)
        # 2 = operand included in operator with argument as list (field operator - args)
        # 3 = operand included in operator with argument literal
        self.FILTERING = {
            # integer
            'int': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'SB'), # spinbox
                  ('<', _tr('Operator', '<'), 0, 'SB'),
                  ('<=', _tr('Operator', '<='), 0, 'SB'),
                  ('>', _tr('Operator', '>'), 0, 'SB'),
                  ('>=', _tr('Operator', '>='), 0, 'SB'),
                  ('= ANY(%s)', _tr('Operator', 'In'), 2, 'LEI'), # line edit int list
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None),
                  ('=', _tr('Operator', 'From list'), 0, 'LIST')], # list of reference values
            # decimal number
            'decimal': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'DSB'), # double spinbox
                  ('<', _tr('Operator', '<'), 0, 'DSB'),
                  ('<=', _tr('Operator', '<='), 0, 'DSB'),
                  ('>', _tr('Operator', '>'), 0, 'DSB'),
                  ('>=', _tr('Operator', '>='), 0, 'DSB'),
                  ('= ANY(%s)', _tr('Operator', 'In'), 2, 'LED'), # line edit decimal list
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
            # boolean
            'bool': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'CB'), # checkbox
                  ('IS NULL', _tr('Operator', 'Is null'), 1, None)],
            # string
            'str': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'LE'), # line edit
                  ("ilike '%%'||%s||'%%'", _tr('Operator', 'Contains'), 3, 'LE'),
                  ("ilike %s||'%%'", _tr('Operator', 'Starts with'), 3, 'LE'),
                  ("ilike '%%'||%s", _tr('Operator', 'Ends with'), 3, 'LE'),
                  ('ILIKE ANY(%s)', _tr('Operator', 'In'), 2, 'LES'), # line edit string list case insensitive
                  ('IS NULL', _tr('Operator', 'Is null'), 1, None)],
            # date
            'date': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'DE'), # date edit
                  ('<', _tr('Operator', '<'), 0, 'DE'),
                  ('<=', _tr('Operator', '<='), 0, 'DE'),
                  ('>', _tr('Operator', '>'), 0, 'DE'),
                  ('>=', _tr('Operator', '>='), 0, 'DE'),
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
            # date time
            'datetime': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'DTE'), # date time edit
                  ('<', _tr('Operator', '<'), 0, 'DTE'),
                  ('<=', _tr('Operator', '<='), 0, 'DTE'),
                  ('>', _tr('Operator', '>'), 0, 'DTE'),
                  ('>=', _tr('Operator', '>='), 0, 'DTE'),
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
             # time
            'time': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'TE'), # date time edit
                  ('<', _tr('Operator', '<'), 0, 'TE'),
                  ('<=', _tr('Operator', '<='), 0, 'TE'),
                  ('>', _tr('Operator', '>'), 0, 'TE'),
                  ('>=', _tr('Operator', '>='), 0, 'TE'),
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
            # reference field / list
            'refstr': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'SCB'), # standard combo box
                  ('= ANY(%s)', _tr('Operator', 'In'), 2, 'CCB'), # checkable combo box
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)]}

        self.ORDERING = (('ASC', _tr('Sort', 'Ascending')),
                         ('DESC', _tr('Sort', 'Descending')))

        self.sortfilterClass = sortfilterClass
        self.modelId = None
        self.ui.lineEditSortFilterClass.setText(sortfilterClass)
        self.model: QueryModel|TableModel = model # set also on sortfiltercustomization selection
        # restore settings
        st = QSettings(self)
        if st.value(f"SortFilterDialog/Geometry/{self.sortfilterClass}"):
            self.restoreGeometry(st.value(f"SortFilterDialog/Geometry/{self.sortfilterClass}"))
        # signal/slot connections
        self.ui.pushButtonUserDefault.clicked.connect(self.setUserDefault)
        self.ui.pushButtonClassDefault.clicked.connect(self.setClassDefault)
        self.ui.comboBoxSetting.currentIndexChanged.connect(self.fillCustomizations)
        self.ui.pushButtonNewCustomization.clicked.connect(self.newCustomization)
        self.ui.pushButtonDelete.clicked.connect(self.deleteCurrent)
        self.ui.pushButtonUpdate.clicked.connect(self.updateSettings)
        self.ui.pushButtonSetSorting.clicked.connect(self.setCustomizationSorting)
        self.ui.buttonBox.clicked.connect(self.clicked)
        # create filter and sorting comboboxes
        # filters comboboxes
        for row in range(FILTER_ROWS):
            field = RowComboBox(self)
            field.addItem('', None) # item 0 for clear/reset
            for f, d, r, t in self.model.columns:
                if t: # except None fields
                    field.addItem(d, f)
            field.row = row
            field.currentIndexChanged.connect(self.condIndexChanged)
            neg = RowCheckBox(self)
            neg.row = row
            neg.setToolTip(_tr('SoftFilterDialog','Not'))
            oper = RowComboBox(self)
            oper.row = row
            oper.currentIndexChanged.connect(self.operIndexChanged)
            self.ui.layoutFilters.addWidget(field, row,ff.FIELD)
            self.ui.layoutFilters.addWidget(neg, row, ff.NEGATE)
            self.ui.layoutFilters.addWidget(oper, row,ff.OPERATOR)
            sw = SpacerWidget(self)
            self.ui.layoutFilters.addWidget(sw, row,ff.OPERAND) # position widget only
        if self.model.limitCondition:
            self.ui.checkBoxMaxRows.setChecked(True)
            self.ui.spinBoxMaxRows.setValue(self.model.limitCondition)
        else:
            self.ui.checkBoxMaxRows.setChecked(False)
        # set layout stretch
        self.ui.layoutFilters.setColumnStretch(ff.FIELD, 2)
        self.ui.layoutFilters.setColumnStretch(ff.NEGATE, 0)
        self.ui.layoutFilters.setColumnStretch(ff.OPERATOR, 1)
        self.ui.layoutFilters.setColumnStretch(ff.OPERAND, 1)
        self.ui.layoutFilters.setRowStretch(row + 1, 1)
        # sorting comboboxes
        for row in range(len(self.model.columns)):
            field = RowComboBox(self)
            field.addItem('', None) # item 0 for clear/reset
            for f, d, r, t in self.model.columns:
                field.addItem(d, f)
            field.row = row
            field.currentIndexChanged.connect(self.sortIndexChanged)
            order = QComboBox(self)
            self.ui.layoutSorting.addWidget(field, row, sf.SORTFIELD)
            self.ui.layoutSorting.addWidget(order, row, sf.SORTORDER)
        # set layout stretch
        self.ui.layoutSorting.setColumnStretch(sf.SORTFIELD, 2)
        self.ui.layoutSorting.setColumnStretch(sf.SORTORDER, 1)
        self.ui.layoutSorting.setRowStretch(row + 1, 1)
        # get available customizations
        self.availableCustomizations()
        # set authorization
        self.ui.tabWidget.widget(sti.CUSTOMIZE).setEnabled(session['can_edit_sortfilters'])

    def availableCustomizations(self) -> None:
        "Get available customization from DB and fill combobox"
        # disable signal
        self.ui.comboBoxSetting.currentIndexChanged.disconnect()
        self.ui.comboBoxSetting.clear()
        # get customizations list for class
        try:
            result = list_adaptation('S', self.sortfilterClass)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
            return
        # fill the combobox
        for i, d, y in result:
            self.ui.comboBoxSetting.addItem(d, i)
        # set default for user or class
        daid = get_adapt_default('S', self.sortfilterClass, session['user'])
        cid = self.ui.comboBoxSetting.findData(daid)
        self.ui.comboBoxSetting.setCurrentIndex(cid)
        # ri-enable signal
        self.ui.comboBoxSetting.currentIndexChanged.connect(self.fillCustomizations)
        # disable unavailable options
        if self.ui.comboBoxSetting.count() == 0:
            self.ui.groupBoxCurrent.setDisabled(True)
        else:  # if previously was disabled
            self.ui.groupBoxCurrent.setEnabled(True)
        # set model for current customization
        result = [(1, self.model.__class__.__name__)]  # only current model
        # create field type
        self.fieldType = {f: t for f, d, r, t in self.model.columns}
        # initial settings
        self.fillCustomizations()

    def fillCustomizations(self) -> None:
        "Sets filters and sorting based on current customization"
        if not self.model:
            return
        sortFilterId = self.ui.comboBoxSetting.currentData()
        if sortFilterId is None:
            return
        # initial reset
        # filters
        for row in range(FILTER_ROWS):
            self.ui.layoutFilters.itemAtPosition(row, ff.FIELD).widget().setCurrentIndex(0)
            self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().setChecked(False)
            self.ui.layoutFilters.itemAtPosition(row, ff.OPERATOR).widget().setCurrentIndex(0)
        # sortings
        for row in range(len(self.model.columns)):
            self.ui.layoutSorting.itemAtPosition(row, sf.SORTFIELD).widget().setCurrentIndex(0)
            self.ui.layoutSorting.itemAtPosition(row, sf.SORTORDER).widget().setCurrentIndex(0)
        # get sort and filter params
        try:
            _, filters, sortings = get_adapt_setting(sortFilterId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
            return
        # set filters settings
        for t, row, cmb1, neg, cmb2, wv in filters:
            self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().setCurrentIndex(cmb1)
            self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().setChecked(neg)
            self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().setCurrentIndex(cmb2)
            widget = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
            match widget:
                case QComboBox():
                    widget.setCurrentIndex(int(wv))
                case QLineEdit():
                    widget.setText(wv)
                case QSpinBox():
                    widget.setValue(int(wv or 0))
                case QDoubleSpinBox():
                    widget.setValue(float(wv or 0.0))
                case QDateEdit():
                    widget.setDate(QDate.fromString(wv, Qt.DateFormat.ISODate))
                case QDateTimeEdit():
                    widget.setDateTime(QDateTime.fromString(wv, Qt.DateFormat.ISODate))
                case QTimeEdit():
                    widget.setTime(QTime.fromString(wv, Qt.DateFormat.ISODate))
                case QCheckBox():
                    if wv == 'True':
                        widget.setChecked(True)
                    else:
                        widget.setChecked(False)
                case _:
                    pass
        # limit
        try:
            result = get_adapt_limit(sortFilterId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
        if result:
            self.ui.checkBoxMaxRows.setChecked(True)
            self.ui.spinBoxMaxRows.setValue(result)
        else:
            self.ui.checkBoxMaxRows.setChecked(False)
        # set sorting settings
        for t, row, cmb1, neg, cmb2, wv in sortings:
            self.ui.layoutSorting.itemAtPosition(row, sf.SORTFIELD).widget().setCurrentIndex(cmb1)
            self.ui.layoutSorting.itemAtPosition(row, sf.SORTORDER).widget().setCurrentIndex(cmb2)
        # sort filter class sorting
        self.ui.spinBoxClassSorting.setValue(get_adapt_sorting(sortFilterId))

    def updateSettings(self) -> None:
        "Save modified settings to database"
        if not self.model:
            return
        cid = int(self.ui.comboBoxSetting.currentData())
        columns = []
        # filters
        for row in range(FILTER_ROWS):
            if self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentIndex() != 0:
                cmb1 = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentIndex()
                neg = self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().isChecked()
                cmb2 = self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().currentIndex()
                widget = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
                wv: str|float|bool|None = None
                match widget:
                    case QComboBox():
                        wv = str(widget.currentIndex())
                    case QLineEdit():
                        wv = widget.text()
                    case (QSpinBox()|QDoubleSpinBox()):
                        wv = widget.value()
                    case QDateEdit():
                        wv = widget.date().toString(Qt.DateFormat.ISODate)
                    case QDateTimeEdit():
                        wv = widget.dateTime().toString(Qt.DateFormat.ISODate)
                    case QTimeEdit():
                        wv = widget.time().toString(Qt.DateFormat.ISODate)
                    case QCheckBox():
                        if widget.checkState() == Qt.CheckState.Checked:
                            wv = True
                        else:
                            wv = False
                    case _:
                        wv = None
                columns.append((cid, None, None, None, None, 'F',row, cmb1, neg, cmb2, str(wv)))
        # sorting
        for row in range(len(self.model.columns)):
            if self.ui.layoutSorting.itemAtPosition(row, ff.FIELD).widget().currentIndex() != 0:
                cmb1 = self.ui.layoutSorting.itemAtPosition(row, sf.SORTFIELD).widget().currentIndex()
                cmb2 = self.ui.layoutSorting.itemAtPosition(row, sf.SORTORDER).widget().currentIndex()
                wv = None
                columns.append((cid, None, None, None, None, 'S', row, cmb1, None, cmb2, str(wv)))
        # update sort filter
        try:
            set_adapt_setting(cid, columns)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                _tr("MessageDialog", "Critical"),
                                f"Database error: {er.code}\n{er.message}")
            return
        # limit
        if self.ui.checkBoxMaxRows.isChecked():
            try:
                set_adapt_limit(cid, self.ui.spinBoxMaxRows.value())
            except PyAppDBError as er:
                    QMessageBox.critical(self,
                                         _tr("MessageDialog", "Critical"),
                                         f"Database error: {er.code}\n{er.message}")
                    return

        QMessageBox.information(self,
                                _tr("MessageDialog", "Information"),
                                _tr("Dialog", "Current customization was updated"))

    def condIndexChanged(self, index: int) -> None:
        "Set combobox items (operator) and operand QWidget"
        if not self.model or index < 0:
            return
        # get current row number
        s = self.sender()
        if not isinstance(s, RowComboBox):
            return
        row = s.row
        # reset negate
        self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().setChecked(False)
        # if index is zero reset everythinga of the row
        if index == 0:
            # reset operator
            self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().setCurrentIndex(0)
            return
        # get field type
        field = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentData()
        ftype = self.fieldType.get(field)
        if not ftype:
            return
        # set operator alternatives
        self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().clear()
        for o, d, r, w in self.FILTERING[ftype]:
            if hasattr(self.model, 'reference') and w == 'LIST':
                if field not in self.model.reference: # skip list if not required
                    continue
            self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().addItem(d, o)

    def operIndexChanged(self, index: int) -> None:
        "Create a widget for field and operator"
        if not self.model or index < 0:
            return
        # get current row number
        s = self.sender()        
        if not isinstance(s, RowComboBox):
            return
        row = s.row  
        # clear if index is zero
        if index == 0:
            # delete previous widget (MANDATORY)
            w = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
            self.ui.layoutFilters.removeWidget(w)
            w.deleteLater()
            # add spacer
            sw = SpacerWidget(self) # spacer widget
            self.ui.layoutFilters.addWidget(sw, row,ff.OPERAND)
            return
        # get field type
        field = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentData()
        fi = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentIndex() -1
        ftype = self.fieldType[field]
        w = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
        nwt = self.FILTERING[ftype][index][3]
        # insert new operand widget
        widget: QSpinBox|QDoubleSpinBox|QCheckBox|QDateEdit|QDateTimeEdit|QLineEdit|QComboBox|CheckableComboBox|QWidget
        match nwt:
            case 'SB': # spinbox
                widget = QSpinBox(self)
                widget.setRange(0, 2147483647)
            case 'DSB': # double spinbox
                widget = QDoubleSpinBox(self)
                widget.setDecimals(2)
                widget.setMaximum(99999999.99)
            case 'CB': # check box
                widget = QCheckBox(self)
            case 'DE': # date edit
                widget = QDateEdit(QDate.currentDate(), self)
                widget.setCalendarPopup(True)
                widget.setMinimumDate(QDate(1800, 1, 1))
                widget.setMaximumDate(QDate(3000, 12, 31))
                widget.setDate(QDate.currentDate())
            case 'DTE': # date time edit
                widget = QDateTimeEdit(self)
                widget.setCalendarPopup(True)
                widget.setMinimumDate(QDate(1800, 1, 1))
                widget.setMaximumDate(QDate(3000, 12, 31))
                widget.setDate(QDate.currentDate())
            case 'TE': # time edit
                widget = QTimeEdit(QTime.currentTime(), self)
                #widget.setTime(QTime.currentTime())
            case 'LE': # line edit
                widget = QLineEdit(self)
            case 'LES': # line edit string list
                widget = LineEditStrings(self)
            case 'LEI': # line edit int list
                widget = LineEditInts(self)
            case 'LED': # line edit decimal list
                widget = LineEditDecimals(self)
            case 'SCB': # standard combo box
                widget = QComboBox(self)
                for k, v in get_list(self.model.columns[fi][6]):
                    widget.addItem(v, k)
            case 'CCB': # chackable combo box
                widget = CheckableComboBox(self)
                for k, v in get_list(self.model.columns[fi][6]):
                    widget.addItem(v, k)
            case 'LIST':
                if hasattr(self.model, 'reference'):
                    widget = QComboBox(self)
                    for k, v in self.model.reference[field]():
                        widget.addItem(v, k)
                else:
                    widget = SpacerWidget(self)
            case _: # no widget required (is null/is not null)
                widget = SpacerWidget(self)
        self.ui.layoutFilters.removeWidget(w)
        w.deleteLater()
        # new widget
        self.ui.layoutFilters.addWidget(widget, row,ff.OPERAND)

    def sortIndexChanged(self, index: int) -> None:
        "Set combobox items and parameter qwidget"
        if not self.model or index < 0:
            return
        # get current row number
        s = self.sender()        
        if not isinstance(s, RowComboBox):
            return
        row = s.row
        # clear first
        self.ui.layoutSorting.itemAtPosition(row, sf.SORTORDER).widget().clear()
        if index != 0:
            for i, j in self.ORDERING:
                self.ui.layoutSorting.itemAtPosition(row, sf.SORTORDER).widget().addItem(j, i)

    def newCustomization(self) -> None:
        "Create a new customization"
        name = self.ui.lineEditNewName.text()
        try:
            cid = create_adaptation('S', self.sortfilterClass, name, None)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                                _tr("MessageDialog", "Critical"),
                                f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "New customization saved"))
            self.ui.lineEditNewName.clear()
            self.availableCustomizations() # reload all customizations including new one

    def deleteCurrent(self) -> None:
        "Remove current customization from database"
        cid = int(self.ui.comboBoxSetting.currentData())
        if is_system_object(cid):
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("View", "System customization cannot be deleted"))
            return
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                _tr("View", "Are you sure to delete the current customization ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return
        try:
            delete_adaptation(cid)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                                _tr("MessageDialog", "Critical"),
                                f"Database error: {er.code}\n{er.message}")
        else:
            self.availableCustomizations()
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current customization deleted"))

    def setCustomizationSorting(self) -> None:
        "Set current customization sort index"
        if self.ui.comboBoxSetting.count() == 0:
            return
        sortfilterId = int(self.ui.comboBoxSetting.currentData())
        try:
            set_adapt_sorting(sortfilterId, self.ui.spinBoxClassSorting.value())
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current customization sorting updated"))
            
    def setUserDefault(self) -> None:
        "Set current adaptation as default for current user"
        if self.ui.comboBoxSetting.count() == 0:
            return
        cid = int(self.ui.comboBoxSetting.currentData())
        # get sort and filter params
        try:
            set_adapt_user_default('S',
                               self.sortfilterClass,
                               session['user'],
                               cid)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Critical"),
                               f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current adaptation set as default for current user"))

    def setClassDefault(self) -> None:
        "Set current adaptation as default for current class"
        if self.ui.comboBoxSetting.count() == 0:
            return
        cid = int(self.ui.comboBoxSetting.currentData())
        # get sort and filter params
        try:
            set_adapt_class_default(cid)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                            _tr("MessageDialog", "Critical"),
                            f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current adaptation set as default for class"))

    def clicked(self, button: QPushButton|None = None) -> None:
        "Intercept Reset button action"
        if button == self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Reset):
            for r in range(self.ui.layoutFilters.rowCount()):
                if self.ui.layoutFilters.itemAtPosition(r,ff.FIELD):
                    self.ui.layoutFilters.itemAtPosition(r,ff.FIELD).widget().setCurrentIndex(0)
                if self.ui.layoutFilters.itemAtPosition(r, ff.NEGATE):
                    self.ui.layoutFilters.itemAtPosition(r, ff.NEGATE).widget().setChecked(False)
                if self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR):
                    self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().setCurrentIndex(0)
            for r in range(self.ui.layoutSorting.rowCount()):
                if self.ui.layoutSorting.itemAtPosition(r,ff.FIELD):
                    self.ui.layoutSorting.itemAtPosition(r,ff.FIELD).widget().setCurrentIndex(0)

    def applySortFilter(self) ->None:
        "Generate the where conditions and update model"
        if not self.model:
            return
        # get filters
        self.model.whereCondition.clear()
        v: list|str|int|float|QDate|QDateTime|QTime|bool|None
        for r in range(FILTER_ROWS):
            if (self.ui.layoutFilters.itemAtPosition(r,ff.FIELD).widget().currentIndex() != 0 and # field
                self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().currentIndex() != 0): # operator
                ty = self.model.columns[self.ui.layoutFilters.itemAtPosition(r,ff.FIELD).widget().currentIndex() -1][3]
                fl = self.ui.layoutFilters.itemAtPosition(r,ff.FIELD).widget().currentData()
                ng = self.ui.layoutFilters.itemAtPosition(r, ff.NEGATE).widget().isChecked()
                op = self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().currentData()
                oi = self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().currentIndex()
                wd = self.ui.layoutFilters.itemAtPosition(r,ff.OPERAND).widget()
                match wd:
                    case CheckableComboBox():
                        v = wd.currentData() # list
                    case QComboBox():
                        v = wd.currentData()
                    case LineEditStrings()|LineEditInts()|LineEditDecimals(): # lists
                        v = wd.value()
                    case QLineEdit(): # must be after list edit because is subclass of QLineEdit
                        v = wd.text()
                    case (QSpinBox()|QDoubleSpinBox()):
                        v = wd.value()
                    case QDateEdit():
                        v = wd.date()
                    case QTimeEdit(): # time before datetime because is subclass of QDateTimeEdit
                        v = wd.time()
                    case QDateTimeEdit():
                        v = wd.dateTime()
                    case QCheckBox():
                        if wd.checkState() == Qt.CheckState.Checked:
                            v = True
                        else:                            
                            v = False
                    case _:
                        v = None
                arg: Any
                match self.FILTERING[ty][oi][2]:
                    case 0:
                        cond = f"{fl} {op} %s"
                        arg = v
                    case 1:
                        cond = f"{fl} {op}"
                        arg = None
                    case 2:
                        cond = f"{fl} {op}"
                        arg = v.split() if isinstance(v, str) else v
                    case 3:
                        cond = f"{fl} {op}"
                        arg = v
                    case _:
                        pass
                if ng:
                    cond = f"NOT {cond}" 
                print("WHERE ", cond, arg)
                self.model.addWhere(cond, arg)
        if self.ui.checkBoxMaxRows.isChecked():
            self.model.limitCondition = self.ui.spinBoxMaxRows.value()
        else:
            self.model.limitCondition = None
        # get orderby clause
        sorting = []
        for r in range(len(self.model.columns)):
            if self.ui.layoutSorting.itemAtPosition(r, sf.SORTFIELD).widget().currentIndex() != 0:
                f = self.ui.layoutSorting.itemAtPosition(r, sf.SORTFIELD).widget().currentData()
                s = self.ui.layoutSorting.itemAtPosition(r, sf.SORTORDER).widget().currentData()
                sorting.append(f'{f} {s}')
        self.model.orderByExpression.clear()
        for i in sorting:
            self.model.addOrderBy(i)
        # update model and form
        if hasattr(self.parent(), 'setIndexModel'):
            self.parent().setIndexModel(self.model) # type: ignore
        if hasattr(self.parent(), 'reload'):
            self.parent().reload()  # type: ignore
        
    def accept(self) -> None:
        "Apply sorting and filtering conditions to model"
        self.applySortFilter()
        super().accept()

    def done(self, r: int) -> None:
        "Save local settings on exit, even in accetp/reject/finished"
        # save settings
        st = QSettings(self)
        st.setValue(f"SortFilterDialog/Geometry/{self.sortfilterClass}", self.saveGeometry())
        super().done(r)


class EventFilterDialog(QDialog):
    "Event filter dialog, choice of event, date and day part for event related models"

    def __init__(self, 
                 parent: QWidget,
                 show_date: bool = False,
                 show_daypart: bool = False
                 ) -> None:
        super().__init__(parent)
        self.ui = Ui_EventFilterDialog()
        self.ui.setupUi(self)
        self.ui.groupBoxDate.setVisible(show_date)
        self.ui.groupBoxDayPart.setVisible(show_daypart)
        self.adjustSize()
        # fill event combobox
        for i, d in event_lookup():
            self.ui.comboBoxEvent.addItem(d, i)
        self.ui.comboBoxEvent.setCurrentText(session['event_description'])
        self.ui.comboBoxEvent.currentIndexChanged.connect(self.setDate)
        # initial date set
        self.setDate()
        
    def setDate(self) -> None:
        "Set date to the first of selected event"
        event = self.ui.comboBoxEvent.currentData()
        result = get_event_data(event)
        if not result:
            return
        desc, start_date, end_date, price_list = result
        today = QDateTime.currentDateTime()
        if start_date <= today <= end_date:
            self.ui.dateEditDate.setDate(today.date())
        else:
            self.ui.dateEditDate.setDate(start_date.date())

    def accept(self) -> None:
        "Apply event filter conditions to model"
        if self.ui.groupBoxDate.isChecked():
            date = self.ui.dateEditDate.date()
        else:
            date = None
        if self.ui.groupBoxDayPart.isChecked():
            dayPart = 'L' if self.ui.radioButtonLunch.isChecked() else 'D'
        else:
            dayPart = None
        from typing import Any, cast

        if hasattr(self.parent(), 'updateFilterConditions'):
            cast(Any, self.parent()).updateFilterConditions(self.ui.comboBoxEvent.currentData(), 
                                                            date, 
                                                            dayPart)

        super().accept()



class PrintDialog(QDialog):
    "Print dialog"
    
    def __init__(self, 
                 parent: QWidget, 
                 reportClass: str|None = None,
                 l10n: str|None = None,
                 reportId: int|None = None
                 ) -> None:
        super().__init__(parent)
        self.ui = Ui_PrintDialog()
        self.ui.setupUi(self)
        # can't be class variables for translation requirements
        # object type (operator, operator description, format, widget)
        # format:
        # 0 = require operand argument (field operator %s - args)
        # 1 = no require operand (field operator)
        # 2 = operand included in operator with argument as list (field operator - args)
        # 3 = operand included in operator with argument literal
        self.FILTERING = {
            # integer
            'int': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'SB'), # spinbox
                  ('<', _tr('Operator', '<'), 0, 'SB'),
                  ('<=', _tr('Operator', '<='), 0, 'SB'),
                  ('>', _tr('Operator', '>'), 0, 'SB'),
                  ('>=', _tr('Operator', '>='), 0, 'SB'),
                  ('= ANY(%s)', _tr('Operator', 'In'), 2, 'LEI'), # line edit int list
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None),
                  ('=', _tr('Operator', 'From list'), 0, 'LIST')], # list of reference values
            # decimal number
            'decimal': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'DSB'), # double spinbox
                  ('<', _tr('Operator', '<'), 0, 'DSB'),
                  ('<=', _tr('Operator', '<='), 0, 'DSB'),
                  ('>', _tr('Operator', '>'), 0, 'DSB'),
                  ('>=', _tr('Operator', '>='), 0, 'DSB'),
                  ('= ANY(%s)', _tr('Operator', 'In'), 2, 'LED'), # line edit decimal list
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
            # boolean
            'bool': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'CB'), # checkbox
                  ('IS NULL', _tr('Operator', 'Is null'), 1, None)],
            # string
            'str': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'LE'), # line edit
                  ("ilike '%%'||%s||'%%'", _tr('Operator', 'Contains'), 3, 'LE'),
                  ("ilike %s||'%%'", _tr('Operator', 'Starts with'), 3, 'LE'),
                  ("ilike '%%'||%s", _tr('Operator', 'Ends with'), 3, 'LE'),
                  ('ILIKE ANY(%s)', _tr('Operator', 'In'), 2, 'LES'), # line edit string list case insensitive
                  ('IS NULL', _tr('Operator', 'Is null'), 1, None)],
            # date
            'date': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'DE'), # date edit
                  ('<', _tr('Operator', '<'), 0, 'DE'),
                  ('<=', _tr('Operator', '<='), 0, 'DE'),
                  ('>', _tr('Operator', '>'), 0, 'DE'),
                  ('>=', _tr('Operator', '>='), 0, 'DE'),
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
            # date time
            'datetime': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'DTE'), # date time edit
                  ('<', _tr('Operator', '<'), 0, 'DTE'),
                  ('<=', _tr('Operator', '<='), 0, 'DTE'),
                  ('>', _tr('Operator', '>'), 0, 'DTE'),
                  ('>=', _tr('Operator', '>='), 0, 'DTE'),
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
             # time
            'time': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'TE'), # date time edit
                  ('<', _tr('Operator', '<'), 0, 'TE'),
                  ('<=', _tr('Operator', '<='), 0, 'TE'),
                  ('>', _tr('Operator', '>'), 0, 'TE'),
                  ('>=', _tr('Operator', '>='), 0, 'TE'),
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)],
            # reference field / list
            'refstr': [('', '', 0, None),  # first row means no data
                  ('=', _tr('Operator', '='), 0, 'SCB'), # standard combo box
                  ('= ANY(%s)', _tr('Operator', 'In'), 2, 'CCB'), # checkable combo box
                  ('IS NULL', _tr('Operator', 'Is Null'), 1, None)]}
        
        # omit ordering for reports as it is useless

        self.PDFVERSION = [(QPagedPaintDevice.PdfVersion.PdfVersion_1_4, _tr('Dialog', 'Pdf 1.4')),
                           (QPagedPaintDevice.PdfVersion.PdfVersion_A1b, _tr('Dialog', 'Pdf A-1b')),
                           (QPagedPaintDevice.PdfVersion.PdfVersion_1_6, _tr('Dialog', 'Pdf 1.6'))]

        self.l10n = l10n or session['l10n']
        self.reportClass = reportClass
        self.ui.labelReportClass.setText(reportClass or _tr("ReportDialog", "None"))
        # set button icons
        self.ui.toolButtonPrintPreview.setIcon(currentIcon['print_preview'])
        self.ui.toolButtonPrint.setIcon(currentIcon['print_printer'])
        self.ui.toolButtonPrintDirect.setIcon(currentIcon['print_direct'])
        self.ui.toolButtonPrintPDF.setIcon(currentIcon['print_pdf'])
        # printer list
        self.ui.comboBoxPrinters.addItems(QPrinterInfo.availablePrinterNames())
        self.ui.comboBoxPrinters.setCurrentText(QPrinterInfo.defaultPrinterName())
        # pdf format
        self.ui.comboBoxPDFVersion.setItemList(self.PDFVERSION)
        # restore settings
        st = QSettings(self)
        if st.value(f"PrintDialog/Geometry/{self.reportClass}"):
            self.restoreGeometry(st.value(f"PrintDialog/Geometry/{self.reportClass}"))
        self.ui.lineEditDirectory.setText(st.value("PrintDialog/PDFDirectory", QDir().currentPath()))
        self.ui.checkBoxOpenPDF.setChecked(st.value("PrintDialog/PDFOpenFileAfterCreate", 'false') == 'true')
        self.ui.comboBoxPDFVersion.setCurrentIndex(st.value("PrintDialog/PDFVersion", 1, type=int))
        self.ui.spinBoxResolution.setValue(st.value("PrintDialog/PDFResolution", 100, type=int))
        # report list for customizations or given report code
        if reportId:
            self.ui.comboBoxReportList.addItem(report_description(reportId), reportId)
        else:
            if self.reportClass:
                for i, c, d in get_report_list(self.reportClass, self.l10n):
                    self.ui.comboBoxReportList.addItem(d, i)
        # signal for change report customization
        self.ui.comboBoxReportCustomizations.currentIndexChanged.connect(self.setReportCustomization)
        self.ui.comboBoxReportList.currentIndexChanged.connect(self.setReportCustomization)
        # signal/slot for buttonbox
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.reset)
        # signal/slot for toolbuttons
        self.ui.toolButtonPrintPreview.clicked.connect(self.printPreview)
        self.ui.toolButtonPrint.clicked.connect(self.printReport)
        self.ui.toolButtonPrintDirect.clicked.connect(self.printDirect)
        self.ui.toolButtonPrintPDF.clicked.connect(self.printPDF)
        # signal/slot other
        self.ui.pushButtonDelete.clicked.connect(self.deleteReportCustomization)
        self.ui.pushButtonNewCustomization.clicked.connect(self.saveNewCustomizationAs)
        self.ui.pushButtonUpdate.clicked.connect(self.saveReportCustomization)
        self.ui.pushButtonSelectDirectory.clicked.connect(self.selectDirectoryClicked)
        self.ui.pushButtonSetSorting.clicked.connect(self.setReportCustomizationSorting)
        self.ui.pushButtonUserDefault.clicked.connect(self.setUserDefault)
        self.ui.pushButtonClassDefault.clicked.connect(self.setClassDefault)
        # check authorization
        self.ui.tabWidget.widget(pti.OPTION).setEnabled(session['can_edit_reports'] or
                                            session['is_admin'])
        # create filter comboboxes
        for row in range(FILTER_ROWS):
            field = RowComboBox(self)
            field.row = row
            field.currentIndexChanged.connect(self.condIndexChanged)
            neg = RowCheckBox(self)
            neg.row = row
            neg.setToolTip(_tr('SoftFilterDialog','Not'))
            oper = RowComboBox(self)
            oper.row = row
            oper.currentIndexChanged.connect(self.operIndexChanged)
            self.ui.layoutFilters.addWidget(field, row,ff.FIELD)
            self.ui.layoutFilters.addWidget(neg, row, ff.NEGATE)
            self.ui.layoutFilters.addWidget(oper, row,ff.OPERATOR)
            sw = SpacerWidget(self)
            self.ui.layoutFilters.addWidget(sw, row,ff.OPERAND) # position widget only
        # set layout stretch
        self.ui.layoutFilters.setColumnStretch(ff.FIELD, 2)
        self.ui.layoutFilters.setColumnStretch(ff.NEGATE, 0)
        self.ui.layoutFilters.setColumnStretch(ff.OPERATOR, 1)
        self.ui.layoutFilters.setColumnStretch(ff.OPERAND, 1)
        self.ui.layoutFilters.setRowStretch(row + 1, 1)
        # report customization list
        self.reportCustomizationList()
        self.setReportCustomization(-1)  # initial settings

    def reset(self) -> None:
        "Clear all filters"
        for i in range(self.ui.layoutFilters.rowCount()):
            if self.ui.layoutFilters.itemAtPosition(i, 0):
                self.ui.layoutFilters.itemAtPosition(i, 0).widget().setCurrentIndex(0)
        
    def show(self) -> None:
        "Show modal dialog if a report is available"
        # no report available, exit
        if self.ui.comboBoxReportList.count() != 0:
            super().show()
        else:
            MessageBoxCritical(self,
                               _tr('MessageDialog', 'Critical'),
                               _tr('Dialog', 'No report available'))

    def reportCustomizationList(self) -> None:
        "Fill available customizations"
        # disable signal first
        self.ui.comboBoxReportCustomizations.currentIndexChanged.disconnect(self.setReportCustomization)
        # report customization list for current class and l10n
        self.ui.comboBoxReportCustomizations.clear()
        try:
            if self.reportClass:
                result = report_class_adapt_list(self.reportClass, session['l10n'])
                for i, j, in result:
                    self.ui.comboBoxReportCustomizations.addItem(j, i)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', 'Critical'),
                                 f"Database error: {er.code}\n{er.message}")
            return
        # reenable signal
        self.ui.comboBoxReportCustomizations.currentIndexChanged.connect(self.setReportCustomization)

    def saveReportCustomization(self) -> None:
        "Save current customization settings"
        cid = self.ui.comboBoxReportCustomizations.currentData()
        columns: Any = []
        wv: int|str|float|QDate|QDateTime|bool|list[object]|None
        # parameters
        for row in range(self.ui.layoutParameters.rowCount() - 1):
            if not self.ui.layoutParameters.itemAtPosition(row, 1):  # some time rowCount is wrong
                continue
            widget = self.ui.layoutParameters.itemAtPosition(row, 1).widget()
            match widget:
                case QComboBox():
                    wv = widget.currentIndex()
                case QLineEdit():
                    wv = widget.text()
                case (QSpinBox()|QDoubleSpinBox()):
                    wv = widget.value()
                case QDateEdit():
                    wv = widget.date().toString(Qt.DateFormat.ISODate)
                case QDateTimeEdit():
                    wv = widget.dateTime().toString(Qt.DateFormat.ISODate)
                case QCheckBox():
                    if widget.checkState() == Qt.CheckState.Checked:
                        wv = True
                    else:
                        wv = False
                case _:
                    raise ReportPrintError("Unable to identify parameter type")
            columns.append((cid, None, None, None, None, 'P', row, None, None, None, str(wv)))
        # filters
        for row in range(FILTER_ROWS):
            if self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentIndex() != 0:
                cmb1 = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentIndex()
                neg = self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().isChecked()
                cmb2 = self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().currentIndex()
                widget = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
                match widget:
                    case QComboBox():
                        wv = str(widget.currentIndex())
                    case QLineEdit():
                        wv = widget.text()
                    case (QSpinBox()|QDoubleSpinBox()):
                        wv = widget.value()
                    case QDateEdit():
                        wv = widget.date().toString(Qt.DateFormat.ISODate)
                    case QDateTimeEdit():
                        wv = widget.dateTime().toString(Qt.DateFormat.ISODate)
                    case QTimeEdit():
                        wv = widget.time().toString(Qt.DateFormat.ISODate)
                    case QCheckBox():
                        if widget.checkState() == Qt.CheckState.Checked:
                            wv = True
                        else:
                            wv = False
                    case _:
                        wv = None
                columns.append((cid, None, None, None, None, 'F',row, cmb1, neg, cmb2, str(wv)))
        try:
            set_adapt_setting(cid, columns)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                    _tr("MessageDialog", "Critical"),
                                    f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Customization saved"))

    def deleteReportCustomization(self) -> None:
        "Delete current report customization"
        custId = self.ui.comboBoxReportCustomizations.currentData()
        if is_system_object(custId):
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("View", "System customization cannot be deleted"))
            return
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                _tr("View", "Are you sure to delete the current customization ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return
        try:
            delete_adaptation(custId)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Critical"),
                               f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Customization deleted"))
        # update report customization list
        self.reportCustomizationList()

    def saveNewCustomizationAs(self) -> None:
        "Create a new customization"
        if not self.reportClass:
            return
        report_id = self.ui.comboBoxReportList.currentData()
        description = self.ui.lineEditNewName.text()
        if not report_id or not description:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Critical"),
                               _tr("Dialog", "You must fill all the parameters of a new customization"))
            return
        try:
            create_adaptation('R', self.reportClass, description, report_id)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Critical"),
                               f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "New customization '{}' created").format(description))
        self.ui.lineEditNewName.clear()
        # update report customization list
        self.reportCustomizationList()

    def setCustomizationSetting(self) -> None:
        "Restore saved customization settings"
        cid = self.ui.comboBoxReportCustomizations.currentData()
        try:
            params, filters, skip = get_adapt_setting(cid)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
            return
        # parameters
        for t, row, cmb1, neg, cmb2, wv in params:
            if not wv:  # this happens on report modification, old customization could refer to deleted objects
                continue
            widget = self.ui.layoutParameters.itemAtPosition(row, 1).widget()
            match widget:
                case QLineEdit():
                    widget.setText(wv)
                case QSpinBox():
                    widget.setValue(int(wv or 0))
                case QDoubleSpinBox():
                    widget.setValue(float(wv or 0.0))
                case QDateEdit():
                    widget.setDate(QDate.fromString(wv, Qt.DateFormat.ISODate))
                case QDateTimeEdit():
                    widget.setDateTime(QDateTime.fromString(wv, Qt.DateFormat.ISODate))
                case QCheckBox():
                    if wv == 'True':
                        widget.setChecked(True)
                    else:
                        widget.setChecked(False)
        # set filters settings
        for t, row, cmb1, neg, cmb2, wv in filters:
            self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().setCurrentIndex(cmb1)
            self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().setChecked(neg)
            self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().setCurrentIndex(cmb2)
            widget = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
            match widget:
                case QComboBox():
                    widget.setCurrentIndex(int(wv))
                case QLineEdit():
                    widget.setText(wv)
                case QSpinBox():
                    widget.setValue(int(wv or 0))
                case QDoubleSpinBox():
                    widget.setValue(float(wv or 0.0))
                case QDateEdit():
                    widget.setDate(QDate.fromString(wv, Qt.DateFormat.ISODate))
                case QDateTimeEdit():
                    widget.setDateTime(QDateTime.fromString(wv, Qt.DateFormat.ISODate))
                case QTimeEdit():
                    widget.setTime(QTime.fromString(wv, Qt.DateFormat.ISODate))
                case QCheckBox():
                    if wv == 'True':
                        widget.setChecked(True)
                    else:
                        widget.setChecked(False)
                case _:
                    pass
        # set pdf file name if a report exists
        if cid:
            self.ui.lineEditFileName.setText(self.report.options.get('documentName'))

    def setReportCustomization(self, index: int) -> None:
        "Set report definition from customization and create widgets"
        custId = self.ui.comboBoxReportCustomizations.currentData()
        if custId:
            # create a report instance for current report id and l10n
            report_id, cd, cl, report_desc, l10n = get_report_from_adapt(custId)
            self.ui.comboBoxReportList.setCurrentText((report_desc))
        else:
            # no customizations, use the current report
            report_id =  self.ui.comboBoxReportList.currentData()    
        if not report_id:
            return
        self.report = Report(report_xml(report_id))
        for row in range(self.ui.layoutParameters.rowCount()):
            for c in range(3):
                if self.ui.layoutParameters.itemAtPosition(row, c):
                    wg = self.ui.layoutParameters.itemAtPosition(row, c).widget()
                    self.ui.layoutParameters.removeWidget(wg)
                    wg.deleteLater()
                    wg = None
        # create parameters
        if not self.report.parameter:
            self.ui.tabWidget.setTabEnabled(pti.PARAMS, False)
        else:
            self.ui.tabWidget.setTabEnabled(pti.PARAMS, True)
            self.ui.tabWidget.setCurrentIndex(pti.PARAMS)
        for row, par in enumerate(self.report.parameter):
            label = QLabel(self.report.parameter[par].description, self)
            widget: QWidget
            match self.report.parameter[par].ptype:
                case 'list':
                    widget = QComboBox(self)
                    for k, v in self.report.parameter[par].items.items():
                        widget.addItem(v, k)
                case 'bool':
                    widget = QCheckBox(self)
                    widget.setChecked(self.report.parameter[par].value)
                case 'int':
                    widget = QSpinBox(self)
                    widget.setValue(self.report.parameter[par].value)
                case 'float':
                    widget = QDoubleSpinBox(self)
                    widget.setDecimals(2)
                    widget.setRange(-9999999.99, 9999999.99)
                    widget.setValue(self.report.parameter[par].value)
                case 'date':
                    widget = QDateEdit(self.report.parameter[par].value)
                    widget.setCalendarPopup(True)
                case 'str':
                    widget = QLineEdit(self)
                    widget.setText(self.report.parameter[par].value)
                case 'reference':
                    widget = RelationalComboBox(self)
                    widget.setFunction(referenceList[self.report.parameter[par].referenceList])
                case _:
                    raise ReportPrintError("Unable to identify parameter type")
            cast(Any, widget).param = par
            self.ui.layoutParameters.addWidget(label, row, 0)
            self.ui.layoutParameters.addWidget(widget, row, 1)
        if self.report.parameter:
            self.ui.layoutParameters.setColumnStretch(1, 1)
            self.ui.layoutParameters.setRowStretch(row + 1, 1)
        # filters already created in init only fill the field comboboxes values
        for row in range(FILTER_ROWS):
            field = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget()
            field.currentIndexChanged.disconnect(self.condIndexChanged)
            field.clear()
            field.addItem('', None) # item 0 for clear/reset
            for k, v in self.report.conditions.items():
                 field.addItem(v.description, k)
            field.currentIndexChanged.connect(self.condIndexChanged)
        # report class sorting
        self.ui.spinBoxClassSorting.setValue(get_adapt_sorting(custId))
        # restore customizations
        self.setCustomizationSetting()

    def setReportCustomizationSorting(self) -> None:
        "Set current report sorting for report class"
        if self.ui.comboBoxReportCustomizations.count() == 0:
            return
        custId = self.ui.comboBoxReportCustomizations.currentData()
        try:
            set_adapt_sorting(custId,self.ui.spinBoxClassSorting.value())
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current customization sorting updated"))
        # apply sorting
        self.reportCustomizationList()
        self.setReportCustomization(-1)  # initial settings
        
    def setUserDefault(self) -> None:
        "Set current adaptation as default for current user"
        if self.ui.comboBoxReportCustomizations.count() == 0:
            return
        if not self.reportClass:
            return
        cid = int(self.ui.comboBoxReportCustomizations.currentData())
        try:
            set_adapt_user_default('R',
                                   self.reportClass,
                                   session['user'],
                                   cid)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Critical"),
                               f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current adaptation set as default for current user"))

    def setClassDefault(self) -> None:
        "Set current adaptation as default for current class"
        if self.ui.comboBoxReportCustomizations.count() == 0:
            return
        cid = int(self.ui.comboBoxReportCustomizations.currentData())
        try:
            set_adapt_class_default(cid)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                            _tr("MessageDialog", "Critical"),
                            f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Dialog", "Current adaptation set as default for class"))


    def condIndexChanged(self, index: int) -> None:
        "Set combobox items (operator) and operand QWidget"
        if index < 0:
            return
        # get current row number
        s = self.sender()        
        if not isinstance(s, RowComboBox):
            return
        row = s.row
        # reset negate
        self.ui.layoutFilters.itemAtPosition(row, ff.NEGATE).widget().setChecked(False)
        # clear if index is zero
        if index == 0:
            # reset operator
            self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().setCurrentIndex(0)
            return
        # get field type
        ftype = self.report.conditions[self.sender().currentData()].ftype # type: ignore[attr-defined]
        if not ftype:
            return
        # set operator alternatives
        self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().clear()
        for o, d, r, w in self.FILTERING[ftype]:
            data = cast(Any, self.sender()).currentData()
            if hasattr(self.report.conditions[data], 'reference') and w == 'LIST':
                continue
            self.ui.layoutFilters.itemAtPosition(row,ff.OPERATOR).widget().addItem(d, o)
        
    def operIndexChanged(self, index: int) -> None:
        "Create a widget for field and operator"
        if index < 0:
            return
        # get current row number
        s = self.sender()        
        if not isinstance(s, RowComboBox):
            return
        row = s.row
        # clear if index is zero
        if index == 0:
            # delete previous widget (MANDATORY)
            w = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
            self.ui.layoutFilters.removeWidget(w)
            w.deleteLater()
            # add spacer
            sw = SpacerWidget(self) # spacer widget
            self.ui.layoutFilters.addWidget(sw, row,ff.OPERAND)
            return
        # get field type
        field = self.ui.layoutFilters.itemAtPosition(row,ff.FIELD).widget().currentData()
        ftype = self.report.conditions[field].ftype # type: ignore[attr-defined]
        w = self.ui.layoutFilters.itemAtPosition(row,ff.OPERAND).widget()
        nwt = self.FILTERING[ftype][index][3]
        # insert new operand widget
        widget: QSpinBox|QDoubleSpinBox|QCheckBox|QDateEdit|QDateTimeEdit|QLineEdit|QComboBox|CheckableComboBox|QWidget
        match nwt:
            case 'SB': # spinbox
                widget = QSpinBox(self)
                widget.setRange(0, 2147483647)
            case 'DSB': # double spinbox
                widget = QDoubleSpinBox(self)
                widget.setDecimals(2)
                widget.setMaximum(99999999.99)
            case 'CB': # check box
                widget = QCheckBox(self)
            case 'DE': # date edit
                widget = QDateEdit(QDate.currentDate(), self)
                widget.setCalendarPopup(True)
                widget.setMinimumDate(QDate(1800, 1, 1))
                widget.setMaximumDate(QDate(3000, 12, 31))
                widget.setDate(QDate.currentDate())
            case 'DTE': # date time edit
                widget = QDateTimeEdit(self)
                widget.setCalendarPopup(True)
                widget.setMinimumDate(QDate(1800, 1, 1))
                widget.setMaximumDate(QDate(3000, 12, 31))
                widget.setDate(QDate.currentDate())
            case 'TE': # time edit
                widget = QTimeEdit(QTime.currentTime(), self)
                #widget.setTime(QTime.currentTime())
            case 'LE': # line edit
                widget = QLineEdit(self)
            case 'LES': # line edit string list
                widget = LineEditStrings(self)
            case 'LEI': # line edit int list
                widget = LineEditInts(self)
            case 'LED': # line edit decimal list
                widget = LineEditDecimals(self)
            case 'SCB': # standard combo box
                widget = QComboBox(self)
                # for k, v in get_list(self.model.columns[fi][6]):
                #     widget.addItem(v, k)
            case 'CCB': # chackable combo box
                widget = CheckableComboBox(self)
                # for k, v in get_list(self.model.columns[fi][6]):
                #     widget.addItem(v, k)
            case 'LIST':
                # if hasattr(self.model, 'reference'):
                #     widget = QComboBox(self)
                #     for k, v in self.model.reference[field]():
                #         widget.addItem(v, k)
                # else:
                #     widget = SpacerWidget(self)
                widget = SpacerWidget(self)
            case _: # no widget required (is null/is not null)
                widget = SpacerWidget(self)
        self.ui.layoutFilters.removeWidget(w)
        w.deleteLater()
        # new widget
        self.ui.layoutFilters.addWidget(widget, row,ff.OPERAND)
        
    def generateReport(self) -> bool:
        "Generate sql query, where condition, order by expression and report"
        # get parameters current value
        if self.ui.tabWidget.isTabEnabled(0):
            self.report.parameter.clear()
            for r in range(self.ui.layoutParameters.rowCount()):
                if self.ui.layoutParameters.itemAtPosition(r, 1):
                    w = self.ui.layoutParameters.itemAtPosition(r, 1).widget()
                    match w:
                        case QCheckBox():
                            self.report.parameter[w.param] = w.isChecked() # type: ignore[attr-defined]
                        case QSpinBox():
                            self.report.parameter[w.param] = w.value() # type: ignore[attr-defined]
                        case QDoubleSpinBox():
                            self.report.parameter[w.param] = w.value() # type: ignore[attr-defined]
                        case QDateEdit():
                            self.report.parameter[w.param] = w.date() # type: ignore[attr-defined]
                        case QLineEdit():
                            self.report.parameter[w.param] = w.text() # type: ignore[attr-defined]
                        case RelationalComboBox():
                            self.report.parameter[w.param] = w.currentData() # type: ignore[attr-defined] #(w.currentData(), w.currentText())
                        case QComboBox():
                            self.report.parameter[w.param] = w.currentData() # type: ignore[attr-defined] #(w.currentData(), w.currentText())
                        case _:
                            raise ReportException("Unknown object type")
        # get filters
        condition = []
        argument = []
        v: list|str|int|float|QDate|QDateTime|QTime|bool|None
        for r in range(FILTER_ROWS):
            if (hasattr(self.ui.layoutFilters.itemAtPosition(r,ff.FIELD), 'widget') and  # can happended if no filters
                (self.ui.layoutFilters.itemAtPosition(r,ff.FIELD).widget().currentIndex() != 0 and  # field
                 self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().currentIndex() != 0)):  # operator
                fl = self.ui.layoutFilters.itemAtPosition(r,ff.FIELD).widget().currentData()
                ty = self.report.conditions[fl].ftype
                ng = self.ui.layoutFilters.itemAtPosition(r, ff.NEGATE).widget().isChecked()
                op = self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().currentData()
                oi = self.ui.layoutFilters.itemAtPosition(r,ff.OPERATOR).widget().currentIndex()
                wd = self.ui.layoutFilters.itemAtPosition(r,ff.OPERAND).widget()
                match wd:
                    case CheckableComboBox():
                        v = wd.currentData() # list
                    case QComboBox():
                        v = wd.currentData()
                    case LineEditStrings()|LineEditInts()|LineEditDecimals(): # lists
                        v = wd.value()
                    case QLineEdit():
                        v = wd.text()
                    case QSpinBox()|QDoubleSpinBox():
                        v = wd.value()
                    case QDateEdit():
                        v = wd.date()
                    case QTimeEdit(): # time before datetime because is subclass of QDateTimeEdit
                        v = wd.time()
                    case QDateTimeEdit():
                        v = wd.dateTime()
                    case QCheckBox():
                        if wd.checkState() == Qt.CheckState.Checked:
                            v = True
                        else:
                            v = False
                    case _:
                        v = None
                arg: Any
                match self.FILTERING[ty][oi][2]:
                    case 0:
                        cond = f"{fl} {op} %s"
                        arg = v
                    case 1:
                        cond = f"{fl} {op}"
                        arg = None
                    case 2:
                        cond = f"{fl} {op}"
                        arg = v.split() if isinstance(v, str) else v
                    case 3:
                        cond = f"{fl} {op}"
                        arg = v
                    case _:
                        pass
                if ng:
                    cond = f"NOT {cond}"
                condition.append(cond)
                argument.append(arg)
        self.where = list(zip(condition, argument))
        #print("WHERE:", self.where)
        # create self.data
        if self.report.query:
            try:
                 # cursor wait
                QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
                self.report.data = report_query(self.report, self.where)
            except PyAppDBError as er:
                msg = _tr('PrintDialog', 'Error executing database query')
                msg = f"{msg}\n{er}"
                MessageBoxCritical(self,
                                   _tr('PrintDialog', 'Database error'),
                                   msg)
                return False
            finally:
                # cursor restore
                QApplication.restoreOverrideCursor()
        if not self.report.data:
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Dialog', "No data to render"))
            return False
        # cursor wait
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        # generate a report
        self.report.generate()
        # cursor restore
        QApplication.restoreOverrideCursor()
        return True

    def printPreview(self) -> None:
        "Generate report and show a print preview"
        if not self.generateReport():
            return
        # print preview
        dialog = QPrintPreviewDialog(self)
        dialog.setWindowFlags(Qt.WindowType.Dialog|
                              Qt.WindowType.WindowMinMaxButtonsHint|
                              Qt.WindowType.WindowCloseButtonHint)
        dialog.setWindowTitle(_tr("Dialog", "Print preview"))
        # open in fit width
        pp = dialog.findChild(QPrintPreviewWidget)
        if pp:
            pp.setZoomMode(QPrintPreviewWidget.ZoomMode.FitToWidth)
        # start
        dialog.paintRequested.connect(self.report.print)
        try:
            dialog.exec()
        except ReportException as er:
            QMessageBox.critical(self,
                                 _tr("Dialog", "Critical"),
                                 str(er))

    def printReport(self) -> None:
        "Generate report, choose a printer and print"
        if not self.generateReport():
            return
        # print with printer configuration
        printer = QPrinter(QPrinterInfo.printerInfo(self.ui.comboBoxPrinters.currentText()))
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            try:
                self.report.print(printer)
            except ReportException as er:
                QMessageBox.critical(self,
                                     _tr("Dialog", "Critical"),
                                     str(er))

    def printDirect(self) -> None:
        "Generated report and print"
        if not self.generateReport():
            return
        printer = QPrinter(QPrinterInfo.printerInfo(self.ui.comboBoxPrinters.currentText()))
        try:
            self.report.print(printer)
        except ReportException as er:
            QMessageBox.critical(self,
                                 _tr("Dialog", "Critical"),
                                 str(er))

    def printPDF(self) -> None:
        "Generated report and a pdf file, optionally open it"
        if not self.generateReport():
            return
        if self.ui.lineEditDirectory.text() == "":
            MessageBoxCritical(self,
                               _tr('MessageDialog', 'Critical'),
                               _tr('Dialog', "Export directory not set"))
            return
        if self.ui.lineEditFileName.text() == "":
            MessageBoxCritical(self,
                               _tr('MessageDialog', 'Critical'),
                               _tr('Dialog', "File name not set"))
            return
        file_name = self.ui.lineEditDirectory.text() + "/" + self.ui.lineEditFileName.text() + ".pdf"
        if QFile(file_name).exists():
            if QMessageBox.question(self,
                                    _tr('MessageDialog', 'Question'),
                                    _tr('Dialog', "File {} exists, overwrite ?").format(file_name),
                                    QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
                                    ) == QMessageBox.StandardButton.No:
                return
        paintDevice = QPdfWriter(file_name)
        paintDevice.setResolution(600) # platform independent, better to set it before setting pdf version
        paintDevice.setPdfVersion(self.ui.comboBoxPDFVersion.currentData())
        paintDevice.setResolution(self.ui.spinBoxResolution.value())
        try:
            self.report.print(paintDevice)
        except ReportException as er:
            QMessageBox.critical(self,
                                 _tr("Dialog", "Critical"),
                                 str(er))
            return
        # open file if requested
        if self.ui.checkBoxOpenPDF.isChecked():
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr('Dialog', "PDF file created"))

    def selectDirectoryClicked(self) -> None:
        "Select export directory"
        dirname = QFileDialog.getExistingDirectory(
            self,
            _tr('Dialog', "Select export directory"),
            self.ui.lineEditDirectory.text(),
            QFileDialog.Option.ShowDirsOnly
        )
        if dirname:
            self.ui.lineEditDirectory.setText(dirname)

    def done(self, r: int) -> None:
        "Save local settings on exit, even in accetp/reject/finishe"
        # save settings
        st = QSettings(self)
        st.setValue(f"PrintDialog/Geometry/{self.reportClass}", self.saveGeometry())
        st.setValue("PrintDialog/PDFDirectory", self.ui.lineEditDirectory.text())
        st.setValue("PrintDialog/PDFOpenFileAfterCreate", self.ui.checkBoxOpenPDF.isChecked())
        st.setValue("PrintDialog/PDFVersion", self.ui.comboBoxPDFVersion.currentIndex())
        st.setValue("PrintDialog/PDFResolution", self.ui.spinBoxResolution.value())
        super().done(r)


class _DateTimeInputDialog(QDialog):
    "Input dialog for one date value"

    def __init__(self, parent: QWidget|None = None) -> None:
        "Initialize"
        super().__init__(parent)
        self.ui = Ui_DateTimeInputDialog()
        self.ui.setupUi(self)
        self.ui.labelText.setText(_tr('Dialog', "Select a date:"))
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
       
def DateTimeInputDialog(text: str) -> tuple[QDateTime | None, bool] :
    "Get a date value from user"
    dialog = _DateTimeInputDialog()
    dialog.ui.labelText.setText(text)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return dialog.ui.dateTimeEdit.dateTime(), True
    else:
        return None, False