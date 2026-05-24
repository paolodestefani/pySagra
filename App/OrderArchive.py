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
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QVBoxLayout
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

# index model order header
(I_ID, EVENT, I_DATETIME, I_NUMBER, I_DATE, I_TIME, I_STATDATE, I_STATDAYPART, I_CASHDESK,
 I_DELIVERY, I_EP, I_TABLE, I_CUSTOMER, I_COVERS, I_AMOUNT, I_DISCOUNT, I_CASH, I_CHANGE,
 I_STATUS, I_FULLFILLMENT, 
 I_USER_INS, I_DATE_INS, I_USER_UPD, I_DATE_UPD) = range(24)

# model order header
(ID, EVENT, DATETIME, NUMBER, DATE, TIME, STATDATE, STATDAYPART, CASHDESK,
 DELIVERY, EP, FW, TABLE, CUSTOMER, CONTACT, COVERS, AMOUNT, DISCOUNT, CASH, CHANGE,
 STATUS, FULLFILLMENT, USER_INS, DATE_INS, USER_UPD, DATE_UPD) = range(26)

# model order header department
(P_ID, P_IDHEADER, P_DEPARTMENT, P_NOTE, P_OTHER, P_BARCODE, P_FULLFILLMENT) = range(7)

# model order detail
(D_ID, D_IDHEADER, D_ITEM, D_VARIANTS, D_QUANTITY, D_PRICE, D_AMOUNT) = range(7)

# tree model order detail department
(M_DEP, M_ITEM, M_VARIANTS, M_QUANTITY, M_PARENT, M_CHILD) = range(6)


