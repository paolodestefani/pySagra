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


"""Order number management

This module is used to manage order number options

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget

# application modules
from App import session
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Database.Models import OrderNumberingModel
from App.Database.Lookup import event_lookup
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Dialog import EventFilterDialog
from App.Widget.Form import FormViewManager
from App.Ui.GenericFormViewWidget import Ui_GenericFormViewWidget


# logger
logger = logging.getLogger(__name__)


class ordn(IntEnum):
    ID = 0
    EVENT = 1
    EVENT_DATE = 2
    DAY_PART = 3
    CURRENT_VALUE = 4
    USER_INS = 5
    DATE_INS = 6
    USER_UPD = 7
    DATE_UPD = 8


def orderNumbering(action: QAction, checked: bool = False) -> None:
    "Manage order number current values"
    logger.info('Starting order numbers form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    dw = OrderNumberingForm(mw, title, auth)
    #dw.reload() # not required because filtered model is loaded at init
    mw.addTab(title, dw)
    logger.info('Order numbers form added to main window')


class OrderNumberingForm(FormViewManager[Ui_GenericFormViewWidget]):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = OrderNumberingModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, False, False, False, False,
                                True, False, False, False)
        self.ui = Ui_GenericFormViewWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setLayoutName('OrderNumbering')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ordn.EVENT, RelationDelegate(self, event_lookup))
        # event filter overwrite standard sort and filter dialog
        self.sortFilterDialog = EventFilterDialog(self, show_date = True, show_daypart = True) # type: ignore
        # scripting init
        self.script = scriptInit(self)
        # initial filter conditions to current event
        if session['event_id']:
            self.updateFilterConditions(session['event_id'])
        else:
            self.sortFilterDialog.show()
        
    def updateFilterConditions(self, event, eventDate=None, dayPart=None):
        "Update model for new event id, date and day part"
        self.model.addWhere('event_id = %s', event)
        if eventDate:
            self.model.addWhere('event_date = %s', eventDate)
        if dayPart:
            self.model.addWhere('day_part = %s', dayPart)
        self.model.select()

    @scriptMethod
    def new(self) -> None:
        "Edit second column of the view on new inserted rows"
        super().new()
        model = self.ui.tableView.model()
        row = model.rowCount() -1
        index = model.index(row, ordn.EVENT)
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