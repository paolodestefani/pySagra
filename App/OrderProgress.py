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
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QDate
from PySide6.QtCore import QLocale
from PySide6.QtCore import QSettings
from PySide6.QtGui import QAction
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QTableWidgetItem

# application modules
from App import session
from App.Database.Order import get_order_header_department_details
from App.Database.Order import update_order_header_department_status
from App.Database.Order import set_order_as_processed
from App.Database.Order import set_order_as_unprocessed
from App.Database.Models import OrderStatusModel
from App.Widget.Form import FormViewManager
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import RelationDelegate
from App.Ui.OrderProgressWidget import Ui_OrderProgressWidget
from App.Common.L10n import _tr
from App.Common.ExceptionHandler import gui_exception_context


# logger
logger = logging.getLogger(__name__)

# order status qwery model
class ords(IntEnum):
    COMPANY_ID          = 0
    COMPANY_DESC        = 1
    EVENT_ID            = 2
    EVENT_DESC          = 3
    ORDER_HEADER_ID     = 4
    ORDER_DATE_TIME     = 5
    ORDER_DATE          = 6
    ORDER_TIME          = 7
    STAT_ORDER_DATE     = 8
    STAT_ORDER_DAYPART  = 9
    ORDER_NUMBER        = 10
    DELIVERY            = 11
    TABLE_NUM           = 12
    CUSTOMER_NAME       = 13
    COVERS              = 14
    STATUS              = 15
    FULFILLMENT_DATE    = 16
    CASH_DESK           = 17
    USER_INS            = 18
    FROM_WEB            = 19
    DEPARTMENT1         = 20
    FULFILLMENT1        = 21
    DEPARTMENT2         = 22
    FULFILLMENT2        = 23
    DEPARTMENT3         = 24
    FULFILLMENT3        = 25
    DEPARTMENT4         = 26
    FULFILLMENT4        = 27
    DEPARTMENT5         = 28
    FULFILLMENT5        = 29
    DEPARTMENT6         = 30
    FULFILLMENT6        = 31
                        

class ordp(IntEnum):
    ID          = 0
    BARCODE     = 1
    NUMBER      = 2
    DATE        = 3
    TIME        = 4
    DELIVERY    = 5
    TABLE       = 6
    CUSTOMER    = 7
    DEPARTMENT  = 8
    FULFILLMENT = 9


def deliveryType():
    return [('T', _tr('OrderProgress', 'Table')),
            ('A', _tr('OrderProgress', 'Take Away'))]
    
def dayPartMapping():
    return [('L', _tr('OrderProgress', 'Lunch')),
            ('D', _tr('OrderProgress', 'Dinner'))]

def orderStatus():
    return [('A', _tr('OrderProgress', 'Acquired')),
            ('I', _tr('OrderProgress', 'In progress')),
            ('P', _tr('OrderProgress', 'Processed'))]


def orderProgress(action: QAction, checked: bool = False) -> None:
    "Order progress"
    logger.info('Starting order progress dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[2]: # no execute permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderProgress', 'No access right to this feature'))
        return
    # exit if no event available
    if not session['event_id']:
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderProgress', 'No event available, for order progress '
                                'is necessary to setup an event for the current date'))
        return
    opf = OrderProgressForm(mw, title, auth)
    opf.reload()
    mw.addTab(title, opf)
    logger.info('Order progress form shown')


