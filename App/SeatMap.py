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

"""Tables

This module provides a form to manage tables archive


"""

# standard library
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QColorDialog
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QButtonGroup
from PySide6.QtWidgets import QSizePolicy

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Database.SeatMap import table_delete
from App.Database.Models import SeatMapModel
from App.Database.Setting import SettingClass
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Ui.SeatMapWidget import Ui_SeatMapWidget
from App.Widget.Form import  FormManager
from App.Widget.Control import ButtonSeat
from App.Widget.Control import ButtonColor
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import ColorDelegate
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Dialog import PrintDialog


# logger
logger = logging.getLogger(__name__)

(ID, TABLE_CODE, ROW, COLUMN, TEXT_COLOR, BACKGROUND_COLOR,
 IS_UNAVAILABLE, IS_OBSOLETE, 
 USER_INS, DATE_INS, USER_UPD, DATE_UPD) = range(12)

EDIT, PREVIEW = range(2)


def seatMap(action: QAction, checked: bool = False) -> None:
    "Manage seat map"
    logger.info('Starting seat map Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    tw = SeatMapForm(mw, title, auth)
    tw.reload()
    mw.addTab(title, tw)
    logger.info('Tables Form added to main window')


class SeatMapForm(FormManager[Ui_SeatMapWidget]):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = SeatMapModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        self.reloadConfirmation = False
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, False, True, True)
        self.ui = Ui_SeatMapWidget()
        self.ui.setupUi(self)
        self.view = self.ui.tableView  # required for formviewmanager
        self.ui.tableView.setModel(model)
        self.ui.tableView.setLayoutName('SeatMap')
        # self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView.activateWindow()
        self.ui.tableView.setSortingEnabled(True)
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        # custom delegates
        self.ui.tableView.setItemDelegateForColumn(TABLE_CODE, GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ROW, GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(COLUMN, GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TEXT_COLOR, ColorDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(BACKGROUND_COLOR, ColorDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(IS_OBSOLETE, BooleanDelegate(self))
        # map view to mapper and mapper to view
        self.ui.tableView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)
        self.mapper.currentIndexChanged.connect(self.ui.tableView.selectRow)
        self.setting = SettingClass()
        # generate tables
        self.bgcolor = '#007f00' # default background color for generated tables
        self.txcolor = '#FFFFFF' # default text color for generated tables
        # bg colors buttons
        self.bgbc = QButtonGroup(self)
        for i, c in ((self.ui.pushButtonBGC1, '#00007f'),
                     (self.ui.pushButtonBGC2, '#005500'),
                     (self.ui.pushButtonBGC3, '#0055ff'),
                     (self.ui.pushButtonBGC4, '#55aaff'),
                     (self.ui.pushButtonBGC5, '#55007f'),
                     (self.ui.pushButtonBGC6, '#9d9d00'),
                     (self.ui.pushButtonBGC7, '#d10000'),
                     (self.ui.pushButtonBGC8, '#478f6a'),
                     (self.ui.pushButtonBGC9, '#a33651'),
                     (self.ui.pushButtonBGC10, '#FF0000')):
            i.setBackgroundColor(c)
            self.bgbc.addButton(i)
        self.ui.spinBoxRows.setValue(self.setting['table_list_rows'])
        self.ui.spinBoxColumns.setValue(self.setting['table_list_columns'])
        self.ui.spinBoxSpacing.setValue(self.setting['table_list_spacing'])
        # signal/slot
        self.bgbc.buttonClicked.connect(self.backgroundColorButtonClicked)
        self.ui.pushButtonChooseBackground.clicked.connect(self.chooseBackground)
        self.ui.pushButtonChooseText.clicked.connect(self.chooseText)
        self.ui.pushButtonGenerateTables.clicked.connect(self.generateTableNumbers)
        self.ui.pushButtonDeleteAll.clicked.connect(self.deleteAll)
        #self.ui.pushButtonGenerateTables.clicked.connect(self.generateTables)
        self.ui.pushButtonPreview.clicked.connect(self.showPreview)
        # initial value
        self.ui.pushButtonPreview.setText(_tr("StandTableSeatMap", "Swith to Preview"))
        self.ui.groupBoxBaseGeometry.setVisible(False)
        self.ui.groupBoxMinimunSize.setVisible(False)
        # scripting init
        self.script = scriptInit(self)
        #self.updateExample()

    @scriptMethod
    def new(self) -> None:
        super().new()

    @scriptMethod
    def save(self) -> None:
        super().save()

    @scriptMethod
    def delete(self) -> None:
        "Delete and update current table"
        table = self.model.data(self.model.index(self.mapper.currentIndex(), TABLE_CODE))
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('Table', "Are you sure you want to delete table {} ?".format(table)),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    @scriptMethod
    def deleteAll(self, checked: bool = False) -> None:
        "Delete all tables"
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                _tr("Table", "Are you sure you want to delete ALL tables ?"),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No
                                ) == QMessageBox.StandardButton.Yes:
            with gui_exception_context(self, _tr("SeatMap", "Delete all tables")):
                table_delete()
                self.ui.tableView.model().select()
                self.mapper.toFirst()

    @scriptMethod
    def reload(self) -> None:
        super().reload()
    
    def showPreview(self, clicked: bool) -> None:
        "Show/Hide preview of th tables/Buttons available in the model"
        if clicked:
            self.ui.stackedWidget.setCurrentIndex(PREVIEW)
            self.ui.pushButtonPreview.setText(_tr("StandTable", "Back to Edit"))
            self.ui.groupBoxBaseGeometry.setVisible(True)
            self.ui.groupBoxMinimunSize.setVisible(True)
        else:
            self.ui.stackedWidget.setCurrentIndex(EDIT)
            self.ui.pushButtonPreview.setText(_tr("StandTable", "Swith to Preview"))
            self.ui.groupBoxBaseGeometry.setVisible(False)
            self.ui.groupBoxMinimunSize.setVisible(False)
            return
        # save geometry
        self.setting['table_list_rows'] = self.ui.spinBoxRows.value()
        self.setting['table_list_columns'] = self.ui.spinBoxColumns.value()
        self.setting['table_list_spacing'] = self.ui.spinBoxSpacing.value()
        # create a preview
        # buttons for tables
        # clean first
        while self.ui.gridLayoutPreview.count():
            w = self.ui.gridLayoutPreview.takeAt(0).widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        # new widets from model, don't need to save before preview
        for r in range(self.model.rowCount() + 1):
            cod = self.model.index(r, TABLE_CODE).data()
            row = self.model.index(r, ROW).data()
            col = self.model.index(r, COLUMN).data()
            tc = self.model.index(r, TEXT_COLOR).data()
            bc = self.model.index(r, BACKGROUND_COLOR).data()
            un = True if self.model.index(r, IS_UNAVAILABLE).data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked else False
            ob = True if self.model.index(r, IS_OBSOLETE).data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked else False
            b = ButtonSeat(self, 
                           cod, 
                           QFont(self.setting['table_list_font_family'] or "Arial",
                                 int(self.setting['table_list_font_size'] or 7),
                                 QFont.Weight.Bold if not un else QFont.Weight.Normal),
                           tc, 
                           bc,
                           un)
            # show only not obsolete tables
            if row is None or col is None or ob is True:
                continue
            self.ui.gridLayoutPreview.addWidget(b, row, col)
        # fill the remaining cells of gl with an empty widget
        for r in range(1, int(self.setting['table_list_rows'] or 0) + 1):
            for c in range(1, int(self.setting['table_list_columns'] or 0) + 1):
                if self.ui.gridLayoutPreview.itemAtPosition(r, c) is None:
                    w = QWidget(self)
                    w.setMinimumWidth(self.ui.spinBoxMinWidth.value())
                    w.setMinimumHeight(self.ui.spinBoxMinHeight.value())
                    w.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.ui.gridLayoutPreview.addWidget(w, r, c)
                    
    @scriptMethod
    def print(self) -> None:
        "Tables report"
        dialog = PrintDialog(self, 'TABLE')
        dialog.show()
        
    def backgroundColorButtonClicked(self, button: ButtonColor) -> None:
        "Choose the button's background color for example buttons"
        color = QColorDialog.getColor(Qt.GlobalColor.white, self)
        if not color.isValid():
            return
        button.setBackgroundColor(color.name())

    def chooseBackground(self) -> None:
        "Choose the background color"
        color = QColorDialog.getColor(Qt.GlobalColor.white, self)
        if not color.isValid():
            return
        self.bgcolor = color.name()
        self.ui.pushButtonExample.setBackgroundColor(self.bgcolor)

    def chooseText(self) -> None:
        "Choose the text color"
        color = QColorDialog.getColor(Qt.GlobalColor.black, self)
        if not color.isValid():
            return
        self.txcolor = color.name()
        self.ui.pushButtonExample.setTextColor(self.txcolor)

    @scriptMethod
    def generateTableNumbers(self) -> None:
        "Generate tables code and position and add to table list"
        startRow = self.ui.spinBoxStartRow.value()
        rows = self.ui.spinBoxNumRows.value()
        columns = self.ui.spinBoxNumColumns.value()
        prefix = self.ui.lineEditPrefix.text()
        suffix = self.ui.lineEditSuffix.text()
        rowPadding = self.ui.spinBoxRowPadding.value()
        columnPadding = self.ui.spinBoxColumnPadding.value()
        textColor = self.txcolor
        backgroundColor = self.bgcolor
        colors = [i.backgroundColor.name() for i in (self.ui.pushButtonBGC1, self.ui.pushButtonBGC2,
                                              self.ui.pushButtonBGC3, self.ui.pushButtonBGC4,
                                              self.ui.pushButtonBGC5, self.ui.pushButtonBGC6,
                                              self.ui.pushButtonBGC7, self.ui.pushButtonBGC8,
                                              self.ui.pushButtonBGC9, self.ui.pushButtonBGC10)]
        colorIndex = 0
        if self.ui.radioButtonRowColumn.isChecked():
            for r in range(startRow, startRow + rows):
                if self.ui.checkBoxChangeBackgroundColor.isChecked():
                    backgroundColor = colors[colorIndex]
                    colorIndex += 1
                    if colorIndex == 10:
                        colorIndex = 0
                for c in range(1, columns + 1):
                    code = prefix + str(r).zfill(rowPadding) + str(c).zfill(columnPadding) + suffix
                    self.model.insertRow(self.model.rowCount())
                    modelRow = self.model.rowCount() - 1
                    self.model.setData(self.model.index(modelRow, TABLE_CODE), code)
                    self.model.setData(self.model.index(modelRow, ROW), r)
                    self.model.setData(self.model.index(modelRow, COLUMN), c)
                    self.model.setData(self.model.index(modelRow, TEXT_COLOR), textColor)
                    self.model.setData(self.model.index(modelRow, BACKGROUND_COLOR), backgroundColor)
                    self.model.setData(self.model.index(modelRow, IS_OBSOLETE), False)

        else:
            for c in range(1, columns + 1):
                if self.ui.checkBoxChangeBackgroundColor.isChecked():
                    backgroundColor = colors[colorIndex]
                    colorIndex += 1
                    if colorIndex == 10:
                        colorIndex = 0
                for r in range(startRow, rows + 1):
                    code = prefix + str(c).zfill(columnPadding) + str(r).zfill(rowPadding) + suffix
                    self.model.insertRows(self.model.rowCount(), 1)
                    modelRow = self.model.rowCount() - 1
                    self.model.setData(self.model.index(modelRow, TABLE_CODE), code)
                    self.model.setData(self.model.index(modelRow, ROW), r)
                    self.model.setData(self.model.index(modelRow, COLUMN), c)
                    self.model.setData(self.model.index(modelRow, TEXT_COLOR), textColor)
                    self.model.setData(self.model.index(modelRow, BACKGROUND_COLOR), backgroundColor)
                    self.model.setData(self.model.index(modelRow, IS_OBSOLETE), False)
