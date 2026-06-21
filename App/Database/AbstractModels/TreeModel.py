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
from typing import Tuple, List
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
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn
from App.Core.L10n import _tr


# logger
logger = logging.getLogger(__name__)

class stt(IntEnum):
    UPDATED     = 0 
    INSERTED    = 1
    SYNC        = 2

FIELD, DESCRIPTION, RO, TYPE = range(4) # field columnsattributes

# Dummy constants for state management (replace with your actual constants or strings)
#INSERTED = 'INSERTED'
#UPDATED = 'UPDATED'


def get_menu_tree(parent: str) -> list[tuple]:
    "Returns actions for given menu parent item"
    sql = """
SELECT 
    parent,
    child,
    item_type,
    coalesce(description, ''),
    sorting,
    coalesce(action, ''),
    object_version
FROM system.menu_toolbar_item m
WHERE parent = %s
ORDER BY sorting;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(sql, (parent,))
        return cur.fetchall()


class TreeItem:
    """A row in the tree model with editing and change-tracking capabilities."""
    ovField = OVFIELD

    def __init__(self, data: dict[int, Any], parent: Optional[TreeItem] = None) -> None:
        self.parentItem = parent
        self.itemData = data  # dict of column: value
        self.childItems: list[TreeItem] = []
        self.state: Optional[int] = None  # E.g., 'Updated', 'Inserted'
        self.pkey: Any = None
        self.toModify: dict[int, Any] = {}  # Tracks columns of modified cells
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

    def childFieldValue(self, fieldColumn: int) -> Any:
        return self.itemData.get(fieldColumn)

    def data(self, column: int) -> Any:
        """Safe O(1) data retrieval for the specific column."""
        return self.itemData.get(column)

    def setData(self, column: int, value: Any) -> bool:
        """Updates data in memory and tracks the modification for PostgreSQL."""
        # Prevent redundant writing if the value has not changed
        if self.itemData.get(column) == value:
            return False

        # Apply change
        self.itemData[column] = value

        # Only mark as 'Updated' if it's an existing row (not a freshly 'Inserted' one)
        if self.state != stt.INSERTED:
            self.state = stt.UPDATED
            
        # Register the column index as modified (useful for building dynamic SQL updates)
        self.toModify[column] = True
        return True

    def insertChildren(self, position: int, count: int, columns_count: int) -> bool:
        """Inserts blank child items at a specific row position."""
        if position < 0 or position > len(self.childItems):
            return False
            
        for _ in range(count):
            # Create a sparse dictionary populated with None for the columns
            blank_data = {col: None for col in range(columns_count)}
            item = TreeItem(blank_data, self)
            item.state = stt.INSERTED
            self.childItems.insert(position, item)
        return True

    def removeChildren(self, position: int, count: int) -> bool:
        """Removes child items from a specific row position."""
        if position < 0 or position + count > len(self.childItems):
            return False
        for _ in range(count):
            self.childItems.pop(position)
        return True
    

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
        self.clear()
        self.rootItem = TreeItem({i: None for i, _ in enumerate(self.columns)})
        self.rootItem.itemData[self.childFieldColumn] = value 
        
        self.beginResetModel()
        self._walk(self.rootItem)
        self.endResetModel()

    def _walk(self, parentItem: TreeItem) -> None:
        """Recursively fetches child items from PostgreSQL based on the parent value."""
        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            parent_value = parentItem.childFieldValue(self.childFieldColumn)
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
            return self.columns[section][0]  # Field name/description
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
        if self.rootItem:
            self.rootItem.childItems.clear()


class TreeModel(QAbstractItemModel):
    """A writable tree model that tracks inserts, updates, and deletes for PostgreSQL sync."""

    userDataChanged = Signal()  # Emitted only when actual data modifications happen

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.table: Optional[str] = None
        self.columns: Any = []  # List of tuples: (field name, field description, read only flag, field type)
        self.primaryKey: Tuple[str, str] = ('', '')  # Dynamic primary key fields
        self.parentField: Optional[str] = None
        self.parentFieldColumn: Optional[int] = None
        self.childField: Optional[str] = None
        self.childFieldColumn: Optional[int] = None
        self.isEditable = True
        self.rootItem: Optional[TreeItem] = None
        self.toDelete: List[TreeItem] = []
        self.orderByExpressions: List[str] = []
        self.repr = 'Generic tree model'
        
        # Internal configuration helpers populated during select()
        self._cols = 0
        self._pkcols: range = range(0)
        self._ovcol = 0
        self._script = ""
        self._hasChildScript = ""

    def __repr__(self) -> str:
        return self.repr

    def select(self) -> None:
        """Constructs the targeted SQL SELECT queries for hierarchical walking."""
        fields = ", ".join([f"{i[0]}" for i in self.columns]
                           + [f"{i}" for i in self.primaryKey]
                           + ["object_version"])
        self._cols = len(self.columns)
        self._pkcols = range(self._cols, self._cols + len(self.primaryKey))
        self._ovcol = self._cols + len(self.primaryKey)
        
        self._script = f"SELECT {fields} \nFROM {self.table}\nWHERE {self.parentField} = %s"
        if self.orderByExpressions:
            self._script += f"\nORDER BY {', '.join(self.orderByExpressions)}"
        self._script += ";"
        self._hasChildScript = f"SELECT {self.childField}\nFROM {self.table} \nWHERE {self.parentField} = %s;"

    def filter(self, detailColumn: int, value: Any) -> None:
        """Initializes the root node and pulls data from the database."""
        self.clear()
        self.rootItem = TreeItem({i: None for i, _ in enumerate(self.columns)})
        if self.childFieldColumn is not None:
            self.rootItem.itemData[self.childFieldColumn] = value 
            
        self.beginResetModel()
        self._walk(self.rootItem)
        self.endResetModel()

    def _walk(self, parentItem: TreeItem) -> None:
        """Recursively steps through database records to construct the network of tree nodes."""
        if self.childFieldColumn is None:
            return
            
        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            parent_value = parentItem.childFieldValue(self.childFieldColumn)
            cur.execute(self._script, (parent_value,))
            
            for record in cur:
                item_data = {}
                for i in range(len(self.columns)):
                    item_data[i] = record[i]
                    
                node = TreeItem(item_data, parentItem)
                node.pkey = {self.primaryKey[i - self._cols]: record[i] for i in self._pkcols}
                node.objectVersion = record[self._ovcol]
                node.state = stt.SYNC  # Synchronized state
                
                parentItem.appendChild(node)
                self._walk(node)

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        parentItem = self.getItem(parent)
        return parentItem.childCount() if parentItem else 0

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self.columns)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Handles pure visualization rendering and formatting configurations."""
        if not index.isValid():
            return None

        item = self.getItem(index)
        if not item:
            return None

        col = index.column()
        result = item.itemData.get(col)
        
        # Identify if column type is defined as 'bool' (index 3 in configuration tuple)
        is_bool_column = (self.columns[col][3] == 'bool') if col < len(self.columns) else False

        match role:
            case Qt.ItemDataRole.DisplayRole | Qt.ItemDataRole.EditRole:
                return None if (is_bool_column or isinstance(result, bool)) else result

            case Qt.ItemDataRole.CheckStateRole if is_bool_column or isinstance(result, bool):
                return Qt.CheckState.Checked if result else Qt.CheckState.Unchecked

            case Qt.ItemDataRole.TextAlignmentRole:
                if isinstance(result, (int, float, Decimal, QDate, QDateTime)) and not isinstance(result, bool):
                    return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

            case _:
                return None

    def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        """Safely mutates values on the targeted node and registers update telemetry flags."""
        if not index.isValid():
            return False

        item = self.getItem(index)
        if not item:
            return False

        col = index.column()
        is_bool_column = (self.columns[col][3] == 'bool') if col < len(self.columns) else False

        # 1. Normalize the inputs according to roles
        new_value: Any
        if role == Qt.ItemDataRole.CheckStateRole and is_bool_column:
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

        # 2. Block evaluation if identical values are submitted
        if item.itemData.get(col) == new_value:
            return False

        # 3. Store modification telemetry inside the node
        item.itemData[col] = new_value
        item.toModify[col] = True

        if item.state != stt.INSERTED:  
            item.state = stt.UPDATED

        # 4. Trigger structural and user-defined repaint signals
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole, Qt.ItemDataRole.CheckStateRole])
        self.userDataChanged.emit()
        return True

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        """Returns cell permissions, enforcing the column configuration's read-only index."""
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
            
        base_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        col = index.column()
        
        # Check read-only boolean flag (index 2 in columns tuple layout)
        is_readonly = self.columns[col][2] if col < len(self.columns) else True
        
        if self.isEditable and not is_readonly:
            return base_flags | Qt.ItemFlag.ItemIsEditable
            
        return base_flags

    def getItem(self, index: QModelIndex | QPersistentModelIndex) -> Optional[TreeItem]:
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section][0]
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
        """Inserts new uninitialized records into the tree memory structure."""
        parentItem = self.getItem(parent)
        if not parentItem or position < 0 or position > len(parentItem.childItems):
            return False
            
        self.beginInsertRows(parent, position, position + count - 1)

        for _ in range(count):
            # Safe sparse dictionary initialized for all columns to avoid KeyError
            blank_data = {col: None for col in range(self.columnCount())}
            item = TreeItem(blank_data, parentItem)
            item.state = stt.INSERTED
            parentItem.childItems.insert(position, item)

        self.endInsertRows()
        return True

    def removeRows(self, position: int, count: int, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> bool:
        """Removes items from the hierarchy and buffers them inside self.toDelete for SQL deletion."""
        parentItem = self.getItem(parent)
        if not parentItem or position < 0 or position + count > len(parentItem.childItems):
            return False
            
        self.beginRemoveRows(parent, position, position + count - 1)
        for _ in range(count):
            deleted_row = parentItem.childItems.pop(position)
            self.toDelete.append(deleted_row)
            
        self.endRemoveRows()
        self.userDataChanged.emit()
        return True

    def addOrderBy(self, expression: str) -> None:
        self.orderByExpressions.append(expression)

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value: Any, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if role != Qt.ItemDataRole.EditRole or orientation != Qt.Orientation.Horizontal:
            return False
        if not self.rootItem:
            return False
        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)
        return result

    def clear(self) -> None:
        """Flushes the active tracking pools and memory nodes."""
        if self.rootItem:
            self.rootItem.childItems.clear()
        self.toDelete.clear()

    def submit(self) -> bool:
        return True

    def submitAll(self, detailColumn: Optional[int] = None, value: Any = None) -> bool:
        """Processes all accumulated memory changes (Inserts, Updates, Deletes) against PostgreSQL.
        
        Handles Master-Detail keys passed by FormIndexManager for proper relational mapping.
        """
        if not self.rootItem:
            return True

        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            # 1. Process Deletions first to respect foreign keys (self.toDelete)
            for item in self.toDelete:
                if item.pkey:
                    # TODO: Generate your dynamic DELETE statement here with Optimistic Locking
                    # sql = f"DELETE FROM {self.table} WHERE ... AND object_version = %s;"
                    pass

            # 2. Process Inserts and Updates by traversing the living memory tree
            def _save_walk(node: TreeItem) -> None:
                if node.state == stt.INSERTED:
                    # SCENARIO 1: Top-level node in the current view
                    if node.parentItem == self.rootItem:
                        if detailColumn is not None:
                            node.itemData[detailColumn] = value
                            
                    # SCENARIO 2: Sub-node inserted under an existing tree item
                    else:
                        parent_node = node.parentItem
                        if parent_node and self.childFieldColumn is not None and self.parentFieldColumn is not None:
                            # The foreign key (parent) becomes the unique identifier (child) of the parent node
                            parent_db_value = parent_node.itemData.get(self.childFieldColumn)
                            node.itemData[self.parentFieldColumn] = parent_db_value

                    # TODO: Generate your dynamic INSERT statement here
                    # Clear tracking state ONLY if it was processed
                    node.state = stt.SYNC
                    node.toModify.clear()

                elif node.state == stt.UPDATED:
                    # TODO: Generate your dynamic UPDATE statement here based on node.toModify
                    # Use node.objectVersion for Optimistic Locking verification
                    
                    # Clear tracking state ONLY if it was processed
                    node.state = stt.SYNC
                    node.toModify.clear()

                # Keep stepping through child objects recursively (always explore the tree)
                for child in node.childItems:
                    _save_walk(child)

            # Start the saving process from the top-level items under rootItem
            for child in self.rootItem.childItems:
                _save_walk(child)

            # Clear deletion pool since all queued records are flushed to db
            self.toDelete.clear()
            self.isDirty = False
            
        return True
