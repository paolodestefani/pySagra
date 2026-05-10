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

"""Toolbar

This module manages application toolbars

"""

# standard library
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox


# application modules
from App import session
#from App import currentAction
from App import currentIcon
from App.Core.L10n import _tr
from App.Database.Exceptions import PyAppDBError
from App.Database.Models import ToolbarIndexModel
from App.Database.Models import ToolbarModel
from App.Database.Models import ToolbarItemTreeModel
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import ActionDelegate
from App.Widget.Form import FormIndexManager
from App.Widget.Dialog import PrintDialog
from App.Ui.ToolbarWidget import Ui_ToolbarWidget
from App.Ui.DuplicateDialog import Ui_DuplicateDialog


# logger
logger = logging.getLogger(__name__)

CODE, DESCRIPTION, SYSTEM = range(3)

PARENT, CHILD, ITEMDESCRIPTION, SORTING, ITEMTYPE, ACTION = range(6)


def toolbar(action: QAction, checked: bool = False) -> None:
    "Show/Edit toolbars"
    logging.info('Starting toolbar Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    tf = ToolbarForm(mw, title, auth)
    tf.applySortFilter()
    mw.addTab(title, tf)
    logging.info('Toolbar Form added to main window')   


class ToolbarForm(FormIndexManager):
    "Toolbar form management"

    def __init__(self, parent: QWidget, title: str, auth: str)-> None: # no parent for tabwidget widget pages
        super().__init__(parent, auth)
        model = ToolbarModel()
        idxModel = ToolbarIndexModel()
        treeModel = ToolbarItemTreeModel()
        treeModel.select()
        self.setModel(model, idxModel)
        self.addDetailRelation(treeModel, 0, 0)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, False, False)
        self.ui = Ui_ToolbarWidget()
        self.ui.setupUi(self)
        # icons for add/remove buttons
        self.ui.pushButtonAddChild.setIcon(currentIcon['edit_add_child'])
        self.ui.pushButtonAdd.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemove.setIcon(currentIcon['edit_remove'])
        self.setIndexView(self.ui.tableView)
        # widget settings
        self.ui.tableView.setLayoutName('ToolbarIndex')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.mapper.addMapping(self.ui.lineEditCode, CODE)
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        self.mapper.addMapping(self.ui.checkBoxSystem, SYSTEM)
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # menu item treeview
        self.ui.treeViewMenuItems.setModel(treeModel)
        self.ui.treeViewMenuItems.setItemDelegateForColumn(ACTION, ActionDelegate(self))
        # signal/slot
        self.ui.pushButtonAddChild.clicked.connect(self.addChild)
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)

    def addChild(self) -> None:
        "Add child item to current"
        index = self.ui.treeViewMenuItems.selectionModel().currentIndex()
        model = self.ui.treeViewMenuItems.model()
        if model.columnCount(index) == 0:
            if not model.insertColumn(0, index):
                return
        if not model.insertRow(0, index):
            return
        for column in range(model.columnCount(index)):
            child = model.index(0, column, index)
            model.setData(child, "[No data]", Qt.ItemDataRole.EditRole)
            if model.headerData(column, Qt.Orientation.Horizontal) is None:
                model.setHeaderData(column, Qt.Orientation.Horizontal, "[No header]", Qt.ItemDataRole.EditRole)

        self.ui.treeViewMenuItems.selectionModel().setCurrentIndex(model.index(0, 0, index),
                                                                   QItemSelectionModel.SelectionFlag.ClearAndSelect)

    def add(self) -> None:
        "Add element"
        index = self.ui.treeViewMenuItems.selectionModel().currentIndex()
        model = self.ui.treeViewMenuItems.model()
        if not model.insertRow(index.row() + 1, index.parent()):
            return
        for column in range(model.columnCount(index.parent())):
            child = model.index(index.row() + 1, column, index.parent())
            model.setData(child, "[No data]", Qt.ItemDataRole.EditRole)
            if model.headerData(column, Qt.Orientation.Horizontal) is None:
                model.setHeaderData(column, Qt.Orientation.Horizontal, "[No header]", Qt.ItemDataRole.EditRole)

    def remove(self) -> None:
        "Remove element"
        index = self.ui.treeViewMenuItems.selectionModel().currentIndex()
        model = self.ui.treeViewMenuItems.model()
        if (model.removeRow(index.row(), index.parent())):
            pass

    def mapperIndexChanged(self, row: int) -> None:
        "Make uneditable system profiles"
        super().mapperIndexChanged(row)
        if self.ui.checkBoxSystem.isChecked():
            self.ui.lineEditCode.setReadOnly(True)
            self.ui.lineEditDescription.setReadOnly(True)
        else:
            self.ui.lineEditCode.setReadOnly(False)
            self.ui.lineEditDescription.setReadOnly(False)

    def delete(self) -> None:
        "Delete current toolbar"
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Toolbar', "Is not possible to delete a system shortcut scheme"))
            return
        scheme = self.ui.lineEditCode.text()
        description = self.ui.lineEditDescription.text()
        msg = _tr('Toolbar', "Are you sure you want to delete this scheme ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{scheme} - {description}",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    def new(self) -> None:
        "Inser a new toolbar"
        super().new()
        self.ui.lineEditCode.setEnabled(True)
        self.ui.lineEditCode.setFocus()

    def save(self) -> None:
        "Save data, set widgets to default state"
        self.ui.lineEditCode.setDisabled(True)
        super().save()

    def reload(self) -> None:
        "Reload data, set widgets to default state"
        self.ui.lineEditCode.setDisabled(True)
        super().reload()

