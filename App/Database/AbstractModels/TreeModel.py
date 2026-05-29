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
from typing import Any

# psycopg
import psycopg

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QModelIndex

# application modules
from App.Database import OVFIELD
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn
from App.Core.L10n import _tr


UPDATED, INSERTED, DELETED = range(3)

FIELD, DESCRIPTION, RO, TYPE = range(4) # field columnsattributes


def get_menu_tree(parent: str) -> list[str]:
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
    try:
        with appconn.cursor() as cur:
            cur.execute(sql, (parent,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


class TreeItem():
    "A row in the tree model"
    ovField = 'object_version'

    def __init__(self, data: dict[int, Any], parent: TreeItem|None = None) -> None:
        self.parentItem = parent
        self.itemData = data  # dict of column:value values
        self.childItems: list[TreeItem] = []
        self.state = None  # Updated, Inserted (removed items managed in treeModel)
        self.pkey = None
        self.toModify: dict[int, Any] = {}  # column of the modified cell
        
    def child(self, row: int) -> TreeItem|None:
        if 0 <= row < len(self.childItems):
            return self.childItems[row]
        else:
            return None

    def appendChild(self, item: TreeItem) -> None:
        self.childItems.append(item)

    def childCount(self) -> int:
        return len(self.childItems)

    def childNumber(self) -> int:
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        else:
            return 0

    def columnCount(self) -> int:
        return len(self.itemData)

    #def data(self, column):
        #if column < 0 or column >= len(self.itemData):
            #return None
        #return self.itemData[column]

    #def setData(self, column, value):
        #if column < 0 or column >= len(self.itemData):
            #return False
        ## save the column of the modified cell
        #self.toModify[column] = None
        #self.itemData[column] = value
        #return True

    #def insertChildren(self, position, count, columns):
        #if position < 0 or position > len(self.childItems):
            #return False
        #for row in range(count):
            #data = [None for v in range(columns)]
            #item = TreeItem(data, self)
            #item.parentFieldValue = self.childFieldValue
            #item.state = INSERTED
            #self.childItems.insert(position, item)
        #return True

    #def insertColumns(self, position, columns):
        #if position < 0 or position > len(self.itemData):
            #return False
        #for column in range(columns):
            #self.itemData.insert(position, None)
        #for child in self.childItems:
            #child.insertColumns(position, columns)
        #return True

    def parent(self) -> TreeItem|None:
        return self.parentItem

    #def removeChildren(self, position, count):
        #if position < 0 or position + count > len(self.childItems):
            #return False
        #for row in range(count):
            #self.childItems.pop(position)
        #return True

    #def removeColumns(self, position, columns):
        #if position < 0 or position + columns > len(self.itemData):
            #return False
        #for column in range(columns):
            #self.itemData.pop(position)
        #for child in self.childItems:
            #child.removeColumns(position, columns)
        #return True

    #def parentFieldValue(self):
        #return self.itemData[0]

    def childFieldValue(self, fieldColumn: int) -> Any:
        return self.itemData[fieldColumn]
    
    

class TreeQueryModel(QAbstractItemModel):
    "A tree model from a fixed number on nestet query"
    
    def __init__(self, parent: QObject|None = None) -> None:
        super().__init__(parent)
        self.isEditable = False
        self.rootItem: TreeItem|None = None
        self.orderByExpressions: list[str] = []
        self.repr: str = 'Generic tree query model' # printable representation of the object
        self.script: list[str] = [] # in subclasses the definition and number of sql script
        self.currentLevel = 0
        self.columns: Any = []  # list of tuples (field name, field description, read only flag, field type)
        self.childFieldColumn: int = 0 # column of the child field in the query result, set by the subclass
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr

    def setRepr(self, text: str) -> None:
        "Change the object representation text"
        self.repr = text

    def filter(self, column: int, value: Any) -> None:
        self.clear()
        self.rootItem = TreeItem({i: None for i, c in enumerate(self.columns)})
        self.rootItem.itemData[self.childFieldColumn] = value 
        self.beginResetModel()
        self._walk(self.rootItem)
        self.endResetModel()

    def _walk(self, parentItem):
        try:
            with appconn.cursor() as cur:
                x = parentItem.childFieldValue(self.childFieldColumn)
                cur.execute(self.script[self.currentLevel], (x,))
                for record in cur:
                    itemData = dict()
                    # selected fields
                    for i in range(len(self.columns)):
                        itemData[i] = record[i]
                    n = TreeItem(itemData, parentItem)
                    parentItem.appendChild(n)
                    self.currentLevel += 1
                    self._walk(n)
                    self.currentLevel -= 1
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er)

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        if parentItem:
            return parentItem.childCount()
        return 0

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole, Qt.DecorationRole):
            return None
        item = self.getItem(index)
        return item.itemData[index.column()]

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section][1] # field description
        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()
        parentItem = self.getItem(parent)
        if not parentItem:
            return QModelIndex()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = self.getItem(index)
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def addOrderBy(self, expression):
        self.orderByExpressions.append(expression)

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False
        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)
        return result

    def clear(self):
        "Delete all model items"
        if self.rootItem:
            self.rootItem.childItems.clear()
    
    def submitAll(self, pkey: Any = None) -> bool:
        "Submit all changes to the database, in this model there are no changes allowed, so just return True"
        return True


