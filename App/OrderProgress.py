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

"""Order progress

This module provides a dialog for manage order progress


"""

# standard library
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QLocale
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QTableWidgetItem

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Database.Order import get_order_header_department_details
from App.Database.Order import update_order_header_department_status
from App.Database.Setting import SettingClass
from App.Database.Models import OrderStatusModel
from App.Widget.Form import FormViewManager
from App.Widget.Delegate import GenericDelegate
#from App.Ui.OrderProgressDialog import Ui_OrderProgressDialog
from App.Ui.OrderProgressWidget import Ui_OrderProgressWidget
from App.Core.L10n import _tr



ID, BARCODE, NUM, DATE, TIME, DELIVERY, TABLE, CUSTOMER, DEPARTMENT, FULLFILLMENT = range(10)


def limitType() -> list:
    return [('E', _tr('Status', 'Event')),
            ('T', _tr('Status', 'Today')),
            ('L', _tr('Status', 'Today Lunch')),
            ('D', _tr('Status', 'Today Dinner'))]



def orderProgress(action: QAction, checked: bool = False) -> None:
    "Order progress"
    logging.info('Starting order progress diaform')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    #icon = currentAction['app_activity_order_progress'].icon()
    #dlg = OrderProgressDialog(mw, title, icon, auth)
    #dlg.exec()
    opf = OrderProgressForm(mw, title, auth)
    opf.reload()
    mw.addTab(title, opf)
    logging.info('Order progress form shown')


