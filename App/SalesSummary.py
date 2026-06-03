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

"""Sales summary

This module contains a custom view to display event Sales summary


"""

# standard library
from enum import IntEnum
import logging
from typing import cast
from typing import Any

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Database.Models import SalesSummaryModel
from App.Ui.SalesSummaryWidget import Ui_SalesSummaryWidget
from App.Core.L10n import _tr
from App.Widget.Delegate import GenericDelegate
from App.Widget.Form import FormViewManager
from App.Widget.Dialog import PrintDialog
from App.Widget.Dialog import EventFilterDialog


# logger
logger = logging.getLogger(__name__)


class ss(IntEnum):
    EVENT       = 0
    EVENT_DESC  = 1
    DATE        = 2
    ORDERS_L    = 3
    ORDERS_D    = 4
    ORDERS      = 5
    COVERS_L    = 6
    COVERS_D    = 7
    COVERS      = 8
    TAKEAWAY_L  = 9
    TAKEAWAY_D  = 10
    TAKEAWAY    = 11
    TABLE_L     = 12
    TABLE_D     = 13
    TABLE       = 14
    AMOUNT_L    = 15
    AMOUNT_D    = 16
    AMOUNT      = 17
    DISCOUNT_L  = 18
    DISCOUNT_D  = 19
    DISCOUNT    = 20
    ELECT_L     = 21
    ELECT_D     = 22
    ELECT       = 23
    CASH_L      = 24
    CASH_D      = 25
    CASH        = 26
    TOTAL_L     = 27
    TOTAL_D     = 28
    TOTAL       = 29


def salesSummary(action: QAction, checked: bool = False):
    "Sales summary"
    logger.info('Starting Sales summary Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    cw = SalesSummaryForm(mw, title, auth)
    mw.addTab(title, cw)
    logger.info('Sales summary Form added to main window')


class SalesSummaryForm(FormViewManager[Ui_SalesSummaryWidget]):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = SalesSummaryModel(self)
        model.setParameter('event_id', session['event_id'])
        self.setModel(cast(Any, model))
        self.tabName = title
        self.helpLink = None
        # overwrite standard sortfilterdialog with event filter dialog
        self.sortFilterDialog = EventFilterDialog(self, show_date = False, show_daypart = False)
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, False, False, False, False,
                                True, False, True, True)
        self.ui = Ui_SalesSummaryWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.view = self.ui.tableView # required for formviewmanager
        self.ui.tableView.setLayoutName('SalesSummary')
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        # daily details
        self.ui.checkBoxDetail.checkStateChanged.connect(self.showDetails)
        self.showDetails(Qt.CheckState.Unchecked)
        # initial filter conditions to current event
        if session['event_id']:
            self.updateFilterConditions(session['event_id'])
        else:
            self.sortFilterDialog.show()
        
    def updateFilterConditions(self, event, eventDate=None, dayPart=None) -> None:
        "Update model for new event id"
        if hasattr(self.model, 'setParameter'):
            self.model.setParameter('event_id', event)
            self.model.select()

    def showDetails(self, state) -> None:
        if state == Qt.CheckState.Unchecked:
            self.ui.tableView.setColumnHidden(ss.ORDERS_L, True)
            self.ui.tableView.setColumnHidden(ss.ORDERS_D, True)
            self.ui.tableView.setColumnHidden(ss.COVERS_L, True)
            self.ui.tableView.setColumnHidden(ss.COVERS_D, True)
            self.ui.tableView.setColumnHidden(ss.TAKEAWAY_L, True)
            self.ui.tableView.setColumnHidden(ss.TAKEAWAY_D, True)
            self.ui.tableView.setColumnHidden(ss.TABLE_L, True)
            self.ui.tableView.setColumnHidden(ss.TABLE_D, True)
            self.ui.tableView.setColumnHidden(ss.AMOUNT_L, True)
            self.ui.tableView.setColumnHidden(ss.AMOUNT_D, True)
            self.ui.tableView.setColumnHidden(ss.DISCOUNT_L, True)
            self.ui.tableView.setColumnHidden(ss.DISCOUNT_D, True)
            self.ui.tableView.setColumnHidden(ss.ELECT_L, True)
            self.ui.tableView.setColumnHidden(ss.ELECT_D, True)
            self.ui.tableView.setColumnHidden(ss.CASH_L, True)
            self.ui.tableView.setColumnHidden(ss.CASH_D, True)
            self.ui.tableView.setColumnHidden(ss.TOTAL_L, True)
            self.ui.tableView.setColumnHidden(ss.TOTAL_D, True)
        else:
            self.ui.tableView.setColumnHidden(ss.ORDERS_L, False)
            self.ui.tableView.setColumnHidden(ss.ORDERS_D, False)
            self.ui.tableView.setColumnHidden(ss.COVERS_L, False)
            self.ui.tableView.setColumnHidden(ss.COVERS_D, False)
            self.ui.tableView.setColumnHidden(ss.TAKEAWAY_L, False)
            self.ui.tableView.setColumnHidden(ss.TAKEAWAY_D, False)
            self.ui.tableView.setColumnHidden(ss.TABLE_L, False)
            self.ui.tableView.setColumnHidden(ss.TABLE_D, False)
            self.ui.tableView.setColumnHidden(ss.AMOUNT_L, False)
            self.ui.tableView.setColumnHidden(ss.AMOUNT_D, False)
            self.ui.tableView.setColumnHidden(ss.DISCOUNT_L, False)
            self.ui.tableView.setColumnHidden(ss.DISCOUNT_D, False)
            self.ui.tableView.setColumnHidden(ss.ELECT_L, False)
            self.ui.tableView.setColumnHidden(ss.ELECT_D, False)
            self.ui.tableView.setColumnHidden(ss.CASH_L, False)
            self.ui.tableView.setColumnHidden(ss.CASH_D, False)
            self.ui.tableView.setColumnHidden(ss.TOTAL_L, False)
            self.ui.tableView.setColumnHidden(ss.TOTAL_D, False)

    def print(self) -> None:
        "Sales summary report"
        dialog = PrintDialog(self, 'SALES_SUMMARY')
        if not dialog.ui.layoutFilters.itemAtPosition(0, 0):
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("SalesSummary", "A report customization for Sales summary is required"))
            return
        # set current daily detail setting
        dialog.ui.layoutParameters.itemAtPosition(0, 1).widget().setChecked(self.ui.checkBoxDetail.isChecked())
        # filter on current selected event
        dialog.ui.layoutFilters.itemAtPosition(0, 0).widget().setCurrentIndex(1)
        dialog.ui.layoutFilters.itemAtPosition(0, 2).widget().setCurrentIndex(1)
        if hasattr(self.model, 'parameter'):
            dialog.ui.layoutFilters.itemAtPosition(0, 3).widget().setValue(self.model.parameter['event_id'])
        dialog.show()