class TreeModel(QAbstractItemModel):

    userDataChanged = Signal()  # can not use dataChanged because is emitted even on select

    def __init__(self, parent: QObject|None = None) -> None:
        super().__init__(parent)
        self.table: str|None = None
        self.columns: Any = []  # list of tuples (field name, field description, read only flag, field type)
        self.primaryKey: tuple[str, str] = ('', '')  # list of primary key field names
        self.parentField: str|None = None
        self.parentFieldColumn: int|None = None
        self.childField: str|None = None
        self.childFieldColumn: int|None = None
        self.isEditable = True
        self.rootItem: TreeItem|None = None
        self.toDelete: list[TreeItem] = []
        self.orderByExpressions: list[str] = []
        self.repr = 'Generic tree model' # printable representation of the object
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr

    def select(self) -> None:
        "Create the tree model from database select"
        # select fields + primary key fields + object version field
        fields = ", ".join([f"{i[FIELD]}" for i in self.columns]
                           + [f"{i}" for i in self.primaryKey]
                           + [f"{OVFIELD}"])
        self._cols = len(self.columns)
        self._pkcols = range(self._cols, self._cols + len(self.primaryKey))
        self._ovcol = self._cols + len(self.primaryKey)
        self._script = f"SELECT {fields} \nFROM {self.table}\nWHERE {self.parentField} = %s"
        if self.orderByExpressions:
            self._script += f"\nORDER BY {', '.join(self.orderByExpressions)}"
        self._script += ";"
        self._hasChildScript = f"SELECT {self.childField}\nFROM {self.table} \nWHERE {self.parentField} = %s;"

    def filter(self, detailColumn: int, value) -> None:
        #if not referenceKey:
            #return
        self.clear()
        self.rootItem = TreeItem({i: None for i, c in enumerate(self.columns)})
        #f = {i+1: c[1] for i, c in enumerate(self.columns)}
        #f.update({0:None})
        #self.rootItem = TreeItem(f)
        self.rootItem.itemData[1] = value #list(referenceKey.values())[0]
        self.beginResetModel()
        self._walk(self.rootItem)
        self.endResetModel()

    #def hasChild(self, childValue):
        #with appconn.cursor() as cur:
            #cur.execute(self._hasChildScript, (childValue,))
            #if cur.rowcount:
                #return True
            #return False

    def _walk(self, parentItem):
        try:
            with appconn.cursor() as cur:
                #print("Mogrify",cur.mogrify(script, args))
                x = parentItem.childFieldValue(self.childFieldColumn)
                cur.execute(self._script, (x,))
                for record in cur:
                    #print("Rec", record)
                    itemData = dict()
                    # selected fields
                    for i in range(len(self.columns)):
                        itemData[i] = record[i]
                    n = TreeItem(itemData, parentItem)
                    # primary key fields
                    n.pkey = {self.primaryKey[i - self._cols]: record[i] for i in self._pkcols}
                    # row timestamp
                    n.objectVersion = record[self._ovcol]
                    n.state='S'
                    parentItem.appendChild(n)
                    # if self.hasChild(n.itemData[self.sqlChildFieldColumn]):
                    self._walk(n)
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er)

    def rowCount(self, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        if parentItem:
            return parentItem.childCount()
        return 0

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole, Qt.DecorationRole):
            return None
        item = self.getItem(index)
        return item.itemData[index.column()]

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False
        item = self.getItem(index)
        if index.column() < 0 or index.column() >= len(item.itemData):
            return False
        item.itemData[index.column()] = value
        item.toModify[index.column()] = None
        self.dataChanged.emit(index, index)
        self.userDataChanged.emit()
        if item.state != INSERTED:  # inserted items must be saved before update
            item.state = UPDATED
        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        #flags = Qt.ItemFlags(QAbstractItemModel.flags(self, index) | Qt.ItemIsEditable)
        #if self.columns[index.column()][2]:
            #flags = flags ^ Qt.ItemIsEditable
        #return flags
        return Qt.ItemIsEnabled|Qt.ItemIsEditable|Qt.ItemIsSelectable

    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.rootItem

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section][0]
        return None

    def index(self, row, column, parent=QModelIndex()):
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()
        parentItem = self.getItem(parent)
        if not parentItem:
            return QModelIndex()
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = self.getItem(index)
        parentItem = childItem.parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.childNumber(), 0, parentItem)

    def insertRows(self, position, count, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + count - 1)

        if position < 0 or position > len(parentItem.childItems):
            return False
        for row in range(count):
            data = [None] * self.rootItem.columnCount()
            item = TreeItem(data, parentItem)
            #item.parentFieldValue = parentItem.childFieldValue
            item.state = INSERTED
            parentItem.childItems.insert(position, item)

        self.endInsertRows()
        return True

    def removeRows(self, position, count, parent=QModelIndex()):
        parentItem = self.getItem(parent)
        if position < 0 or position + count > len(parentItem.childItems):
            return False
        self.beginRemoveRows(parent, position, position + count - 1)
        for row in range(count):
            dr = parentItem.childItems.pop(position)
            self.toDelete.append(dr) # store a reference to the removed treeitem for db deletion on submitAll
        self.endRemoveRows()
        self.userDataChanged.emit()
        return True

    def addOrderBy(self, expression):
        self.orderByExpressions.append(expression)

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole):
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False
        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)
        return result

    def clear(self):
        "Delete all model items"
        if self.rootItem:
            self.rootItem.childItems.clear()

    def submit(self):
        return True

    def submitAll(self, pkey):
        if not self.rootItem: # empty model
            return True
        # construct sql check statement
        self.sqlCheck = (f"SELECT {', '.join(self.sqlPrimaryKey)}"
                         f"\nFROM {self.sqlTable}"
                         f"\nWHERE {' AND '.join([f'{i} = %({i})s' for i in self.sqlPrimaryKey + ('object_version',)])};")

        self._store(self.rootItem)  # for inserted/updated items
        # for deleted items
        try:
            with appconn.cursor() as cur: # manual submit, no commit
                for dd in self.toDelete:
                    # check if record was modified
                    args = dd.pkey.copy()
                    args['object_version'] = dd.objectVersion # self.toDelete[row]['rowtimestamp']
                    #print("SQL delete check", cur.mogrify(self.sqlCheck, args))
                    cur.execute(self.sqlCheck, args)
                    if cur.rowcount == 0:
                        self.pgError = _tr("Model", "Row modified before delete")
                        return False
                    # delete record
                    # where = " AND ".join([f"{i} = %({i})s" for i in self.toDelete[row]['pkey']])
                    where = " AND ".join([f"{i} = %({i})s" for i in dd.pkey])
                    script = (f"DELETE FROM {self.sqlTable}\n"
                              f"WHERE {where};")
                    #args = dict()
                    # args.update(self.toDelete[row]['pkey'])
                    #args.update(dd.pkey)
                    #print("SQL delete", cur.mogrify(script, args))
                    #print("** DELETE **")
                    #print(cur.mogrify(script, dd.pkey))
                    cur.execute(script, dd.pkey)
                # clear deleted record list
                self.toDelete.clear()
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er)
        else:
            return True

    def _store(self, item):
        for child in item.childItems:
            if child.childItems:
                self._store(child)
            if child.state == UPDATED:
                # updated all the item is stored
                try:
                    with appconn.cursor() as cur:  # manual submit, no commit
                        # *** UPDATE ***
                        for column in child.toModify:
                            # check if record was already modified
                            args = child.pkey.copy()
                            args['object_version'] = child.objectVersion
                            cur.execute(self.sqlCheck, args)
                            if cur.rowcount == 0:
                                pgerror = _tr("Model", "Row modified before update")
                                raise PyAppDBError(0, pgerror)
                            # update record
                            fields = ", ".join([f"{self.columns[i][0]} = %({self.columns[i][0]})s" for i in child.toModify])
                            # fields = ", ".join([f"{i[0]} = %({i[0]})s" for i in self.columns if i[0] not in self.sqlPrimaryKey and not i[2]])  # exclude primary key and read only fields
                            where = " AND ".join([f"{i} = %({i})s" for i in child.pkey])
                            fieldsback = ", ".join([i[0] or 'Null' for i in self.columns] + ['object_version'])
                            script = (f"UPDATE {self.sqlTable}\n"
                                      f"SET {fields}\n"
                                      f"WHERE {where}\n"
                                      f"RETURNING {fieldsback};")
                            args = {self.columns[i][0]: child.itemData[i] for i in child.toModify}
                            #args = {c[0]: self.dataSet[row][i] for i, c in enumerate(self.columns) if c[0] not in self.sqlPrimaryKey and not c[2]}
                            args.update(child.pkey.copy())
                            #print("** UPDATE **")
                            #print(script)
                            #print(args)
                            cur.execute(script, args)
                            # repopulate the modified row
                            for record in cur:
                                # selected fields
                                for i in range(len(self.columns)):
                                    child.itemData[i] = record[i]
                                # row timestamp
                                child.objectVersion = record[i + 1]  # row timestamp is always the last column
                            # self.dataChanged.emit(self.index(row, 0), self.index(row, 0)) # if any trigger modify de record
                        # clear modified record list
                        child.toModify.clear()
                        child.state = None
                except psycopg.Error as er:
                    raise PyAppDBError(er.diag.sqlstate, er)
            if child.state == INSERTED:
                try:
                    with appconn.cursor() as cur:  # manual submit, no commit
                        # *** INSERT ***
                        fieldList = [i[0] for i in self.columns if i[0] and not i[2]]
                        valueList = [f"%({i[0]})s" for i in self.columns if i[0] and not i[2]]
                        #if self.recordType:
                            #fieldList += [i for i in self.recordType]
                            #valueList += [f"'{self.recordType[i]}'" for i in self.recordType]  # record type must be string
                        fields = ", ".join(fieldList)
                        values = ", ".join(valueList)
                        fieldsback = ", ".join([i[0] or 'Null' for i in self.columns] + ['object_version'])
                        script = (f"INSERT INTO {self.sqlTable}\n"
                                  f"({fields})\n"
                                  f"VALUES ({values})\n"
                                  f"RETURNING {fieldsback};")
                        args = {c[0]: child.itemData[i] for i, c in enumerate(self.columns) if c[0] and not c[2]}
                        # if self.automaticPKey:
                            #for i in self.sqlPrimaryKey:
                                #args[i] = DEFAULT
                        # print(cur.mogrify(script, args))
                        #print("** INSERT **")
                        #print(script)
                        #print(args)
                        cur.execute(script, args)
                        # repopulate the inserted row
                        for record in cur:
                            # selected fields
                            for i in range(len(self.columns)):
                                child.itemData[i] = record[i]
                            # row timestamp
                            child.objectVersion = record[i + 1]  # row timestamp is always the last column
                        # self.dataChanged.emit(self.index(row, 0), self.index(row, cols))  # if any trigger modify de record
                    # clear insert record list
                    child.state = None
                except psycopg.Error as er:
                    raise PyAppDBError(er.diag.sqlstate, er)