class OrderProgressForm(FormViewManager[Ui_OrderProgressWidget]):
    
    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        self.tabName = title
        self.helpLink = None
        self.reloadConfirmation = False
        self.setModel(OrderStatusModel(self))
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, False, False, False, False,
                                True, False, True, True)
        self.ui = Ui_OrderProgressWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableViewOrder)  # required for formviewmanager
        self.ui.tableViewOrder.setLayoutName('orderStatus')
        self.ui.tableViewOrder.setItemDelegate(GenericDelegate(self))
        # set default filter values
        self.ui.checkBoxAcquired.setChecked(True)
        self.ui.checkBoxInProgress.setChecked(True)
        self.ui.comboBoxLimit.setFunction(limitType)
        # select initial event, ask if current event is None
        if session['event_id']:
            self.selectedEvent = session['event_id']
            self.updateFilterConditions(session['event_id'])
        else:
            self.selectedEvent = None
            self.setFilters()
        #self.ui.checkBoxAcquired.checkStateChanged.connect(self.updateFilterConditions)
        #self.ui.checkBoxInProgress.checkStateChanged.connect(self.updateFilterConditions)
        #self.ui.checkBoxProcessed.checkStateChanged.connect(self.updateFilterConditions)
        #self.ui.comboBoxLimit.currentIndexChanged.connect(self.updateFilterConditions)
        # scans tablewidget
        header = [_tr('OrderProgress', "ID"),
                  _tr('OrderProgress', "Barcode"),
                  _tr('OrderProgress', "Num"),
                  _tr('OrderProgress', "Date"),
                  _tr('OrderProgress', "Time"),
                  _tr('OrderProgress', "Delivery"),
                  _tr('OrderProgress', "Table"),
                  _tr('OrderProgress', "Customer"),
                  _tr('OrderProgress', "Department"),
                  _tr('OrderProgress', "Fullfillment date")]
        self.ui.tableWidgetScans.setColumnCount(len(header))
        self.ui.tableWidgetScans.setSortingEnabled(False)
        self.ui.tableWidgetScans.setHorizontalHeaderLabels(header)
        self.ui.tableWidgetScans.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ui.tableWidgetScans.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.SelectedClicked)
        self.ui.tableWidgetScans.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableWidgetScans.setAlternatingRowColors(True)
        self.ui.tableWidgetScans.setWordWrap(False)
        # self.ui.tableWidgetScans.hideColumn(ID)
        # signal/slot connections
        self.ui.lineEditBarcode.editingFinished.connect(self.scan)
        self.ui.pushButtonSetAsUnprocessed.clicked.connect(self.setAsUnprocessed)
        
    def reload(self):
        super().reload()
        self.updateFilterConditions(self.selectedEvent)
        # focus on barcode lineedit must be after widgets is shown
        self.ui.lineEditBarcode.setFocus
        
    def updateFilterConditions(self, event, eventDate=None, dayPart=None):
        "Update model filter conditions"
        self.selectedEvent = event
        self.whereConditions = []
        # stock model
        self.model.addWhere('event_id = %s', event)
        # status
        status = []
        if self.ui.checkBoxAcquired.isChecked():
            status.append("A")
        if self.ui.checkBoxInProgress.isChecked():
            status.append("I")
        if self.ui.checkBoxProcessed.isChecked():
            status.append("P")
        self.model.addWhere("status = ANY(%s)", [status])
        # limit
        if self.ui.comboBoxLimit.currentData == 'T':
            self.model.addWhere("event_date = %s", QDateTime.currentDateTime())
        elif self.ui.comboBoxLimit.currentData == 'L':
            self.model.addWhere("stat_order_date = %s", QDateTime.currentDateTime())
            self.model.addWhere("stat_order_day_part = %s", 'L')
        elif self.ui.comboBoxLimit.currentData == 'D':
            self.model.addWhere("stat_order_date = %s", QDateTime.currentDateTime())
            self.model.addWhere("stat_order_day_part = %s", 'D')
        # reload
        self.model.select()

    def setFilters(self):
        "Filters event and items"
        # create filter dialog if not exists
        if not hasattr(self, 'sortFilterDialog'):
            self.sortFilterDialog = EventFilterDialog(self, session['event'])
        self.sortFilterDialog.show()
        
    def scan(self):
        "Update order header department status, insert a record in scans history"
        barcode = self.ui.lineEditBarcode.text()
        if not barcode:  # could be an empty string
            return
        # get order header department details
        try:
            result = get_order_header_department_details(barcode)
        except Exception as er:
            msg = _tr("OrderProgress", "Errore on getting order details")
            QMessageBox.critical(self,
                                 msg,
                                 f"{er}")
            return
        if not result:  # no order dep fuond for that id
            QMessageBox.warning(self,
                                _tr('MessageDialog', 'Warning'),
                                _tr('OrderProgress', 'Order not found'))
            self.ui.lineEditBarcode.clear()
            self.ui.lineEditBarcode.setFocus()
            return

        (ohdid, ohid, onum, odate, otime, odelivery, otable, ocustomer,
         odep, odepdesc, ofullfillmentdate) = result

        if ofullfillmentdate:  # order already processed
            if QMessageBox.question(self,
                                    _tr('MessageDialog', 'Question'),
                                    _tr('OrderProgress', 'Order already processed, process again ?'),
                                    QMessageBox.Yes | QMessageBox.No,  # butons
                                    QMessageBox.No  # default botton
                                    ) == QMessageBox.No:
                self.ui.lineEditBarcode.clear()
                self.ui.lineEditBarcode.setFocus()
                return

        self.ui.lineEditBarcode.clear()
        self.ui.lineEditBarcode.setFocus()
        # update order header department status, mark as processed order header department
        try:
            update_order_header_department_status(ohdid, True)
        except PyAppDBError as er:
            mbox = QMessageBox(self)
            mbox.setIcon(QMessageBox.Critical)
            mbox.setWindowTitle(_tr("OrderProgress", "Error on update order status"))
            mbox.setText(_tr("OrderProgress", "Database error {}").format(er.code))
            mbox.setDetailedText(er.message)
            mbox.exec_()
        # insert new row in scans history
        row = self.ui.tableWidgetScans.rowCount()
        self.ui.tableWidgetScans.insertRow(row)
        cell = QTableWidgetItem(str(ohdid))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ID, cell)
        cell = QTableWidgetItem(barcode)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, BARCODE, cell)
        cell = QTableWidgetItem(str(onum))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, NUM, cell)
        cell = QTableWidgetItem(odate.toString())
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, DATE, cell)
        cell = QTableWidgetItem(otime.toString())
        cell.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, TIME, cell)
        cell = QTableWidgetItem(odelivery)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.tableWidgetScans.setItem(row, DELIVERY, cell)
        cell = QTableWidgetItem(otable)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, TABLE, cell)
        cell = QTableWidgetItem(ocustomer)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, CUSTOMER, cell)
        cell = QTableWidgetItem(odepdesc)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, DEPARTMENT, cell)
        # datetime shows is current because apdated anyway even if already processed
        dt = session['qlocale'].toString(QDateTime.currentDateTime(), QLocale.FormatType.ShortFormat)
        cell = QTableWidgetItem(dt)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, FULLFILLMENT, cell)
        self.ui.tableWidgetScans.scrollToBottom()

    def setAsUnprocessed(self):
        "Set as unprocessed the current selected line"
        row = self.ui.tableWidgetScans.currentRow()
        if row < 0: # no row selected
            return
        orderId = int(self.ui.tableWidgetScans.item(row, ID).data(Qt.EditRole))
        if orderId < 0:  # no item selected
            return
        if QMessageBox.question(self,
                                _tr('MessageDialog', 'Question'),
                                _tr('OrderProgress', 'Set current selected order as unprocessed ?'),
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            self.ui.lineEditBarcode.setFocus()
            return
        # update order header department status
        try:
            update_order_header_department_status(orderId, False)
        except PyAppDBError as er:
            mbox = QMessageBox(self)
            mbox.setIcon(QMessageBox.Critical)
            mbox.setWindowTitle(_tr("OrderProgress", "Error on update order status"))
            mbox.setText(_tr("OrderProgress", "Database error {}").format(er.code))
            mbox.setDetailedText(er.message)
            mbox.exec()
        # delete row from tablewidget
        self.ui.tableWidgetScans.removeRow(row)
        self.ui.lineEditBarcode.setFocus()
