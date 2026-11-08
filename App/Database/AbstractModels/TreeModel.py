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

"""Tree Models

This module contains generic and reusable tree models for database tables

"""

# standard library
import logging
from decimal import Decimal
from typing import Any
from typing import Optional
from enum import IntEnum

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime

# application modules
from App.Database import OVFIELD
from App.Database.Exceptions import db_exception_context
from App.Database.Exceptions import PyAppDBConcurrencyError
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


class stt(IntEnum):
    UPDATED     = 0
    INSERTED    = 1
    SYNC        = 2

FIELD, DESCRIPTION, RO, TYPE = range(4) # field columns attributes


class TreeItem:
    """A node of the tree: the values of one row and its children"""

    def __init__(self, data: dict[int, Any], parent: Optional[TreeItem] = None) -> None:
        self.parentItem = parent
        self.itemData = data  # dict of column: value
        self.childItems: list[TreeItem] = []
        self.state: Optional[int] = None  # stt value, None for read only trees
        self.pkey: dict[str, Any] = {}  # primary key as read from the database
        self.objectVersion: Any = None

    def child(self, row: int) -> Optional[TreeItem]:
        if 0 <= row < len(self.childItems):
            return self.childItems[row]
        return None

    def appendChild(self, item: TreeItem) -> None:
        self.childItems.append(item)

    def childCount(self) -> int:
        return len(self.childItems)

    def childNumber(self) -> int:
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def columnCount(self) -> int:
        return len(self.itemData)

    def parent(self) -> Optional[TreeItem]:
        return self.parentItem

    def data(self, column: int) -> Any:
        return self.itemData.get(column)