def orderArchive(action: QAction, checked: bool = False) -> None:
    "Manage order archive"
    logging.info('Starting order archive Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    ow = OrderForm(mw, title, auth)
    #ow.reload() # reload after filtering
    mw.addTab(title, ow)
    logging.info('Order archive Form added to main window')

# class OrdersWidget(QWidget, Ui_OrderWidget):

#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setupUi(self)


class OrderForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = OrderHeaderModel(self)
        idxModel = OrderHeaderIndexModel(self)
        modelHeaDep = OrderHeaderDepartmentModel(self)
        modelDet = OrderLineModel(self)
        modelTreeDep = OrderDepartmentTreeModel(self)
        #modelTreeDep.select()
        self.setModel(model, idxModel)
        self.addDetailRelation(modelHeaDep, ID, P_IDHEADER)
        self.addDetailRelation(modelDet, ID, D_IDHEADER)
        self.addDetailRelation(modelTreeDep, ID, 0)
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
        #self.ui.tableView.setModel(self.indexModel)
        self.ui.tableView.setLayoutName('OrderArchiveIndex')
        self.ui.tableView.setItemDelegateForColumn(I_TIME, TimeDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_AMOUNT, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_DISCOUNT, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_CASH, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_CHANGE, AmountDelegate(self))
        # mapper mappings
        # self.mapper.setItemDelegate(PMapperDelegate(self))
        self.mapper.addMapping(self.ui.lineEditCashDesk, CASHDESK)
        self.mapper.addMapping(self.ui.spinBoxNumber, NUMBER)
        self.mapper.addMapping(self.ui.dateEditDate, DATE)
        self.mapper.addMapping(self.ui.timeEditTime, TIME)
        self.ui.comboBoxDelivery.setItemList((('T', _tr('OrderArchive', 'Table')),
                                              ('A', _tr('OrderArchive', 'Take-away'))))
        self.mapper.addMapping(self.ui.checkBoxElectronicPayment, EP)
        self.mapper.addMapping(self.ui.checkBoxWebOrder, FW)
        self.mapper.addMapping(self.ui.comboBoxDelivery, DELIVERY, b"modelDataStr")
        self.mapper.addMapping(self.ui.lineEditTableNumber, TABLE)
        self.mapper.addMapping(self.ui.spinBoxCovers, COVERS)
        self.mapper.addMapping(self.ui.doubleSpinBoxTotalAmount, AMOUNT, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.doubleSpinBoxDiscount, DISCOUNT, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.doubleSpinBoxCash, CASH, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.doubleSpinBoxChange, CHANGE, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.lineEditCustomerName, CUSTOMER)
        self.mapper.addMapping(self.ui.lineEditCustomerContact, CONTACT)
        self.ui.comboBoxStatus.setItemList((('A', _tr('OrderArchive', 'Acquired')),
                                                ('I', _tr('OrderArchive', 'In progress')),
                                                ('P', _tr('OrderArchive', 'Processed'))))
        self.mapper.addMapping(self.ui.comboBoxStatus, STATUS, b"modelDataStr")
        self.mapper.addMapping(self.ui.dateTimeEditFullfillment, FULLFILLMENT, b"modelDataDateTime")
        # details tableView
        self.ui.tableViewDetails.setModel(modelDet)
        self.ui.tableViewDetails.setLayoutName('OrderArchiveDetail')
        #self.ui.tableViewDetails.setItemDelegate(GenericDelegate(self))
        self.ui.tableViewDetails.setItemDelegateForColumn(D_ITEM, RelationDelegate(self, item_all_lookup))
        self.ui.tableViewDetails.setItemDelegateForColumn(D_QUANTITY, QuantityDelegate(self))
        self.ui.tableViewDetails.setItemDelegateForColumn(D_PRICE, AmountDelegate(self))
        self.ui.tableViewDetails.setItemDelegateForColumn(D_AMOUNT, AmountDelegate(self))
        # details department treeView
        self.ui.treeViewDepartmentDetails.setModel(modelTreeDep)
        self.ui.treeViewDepartmentDetails.setItemDelegate(GenericDelegate(self))
        self.ui.treeViewDepartmentDetails.header().resizeSection(M_DEP, 250) # department
        self.ui.treeViewDepartmentDetails.header().resizeSection(M_ITEM, 300) # item
        self.ui.treeViewDepartmentDetails.header().resizeSection(M_VARIANTS, 300) # variants
        self.ui.treeViewDepartmentDetails.setItemDelegateForColumn(M_QUANTITY, QuantityDelegate(self))
        self.ui.treeViewDepartmentDetails.hideColumn(M_PARENT)
        self.ui.treeViewDepartmentDetails.hideColumn(M_CHILD)
        # header department tableView
        self.ui.tableViewDepartmentHeader.setModel(modelHeaDep)
        self.ui.tableViewDepartmentHeader.setLayoutName('OrderArchiveDepartment')
        self.ui.tableViewDepartmentHeader.setItemDelegateForColumn(P_DEPARTMENT, RelationDelegate(self, department_lookup))
        # store setting on form creation
        self.setting = Setting()
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
        if self.ui.comboBoxDelivery.currentData() == 'T':
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
        # PRINT ORDER
        setting = Setting()
        # get order id
        ti = self.model.data(self.model.index(self.mapper.currentIndex(), ID))
        # customer copy
        if self.ui.checkBoxPrintCustomerCopy.isChecked():
            printer = get_printer_name(setting['customer_printer_class'], session['hostname'])
            if not printer:
                QMessageBox.warning(self,
                                    _tr('MessageDialog', "Warning"),
                                    _tr('OrderArchive', "No customer copy printer set for this computer\n"
                                        "Generating a print preview"))
            try:
                printOrderReport(ti, printer)
            except ReportNoDataError:
                QMessageBox.information(self,
                                        _tr('MessageDialog', "Information"),
                                        _tr('OrderArchive', "No data to render"))
            self.ui.checkBoxPrintCustomerCopy.setChecked(False)

        # covers copy
        if self.ui.checkBoxPrintCoverCopy.isChecked():
            printer = get_printer_name(setting['cover_printer_class'], session['hostname'])
            if not printer:
                QMessageBox.warning(self,
                                    _tr('MessageDialog', "Warning"),
                                    _tr('OrderArchive', "No cover copy printer set for this computer\n"
                                        "Generating a print preview"))
            try:
                printOrderCoverReport(ti, printer)
            except ReportNoDataError:
                QMessageBox.information(self,
                                        _tr('MessageDialog', "Information"),
                                        _tr('OrderArchive', "No data to render"))
            self.ui.checkBoxPrintCoverCopy.setChecked(False)
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
                    if not printer:
                        msg = _tr('OrderArchive',
                                  "No department copy printer set for this computer "
                                  "and department {}\nGenerating a print preview")
                        QMessageBox.warning(self,
                                            _tr('MessageDialog', "Warning"),
                                            msg.format(get_department_desc(i)))
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
