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
from App.Database.Exceptions import PyAppDBError
from App.Database.Order import get_order_header_department_details
from App.Database.Order import update_order_header_department_status
from App.Database.Order import set_order_as_processed
from App.Database.Order import set_order_as_unprocessed
from App.Database.Models import OrderStatusModel
from App.Widget.Form import FormViewManager
from App.Widget.Delegate import GenericDelegate
from App.Widget.Dialog import EventFilterDialog
from App.Ui.OrderProgressWidget import Ui_OrderProgressWidget
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context


# logger
logger = logging.getLogger(__name__)

# order status qwery model
class ords(IntEnum):
    COMPANY_ID          = 0
    COMPANY_DESC        = 1
    EVENT_ID            = 2
    EVENT_DESC          = 3
    ORDER_HEADER_ID     = 4
    ORDER_DATE          = 5
    STAT_ORDER_DATE     = 6
    STAT_ORDER_DAYPART  = 7
    ORDER_TIME          = 8
    ORDER_NUMBER        = 9
    DELIVERY            = 10
    TABLE_NUM           = 11
    CUSTOMER_NAME       = 12
    COVERS              = 13
    STATUS              = 14
    FULFILLMENT_DATE    = 15
    CASH_DESK           = 16
    USER_INS            = 17
    FROM_WEB            = 18
    DEPARTMENT1         = 19
    FULFILLMENT1        = 20
    DEPARTMENT2         = 21
    FULFILLMENT2        = 22
    DEPARTMENT3         = 23
    FULFILLMENT3        = 24
    DEPARTMENT4         = 25
    FULFILLMENT4        = 26
    DEPARTMENT5         = 27
    FULFILLMENT5        = 28
    DEPARTMENT6         = 29
    FULFILLMENT6        = 30
                        

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
    title = action.text()
    auth = action.data()
    opf = OrderProgressForm(mw, title, auth)
    opf.reload()
    mw.addTab(title, opf)
    logger.info('Order progress form shown')


class OrderProgressForm(FormViewManager[Ui_OrderProgressWidget]):
    
    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        self.tabName = title
        self.helpLink = None
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
        # self.ui.tableWidgetScans.hideColumn(ID)
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
         odep, odepdesc, ofulfillmentdate) = result

        if ofulfillmentdate:  # order already processed
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
        with gui_exception_context(self, _tr("OrderProgress", "Update order status")):
            update_order_header_department_status(ohdid, True)
        # insert new row in scans history
        row = self.ui.tableWidgetScans.rowCount()
        self.ui.tableWidgetScans.insertRow(row)
        cell = QTableWidgetItem(str(ohdid))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.ID, cell)
        cell = QTableWidgetItem(barcode)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.BARCODE, cell)
        cell = QTableWidgetItem(str(onum))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.NUMBER, cell)
        cell = QTableWidgetItem(odate.toString())
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.DATE, cell)
        cell = QTableWidgetItem(otime.toString())
        cell.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.TIME, cell)
        cell = QTableWidgetItem(odelivery)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.tableWidgetScans.setItem(row, ordp.DELIVERY, cell)
        cell = QTableWidgetItem(otable)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.TABLE, cell)
        cell = QTableWidgetItem(ocustomer)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.CUSTOMER, cell)
        cell = QTableWidgetItem(odepdesc)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.DEPARTMENT, cell)
        # datetime shows is current because apdated anyway even if already processed
        dt = session['qlocale'].toString(QDateTime.currentDateTime(), QLocale.FormatType.ShortFormat)
        cell = QTableWidgetItem(dt)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tableWidgetScans.setItem(row, ordp.FULFILLMENT, cell)
        self.ui.tableWidgetScans.scrollToBottom()
        self.updateFilterConditions()

    def setAsUnprocessed(self):
        "Set as unprocessed the current selected line"
        row = self.ui.tableWidgetScans.currentRow()
        if row < 0: # no row selected
            return
        orderId = int(self.ui.tableWidgetScans.item(row, ordp.ID).data(Qt.EditRole))
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
        with gui_exception_context(self, _tr("OrderProgress", "Update order status")):
            update_order_header_department_status(orderId, False)
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
        
