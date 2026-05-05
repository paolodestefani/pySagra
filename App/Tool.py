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
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App import currentAction
from App.Database.Exceptions import PyAppDBError
from App.Database.Lookup import event_lookup
from App.Database.Tool import delete_event_order
from App.Database.Tool import inventory_rebuild
from App.Database.Tool import ordered_delivered_rebuild
from App.Database.Tool import numbering_rebuild
from App.Database.Tool import set_order_as_processed
from App.Database.Tool import delete_all_orders
from App.Database.Tool import delete_all_web_orders
from App.Database.Tool import delete_all_inventory
from App.Database.Tool import delete_all_events
from App.Database.Tool import delete_all_price_lists
from App.Database.Tool import delete_all_items
from App.Database.Tool import delete_all_departments
from App.Database.Tool import delete_all_tables
from App.Database.Tool import delete_all_cash_desks
from App.Database.Tool import delete_all_printer_classes
from App.Database.Tool import copy_cash_desk
from App.Database.Tool import copy_printer_class
from App.Database.Tool import copy_table
from App.Database.Tool import copy_department

from App.Database.Company import company_list
from App.Ui.EventToolDialog import Ui_EventToolDialog
from App.Ui.DeleteToolDialog import Ui_DeleteToolDialog
from App.Ui.CopyToolDialog import Ui_CopyToolDialog
from App.Core.L10n import _tr



