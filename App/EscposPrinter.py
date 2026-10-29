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


"""Escpos printer

This module is used to manage ESC/POS printer's name and parameters

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Common.L10n import _tr
from App.Common.Scripting import scriptInit
from App.Common.Scripting import scriptMethod
from App.Database.Models import EscposPrinterModel
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import HostNameDelegate
from App.Widget.Form import FormViewManager
from App.Ui.GenericFormViewWidget import Ui_GenericFormViewWidget


# logger
logger = logging.getLogger(__name__)


class ep(IntEnum):
    ID          = 0
    COMPUTER    = 1
    NAME        = 2
    TYPE        = 3
    # network printer
    HOST        = 4
    PORT        = 5
    CON_TIMEOUT = 6
    # USB printer
    ID_VENDOR   = 7
    ID_PRODUCT  = 8
    USB_TIMEOUT = 9
    IN_EP       = 10
    OUT_EP      = 11
    #
    NOTE        = 12
    #
    USER_INS    = 13
    DATE_INS    = 14
    USER_UPD    = 15
    DATE_UPD    = 16
    

def printer_type() -> list:
    return [('U', _tr('EscposPrinter', 'USB')),
            ('N', _tr('EscposPrinter', 'Network'))]


def escposPrinter(action: QAction, checked: bool = False) -> None:
    "Manage ESC/POS printers"
    logger.info('Starting Escpos printer form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('CashDesk', 'No access right to this archive'))
        return
        
    dw = EscposPrinterForm(mw, title, auth)
    dw.reload()
    mw.addTab(title, dw)
    logger.info('Escpos printer form added to main window')


class EscposPrinterForm(FormViewManager[Ui_GenericFormViewWidget]):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = EscposPrinterModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = "help/cash_desk.html"
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, False, False, False, False,
                                False, False, False, False)
        self.ui = Ui_GenericFormViewWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setLayoutName('EscposPrinter')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ep.COMPUTER, HostNameDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ep.TYPE, RelationDelegate(self, printer_type))
        # scripting init
        self.script = scriptInit(self)
        
    @scriptMethod
    def new(self) -> None:
        "Edit second column of the view on new inserted rows"
        super().new()
        model = self.ui.tableView.model()
        row = model.rowCount() - 1
        index = model.index(row, ep.COMPUTER)
        # set the computer name
        model.setData(index, session['hostname'])
        # force cell editing
        self.ui.tableView.setCurrentIndex(index)
        self.ui.tableView.edit(index)

    @scriptMethod
    def save(self) -> None:
        super().save()

    @scriptMethod
    def delete(self) -> None:
        super().delete()

    @scriptMethod
    def reload(self) -> None:
        super().reload()