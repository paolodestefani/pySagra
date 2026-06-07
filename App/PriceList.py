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

"""Price list

This module provides a form manager for price list and related objects

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QInputDialog

# application modules
from App import session
from App import currentIcon
from App.Database.Exceptions import PyAppDBError
from App.Database.Lookup import item_all_lookup
from App.Database.Models import PriceListIndexModel
from App.Database.Models import PriceListModel
from App.Database.Models import PriceListItemModel
from App.Database.PriceList import duplicate_price_list
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import AmountDelegate
from App.Widget.Form import FormIndexManager
from App.Widget.Dialog import PrintDialog
from App.Ui.PriceListWidget import Ui_PriceListWidget
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod


# logger
logger = logging.getLogger(__name__)


class pli(IntEnum):
    ID          = 0
    DESCRIPTION = 1
    USER_INS    = 2
    DATE_INS    = 3
    USER_UPD    = 4
    DATE_UPD    = 5

class pls(IntEnum):
    ID          = 0
    DESCRIPTION = 1
    USER_INS    = 2
    DATE_INS    = 3
    USER_UPD    = 4
    DATE_UPD    = 5

class prc(IntEnum):
    ID          = 0
    ID_PL       = 1
    ITEM        = 2
    PRICE       = 3
    USER_INS    = 4
    DATE_INS    = 5
    USER_UPD    = 6
    DATE_UPD    = 7


def priceList(action: QAction, checked: bool = False) -> None:
    "Manage price list"
    logger.info('Starting price list Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('PriceList', 'No access right to this archive'))
        return
    plw = PriceListForm(mw, title, auth)
    plw.reload()
    mw.addTab(title, plw)
    logger.info('Price list Form added to main window')


class PriceListWidget(QWidget, Ui_PriceListWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)


class PriceListForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = PriceListModel(self)
        idxModel = PriceListIndexModel(self)
        priModel = PriceListItemModel(self)
        self.setModel(model, idxModel)
        self.addDetailRelation(priModel, pli.ID, prc.ID_PL)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, True)
        self.ui = Ui_PriceListWidget()
        self.ui.setupUi(self)
        self.setIndexView(self.ui.tableView)
        # icons for add/remove buttons
        self.ui.pushButtonAdd.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemove.setIcon(currentIcon['edit_remove'])
        self.ui.tableView.setLayoutName('PriceListIndex')
        # mapper mappings
        self.mapper.addMapping(self.ui.lineEditDescription, pls.DESCRIPTION)
        # price list detail
        self.ui.tableViewPrices.setModel(priModel)
        self.ui.tableViewPrices.setLayoutName('PriceListDetail')
        self.ui.tableViewPrices.setItemDelegateForColumn(prc.ITEM, RelationDelegate(self, item_all_lookup))
        self.ui.tableViewPrices.setItemDelegateForColumn(prc.PRICE, AmountDelegate(self))
        # signal slot
        self.ui.pushButtonDuplicate.clicked.connect(self.duplicate)
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)
        # scripting init
        self.script = scriptInit(self)

    @scriptMethod
    def new(self):
        super().new()
        self.ui.lineEditDescription.setFocus()

    @scriptMethod
    def save(self):
        super().save()

    @scriptMethod
    def delete(self):
        "Delete and update current price list"
        msg = _tr('PriceList', "Are you sure you want to delete this price list ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{self.ui.lineEditDescription.text()}",
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        super().delete()

    @scriptMethod
    def reload(self):
        super().reload()

    @scriptMethod
    def add(self):
        "Edit second column of the view on new inserted rows"
        self.ui.tableViewPrices.add()
        model = self.ui.tableViewPrices.model()
        row = model.rowCount() - 1
        index = model.index(row, 1)
        self.ui.tableViewPrices.setCurrentIndex(index)
        self.ui.tableViewPrices.edit(index)

    @scriptMethod
    def remove(self):
        self.ui.tableViewPrices.remove()

    @scriptMethod
    def duplicate(self, checked=False):
        "Duplicate current price list"
        # ask for the new price list description
        text, ok = QInputDialog.getText(self,
                                        _tr('PriceList', 'Duplicate price list'),
                                        _tr('PriceList', 'Name of the new price list'))
        if not ok:
            return
        # get the current price list id
        currentPriceList = self.model.index(self.mapper.currentIndex(), pls.ID).data()
        with gui_exception_context(self, _tr("PriceList", "Duplicate price list")):
            duplicate_price_list(currentPriceList, text)
            QMessageBox.information(self,
                                    _tr('PriceList', 'Price list duplicated'),
                                    _tr('PriceList', 'The price list has been duplicated successfully'))
            self.reload()

    @scriptMethod
    def print(self):
        "Price list report"
        dialog = PrintDialog(self, 'PRICE_LIST')
        dialog.show()
