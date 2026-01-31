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
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App import currentAction  
from App.Database.Setting import SettingClass
from App.Database.Models import ItemsOrderedDeliveredModel
from App.Database.CodeDescriptionList import event_cdl
from App.Widget.Delegate import QuantityDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Form import FormViewManager
from App.Widget.Dialog import PrintDialog
from App.Widget.Dialog import EventFilterDialog
from App.Ui.OrderedDeliveredWidget import Ui_OrderedDeliveredWidget
from App.Core.L10n import _tr



EVENT, DATE, DAY_PART, ITEM, ITEM_DESCRIPTION, ORDERED, DELIVERED = range(7)


def dayPartMapping():
    return [('L', _tr('StockUnload', 'L')),
            ('D', _tr('StockUnload', 'D'))]


def orderedDelivered(auth):
    "Ordered delivered"
    logging.info('Starting ordered delivered Form')
    mw = session['mainwin']
    title = currentAction['app_activity_ordered_delivered'].text()
    auth = currentAction['app_activity_ordered_delivered'].data()
    su = OrderedDeliveredForm(mw, title, auth)
    mw.addTab(title, su)
    logging.info('Ordered delivered Form added to main window')


class OrderedDeliveredForm(FormViewManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = ItemsOrderedDeliveredModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, False, False, False, False,
                                True, False, False, False)
        self.ui = Ui_OrderedDeliveredWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setModel(model)
        self.ui.tableView.setLayoutName('stockUnload')
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableView.activateWindow()
        #self.ui.tableView.setSortingEnabled(True)
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        self.ui.tableView.setItemDelegateForColumn(DAY_PART, RelationDelegate(self, dayPartMapping))
        self.ui.tableView.setItemDelegateForColumn(ORDERED, QuantityDelegate(self, bold=True))
        self.ui.tableView.setItemDelegateForColumn(DELIVERED, QuantityDelegate(self, bold=True))
        # initial filtering
        self.selectedEvent = session['event_id']
        # set date and day part base on current date and time
        setting = SettingClass()
        now = QDateTime.currentDateTime()
        # if time between 0.0.0 and lunch start time stat date is the day before date part is dinner
        if QTime(0, 0) <= now.time() < QTime(setting['lunch_start_time'], 0):
            # dinner of the day before
            self.selectedDate = now.date().addDays(-1)
            self.selectedDayPart = 'D'
        elif QTime(setting['lunch_start_time'], 0) <= now.time() < QTime(setting['dinner_start_time'], 0):
            # lunch
            self.selectedDate = now.date()
            self.selectedDayPart = 'L'
        else:
            # dinner of the current date
            self.selectedDate = now.date()
            self.selectedDayPart = 'D'
        if session['event_id']:
            self.updateFilterConditions(session['event_id'], self.selectedDate, self.selectedDayPart)
            model.select()
        else:
            self.setFilters()
        self.updateTimer = QTimer(self)
        self.updateTimer.setInterval(setting['ordered_delivered_update_interval'] * 1000)
        self.updateTimer.timeout.connect(self.updateUnload)
        self.ui.checkBoxAutomaticUpdate.clicked.connect(self.setAutomaticUpdate)
        if setting['ordered_delivered_automatic_update']:
            self.ui.checkBoxAutomaticUpdate.setChecked(True)
            self.ui.dateTimeEdit.setEnabled(True)
            self.setAutomaticUpdate(True)

    def setAutomaticUpdate(self, state):
        if state:
            self.updateTimer.start()
        else:
            self.updateTimer.stop()

    def updateUnload(self):
        super().reload()
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.updateTimer.start()

    def updateFilterConditions(self, event, eventDate, dayPart):
        "Filter model based on filter dialog selections"
        self.eventParams = (event, eventDate, dayPart)  # used on printing
        model = self.ui.tableView.model()
        model.whereCondition.clear()
        model.addWhere('i.has_delivered_control = %s', True)
        model.addWhere('s.event_id = %s', event)
        model.addWhere('s.event_date = %s', eventDate)
        model.addWhere('s.day_part = %s', dayPart)
        model.select()

    def setFilters(self):
        "Filters event, date, day part"
        if not event_cdl():
            QMessageBox.information(self,
                                _tr('MessageDialog', 'Information'),
                                _tr('StockUnload', 'No event available'))
            return
        # create filter dialog if not exists
        if not hasattr(self, 'sortFilterDialog'):
            self.sortFilterDialog = EventFilterDialog(self,
                                                      self.selectedEvent,
                                                      self.selectedDate,
                                                      self.selectedDayPart)
        self.sortFilterDialog.show()

    def print_(self):
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
        dialog.layoutFilters.itemAtPosition(0, 1).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(0, 2).widget().setValue(self.eventParams[0])
        # date
        dialog.layoutFilters.itemAtPosition(1, 0).widget().setCurrentIndex(2)
        dialog.layoutFilters.itemAtPosition(1, 1).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(1, 2).widget().setDate(self.eventParams[1])
        # day part
        dialog.layoutFilters.itemAtPosition(2, 0).widget().setCurrentIndex(3)
        dialog.layoutFilters.itemAtPosition(2, 1).widget().setCurrentIndex(1)
        dialog.layoutFilters.itemAtPosition(2, 2).widget().setText(self.eventParams[2])
        dialog.show()
