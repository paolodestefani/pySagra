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

"""Web orders

This module provide a form for manage web orders


"""

# standard library
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QVBoxLayout

# application modules
from App import session
from App import currentAction
from App.Database.Exceptions import PyAppDBError
from App.Database.Models import WebOrderHeaderModel
from App.Database.Models import WebOrderLineModel
from App.Database.WebOrder import delete_web_order
from App.Database.WebOrder import web_order_totals
from App.Database.CodeDescriptionList import current_item_cdl
from App.Database.Setting import SettingClass
from App.Widget.Delegate import DecimalDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Form import FormManager
from App.Ui.WebOrderWidget import Ui_WebOrderWidget
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod



(ID, DATETIME, DELIVERY, TABLE, CUSTOMER, COVERS, AMOUNT, PROCESSED) = range(8)
(D_ID, D_IDHEADER, D_ITEM, D_QUANTITY, D_PRICE) = range(5)


def deliveryType():
    return [('T', _tr('WebOrder', 'Table')),
            ('A', _tr('WebOrder', 'Take-away'))]


def webOrder() -> None:
    "Manage web orders"
    logging.info('Starting web orders form')
    mw = session['mainwin']
    title = currentAction['app_file_web_order'].text()
    auth = currentAction['app_file_web_order'].data()
    wow = WebOrderForm(mw, title, auth)
    wow.reload()
    mw.addTab(title, wow)
    logging.info('Web orders form added to main window')


class WebOrderForm(FormManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = WebOrderHeaderModel()
        modelDetail = WebOrderLineModel()
        self.setModel(model)
        self.addDetailRelation(modelDetail, ID, D_IDHEADER)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, True)
        self.ui = Ui_WebOrderWidget()
        self.ui.setupUi(self)
        # layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.addWidget(self.ui)
        # self.setLayout(layout)
        self.setting = SettingClass()
        # web order header
        self.ui.tableViewHeader.setModel(model)
        self.ui.tableViewHeader.setLayoutName('webOrder')
        self.ui.tableViewHeader.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableViewHeader.setItemDelegateForColumn(DELIVERY, RelationDelegate(self, deliveryType))
        self.ui.tableViewHeader.setItemDelegateForColumn(AMOUNT, DecimalDelegate(self, currency=True))
        self.ui.tableViewHeader.setItemDelegateForColumn(PROCESSED, BooleanDelegate(self))
        # web order detail
        self.ui.tableViewDetails.setModel(modelDetail)
        self.ui.tableViewDetails.setLayoutName('webOrderDetail')
        self.ui.tableViewDetails.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableViewDetails.setItemDelegateForColumn(D_ITEM, RelationDelegate(self, current_item_cdl))
        self.ui.tableViewDetails.setItemDelegateForColumn(D_QUANTITY, DecimalDelegate(self, self.setting['quantity_decimal_places']))
        self.ui.tableViewDetails.setItemDelegateForColumn(D_PRICE, DecimalDelegate(self, currency=True))
        # map view to mapper and mapper to view
        #self.ui.tableViewHeader.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)
        #self.mapper.currentIndexChanged.connect(self.ui.tableViewHeader.selectRow)
        # signal/slot mappings
        # self.ui.lineEditBarcode.editingFinished.connect(self.findWebOrder)
        self.ui.pushButtonDelete.clicked.connect(self.deleteOrders)
        self.model.dataChanged.connect(self.recalcTotals)
        # scripting init
        self.script = scriptInit(self)

    @scriptMethod
    def reload(self):
        super().reload()

    @scriptMethod
    def deleteOrders(self, checked=False):
        "Delete web orders not processed or all"
        if self.ui.checkBoxIncludeNotProcessed.isChecked():
            question = _tr('WebOrder', "Are you sure you want to delete all web orders ?")
        else:
            question = _tr('WebOrder', "Are you sure you want to delete unprocessed web orders ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                question,
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return

        try:
            delete_web_order(self.ui.checkBoxIncludeNotProcessed.isChecked())
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', 'Critical'),
                                 f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('WebOrder', 'Web orders deleted'))
        self.reload()

    @scriptMethod
    def recalcTotals(self, topLeft=None, bottomRight=None, roles=None):
        "Recalc totale and set lcd indicator vaoues"
        total, processed, unprocessed = web_order_totals()
        self.ui.lcdNumberTotal.display(total)
        self.ui.lcdNumberProcessed.display(processed)
        self.ui.lcdNumberUnprocessed.display(unprocessed)