def eventBasedTool(action: QAction, checked: bool = False) -> None:
    "Launch event based tool dialog"
    logging.info('Starting event based tool dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    if auth != 'X':
        QMessageBox.information(mw,
                                _tr('MessageDialog', 'Information'),
                                _tr('Utility', 'You are not authorized to use this utility'))
        return
    if not event_lookup():
        QMessageBox.information(mw,
                                _tr('MessageDialog', 'Information'),
                                _tr('Utility', 'No event available'))
        return
    dlg = EventToolDialog(mw, title, icon)
    if dlg.exec() == QDialog.DialogCode.Rejected:
        return
    dlg.close()
    logging.info('Delete event based tool shown')
    
def deleteTool(action: QAction, checked: bool = False) -> None:
    "Delete selected objects from current company"
    logging.info('Starting delete tool dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    if auth != 'X':
        QMessageBox.information(mw,
                                _tr('MessageDialog', 'Information'),
                                _tr('Utility', 'You are not authorized to use this utility'))
        return
    dlg = DeleteToolDialog(mw, title, icon)
    if dlg.exec() == QDialog.DialogCode.Rejected:
        return
    dlg.close()
    logging.info('Delete tool dialog shown')

def copyTool(action: QAction, checked: bool = False) -> None:
    "Copy selected objects from a selected company to the current company"
    logging.info('Starting copy tool dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    if auth != 'X':
        QMessageBox.information(mw,
                                _tr('MessageDialog', 'Information'),
                                _tr('Utility', 'You are not authorized to use this utility'))
        return
    dlg = CopyToolDialog(mw, title, icon)
    if dlg.exec() == QDialog.DialogCode.Rejected:
        return
    dlg.close()
    logging.info('Copy tool dialog shown')
    


class EventToolDialog(QDialog):

    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.ui = Ui_EventToolDialog()
        self.ui.setupUi(self)
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
        self.ui.progressBar.hide()
       
    def updateWarning(self, index):
        "Update warning text according to selected utility"
        utility_id = self.ui.comboBoxUtility.currentData()
        if utility_id == 0:
            self.ui.groupBoxWarning.setTitle(_tr('Utility', 'Warning'))
            self.ui.labelWarning.setText(_tr('Utility', 
                                             "This utility function delete ALL "
                                             "orders of the selected event. It's not possible "
                                             "to undo this operation."))
        elif utility_id == 1:
            self.ui.groupBoxWarning.setTitle(_tr('Utility', 'Information'))
            self.ui.labelWarning.setText(_tr('Utility', 
                                             "This utility function rebuild stock "
                                             "unload from orders of the selected event. Use "
                                             "this when changed item state/flags "
                                             "or when manually altered orders."))
        elif utility_id == 2:
            self.ui.groupBoxWarning.setTitle(_tr('Utility', 'Information'))
            self.ui.labelWarning.setText(_tr('Utility', 
                                             "This utility function rebuild "
                                             "numbering from orders of the selected event."))
        elif utility_id == 3:
            self.ui.groupBoxWarning.setTitle(_tr('Utility', 'Information'))
            self.ui.labelWarning.setText(_tr('Utility', 
                                             "This utility function mark all "
                                             "orders as processed at the order date"))

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
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        QCoreApplication.processEvents() # update dialog
        #self.ui.progressBar.setText(_tr('Utility', 'Processing...'))
        self.ui.progressBar.show()
        self.ui.progressBar.setRange(0, 0)  # infinite progress
        try:
            utilities[utility_id][FUNC](event_id), 
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', 'Critical'),
                                 f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Utility', 'Operation completed successfully'))
        finally:
            self.ui.progressBar.setRange(0, 100)
            self.ui.progressBar.hide()
            #super().accept()


class DeleteToolDialog(QDialog):

    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.ui = Ui_DeleteToolDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        self.ui.groupBoxWarning.setTitle(_tr('Utility', 'warning'))
        self.ui.labelWarning.setText(_tr('Utility', 
                                         "This utility deletes ALL the data from the "
                                         "selected objects of the current company. It's not possible "
                                         "to undo this operation. Use with caution!\n"
                                         "You can recover data only from a backup copy of the database."))
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).setDefault(True)
       
    def accept(self):
        "Proceed with the selected utility"
        
        if QMessageBox.question(self,
                                _tr("Utility","Delete Tool"),
                                _tr("Utility", "Are you sure you want to delete all the records "
                                    "of the selected objects from the current company ?"),
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        try:
            if self.ui.checkBoxOrder.isChecked():
                delete_all_orders()
            if self.ui.checkBoxWebOrder.isChecked():
                delete_all_web_orders()
            if self.ui.checkBoxInventory.isChecked():
                delete_all_inventory()
            if self.ui.checkBoxEvent.isChecked():
                delete_all_events()
            if self.ui.checkBoxPriceList.isChecked():
                delete_all_price_lists()
            if self.ui.checkBoxItem.isChecked():
                delete_all_items()
            if self.ui.checkBoxDepartment.isChecked():
                delete_all_departments()
            if self.ui.checkBoxTable.isChecked():
                delete_all_tables()
            if self.ui.checkBoxCashDesk.isChecked():
                delete_all_cash_desks()
            if self.ui.checkBoxPrinterClass.isChecked():
                delete_all_printer_classes()
                
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', 'Critical'),
                                 f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Utility', 'Operation completed successfully'))


class CopyToolDialog(QDialog):
    "A dialog to copy selected objects from a selected company to the current company"

    def __init__(self, parent, title, icon):
        super().__init__(parent)
        self.ui = Ui_CopyToolDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        for i, d in company_list():
            if i != session['current_company']:
                self.ui.comboBoxCompany.addItem(d, i)
        self.ui.labelWarning.setText(_tr('Utility', 
                                         "This utility append ALL the records from the "
                                         "selected objects of the selected company to the current company. "
                                         "It's not possible to undo this operation. Use with caution!\n"
                                         "You can recover data only from a backup copy of the database."))
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).setDefault(True)
    
    def accept(self):
        "Proceed with the selected utility"
        # selected company id
        company_id = self.ui.comboBoxCompany.currentData()
        if QMessageBox.question(self,
                                _tr("Utility","Copy Tool"),
                                _tr("Utility", "Are you sure you want to copy all the records "
                                    "of the selected objects of the selected company to the current company ?"),
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        try:
            if self.ui.checkBoxCashDesk.isChecked():
                copy_cash_desk(company_id)
            if self.ui.checkBoxPrinterClass.isChecked():
                copy_printer_class(company_id)
            if self.ui.checkBoxTable.isChecked():
                copy_table(company_id)
            # if self.ui.checkBoxSettings.isChecked():
            #     copy_settings(company_id)
            if self.ui.checkBoxDepartment.isChecked():
                copy_department(company_id)
            # if self.ui.checkBoxItem.isChecked():
            #     copy_items(company_id)
            # if self.ui.checkBoxInventory.isChecked():
            #     copy_inventory(company_id)
            # if self.ui.checkBoxPriceList.isChecked():
            #     copy_price_lists(company_id)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                _tr('MessageDialog', 'Critical'),
                                f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Utility', 'Operation completed successfully'))
