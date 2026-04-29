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


"""Departments

This module is used to manage department archive


"""

# standard library
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QStyledItemDelegate
#from PySide6.QtWidgets import QAbstractItemView

# application modules
from App import session
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Database.Lookup import printer_class_lookup
from App.Database.Models import DepartmentModel
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Delegate import IntegerDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import GenericDelegate
from App.Widget.Form import FormViewManager
from App.Ui.DepartmentWidget import Ui_DepartmentWidget


(ID, DESCRIPTION, SORTING, PRINTER, OBSOLETE, NOMANAGE, TAKEAWAY,
 USER_INS, DATE_INS, USER_UPD, DATE_UPD) = range(11)


def department(action: QAction, checked: bool = False) -> None:
    "Manage departments"
    logging.info('Starting departments Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    dw = DepartmentForm(mw, title, auth)
    dw.reload()
    mw.addTab(title, dw)
    logging.info('Departments Form added to main window')


class DepartmentForm(FormViewManager[Ui_DepartmentWidget]):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = DepartmentModel(self)
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, False, False, False, False,
                                False, False, False, False)
        self.ui = Ui_DepartmentWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setLayoutName('department')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        #self.ui.tableView.setItemDelegate(QStyledItemDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(PRINTER, RelationDelegate(self, printer_class_lookup))
        #self.ui.tableView.setItemDelegateForColumn(SORTING, IntegerDelegate(self))
        #self.ui.tableView.setItemDelegateForColumn(OBSOLETE, BooleanDelegate(self))
        #self.ui.tableView.setItemDelegateForColumn(NOMANAGE, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(TAKEAWAY, BooleanDelegate(self))
        # scripting init
        self.script = scriptInit(self)

    @scriptMethod
    def new(self) -> None:
        "Edit second column of the view on new inserted rows"
        super().new()
        model = self.ui.tableView.model()
        row = model.rowCount() -1
        index = model.createIndex(row, DESCRIPTION)
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