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
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentAction
from App.Database.Models import SalesSummaryModel
from App.Database.Lookup import event_lookup
from App.Ui.SalesSummaryWidget import Ui_SalesSummaryWidget
from App.Core.L10n import _tr
from App.Widget.Delegate import AmountDelegate
from App.Widget.Form import FormViewManager
from App.Widget.Dialog import PrintDialog
from App.Widget.Dialog import EventFilterDialog



(EVENT, EVENT_DESCRIPTION, DATE,
 ORDERS_L, ORDERS_D, ORDERS,
 COVERS_L, COVERS_D, COVERS,
 TAKEAWAY_L, TAKEAWAY_D, TAKEAWAY,
 TABLE_L, TABLE_D, TABLE,
 CASH_L, CASH_D, CASH,
 ELECTRONIC_L, ELECTRONIC_D, ELECTRONIC,
 AMOUNT_L, AMOUNT_D, AMOUNT,
 DISCOUNT_L, DISCOUNT_D, DISCOUNT,
 TOTAL_L, TOTAL_D, TOTAL) = range(30)


def salesSummary(auth):
    "Sales summary"
    logging.info('Starting Sales summary Form')
    mw = session['mainwin']
    title = currentAction['app_activity_sales_summary'].text()
    auth = currentAction['app_activity_sales_summary'].data()
    cw = SalesSummaryForm(mw, title, auth)
    mw.addTab(title, cw)
    logging.info('Sales summary Form added to main window')


class SalesSummaryForm(FormViewManager[Ui_SalesSummaryWidget]):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = SalesSummaryModel(self)
        model.setParameter('event_id', session['event_id'])
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # overwrite standard sortfilterdialog with event filter dialog
        self.sortFilterDialog = EventFilterDialog(self, session['event_id']) # type: ignore
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, False, False, False, False,
                                True, False, True, False)
        self.ui = Ui_SalesSummaryWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.view = self.ui.tableView # required for formviewmanager
        self.ui.tableView.setLayoutName('salesSummary')
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        self.ui.tableView.setItemDelegateForColumn(TAKEAWAY_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TAKEAWAY_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TAKEAWAY, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TABLE_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TABLE_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TABLE, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(CASH_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(CASH_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(CASH, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ELECTRONIC_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ELECTRONIC_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(ELECTRONIC, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(AMOUNT_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(AMOUNT_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(AMOUNT, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(DISCOUNT_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(DISCOUNT_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(DISCOUNT, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TOTAL_L, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TOTAL_D, AmountDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TOTAL, AmountDelegate(self))
        # daily details
        self.ui.checkBoxDetail.checkStateChanged.connect(self.showDetails)
        self.showDetails(Qt.CheckState.Unchecked)

    def showDetails(self, state):
        if state == Qt.Unchecked:
            self.ui.tableView.setColumnHidden(ORDERS_L, True)
            self.ui.tableView.setColumnHidden(ORDERS_D, True)
            self.ui.tableView.setColumnHidden(COVERS_L, True)
            self.ui.tableView.setColumnHidden(COVERS_D, True)
            self.ui.tableView.setColumnHidden(TAKEAWAY_L, True)
            self.ui.tableView.setColumnHidden(TAKEAWAY_D, True)
            self.ui.tableView.setColumnHidden(TABLE_L, True)
            self.ui.tableView.setColumnHidden(TABLE_D, True)
            self.ui.tableView.setColumnHidden(CASH_L, True)
            self.ui.tableView.setColumnHidden(CASH_D, True)
            self.ui.tableView.setColumnHidden(ELECTRONIC_L, True)
            self.ui.tableView.setColumnHidden(ELECTRONIC_D, True)
            self.ui.tableView.setColumnHidden(AMOUNT_L, True)
            self.ui.tableView.setColumnHidden(AMOUNT_D, True)
            self.ui.tableView.setColumnHidden(DISCOUNT_L, True)
            self.ui.tableView.setColumnHidden(DISCOUNT_D, True)
            self.ui.tableView.setColumnHidden(TOTAL_L, True)
            self.ui.tableView.setColumnHidden(TOTAL_D, True)
        else:
            self.ui.tableView.setColumnHidden(ORDERS_L, False)
            self.ui.tableView.setColumnHidden(ORDERS_D, False)
            self.ui.tableView.setColumnHidden(COVERS_L, False)
            self.ui.tableView.setColumnHidden(COVERS_D, False)
            self.ui.tableView.setColumnHidden(TAKEAWAY_L, False)
            self.ui.tableView.setColumnHidden(TAKEAWAY_D, False)
            self.ui.tableView.setColumnHidden(TABLE_L, False)
            self.ui.tableView.setColumnHidden(TABLE_D, False)
            self.ui.tableView.setColumnHidden(CASH_L, False)
            self.ui.tableView.setColumnHidden(CASH_D, False)
            self.ui.tableView.setColumnHidden(ELECTRONIC_L, False)
            self.ui.tableView.setColumnHidden(ELECTRONIC_D, False)
            self.ui.tableView.setColumnHidden(AMOUNT_L, False)
            self.ui.tableView.setColumnHidden(AMOUNT_D, False)
            self.ui.tableView.setColumnHidden(DISCOUNT_L, False)
            self.ui.tableView.setColumnHidden(DISCOUNT_D, False)
            self.ui.tableView.setColumnHidden(TOTAL_L, False)
            self.ui.tableView.setColumnHidden(TOTAL_D, False)

    def updateFilterConditions(self, event_id, eventDate=None, dayPart=None):
        self.model.setParameter('event_id', event_id)
        self.model.select()

    def setFilters(self):
        "Filter event from combobox"
        if not event_lookup():
            QMessageBox.information(self,
                                _tr('MessageDialog', 'Information'),
                                _tr('SalesSummary', 'No event available'))
            return
        # create filter dialog if not exists
        #if not hasattr(self, 'sortFilterDialog'):
        #self.sortFilterDialog = EventFilterDialog(self, session['event_id'])
        self.sortFilterDialog.show()

    def print(self):
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
        dialog.ui.layoutFilters.itemAtPosition(0, 1).widget().setCurrentIndex(1)
        dialog.ui.layoutFilters.itemAtPosition(0, 2).widget().setValue(self.model.parameter['event_id'])
        dialog.show()
