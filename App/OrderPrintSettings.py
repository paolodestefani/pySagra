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

"""Order print settings

This module prvide a form and related classes for manage order print settings


"""

# standard library
from enum import IntEnum
from functools import partial
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QMessageBox
from PySide6.QtPrintSupport import QPrinterInfo
from PySide6.QtNetwork import QHostInfo

# application modules
from App import session
from App import currentIcon
from App.Common.L10n import _tr
from App.Common.Scripting import scriptInit
from App.Common.Scripting import scriptMethod
from App.Database.Models import OrderPrintSettingsIndexModel
from App.Database.Models import OrderPrintSettingsModel
#from App.Database.Models import OrderPrintDepartmentSettingstModel
from App.Database.Lookup import order_driver_report_lookup
from App.Database.Lookup import order_escpos_report_lookup
from App.Database.Lookup import cover_order_driver_report_lookup
from App.Database.Lookup import cover_order_escpos_report_lookup
from App.Database.Lookup import department_order_driver_report_lookup
from App.Database.Lookup import department_order_escpos_report_lookup
from App.Database.Lookup import escpos_printer_lookup
from App.Database.Lookup import department_lookup
from App.Database.OrderPrintSettings import copy_order_print_settings
from App.Database.Escpos import get_escpos_printers

from App.Widget.Dialog import PrintDialog
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import ReadOnlyDelegate
from App.Widget.Delegate import PrintersDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import HostNameDelegate
#from App.Ui.OrderPrintSettingsWidget import Ui_OrderPrintSettingsWidget
from App.Widget.Form import FormViewManager
from App.Ui.OrderPrintSettingsWidget import Ui_OrderPrintSettingsWidget


# logger
logger = logging.getLogger(__name__)


class ops(IntEnum):
    ID                  = 0
    HOSTNAME            = 1
    PRINT_TYPE          = 2
    DEPARTMENT_ID       = 3
    PRINT_COPY          = 4
    PRINT_METHOD        = 5
    NUMBER_OF_COPIES    = 6
    DRIVER_REPORT       = 7
    DRIVER_PRINTER      = 8
    ESCPOS_REPORT       = 9
    ESCPOS_PRINTER      = 10
    USER_INS            = 11
    DATE_INS            = 12
    USER_UPD            = 13
    DATE_UPD            = 14
    
    
def print_type() -> list:
    return [('C', _tr('OrderPrintSettings', 'Customer')),
            ('V', _tr('OrderPrintSettings', 'Cover')),
            ('D', _tr('OrderPrintSettings', 'Department')),
            ('O', _tr('OrderPrintSettings', 'Ordered delivered'))]
    
def print_methods() -> list:
    return [('D', _tr('OrderPrintSettings', 'Driver')),
            ('E', _tr('OrderPrintSettings', 'ESC/POS'))]
    
def available_driver_printers() -> list:
    return [i.printerName() for i in QPrinterInfo.availablePrinters()]


def orderPrintSettings(action: QAction, checked: bool = False) -> None:
    "Show/Edit printer classes"
    logger.info('Starting printers Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderPrintSettings', 'No access right to this archive'))
        return
    pf = OrderPrintSettingsForm(mw, title, auth)
    pf.reload()
    mw.addTab(title, pf)
    logger.info('Printers Form added to main window')


class OrderPrintSettingsForm(FormViewManager[Ui_OrderPrintSettingsWidget]):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = OrderPrintSettingsModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, False)
        self.ui = Ui_OrderPrintSettingsWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setLayoutName('OrderPrintSettings')
        # delegates
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ops.HOSTNAME, HostNameDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ops.PRINT_TYPE, RelationDelegate(self, print_type))
        self.ui.tableView.setItemDelegateForColumn(ops.DEPARTMENT_ID, RelationDelegate(self, partial(department_lookup, null=True)))
        self.ui.tableView.setItemDelegateForColumn(ops.PRINT_METHOD, RelationDelegate(self, print_methods))
        self.ui.tableView.setItemDelegateForColumn(ops.DRIVER_REPORT, RelationDelegate(self, order_driver_report_lookup, null=True))
        self.ui.tableView.setItemDelegateForColumn(ops.ESCPOS_REPORT, RelationDelegate(self, order_escpos_report_lookup, null=True))
        self.ui.tableView.setItemDelegateForColumn(ops.DRIVER_PRINTER, PrintersDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ops.ESCPOS_PRINTER, RelationDelegate(self, get_escpos_printers, null=True))
        # signal / slot
        self.ui.pushButtonCopySettings.clicked.connect(self.copyHostSettings)
        # scripting init
        self.script = scriptInit(self)
        
    def setFromHostName(self, index: int | None) -> None:
        "Fill the combobox of host name already present"
        hosts = set()
        for r in range(self.model.rowCount()):
            hosts.add(self.model.createIndex(r, ops.HOSTNAME).data())
        self.ui.comboBoxFromHostName.clear()
        #print("Hosts", hosts)
        self.ui.comboBoxFromHostName.addItems(list(hosts))
            
    def copyHostSettings(self):
        "Copy all settings from another hostname"
        from_host = self.ui.comboBoxFromHostName.currentText()
        to_host   = self.ui.lineEditNewHostName.text()
        msg = _tr('OrderPrintSettings', f'Copy ALL settings from {from_host} to {to_host} ?')
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                msg,
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        copy_order_print_settings(from_host, to_host)
        self.reload()
        
    @scriptMethod
    def new(self) -> None:
        "Insert a neew printer, focus on description"
        super().new()
        #self.ui.lineEditHostName.setFocus()

    @scriptMethod
    def save(self) -> None:
        "Save everithing"
        super().save()

    @scriptMethod
    def delete(self) -> None:
        "Delete and update current setting"
        super().delete()

    @scriptMethod
    def reload(self) -> None:
        "Reload data"
        super().reload()
        self.setFromHostName(0)

    @scriptMethod
    def print(self) -> None:
        "Printer report"
        dialog = PrintDialog(self, 'PRINT_SETTINGS')
        dialog.show()