class TreeQueryModel(QAbstractItemModel):
    """A read-only tree model populated from sequential nested database queries."""
    
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.isEditable = False
        self.rootItem: Optional[TreeItem] = None
        self.orderByExpressions: list[str] = []
        self.repr: str = 'Generic tree query model'
        self.script: list[str] = []  # List of SQL scripts defined by subclasses per hierarchy level
        self.currentLevel = 0
        self.columns: Any = []  # List of tuples: (field name, field description, read only flag, field type)
        self.childFieldColumn: int = 0  # Index of the child field in the query result

    def __repr__(self) -> str:
        return self.repr

    def setRepr(self, text: str) -> None:
        self.repr = text

    def filter(self, column: int, value: Any) -> None:
        """Initializes the root item and triggers the recursive database walk."""
        # views must know about the reset before the old items are dropped
        self.beginResetModel()
        try:
            self.rootItem = TreeItem({i: None for i, _ in enumerate(self.columns)})
            self.rootItem.itemData[self.childFieldColumn] = value
            self._walk(self.rootItem)
        finally:
            self.endResetModel()

    def _walk(self, parentItem: TreeItem) -> None:
        """Recursively fetches child items from PostgreSQL based on the parent value."""
        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            parent_value = parentItem.data(self.childFieldColumn)
            cur.execute(self.script[self.currentLevel], (parent_value,))
            
            for record in cur:
                item_data = {}
                for i in range(len(self.columns)):
                    item_data[i] = record[i]
                    
                child_node = TreeItem(item_data, parentItem)
                parentItem.appendChild(child_node)
                
                # Recurse deeper into the hierarchy level
                self.currentLevel += 1
                self._walk(child_node)
                self.currentLevel -= 1

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        parentItem = self.getItem(parent)
        return parentItem.childCount() if parentItem else 0

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self.columns)

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        """Returns standard read-only flags. Explicitly excludes ItemIsEditable."""
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Handles pure visualization logic (alignments, hiding raw boolean strings)."""
        if (not index.isValid() 
            or index.row() >= self.rowCount(index.parent()) 
            or index.column() >= self.columnCount()):
            return None

        item = self.getItem(index)
        if not item:
            return None

        col = index.column()
        result = item.data(col)
        
        # Check if column type is defined as 'bool' (index 3 in your columns configuration tuple)
        is_bool_column = (self.columns[col][3] == 'bool') if col < len(self.columns) else False

        match role:
            case Qt.ItemDataRole.DisplayRole:
                # Prevent showing raw text ("True"/"False") for boolean columns
                return None if (is_bool_column or isinstance(result, bool)) else result

            case Qt.ItemDataRole.CheckStateRole if is_bool_column or isinstance(result, bool):
                return Qt.CheckState.Checked if result else Qt.CheckState.Unchecked

            case Qt.ItemDataRole.TextAlignmentRole:
                # Right-align numeric/date data types, left-align everything else (excluding booleans)
                if isinstance(result, (int, float, Decimal, QDate, QDateTime)) and not isinstance(result, bool):
                    return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

            case _:
                return None

    def getItem(self, index: QModelIndex | QPersistentModelIndex) -> Optional[TreeItem]:
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section][DESCRIPTION]
        return None

    def index(self, row: int, column: int, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()
            
        parentItem = self.getItem(parent)
        if not parentItem:
            return QModelIndex()
            
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index: Optional[QModelIndex | QPersistentModelIndex] = None) -> Any:
        """Returns the parent of the model index, or the QObject parent if no index is provided."""
        # If called without arguments, fallback to QObject.parent() to satisfy the supertype signature
        if index is None:
            return super().parent()

        if not index.isValid():
            return QModelIndex()
            
        childItem = self.getItem(index)
        if not childItem:
            return QModelIndex()
            
        parentItem = childItem.parent()
        if parentItem == self.rootItem or parentItem is None:
            return QModelIndex()
            
        return self.createIndex(parentItem.childNumber(), 0, parentItem)


    def addOrderBy(self, expression: str) -> None:
        self.orderByExpressions.append(expression)

    def clear(self) -> None:
        """Deletes all items in the model hierarchy."""
        self.beginResetModel()
        if self.rootItem:
            self.rootItem.childItems.clear()
        self.endResetModel()




class TreeModel(QAbstractItemModel):
    """A writable tree model on a self referencing table: a row is a child of
    the row whose child field matches its parent field.

    A subtree can be shared: the same child code under two parents shows the
    same children in both places (the menus of two languages share submenus).
    The primary key is (parent field, child field); the parent field follows
    the tree and the child field can be set on new rows only.
    Saving uses optimistic concurrency on the object version, as TableModel.
    """

    userDataChanged = Signal()  # Emitted only when actual data modifications happen

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.table: Optional[str] = None
        self.columns: Any = []  # List of tuples: (field name, field description, read only flag, field type)
        self.primaryKey: tuple[str, ...] = ()  # (parent field, child field)
        self.parentField: Optional[str] = None
        self.parentFieldColumn: Optional[int] = None
        self.childField: Optional[str] = None
        self.childFieldColumn: Optional[int] = None
        self.isEditable = True
        # codes whose children can't change, a subtree shared with a read only tree:
        # the rows under them are read only, no row can be added or removed there
        self.lockedCodes: set = set()
        self.isDirty = False
        self.rootItem: Optional[TreeItem] = None
        self.toDelete: list[TreeItem] = []
        self.orderByExpressions: list[str] = []
        self.repr = 'Generic tree model'
        self._script = ""

    def __repr__(self) -> str:
        return self.repr

    def select(self) -> None:
        """Build the query that reads the children of a node"""
        fields = ", ".join([f"{i[FIELD]}" for i in self.columns] + [OVFIELD])
        self._script = f"SELECT {fields}\nFROM {self.table}\nWHERE {self.parentField} = %s"
        if self.orderByExpressions:
            self._script += f"\nORDER BY {', '.join(self.orderByExpressions)}"
        self._script += ";"

    def filter(self, detailColumn: Optional[int], value: Any) -> None:
        """Load the tree whose top level rows have `value` as parent"""
        # views must know about the reset before the old items are dropped
        self.beginResetModel()
        try:
            self.toDelete.clear()
            self.isDirty = False
            self.rootItem = TreeItem({i: None for i, _ in enumerate(self.columns)})
            if self.childFieldColumn is not None:
                self.rootItem.itemData[self.childFieldColumn] = value
                if value is not None:
                    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
                        self._walk(cur, self.rootItem, set())
        finally:
            self.endResetModel()

    def _walk(self, cur: Any, parentItem: TreeItem, ancestors: set) -> None:
        """Read the children of a node, then theirs"""
        code = parentItem.data(self.childFieldColumn)    # type: ignore[arg-type]
        if code in ancestors:   # a loop in the data: stop here
            logger.warning("%s: %s is its own ancestor", self.repr, code)
            return
        cur.execute(self._script, (code,))
        n = len(self.columns)
        for record in cur.fetchall():   # fetch all: the cursor is reused for the children
            node = TreeItem({i: record[i] for i in range(n)}, parentItem)
            node.pkey = {f: record[self._fieldColumn(f)] for f in self.primaryKey}
            node.objectVersion = record[n]
            node.state = stt.SYNC
            parentItem.appendChild(node)
            self._walk(cur, node, ancestors | {code})

    def _fieldColumn(self, field: str) -> int:
        return [c[FIELD] for c in self.columns].index(field)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() != 0:
            return 0
        parentItem = self.getItem(parent)
        return parentItem.childCount() if parentItem else 0

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self.columns)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        item = self.getItem(index)
        if not item:
            return None
        col = index.column()
        result = item.data(col)
        is_bool_column = self.columns[col][TYPE] == 'bool'
        match role:
            case Qt.ItemDataRole.EditRole:
                return result
            case Qt.ItemDataRole.DisplayRole:
                return None if (is_bool_column or isinstance(result, bool)) else result
            case Qt.ItemDataRole.CheckStateRole if is_bool_column:
                return Qt.CheckState.Checked if result else Qt.CheckState.Unchecked
            case Qt.ItemDataRole.TextAlignmentRole:
                if isinstance(result, (int, float, Decimal, QDate, QDateTime)) and not isinstance(result, bool):
                    return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            case _:
                return None

    def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if not index.isValid():
            return False
        item = self.getItem(index)
        if not item:
            return False
        col = index.column()
        new_value: Any
        if role == Qt.ItemDataRole.CheckStateRole and self.columns[col][TYPE] == 'bool':
            new_value = (value in (Qt.CheckState.Checked, Qt.CheckState.Checked.value))
        elif role == Qt.ItemDataRole.EditRole:
            if isinstance(value, Qt.CheckState):
                new_value = (value == Qt.CheckState.Checked)
            elif isinstance(value, str):
                new_value = value if value.strip() else None
            else:
                new_value = value
        else:
            return False
        if item.data(col) == new_value:
            return False
        item.itemData[col] = new_value
        if item.state != stt.INSERTED:
            item.state = stt.UPDATED
        self.isDirty = True
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole, Qt.ItemDataRole.CheckStateRole])
        self.userDataChanged.emit()
        return True

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        """Read only columns and the parent field are never editable, the child field only on new rows"""
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        col = index.column()
        item = self.getItem(index)
        if (not self.isEditable or self.columns[col][RO] or col == self.parentFieldColumn
                or (item is not None and self._isLocked(item.parentItem))
                or (col == self.childFieldColumn and item is not None and item.state != stt.INSERTED)):
            return flags
        return flags | Qt.ItemFlag.ItemIsEditable

    def _isLocked(self, node: Optional[TreeItem]) -> bool:
        """True when the children of the node can't change"""
        if node is None or node is self.rootItem or self.childFieldColumn is None:
            return False
        return node.data(self.childFieldColumn) in self.lockedCodes

    def isLocked(self, index: QModelIndex | QPersistentModelIndex) -> bool:
        """True when the children of the node at index can't change"""
        return self._isLocked(self.getItem(index)) if index.isValid() else False

    def getItem(self, index: QModelIndex | QPersistentModelIndex) -> Optional[TreeItem]:
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section][DESCRIPTION]
        return None

    def index(self, row: int, column: int, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()
        parentItem = self.getItem(parent)
        if not parentItem:
            return QModelIndex()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index: Optional[QModelIndex | QPersistentModelIndex] = None) -> Any:
        """Polymorphic parent implementation to prevent QObject override collisions under Mypy."""
        if index is None:
            return super().parent()
        if not index.isValid():
            return QModelIndex()
        childItem = self.getItem(index)
        if not childItem:
            return QModelIndex()
        parentItem = childItem.parent()
        if parentItem == self.rootItem or parentItem is None:
            return QModelIndex()
        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def insertRows(self, position: int, count: int, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> bool:
        """Insert new rows under a node, their parent field shows the code of that node"""
        parentItem = self.getItem(parent)
        if (not self.isEditable or not parentItem or self._isLocked(parentItem)
                or position < 0 or position > len(parentItem.childItems)):
            return False
        self.beginInsertRows(parent, position, position + count - 1)
        for _ in range(count):
            item = TreeItem({col: None for col in range(self.columnCount())}, parentItem)
            if self.parentFieldColumn is not None and self.childFieldColumn is not None:
                item.itemData[self.parentFieldColumn] = parentItem.data(self.childFieldColumn)
            item.state = stt.INSERTED
            parentItem.childItems.insert(position, item)
        self.endInsertRows()
        self.isDirty = True
        self.userDataChanged.emit()
        return True

    def removeRows(self, position: int, count: int, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> bool:
        """Remove rows with their subtree; the saved ones are deleted on submitAll"""
        parentItem = self.getItem(parent)
        if (not self.isEditable or not parentItem or self._isLocked(parentItem)
                or position < 0 or position + count > len(parentItem.childItems)):
            return False
        self.beginRemoveRows(parent, position, position + count - 1)
        for _ in range(count):
            item = parentItem.childItems.pop(position)
            if item.state != stt.INSERTED:
                self.toDelete.append(item)
        self.endRemoveRows()
        self.isDirty = True
        self.userDataChanged.emit()
        return True

    def addOrderBy(self, expression: str) -> None:
        self.orderByExpressions.append(expression)

    def clear(self) -> None:
        """Drop every node and pending delete"""
        self.beginResetModel()
        if self.rootItem:
            self.rootItem.childItems.clear()
        self.toDelete.clear()
        self.endResetModel()

    def submit(self) -> bool:
        return True

    def submitAll(self, detailColumn: Optional[int] = None, value: Any = None) -> bool:
        """Write deletes, updates and inserts in one transaction, then read the tree back.

        `value` is the code of the master record: the parent of the top level rows,
        known only on save when the master record is new.
        """
        if (not self.rootItem or self.childFieldColumn is None or self.parentFieldColumn is None
                or self.childField is None):
            return True
        parentCol, childCol, childField = self.parentFieldColumn, self.childFieldColumn, self.childField
        if value is not None:
            self.rootItem.itemData[childCol] = value
        whereKey = " AND ".join([f"{k} = %({k})s" for k in self.primaryKey])
        whereVersion = f"{whereKey} AND {OVFIELD} = %({OVFIELD})s"
        # fields written: editable columns with a name, the key is never updated
        writable = [(i, c[FIELD]) for i, c in enumerate(self.columns) if c[FIELD] and not c[RO]]
        updatable = [(i, f) for i, f in writable if f not in self.primaryKey]
        setFields = ", ".join([f"{f} = %({f})s" for _, f in updatable]) or f"{OVFIELD} = {OVFIELD}"

        def save(cur: Any, node: TreeItem) -> None:
            # a new row can get a locked code as long as it has no children yet:
            # what is under it would go into the shared subtree
            if node.state != stt.SYNC and self._isLocked(node.parentItem):
                raise PyAppDBError(code='LOCK', message='A shared read only subtree can not be changed',
                                   detail=str(node.parentItem.data(childCol)))   # type: ignore[union-attr]
            if node.state == stt.UPDATED:
                args = {f: node.data(i) for i, f in updatable} | node.pkey | {OVFIELD: node.objectVersion}
                cur.execute(f"UPDATE {self.table} SET {setFields} WHERE {whereVersion};", args)
                if cur.rowcount == 0:
                    raise PyAppDBConcurrencyError()
            elif node.state == stt.INSERTED:
                # the parent field follows the tree: the code of the parent node
                node.itemData[parentCol] = node.parentItem.data(childCol)   # type: ignore[union-attr]
                args = {f: node.data(i) for i, f in writable}
                fields = ", ".join(args)
                # an empty field takes the column default of the table
                values = ", ".join(["DEFAULT" if v is None else f"%({f})s" for f, v in args.items()])
                cur.execute(f"INSERT INTO {self.table} ({fields}) VALUES ({values});", args)
            for child in node.childItems:
                save(cur, child)

        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            for node in self.toDelete:
                cur.execute(f"DELETE FROM {self.table} WHERE {whereVersion};",
                            node.pkey | {OVFIELD: node.objectVersion})
                if cur.rowcount == 0:
                    raise PyAppDBConcurrencyError()
                self._deleteUnused(cur, node.pkey[childField])
            for node in self.rootItem.childItems:
                save(cur, node)
        # read back: new object versions and whatever triggers wrote
        self.filter(detailColumn, self.rootItem.data(childCol))
        return True

    def _deleteUnused(self, cur: Any, code: Any) -> None:
        """Delete the children of `code` when no row refers to it any more,
        a subtree still used by another parent stays"""
        cur.execute(f"SELECT 1 FROM {self.table} WHERE {self.childField} = %s LIMIT 1;", (code,))
        if cur.fetchone():
            return
        cur.execute(f"DELETE FROM {self.table} WHERE {self.parentField} = %s RETURNING {self.childField};", (code,))
        for (child,) in cur.fetchall():
            self._deleteUnused(cur, child)
