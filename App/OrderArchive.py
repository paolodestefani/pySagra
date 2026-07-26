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

"""Order archive

This module provides form and related classes for manage order archive

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QCheckBox

# application modules
from App import session
from App.Database.Setting import Setting
from App.Database.Printer import get_printer_name
from App.Database.Department import get_department_printer_class
from App.Database.Department import department_list
from App.Database.Department import get_department_desc
from App.Database.Models import OrderHeaderIndexModel
from App.Database.Models import OrderHeaderModel
from App.Database.Models import OrderHeaderDepartmentModel
from App.Database.Models import OrderLineModel
from App.Database.Models import OrderDepartmentTreeModel
from App.Database.Lookup import item_all_lookup
from App.Database.Lookup import department_lookup
from App.Widget.Dialog import MessageBoxCritical
from App.Widget.Dialog import PrintDialog
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import QuantityDelegate
from App.Widget.Delegate import AmountDelegate
from App.Widget.Delegate import PriceDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import TimeDelegate
from App.Widget.Form import FormIndexManager
from App.Ui.OrderWidget import Ui_OrderWidget
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Report.ReportEngine import ReportException
from App.Report.ReportEngine import ReportNoDataError
from App.Report.Order import printOrderReport
from App.Report.Order import printOrderCoverReport
from App.Report.Order import printOrderDepartmentReport


# logger
logger = logging.getLogger(__name__)

# index model order header
class ordi(IntEnum):
    ID              = 0
    EVENT           = 1
    DESCEVENT       = 2
    DATE_TIME       = 3
    NUMBER          = 4
    DATE            = 5
    TIME            = 6
    STAT_DATE       = 7
    STAT_DAYPART    = 8
    CASH_DESK       = 9
    DELIVERY        = 10
    EP              = 11
    WO              = 12
    TABLE           = 13
    CUSTOMER        = 14
    COVERS          = 15
    AMOUNT          = 16
    DISCOUNT        = 17
    CASH            = 18
    CHANGE          = 19
    STATUS          = 20
    FULFILLMENT     = 21
    USER_INS        = 22
    DATE_INS        = 23
    USER_UPD        = 24
    DATE_UPD        = 25

# model order header
class ordh(IntEnum):
    ID              = 0
    EVENT           = 1
    DATE_TIME       = 2
    NUMBER          = 3
    DATE            = 4
    TIME            = 5
    STAT_DATE       = 6
    STAT_DAYPART    = 7
    CASH_DESK       = 8
    DELIVERY        = 9
    EP              = 10
    WO              = 11
    TABLE           = 12
    CUSTOMER        = 13
    CONTACT         = 14
    COVERS          = 15
    AMOUNT          = 16
    DISCOUNT        = 17
    CASH            = 18
    CHANGE          = 19
    STATUS          = 20
    FULFILLMENT     = 21
    USER_INS        = 22
    DATE_INS        = 23
    USER_UPD        = 24
    DATE_UPD        = 25

# model order header department
class ordhd(IntEnum):
    ID              = 0
    ID_HEADER       = 1
    DEPARTMENT      = 2
    NOTE            = 3
    OTHER           = 4
    BARCODE         = 5
    FULFILLMENT     = 6
    USER_INS        = 7
    DATE_INS        = 8
    USER_UPD        = 9
    DATE_UPD        = 10

# model order detail
class ordd(IntEnum):
    ID              = 0
    ID_HEADER       = 1
    ITEM            = 2
    VARIANTS        = 3
    QUANTITY        = 4
    PRICE           = 5
    AMOUNT          = 6

# tree model order detail department
class orddd(IntEnum):
    DEPARTMENT      = 0
    ITEM            = 1
    VARIANTS        = 2
    QUANTITY        = 3
    PARENT          = 4
    CHILD           = 5



def deliveryType():
    return [('T', _tr('OrderArchive', 'Table')),
            ('A', _tr('OrderArchive', 'Take Away'))]


def orderStatus():
    return [('A', _tr('OrderArchive', 'Acquired')),
            ('I', _tr('OrderArchive', 'In progress')),
            ('P', _tr('OrderArchive', 'Processed'))]




def orderArchive(action: QAction, checked: bool = False) -> None:
    "Manage order archive"
    logger.info('Starting order archive Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderArchive', 'No access right to this archive'))
        return
    ow = OrderForm(mw, title, auth)
    #ow.reload() # reload after filtering
    mw.addTab(title, ow)
    logger.info('Order archive Form added to main window')


class OrderForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = OrderHeaderModel(self)
        idxModel = OrderHeaderIndexModel(self)
        modelHeaDep = OrderHeaderDepartmentModel(self)
        modelDet = OrderLineModel(self)
        modelTreeDep = OrderDepartmentTreeModel(self)
        #modelTreeDep.select()
        self.setModel(model, idxModel)
        self.addDetailRelation(modelHeaDep, ordi.ID, ordhd.ID_HEADER)
        self.addDetailRelation(modelDet, ordi.ID, ordd.ID_HEADER)
        self.addDetailRelation(modelTreeDep, ordi.ID, orddd.DEPARTMENT)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, True)
        self.ui = Ui_OrderWidget()
        self.ui.setupUi(self)
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('OrderArchiveIndex') 
        self.ui.tableView.setItemDelegateForColumn(ordi.DELIVERY, RelationDelegate(self, deliveryType))
        self.ui.tableView.setItemDelegateForColumn(ordi.TIME, TimeDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ordi.AMOUNT, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ordi.DISCOUNT, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ordi.CASH, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ordi.CHANGE, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ordi.STATUS, RelationDelegate(self, orderStatus))
        # mapper mappings
        self.mapper.addMapping(self.ui.lineEditCashDesk, ordh.CASH_DESK)
        self.mapper.addMapping(self.ui.spinBoxNumber, ordh.NUMBER)
        self.mapper.addMapping(self.ui.dateEditDate, ordh.DATE)
        self.mapper.addMapping(self.ui.timeEditTime, ordh.TIME)
        #self.ui.comboBoxDelivery.setItemList((('T', _tr('OrderArchive', 'Table')),
        #                                      ('A', _tr('OrderArchive', 'Take-away'))))
        self.ui.comboBoxDelivery.setItemList(deliveryType())
        self.mapper.addMapping(self.ui.checkBoxElectronicPayment, ordh.EP)
        self.mapper.addMapping(self.ui.checkBoxWebOrder, ordh.WO)
        self.mapper.addMapping(self.ui.comboBoxDelivery, ordh.DELIVERY, b"modelDataStr")
        self.mapper.addMapping(self.ui.lineEditTableNumber, ordh.TABLE)
        self.mapper.addMapping(self.ui.spinBoxCovers, ordh.COVERS)
        self.mapper.addMapping(self.ui.doubleSpinBoxTotalAmount, ordh.AMOUNT, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.doubleSpinBoxDiscount, ordh.DISCOUNT, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.doubleSpinBoxCash, ordh.CASH, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.doubleSpinBoxChange, ordh.CHANGE, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.lineEditCustomerName, ordh.CUSTOMER)
        self.mapper.addMapping(self.ui.lineEditCustomerContact, ordh.CONTACT)
        self.ui.comboBoxStatus.setItemList(orderStatus())
        self.mapper.addMapping(self.ui.comboBoxStatus, ordh.STATUS, b"modelDataStr")
        self.mapper.addMapping(self.ui.dateTimeEditFullfillment, ordh.FULFILLMENT, b"modelDataDateTime")
        # details tableView
        self.ui.tableViewDetails.setModel(modelDet)
        self.ui.tableViewDetails.setLayoutName('OrderArchiveDetail')
        self.ui.tableViewDetails.setItemDelegateForColumn(ordd.ITEM, RelationDelegate(self, item_all_lookup))
        self.ui.tableViewDetails.setItemDelegateForColumn(ordd.QUANTITY, QuantityDelegate(self))
        self.ui.tableViewDetails.setItemDelegateForColumn(ordd.PRICE, PriceDelegate(self))
        self.ui.tableViewDetails.setItemDelegateForColumn(ordd.AMOUNT, AmountDelegate(self))
        # details department treeView
        self.ui.treeViewDepartmentDetails.setModel(modelTreeDep)
        self.ui.treeViewDepartmentDetails.setItemDelegate(GenericDelegate(self))
        self.ui.treeViewDepartmentDetails.header().resizeSection(orddd.DEPARTMENT, 250) # department
        self.ui.treeViewDepartmentDetails.header().resizeSection(orddd.ITEM, 300) # item
        self.ui.treeViewDepartmentDetails.header().resizeSection(orddd.VARIANTS, 300) # variants
        self.ui.treeViewDepartmentDetails.setItemDelegateForColumn(orddd.QUANTITY, QuantityDelegate(self))
        self.ui.treeViewDepartmentDetails.hideColumn(orddd.PARENT)
        self.ui.treeViewDepartmentDetails.hideColumn(orddd.CHILD)
        # header department tableView
        self.ui.tableViewDepartmentHeader.setModel(modelHeaDep)
        self.ui.tableViewDepartmentHeader.setLayoutName('OrderArchiveDepartment')
        self.ui.tableViewDepartmentHeader.setItemDelegateForColumn(ordhd.DEPARTMENT, RelationDelegate(self, department_lookup))
        # store setting on form creation
        self.setting = Setting()
        # decimals on amount
        decs = self.setting['amount_decimal_places']
        self.ui.doubleSpinBoxTotalAmount.setDecimals(decs)
        self.ui.doubleSpinBoxDiscount.setDecimals(decs)
        self.ui.doubleSpinBoxCash.setDecimals(decs)
        self.ui.doubleSpinBoxChange.setDecimals(decs)
        # enable/disable widget satus
        self.ui.checkBoxPrintCustomerCopy.setDisabled(True)
        self.ui.checkBoxPrintCoverCopy.setDisabled(True)
        self.mapper.currentIndexChanged.connect(self.updateFormWidgets)
        # create departments checkboxes
        self.depCopy = dict()
        for i, dep in department_list(only_active=False, include_menu=False):
            self.depCopy[i] = QCheckBox(dep, self)
            self.depCopy[i].setEnabled(self.setting['print_department_copy'])
            self.ui.groupBoxReprint.layout().addWidget(self.depCopy[i])
        self.ui.pushButtonPrint.clicked.connect(self.reprint)
        # start with open filters dialog
        self.setFilters()
        self.toFirst()
        # scripting init
        self.script = scriptInit(self)

    def updateFormWidgets(self):
        "Enable/disable widgets"
        self.ui.checkBoxPrintCustomerCopy.setEnabled(self.setting['print_customer_copy'])
        row = self.mapper.currentIndex()
        delivery_type = self.model.data(self.model.index(row, ordh.DELIVERY), Qt.ItemDataRole.EditRole)
        if delivery_type == 'T':
            if self.setting['print_cover_copy']:
                self.ui.checkBoxPrintCoverCopy.setEnabled(True)
            self.ui.lineEditTableNumber.setEnabled(True)
        else:
            self.ui.checkBoxPrintCoverCopy.setDisabled(True)
            self.ui.lineEditTableNumber.setDisabled(True)

    @scriptMethod
    def new(self):
        super().new()

    @scriptMethod
    def save(self):
        super().save()

    @scriptMethod
    def delete(self):
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('OrderArchive', "Delete current order ?"),
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        super().delete()

    @scriptMethod
    def reload(self):
        super().reload()

    @scriptMethod
    def print(self):
        "Print order list"
        dialog = PrintDialog(self, 'ORDER_LIST')
        dialog.show()

    @scriptMethod
    def reprint(self, checked=False):
        "Print again the selected order copy"
        current_row = self.mapper.currentIndex()
        if current_row < 0:
            return
        no_print = True
        # PRINT ORDER
        setting = Setting()
        # get order id
        ti = self.model.data(self.model.index(self.mapper.currentIndex(), ordh.ID))
        # customer copy
        if self.ui.checkBoxPrintCustomerCopy.isChecked():
            printer = get_printer_name(setting['customer_printer_class'], session['hostname'])
            try:
                printOrderReport(ti, printer)
            except ReportNoDataError:
                QMessageBox.information(self,
                                        _tr('MessageDialog', "Information"),
                                        _tr('OrderArchive', "No data to render"))
            self.ui.checkBoxPrintCustomerCopy.setChecked(False)
            no_print = False
        # covers copy
        if self.ui.checkBoxPrintCoverCopy.isChecked():
            if self.ui.spinBoxCovers.value() == 0:
                QMessageBox.information(self,
                                        _tr('MessageDialog', "Information"),
                                        _tr('OrderArchive', "No covers, not print required"))
                return
            printer = get_printer_name(setting['cover_printer_class'], session['hostname'])
            try:
                printOrderCoverReport(ti, printer)
            except ReportNoDataError:
                QMessageBox.information(self,
                                        _tr('MessageDialog', "Information"),
                                        _tr('OrderArchive', "No data to render"))
            self.ui.checkBoxPrintCoverCopy.setChecked(False)
            no_print = False
        # departments copies
        if setting['print_department_copy']:
            for i in self.depCopy:
                if self.depCopy[i].isChecked():
                    prncls = get_department_printer_class(i)
                    if not prncls:
                        msg = _tr('OrderArchive',
                                  "No printer class set for this department, skipping")
                        QMessageBox.warning(self,
                                            _tr('MessageDialog', "Warning"),
                                            msg)
                        self.depCopy[i].setChecked(False)
                        continue
                    printer = get_printer_name(prncls, session['hostname'])
                    try:
                        printOrderDepartmentReport(ti, i, printer)
                    except ReportNoDataError:
                        QMessageBox.information(self,
                                                _tr('MessageDialog', "Information"),
                                                _tr('OrderArchive', "No data to render"))
                    except ReportException as er:
                        MessageBoxCritical(self,
                                           _tr('MessageDialog', "Critical"),
                                           _tr('OrderArchive', "Error printing department copy"),
                                           str(er),
                                           )
                    self.depCopy[i].setChecked(False)
                    no_print = False
        # nothing selected
        if no_print:
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('OrderArchive', "No print has been selected"))
            