class OrderProgressForm(FormViewManager[Ui_OrderProgressWidget]):
    
    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        self.tabName = title
        self.helpLink = "help/order_progress.html"
        self.reloadConfirmation = False
        self.setModel(OrderStatusModel(self))
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, False, False, False, False,
                                False, False, False, False)
        self.ui = Ui_OrderProgressWidget()
        self.ui.setupUi(self)
        # restore state
        st = QSettings()
        if s := st.value("OrderProgress/SplitterState", None):
            self.ui.splitter.restoreState(s)
        self.setView(self.ui.tableViewOrder)  # required for formviewmanager
        self.ui.tableViewOrder.setLayoutName('OrderProgress')
        self.ui.tableViewOrder.setItemDelegate(GenericDelegate(self))
        self.ui.tableViewOrder.setItemDelegateForColumn(ords.STAT_ORDER_DAYPART, RelationDelegate(self, dayPartMapping))
        self.ui.tableViewOrder.setItemDelegateForColumn(ords.DELIVERY, RelationDelegate(self, deliveryType))
        self.ui.tableViewOrder.setItemDelegateForColumn(ords.STATUS, RelationDelegate(self, orderStatus))
        # set default filter values
        self.ui.checkBoxAcquired.setChecked(True)
        self.ui.checkBoxInProgress.setChecked(True)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.ui.radioButtonDinner.setChecked(True)
        # signal slot
        self.ui.checkBoxAcquired.checkStateChanged.connect(self.updateFilterConditions)
        self.ui.checkBoxInProgress.checkStateChanged.connect(self.updateFilterConditions)
        self.ui.checkBoxProcessed.checkStateChanged.connect(self.updateFilterConditions)
        self.ui.dateEdit.userDateChanged.connect(self.updateFilterConditions)
        self.ui.radioButtonDinner.toggled.connect(self.updateFilterConditions)
        self.ui.checkBoxWholeEvent.toggled.connect(self.updateFilterConditions)
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
                  _tr('OrderProgress', "Fulfillment date")]
        self.ui.tableWidgetScans.setColumnCount(len(header))
        self.ui.tableWidgetScans.setSortingEnabled(False)
        self.ui.tableWidgetScans.setHorizontalHeaderLabels(header)
        self.ui.tableWidgetScans.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ui.tableWidgetScans.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.SelectedClicked)
        self.ui.tableWidgetScans.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableWidgetScans.setAlternatingRowColors(True)
        self.ui.tableWidgetScans.setWordWrap(False)
        self.ui.tableWidgetScans.hideColumn(ordp.ID)  # hide id column
        self.ui.tableWidgetScans.setItemDelegateForColumn(ordp.DELIVERY, RelationDelegate(self, deliveryType))
        self.ui.tableWidgetScans.setColumnWidth(ordp.BARCODE, 150)
        self.ui.tableWidgetScans.setColumnWidth(ordp.NUMBER, 100)
        self.ui.tableWidgetScans.setColumnWidth(ordp.DATE, 120)
        self.ui.tableWidgetScans.setColumnWidth(ordp.TIME, 100)
        self.ui.tableWidgetScans.setColumnWidth(ordp.DELIVERY, 150)
        self.ui.tableWidgetScans.setColumnWidth(ordp.TABLE, 100)
        self.ui.tableWidgetScans.setColumnWidth(ordp.CUSTOMER, 150)
        self.ui.tableWidgetScans.setColumnWidth(ordp.DEPARTMENT, 150)
        self.ui.tableWidgetScans.setColumnWidth(ordp.FULFILLMENT, 120)
        # signal/slot connections
        self.ui.lineEditBarcode.editingFinished.connect(self.scan)
        self.ui.pushButtonSetUnprocessed.clicked.connect(self.setAsUnprocessed)
        self.ui.pushButtonSetOrderProcessed.clicked.connect(self.setOrderProcessed)
        self.ui.pushButtonSetOrderUnprocessed.clicked.connect(self.setOrderUnprocessed)
        
    def reload(self) -> None:
        "Reload all widgets"
        #super().reload()
        self.updateFilterConditions()
        # focus on barcode lineedit must be after widgets is shown
        self.ui.lineEditBarcode.setFocus()
    
    def updateFilterConditions(self) -> None:
        "Update model filter conditions"
        self.model.whereCondition.clear()
        # event
        self.model.addWhere('event_id = %s', session['event_id'])
        # status
        status = [] 
        if self.ui.checkBoxAcquired.isChecked():
            status.append("A")
        if self.ui.checkBoxInProgress.isChecked():
            status.append("I")
        if self.ui.checkBoxProcessed.isChecked():
            status.append("P")
        self.model.addWhere("status = ANY(%s)", status)
        # subevent if required
        if not self.ui.checkBoxWholeEvent.isChecked():
            # limit date
            self.model.addWhere("stat_order_date = %s", self.ui.dateEdit.date())
            # day part
            if self.ui.radioButtonDinner.isChecked():
                self.model.addWhere("stat_order_day_part = %s", 'D')
            else:
                self.model.addWhere("stat_order_day_part = %s", 'L')
        # reload
        self.model.select()
        self.ui.spinBoxRecords.setValue(self.model.rowCount())

    def scan(self):
        "Update order header department status, insert a record in scans history"
        barcode = self.ui.lineEditBarcode.text()
        if not barcode:  # could be an empty string
            return
        # get order header department details
        with gui_exception_context(self, _tr("OrderProgress", "Error on getting order details")) as outcome:
            result = get_order_header_department_details(barcode)
        if not outcome.ok:
            self.ui.lineEditBarcode.clear()
            self.ui.lineEditBarcode.setFocus()
            return
        if not result:  # no order dep fuond for that id
            QMessageBox.warning(self,
                                _tr('MessageDialog', 'Warning'),
                                _tr('OrderProgress', 'Order not found'))
            self.ui.lineEditBarcode.clear()
            self.ui.lineEditBarcode.setFocus()
            return
        
        (ohdid, ohid, onum, odate, otime, odelivery, otable, ocustomer,
         odep, odepdesc, ofulfillmentdate) = result

        if ofulfillmentdate:  # order already processed
            if QMessageBox.question(self,
                                    _tr('MessageDialog', 'Question'),
                                    _tr('OrderProgress', 'Order already processed, process again ?'),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                    QMessageBox.StandardButton.No  # default botton
                                    ) == QMessageBox.StandardButton.No:
                self.ui.lineEditBarcode.clear()
                self.ui.lineEditBarcode.setFocus()
                return

        self.ui.lineEditBarcode.clear()
        self.ui.lineEditBarcode.setFocus()
        # update order header department status, mark as processed order header department
        with gui_exception_context(self, _tr("OrderProgress", "Update order status")) as outcome:
            update_order_header_department_status(ohdid, True)
        if not outcome.ok:   # not processed: no row in the scans history
            return
        # insert new row in scans history
        row = self.ui.tableWidgetScans.rowCount()
        self.ui.tableWidgetScans.insertRow(row)
        cell = QTableWidgetItem(str(ohdid))
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.ID, cell)
        cell = QTableWidgetItem(barcode)
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.BARCODE, cell)
        cell = QTableWidgetItem(str(onum))
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.NUMBER, cell)
        cell = QTableWidgetItem(session['qlocale'].toString(odate, QLocale.FormatType.ShortFormat))
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.DATE, cell)
        cell = QTableWidgetItem(session['qlocale'].toString(otime, QLocale.FormatType.ShortFormat))
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.TIME, cell)
        cell = QTableWidgetItem(odelivery)
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        cell.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.ui.tableWidgetScans.setItem(row, ordp.DELIVERY, cell)
        cell = QTableWidgetItem(otable)
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.TABLE, cell)
        cell = QTableWidgetItem(ocustomer)
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.CUSTOMER, cell)
        cell = QTableWidgetItem(odepdesc)
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.DEPARTMENT, cell)
        # datetime shows is current because apdated anyway even if already processed
        dt = session['qlocale'].toString(QDateTime.currentDateTime(), QLocale.FormatType.ShortFormat)
        cell = QTableWidgetItem(dt)
        cell.setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.FULFILLMENT, cell)
        self.ui.tableWidgetScans.scrollToBottom()
        self.updateFilterConditions()

    def setAsUnprocessed(self):
        "Set as unprocessed the current selected line"
        row = self.ui.tableWidgetScans.currentRow()
        if row < 0: # no row selected
            return
        orderId = int(self.ui.tableWidgetScans.item(row, ordp.ID).data(Qt.ItemDataRole.EditRole))
        if orderId < 0:  # no item selected
            return
        if QMessageBox.question(self,
                                _tr('MessageDialog', 'Question'),
                                _tr('OrderProgress', 'Set current selected order as unprocessed ?'),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            self.ui.lineEditBarcode.setFocus()
            return
        # update order header department status
        with gui_exception_context(self, _tr("OrderProgress", "Update order status")) as outcome:
            update_order_header_department_status(orderId, False)
        if not outcome.ok:   # still processed: the row stays
            self.ui.lineEditBarcode.setFocus()
            return
        # delete row from tablewidget
        self.ui.tableWidgetScans.removeRow(row)
        self.ui.lineEditBarcode.setFocus()
        self.updateFilterConditions()
        
    def setOrderProcessed(self) -> None:
        "Mark whole order processed"
        current_index = self.ui.tableViewOrder.currentIndex()
        if not current_index.isValid():
            return
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('OrderProgress', 'Mark the selected order as Processed ?'),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        # create a new index that points to column ORDER_HEADER_ID of the same row
        ord_header_id = int(current_index.siblingAtColumn(ords.ORDER_HEADER_ID).data())
        with gui_exception_context(self, _tr('OrderProgress', 'Mark order as processed')):
            set_order_as_processed(ord_header_id)
        self.reload()
    
    def setOrderUnprocessed(self) -> None:
        "Mark whole order unprocessed"
        current_index = self.ui.tableViewOrder.currentIndex()
        if not current_index.isValid():
            return
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('OrderProgress', 'Mark the selected order as Unprocessed ?'),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        # create a new index that points to column ORDER_HEADER_ID of the same row
        ord_header_id = int(current_index.siblingAtColumn(ords.ORDER_HEADER_ID).data())
        with gui_exception_context(self, _tr('OrderProgress', 'Mark order as unprocessed')):
            set_order_as_unprocessed(ord_header_id)
        self.reload()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        "Save splitter status on close event"
        st = QSettings()
        st.setValue("OrderProgress/SplitterState", self.ui.splitter.saveState())
        super().closeEvent(event)
        
