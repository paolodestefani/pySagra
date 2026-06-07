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

"""Items inventory

This module provides stock inventory management

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Database.Lookup import event_lookup
from App.Database.Setting import Setting
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import QuantityDelegate
from App.Widget.Delegate import NewStockDelegate
from App.Widget.Delegate import StockLevelDelegate
from App.Widget.Form import FormViewManager
from App.Widget.Dialog import EventFilterDialog
from App.Database.Lookup import item_with_stock_control_lookup
from App.Database.Models import InventoryModel
from App.Database.Models import KitAvailabilityModel
from App.Database.Models import MenuAvailabilityModel
from App.Database.Tool import inventory_rebuild
from App.Ui.InventoryWidget import Ui_InventoryWidget


# logger
logger = logging.getLogger(__name__)


class inv(IntEnum):
    ID        = 0
    EVENT     = 1
    ITEM      = 2
    LOADED    = 3
    UNLOADED  = 4
    STOCK     = 5
    ORDERED   = 6
    AVAILABLE = 7
    NEW_STOCK = 8


def inventory(action: QAction, checked: bool = False):
    "Manage stock inventory"
    logger.info('Starting inventory Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('Inventory', 'No access right to this archive'))
        return
    sw = InventoryForm(mw, title, auth)
    mw.addTab(title, sw)
    logger.info('Stock inventory Form added to main window')


class InventoryForm(FormViewManager[Ui_InventoryWidget]):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        setting = Setting()
        model = InventoryModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, False, False, False, False,
                                True, False, False, False)
        self.ui = Ui_InventoryWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableViewItem)  # required for formviewmanager
        st = QSettings()
        if st.value("Inventory/SplitterSizes", None):
            self.ui.splitter.setSizes(st.value("Inventory/SplitterSizes"))
        self.ui.tableViewItem.setLayoutName('Inventory')
        self.ui.tableViewItem.setItemDelegateForColumn(inv.EVENT, RelationDelegate(self, event_lookup))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.ITEM, RelationDelegate(self, item_with_stock_control_lookup))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.LOADED, QuantityDelegate(self))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.UNLOADED, QuantityDelegate(self))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.STOCK, StockLevelDelegate(self,
                                                                                 setting['inventory_warning_stock_level'],
                                                                                 setting['inventory_critical_stock_level']))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.ORDERED, QuantityDelegate(self))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.AVAILABLE, StockLevelDelegate(self, 
                                                                                     setting['inventory_warning_stock_level'],
                                                                                     setting['inventory_critical_stock_level']))
        self.ui.tableViewItem.setItemDelegateForColumn(inv.NEW_STOCK, NewStockDelegate(self))
        # kit availability
        self.kitModel = KitAvailabilityModel(self)
        self.ui.tableViewKit.setModel(self.kitModel)
        self.ui.tableViewKit.setLayoutName('itemsInventoryKit')
        self.ui.tableViewKit.setItemDelegateForColumn(2, StockLevelDelegate(self, 
                                                                            setting['inventory_warning_stock_level'],
                                                                            setting['inventory_critical_stock_level']))
        # menu availability
        self.menuModel = MenuAvailabilityModel(self)
        self.ui.tableViewMenu.setModel(self.menuModel)
        self.ui.tableViewMenu.setLayoutName('itemsInventoryMenu')
        self.ui.tableViewMenu.setItemDelegateForColumn(2, StockLevelDelegate(self, 
                                                                             setting['inventory_warning_stock_level'],
                                                                             setting['inventory_critical_stock_level']))
        self.sortFilterDialog = EventFilterDialog(self)
        # select initial event, ask if current event is None
        if session['event_id']:
            self.selectedEvent = session['event_id']
            self.updateFilterConditions(session['event_id'])
        else:
            self.selectedEvent = None
            self.setFilters()
        # splitter
        self.ui.splitter.setStretchFactor(0, 2)
        # scripting init
        self.script = scriptInit(self)

    @scriptMethod
    def save(self) -> None:
        super().save()
        logger.info('Saving inventory')
        # rebuild inventory for new items inserted an already sold
        inventory_rebuild(self.selectedEvent)
        self.updateFilterConditions(self.selectedEvent)

    @scriptMethod
    def reload(self) -> None:
        super().reload()
        logger.info('Reloading inventory')
        self.updateFilterConditions(self.selectedEvent)

    @scriptMethod
    def new(self) -> None:
        # set event on new record
        super().new()
        model = self.ui.tableViewItem.model()
        newRow = model.rowCount() - 1
        newIndex = model.index(newRow, inv.EVENT)
        model.setData(newIndex, self.selectedEvent)
        # edit item cell
        newIndex = model.index(newRow, inv.ITEM)
        self.ui.tableViewItem.edit(newIndex)

    def updateFilterConditions(self, 
                               event: int,
                               eventDate: QDateTime | None = None,
                               dayPart: str | None = None
                               ) -> None:
        "Update model of item, kit and menu on new event id"
        self.selectedEvent = event
        # stock model
        self.ui.tableViewItem.model().whereCondition = [('event_id = %s', event)]
        self.ui.tableViewItem.model().select()
        # kit model
        self.kitModel.setParameter('event', event)
        self.kitModel.select()
        # menu model
        self.menuModel.setParameter('event', event)
        self.menuModel.select()

    def setFilters(self) -> None:
        "Filters event and items"
        if self.sortFilterDialog:
            self.sortFilterDialog.show()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        "Save splitter status on close event"
        st = QSettings()
        st.setValue("Inventory/SplitterSizes", self.ui.splitter.sizes())
        super().closeEvent(event)
