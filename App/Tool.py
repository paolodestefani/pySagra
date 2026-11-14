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

"""Utilities

This module provides application utilities for manage orders and related
archives


"""

# standard library
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Common.ExceptionHandler import gui_exception_context
from App.Database.Connect import appconn
from App.Database.Lookup import event_lookup
from App.Database.Tool import delete_event_order
from App.Database.Tool import inventory_rebuild
from App.Database.Tool import ordered_delivered_rebuild
from App.Database.Tool import numbering_rebuild
from App.Database.Tool import set_order_as_processed
from App.Database.Tool import delete_all_orders
from App.Database.Tool import delete_all_inventory
from App.Database.Tool import delete_all_events
from App.Database.Tool import delete_all_price_lists
from App.Database.Tool import delete_all_items
from App.Database.Tool import delete_all_departments
from App.Database.Tool import delete_all_tables
from App.Database.Tool import delete_all_cash_desks
from App.Database.Tool import copy_cash_desk
from App.Database.Tool import copy_table
from App.Database.Tool import copy_department
from App.Database.Tool import copy_item

from App.Database.Company import company_list
from App.Ui.EventToolDialog import Ui_EventToolDialog
from App.Ui.DeleteToolDialog import Ui_DeleteToolDialog
from App.Ui.CopyToolDialog import Ui_CopyToolDialog
from App.Common.L10n import _tr
from App.System.Help import addHelpAction


# logger
logger = logging.getLogger(__name__)


