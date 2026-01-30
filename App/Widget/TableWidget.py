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

"""Views

This module contains general custom views


"""

# standard library
import os
import csv

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QUrl
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QDropEvent
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtGui import QAction
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentIcon
from App.System import _tr
from App.Database.Exceptions import PyAppDBError
from App.Database.Itemview import list_itemviews
from App.Database.Itemview import create_itemview
from App.Database.Itemview import get_view_columns
from App.Database.Itemview import set_view_columns
from App.Database.Itemview import delete_view_layout
from App.Database.Itemview import set_default_view_layout
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import HideTextDelegate
from App.Widget.Delegate import BooleanDelegate



# navigation status settings

(NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST, FILTER, ADD,
 REMOVE, CHANGE, PRINT, EXPORT) = range(14)

VIEW, EDIT = range(2)
FORM, GRID = range(2)


class TableWidgetItem(QTableWidgetItem):
    def __init__(self, value: object = None) -> None:
        super().__init__()
        if isinstance(value, (int, str, bool, QDate, QDateTime)):
            self._data = value
        else:
            self._data = None

    def flags(self) -> Qt.ItemFlags:
        return Qt.ItemIsEditable

    def data(self, role: Qt.ItemDataRole = Qt.DisplayRole) -> object:
        if role == Qt.DisplayRole:
            return self._data
        else:
            return None

    def setData(self, role: Qt.ItemDataRole, value) -> None:
        self._data = value

    def copy(self) -> TableWidgetItem:
        return TableWidgetItem(self._data)


class TableWidgetDragRows(QTableWidget):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event: QDropEvent) -> None:
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[self.item(row_index, column_index).copy() for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)

    def drop_on(self, event: QDropEvent) -> int:
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos: QPoint, index: QModelIndex) -> bool:
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()
