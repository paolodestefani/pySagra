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
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSettings

# application modules
from App import session
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
from App.Ui.InventoryWidget import Ui_InventoryWidget


# logger
logger = logging.getLogger(__name__)

ID, EVENT, ITEM, LOADED, UNLOADED, STOCK, ORDERED, AVAILABLE, NEW_STOCK = range(9)


def inventory(action: QAction, checked: bool = False):
    "Manage stock inventory"
    logger.info('Starting inventory Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    sw = InventoryForm(mw, title, auth)
    mw.addTab(title, sw)
    logger.info('Stock inventory Form added to main window')


class InventoryForm(FormViewManager[Ui_InventoryWidget]):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
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
        self.ui.tableViewItem.setItemDelegateForColumn(EVENT, RelationDelegate(self, event_lookup))
        self.ui.tableViewItem.setItemDelegateForColumn(ITEM, RelationDelegate(self, item_with_stock_control_lookup))
        self.ui.tableViewItem.setItemDelegateForColumn(LOADED, QuantityDelegate(self))
        self.ui.tableViewItem.setItemDelegateForColumn(UNLOADED, QuantityDelegate(self))
        self.ui.tableViewItem.setItemDelegateForColumn(STOCK, StockLevelDelegate(self,
                                                                                 setting['inventory_warning_stock_level'],
                                                                                 setting['inventory_critical_stock_level']))
        self.ui.tableViewItem.setItemDelegateForColumn(ORDERED, QuantityDelegate(self))
        self.ui.tableViewItem.setItemDelegateForColumn(AVAILABLE, StockLevelDelegate(self, 
                                                                                     setting['inventory_warning_stock_level'],
                                                                                     setting['inventory_critical_stock_level']))
        self.ui.tableViewItem.setItemDelegateForColumn(NEW_STOCK, NewStockDelegate(self))
        # stay on NEW_STOCK column
        #self.ui.tableViewItem.selectionModel().currentChanged.connect(self.columnChanged)
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

    def save(self):
        super().save()
        logger.info('Saving inventory')
        self.updateFilterConditions(self.selectedEvent)

    def reload(self):
        super().reload()
        logger.info('Reloading inventory')
        self.updateFilterConditions(self.selectedEvent)

    def new(self):
        # set event on new record
        super().new()
        model = self.ui.tableViewItem.model()
        newRow = model.rowCount() - 1
        newIndex = model.index(newRow, EVENT)
        model.setData(newIndex, self.selectedEvent)
        # edit item cell
        newIndex = model.index(newRow, ITEM)
        self.ui.tableViewItem.edit(newIndex)

    def updateFilterConditions(self, event, eventDate=None, dayPart=None):
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

    def setFilters(self):
        "Filters event and items"
        self.sortFilterDialog.show()
        
    def close(self, *args, **kwargs) -> bool: # avoid signature change for event handler
        st = QSettings()
        st.setValue("Inventory/SplitterSizes", self.ui.splitter.sizes())
        return super().close() # return value is used by event handler, so return super() result