def eventBasedTool(action: QAction, checked: bool = False) -> None:
    "Launch event based tool dialog"
    logger.info('Starting event based tool dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    if not auth[2]: # no execute permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('Tool', 'No access right to this function'))
        return
    if not event_lookup():
        QMessageBox.information(mw,
                                _tr('MessageDialog', 'Information'),
                                _tr('Tool', 'No event available'))
        return
    dlg = EventToolDialog(mw, title, icon)
    if dlg.exec() == QDialog.DialogCode.Rejected:
        return
    dlg.close()
    logger.info('Delete event based tool shown')
    
def deleteTool(action: QAction, checked: bool = False) -> None:
    "Delete selected objects from current company"
    logger.info('Starting delete tool dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    if not auth[2]: # no execute permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('Tool', 'No access right to this function'))
        return
    dlg = DeleteToolDialog(mw, title, icon)
    if dlg.exec() == QDialog.DialogCode.Rejected:
        return
    dlg.close()
    logger.info('Delete tool dialog shown')

def copyTool(action: QAction, checked: bool = False) -> None:
    "Copy selected objects from a selected company to the current company"
    logger.info('Starting copy tool dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    if not auth[2]: # no execute permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('Tool', 'No access right to this function'))
        return
    dlg = CopyToolDialog(mw, title, icon)
    if dlg.exec() == QDialog.DialogCode.Rejected:
        return
    dlg.close()
    logger.info('Copy tool dialog shown')
    


class EventToolDialog(QDialog):

    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.ui = Ui_EventToolDialog()
        self.ui.setupUi(self)
        addHelpAction(self, "help/event_tool.html")
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        for i, u in ((0, _tr('Utility', 'Delete Orders')),
                     (1, _tr('Utility', 'Inventory rebuild')),
                     (2, _tr('Utility', 'Ordered delivered rebuild')),
                     (3, _tr('Utility', 'Numbering Rebuild')),
                     (4, _tr('Utility', 'Mark Orders as Processed'))):
            self.ui.comboBoxUtility.addItem(u, i)
        for i, d in event_lookup():
            self.ui.comboBoxEvent.addItem(d, i)
        self.ui.comboBoxEvent.setCurrentText(session['event_description'])
        self.ui.comboBoxUtility.currentIndexChanged.connect(self.updateWarning)
        self.updateWarning(0)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).setDefault(True)
       
    def updateWarning(self, index):
        "Update warning text according to selected utility"
        texts = {
            0: (_tr('Utility', 'Warning'),
                _tr('Utility', "This utility function delete ALL "
                               "orders of the selected event. It's not possible "
                               "to undo this operation.")),
            1: (_tr('Utility', 'Information'),
                _tr('Utility', "This utility function rebuild stock "
                               "unload from orders of the selected event. Use "
                               "this when changed item state/flags "
                               "or when manually altered orders.")),
            2: (_tr('Utility', 'Information'),
                _tr('Utility', "This utility function rebuild the ordered and "
                               "delivered quantities from orders of the selected event.")),
            3: (_tr('Utility', 'Information'),
                _tr('Utility', "This utility function rebuild "
                               "numbering from orders of the selected event.")),
            4: (_tr('Utility', 'Information'),
                _tr('Utility', "This utility function mark all "
                               "orders as processed at the order date"))}
        title, text = texts.get(self.ui.comboBoxUtility.currentData(), ('', ''))
        self.ui.groupBoxWarning.setTitle(title)
        self.ui.labelWarning.setText(text)

    def accept(self):
        "Proceed with the selected utility"
        FUNC, DESC, MESSAGE = range(3)
        event_id = self.ui.comboBoxEvent.currentData()
        eventDescription = self.ui.comboBoxEvent.currentText()
        utility_id = self.ui.comboBoxUtility.currentData()
        utilities = {
            0: [delete_event_order, _tr('Utility', 'Delete Orders'), 
                _tr("Utility", "Are you sure you want to delete all orders of event\n"
                               "'{}' ?").format(eventDescription)],
            1: [inventory_rebuild, _tr('Utility', 'Inventory Rebuild'), 
                _tr("Utility", "Are you sure you want to procede with inventory rebuild for event\n"
                               "'{}' ?").format(eventDescription)],
            2: [ordered_delivered_rebuild, _tr('Utility', 'Ordered delivered rebuild'), 
                _tr("Utility", "Are you sure you want to procede with ordered delivered rebuild for event\n"
                               "'{}' ?").format(eventDescription)],
            3: [numbering_rebuild, _tr('Utility', 'Numbering Rebuild'), 
                _tr("Utility", "Are you sure you want to procede with rebuild number sequence for event\n"
                               "'{}' ?").format(eventDescription)],
            4: [set_order_as_processed, _tr('Utility', 'Mark Orders as Processed'), 
                _tr("Utility", "Are you sure you want to mark all orders as processed for event\n"
                               "'{}' ?").format(eventDescription)]}
        if QMessageBox.question(self,
                                utilities[utility_id][DESC],
                                utilities[utility_id][MESSAGE],
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        with gui_exception_context(self, _tr('Utility', 'Execute event tool')):
            utilities[utility_id][FUNC](event_id)
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Utility', 'Operation completed successfully'))


class DeleteToolDialog(QDialog):

    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.ui = Ui_DeleteToolDialog()
        self.ui.setupUi(self)
        addHelpAction(self, "help/delete_tool.html")
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        self.ui.groupBoxWarning.setTitle(_tr('Tool', 'warning'))
        self.ui.labelWarning.setText(_tr('Utility', 
                                         "This utility deletes ALL the data from the "
                                         "selected objects of the current company. It's not possible "
                                         "to undo this operation. Use with caution!\n"
                                         "You can recover data only from a backup copy of the database."))
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).setDefault(True)
       
    def accept(self):
        "Proceed with the selected utility"
        deletes = [(self.ui.checkBoxOrder, delete_all_orders),
                   (self.ui.checkBoxInventory, delete_all_inventory),
                   (self.ui.checkBoxEvent, delete_all_events),
                   (self.ui.checkBoxPriceList, delete_all_price_lists),
                   (self.ui.checkBoxItem, delete_all_items),
                   (self.ui.checkBoxDepartment, delete_all_departments),
                   (self.ui.checkBoxTable, delete_all_tables),
                   (self.ui.checkBoxCashDesk, delete_all_cash_desks)]
        selected = [func for check, func in deletes if check.isChecked()]
        if not selected:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Tool', 'Select the objects to delete'))
            return
        if QMessageBox.question(self,
                                _tr("MessageDialog","Question"),
                                _tr("Tool", "Are you sure you want to delete all the records "
                                    "of the selected objects from the current company ?"),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        # one transaction: a delete that fails, as items still used by another
        # object, leaves everything as it was
        with gui_exception_context(self, _tr('Tool', 'Delete tool')) as outcome:
            with appconn.transaction():
                for func in selected:
                    func()
        if outcome.ok:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Tool', 'Operation completed successfully'))


class CopyToolDialog(QDialog):
    "A dialog to copy selected objects from a selected company to the current company"

    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.ui = Ui_CopyToolDialog()
        self.ui.setupUi(self)
        addHelpAction(self, "help/copy_tool.html")
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        for i, d in company_list():
            if i != session['current_company']:
                self.ui.comboBoxCompany.addItem(d, i)
        self.ui.labelWarning.setText(_tr('Tool', 
                                         "This utility append ALL the records from the "
                                         "selected objects of the selected company to the current company. "
                                         "It's not possible to undo this operation. Use with caution!\n"
                                         "You can recover data only from a backup copy of the database."))
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).setDefault(True)
    
    def accept(self):
        "Proceed with the selected utility"
        # selected company id
        company_id = self.ui.comboBoxCompany.currentData()
        # departments before items: copied items look for them by description
        copies = [(self.ui.checkBoxCashDesk, copy_cash_desk),
                  (self.ui.checkBoxTable, copy_table),
                  (self.ui.checkBoxDepartment, copy_department),
                  (self.ui.checkBoxItem, copy_item)]
        selected = [func for check, func in copies if check.isChecked()]
        if company_id is None or not selected:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Tool', 'Select the company and the objects to copy'))
            return
        if QMessageBox.question(self,
                                _tr("MessageDialog","Question"),
                                _tr("Tool", "Are you sure you want to copy all the records "
                                    "of the selected objects of the selected company to the current company ?"),
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        # one transaction: a copy that fails, as a code already present, copies nothing
        with gui_exception_context(self, _tr('Tool', 'Copy tool')) as outcome:
            with appconn.transaction():
                for func in selected:
                    func(company_id)
        if outcome.ok:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Tool', 'Operation completed successfully'))
