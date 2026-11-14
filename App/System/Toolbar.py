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
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox


# application modules
from App import session
from App import currentIcon
from App.Common.L10n import _tr
from App.Database.Models import ToolbarIndexModel
from App.Database.Models import ToolbarModel
from App.Database.Models import ToolbarItemTreeModel
from App.Database.Menu import system_codes
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import ActionDelegate
from App.Widget.Form import FormIndexManager
from App.Ui.ToolbarWidget import Ui_ToolbarWidget


# logger
logger = logging.getLogger(__name__)

class tb(IntEnum):
    CODE        = 0
    DESCRIPTION = 1
    SYSTEM      = 2

class tbt(IntEnum):
    PARENT          = 0
    CHILD           = 1
    ITEMDESCRIPTION = 2
    SORTING         = 3
    NODETYPE        = 4
    ACTION          = 5


def toolbar(action: QAction, checked: bool = False) -> None:
    "Show/Edit toolbars"
    logging.info('Starting toolbar Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(
            mw,
            _tr('MessageDialog', "Warning"),
            _tr('CashDesk', 'No access right to this archive')
        )
        return
    tf = ToolbarForm(mw, title, auth)
    tf.applySortFilter()
    mw.addTab(title, tf)
    logging.info('Toolbar Form added to main window')   


class ToolbarForm(FormIndexManager):
    "Toolbar form management"

    def __init__(self, parent: QWidget, title: str, auth: tuple)-> None: # no parent for tabwidget widget pages
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
        self.mapper.addMapping(self.ui.lineEditCode, tb.CODE)
        self.mapper.addMapping(self.ui.lineEditDescription, tb.DESCRIPTION)
        self.mapper.addMapping(self.ui.checkBoxSystem, tb.SYSTEM)
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # menu item treeview
        self.ui.treeViewMenuItems.setModel(treeModel)
        self.ui.treeViewMenuItems.setLayoutName('ToolbarItems')
        self.ui.treeViewMenuItems.setItemDelegateForColumn(tbt.ACTION, ActionDelegate(self))
        # signal/slot
        self.ui.pushButtonAddChild.clicked.connect(self.addChild)
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)

    def addChild(self) -> None:
        "Add an item under the current one, as its first child"
        view = self.ui.treeViewMenuItems
        index = view.selectionModel().currentIndex()
        if index.isValid():
            index = index.sibling(index.row(), 0)
        self._insertItem(0, index)
        view.expand(index)

    def add(self) -> None:
        "Add an item after the current one, at the top level when nothing is selected"
        index = self.ui.treeViewMenuItems.selectionModel().currentIndex()
        if index.isValid():
            self._insertItem(index.row() + 1, index.parent())
        else:
            self._insertItem(self.ui.treeViewMenuItems.model().rowCount(), index)

    def _insertItem(self, row: int, parent: QModelIndex) -> None:
        "Insert an item with sorting after the previous one, then edit its code"
        model = self.ui.treeViewMenuItems.model()
        if model.isLocked(parent):
            self._lockedWarning()
            return
        if not model.insertRow(row, parent):
            return
        previous = model.index(row - 1, tbt.SORTING, parent).data() if row > 0 else 0
        model.setData(model.index(row, tbt.SORTING, parent), (previous or 0) + 1)
        model.setData(model.index(row, tbt.NODETYPE, parent), 'T')
        child = model.index(row, tbt.CHILD, parent)
        self.ui.treeViewMenuItems.selectionModel().setCurrentIndex(child, QItemSelectionModel.SelectionFlag.ClearAndSelect)
        self.ui.treeViewMenuItems.edit(child)

    def remove(self) -> None:
        "Remove the current item with its subitems"
        index = self.ui.treeViewMenuItems.selectionModel().currentIndex()
        if index.isValid():
            model = self.ui.treeViewMenuItems.model()
            if model.isLocked(index.parent()):
                self._lockedWarning()
                return
            model.removeRow(index.row(), index.parent())

    def _lockedWarning(self) -> None:
        "A submenu also used by a system toolbar can't change, here or anywhere"
        QMessageBox.information(
            self,
            _tr('MessageDialog', "Information"),
            _tr('Toolbar', "This submenu is also used by a system toolbar, it can not be changed")
        )

    def mapperIndexChanged(self, row: int) -> None:
        "Make uneditable system toolbars"
        super().mapperIndexChanged(row)
        self._setSystem(self.ui.checkBoxSystem.isChecked())

    def _setSystem(self, system: bool) -> None:
        "Nothing of a system toolbar can be changed: code, description and items"
        self.ui.lineEditCode.setReadOnly(system)
        self.ui.lineEditDescription.setReadOnly(system)
        self.ui.treeViewMenuItems.model().isEditable = not system
        for button in (self.ui.pushButtonAddChild, self.ui.pushButtonAdd, self.ui.pushButtonRemove):
            button.setEnabled(not system)

    def delete(self) -> None:
        "Delete current toolbar"
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(
                self,
                _tr('MessageDialog', "Information"),
                _tr('Toolbar', "Is not possible to delete a system toolbar")
            )
            return
        scheme = self.ui.lineEditCode.text()
        description = self.ui.lineEditDescription.text()
        msg = _tr('Toolbar', "Are you sure you want to delete this toolbar ?")
        if QMessageBox.question(
            self,
            _tr('MessageDialog', "Question"),
            f"{msg}\n{scheme} - {description}",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
            ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    def new(self) -> None:
        "Inser a new toolbar"
        super().new()
        self._setSystem(False)   # a new toolbar is never a system one
        self.ui.lineEditCode.setEnabled(True)
        self.ui.lineEditCode.setFocus()

    def save(self) -> None:
        "Save data, set widgets to default state"
        self.ui.lineEditCode.setDisabled(True)
        super().save()

    def reload(self) -> None:
        "Reload data, set widgets to default state"
        self.ui.lineEditCode.setDisabled(True)
        # submenus also used by a system toolbar are read only in every toolbar
        self.ui.treeViewMenuItems.model().lockedCodes = system_codes()
        super().reload()

