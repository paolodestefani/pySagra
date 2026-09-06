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

"""Items ordered delivered

This module provide ordered delivered form management


"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import QDateTime
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Database.Models import ItemsOrderedDeliveredModel
from App.Database.Lookup import event_lookup
from App.Widget.Delegate import QuantityDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Form import FormViewManager
from App.Widget.Dialog import PrintDialog
from App.Widget.Dialog import EventFilterDialog
from App.Ui.OrderedDeliveredWidget import Ui_OrderedDeliveredWidget
from App.Core.L10n import _tr


# logger
logger = logging.getLogger(__name__)


class ord(IntEnum):
    EVENT       = 0
    DATE        = 1
    DAY_PART    = 2
    ITEM        = 3
    ITEM_DESC   = 4
    ORDERED     = 5
    DELIVERED   = 6


def dayPartMapping():
    return [('L', _tr('StockUnload', 'L')),
            ('D', _tr('StockUnload', 'D'))]


def orderedDelivered(action: QAction, checked: bool = False) -> None:
    "Ordered delivered"
    logger.info('Starting ordered delivered Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderedDelivered', 'No access right to this archive'))
        return
    su = OrderedDeliveredForm(mw, title, auth)
    mw.addTab(title, su)
    logger.info('Ordered delivered Form added to main window')


class OrderedDeliveredForm(FormViewManager[Ui_OrderedDeliveredWidget]):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = ItemsOrderedDeliveredModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, False, False, False, False,
                                True, False, True, True)
        self.ui = Ui_OrderedDeliveredWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setModel(model)
        self.ui.tableView.setLayoutName('OrderedDelivered')
        self.ui.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tableView.activateWindow()
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        self.ui.tableView.setItemDelegateForColumn(ord.EVENT, RelationDelegate(self, event_lookup))
        self.ui.tableView.setItemDelegateForColumn(ord.DAY_PART, RelationDelegate(self, dayPartMapping))
        self.ui.tableView.setItemDelegateForColumn(ord.ORDERED, QuantityDelegate(self, bold=True))
        self.ui.tableView.setItemDelegateForColumn(ord.DELIVERED, QuantityDelegate(self, bold=True))
        # initial filtering
        self.sortFilterDialog = EventFilterDialog(self, show_date = True, show_daypart = True) # type: ignore
        # initial filter conditions to current event
        if session['event_id']:
            self.updateFilterConditions(session['event_id'])
        else:
            self.sortFilterDialog.show()
        # hide rows with no ordered
        self.ui.checkBoxOnlyOrdered.checkStateChanged.connect(self.hideRows)
        # scripting init
        self.script = scriptInit(self)
        
    def updateFilterConditions(self, event, eventDate=None, dayPart=None):
        "Filter model based on filter dialog selections"
        self.model.whereCondition.clear()
        self.eventParams = (event, eventDate, dayPart)  # used on printing
        self.model.addWhere('s.event_id = %s', event)
        if eventDate:
            self.model.addWhere('s.event_date = %s', eventDate)
        if dayPart:
            self.model.addWhere('s.day_part = %s', dayPart)
        self.model.select()
        
    def hideRows(self, checked: bool) -> None:
        "Hide rows with no ordered"
        state = True if checked == Qt.CheckState.Checked else False
        for row in range(self.model.rowCount()):
            ordered = self.model.data(self.model.index(row, ord.ORDERED))
            if not ordered or ordered == 0:
                self.ui.tableView.setRowHidden(row, state)
            
    def setAutomaticUpdate(self, state):
        if state:
            self.updateTimer.start()
        else:
            self.updateTimer.stop()

    def updateUnload(self):
        super().reload()
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.updateTimer.start()

    def print(self):
        "Ordered delivered report"
        dialog = PrintDialog(self, 'ORDERED_DELIVERED')
        if not dialog.layoutFilters.itemAtPosition(0, 0):
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("OrderedDelivered", "A report customization for ordered delivered is required"))
            return
        # filter on current selected event/date/datepart
        # report definition must have these conditions and in this order
        # event
        dialog.layoutFilters.itemAtPosition(0, 0).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(0, 2).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(0, 3).widget().setValue(self.eventParams[0])
        # date
        dialog.layoutFilters.itemAtPosition(1, 0).widget().setCurrentIndex(2)
        dialog.layoutFilters.itemAtPosition(1, 2).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(1, 3).widget().setDate(self.eventParams[1])
        # day part
        dialog.layoutFilters.itemAtPosition(2, 0).widget().setCurrentIndex(3)
        dialog.layoutFilters.itemAtPosition(2, 2).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(2, 3).widget().setText(self.eventParams[2])
        dialog.show()
