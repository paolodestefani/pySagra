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

"""Printer classes

This module prvide a form and related classes for manage printer classes


"""

# standard library
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
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Database.Models import PrinterIndexModel
from App.Database.Models import PrinterModel
from App.Database.Models import PrinterDetailModel
from App.Widget.Dialog import PrintDialog
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import ReadOnlyDelegate
from App.Widget.Delegate import PrintersDelegate
from App.Ui.DepartmentPrinterWidget import Ui_DepartmentPrinterWidget


# logger
logger = logging.getLogger(__name__)

ID, DESCRIPTION, USER_INS, DATE_INS, USER_UPD, DATE_UPD = range(6)

P_ID, P_CLASS_ID, P_COMPUTER, P_PRINTER, P_USER_INS, P_DATE_INS, P_USER_UPD, P_DATE_UPD = range(8)


def printer(action: QAction, checked: bool = False) -> None:
    "Show/Edit printer classes"
    logger.info('Starting printers Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    pf = PrinterForm(mw, title, auth)
    pf.reload()
    mw.addTab(title, pf)
    logger.info('Printers Form added to main window')


class PrinterForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = PrinterModel(self)
        idxModel = PrinterIndexModel(self)
        pdModel = PrinterDetailModel(self)
        self.setModel(model, idxModel)
        self.addDetailRelation(pdModel, ID, P_CLASS_ID)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, False)
        self.ui = Ui_DepartmentPrinterWidget()
        self.ui.setupUi(self)
        # icons for add/remove buttons
        self.ui.pushButtonAdd.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemove.setIcon(currentIcon['edit_remove'])
        # set index view, index model will be automatically connected
        self.ui.tableView.setLayoutName('PrinterIndex')
        self.setIndexView(self.ui.tableView)
        # mapper mappings
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        # printers detail
        self.ui.printersTableView.setModel(pdModel)
        self.ui.printersTableView.setLayoutName('Printer')
        self.ui.printersTableView.setItemDelegateForColumn(P_COMPUTER, ReadOnlyDelegate(self))
        # get host name
        self.hostName = QHostInfo.localHostName()
        # get printers list
        self.availablePrinters = [i.printerName() for i in QPrinterInfo.availablePrinters()]
        # printer item delegate
        self.ui.printersTableView.setItemDelegateForColumn(P_PRINTER, PrintersDelegate(self, self.availablePrinters, self.hostName))
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)
        # scripting init
        self.script = scriptInit(self)

    @scriptMethod
    def new(self) -> None:
        "Insert a neew printer, focus on description"
        super().new()
        self.ui.lineEditDescription.setFocus()

    @scriptMethod
    def save(self) -> None:
        "Save everithing"
        super().save()

    @scriptMethod
    def delete(self) -> None:
        "Delete and update current printer"
        msg = _tr('Printers', "Are you sure you want to delete this printer class ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{self.ui.lineEditDescription.text()}",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    @scriptMethod
    def reload(self) -> None:
        "Reload data"
        super().reload()

    @scriptMethod
    def add(self) -> None:
        "Add a new printer"
        # check if a record for current computer name already exists
        model = self.ui.printersTableView.model()
        for i in range(model.rowCount()):
            index = model.index(i, P_COMPUTER)
            if index.data() == self.hostName:
                QMessageBox.information(self,
                                        _tr("MessageDialog", "Information"),
                                        _tr("Printers", "There is already a record with current computer name"))
                return
        cr = self.ui.printersTableView.model().rowCount() # must be before add, with add model have already a new row
        self.ui.printersTableView.add()
        index = self.ui.printersTableView.model().index(cr, P_COMPUTER)
        self.ui.printersTableView.model().setData(index, self.hostName)

    @scriptMethod
    def remove(self) -> None:
        curIndex = self.ui.printersTableView.currentIndex()
        model = self.ui.printersTableView.model()
        index = model.index(curIndex.row(), P_COMPUTER)
        if index.data() != self.hostName:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Printers", "You can remove only the record with current computer name"))
            return
        self.ui.printersTableView.remove()

    @scriptMethod
    def print(self) -> None:
        "Printer report"
        dialog = PrintDialog(self, 'PRINTER')
        dialog.show()
