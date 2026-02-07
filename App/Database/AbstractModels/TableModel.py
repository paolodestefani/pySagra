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

"""Table Models

This module contains generic and reusable table models for database tables

"""

# standard library
import operator
import decimal
import logging
from typing import Any
#from pyexpat import model

# pandas
import pandas as pd

# psycopg
import psycopg

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import QDate
from PySide6.QtCore import QTime
from PySide6.QtCore import QDateTime
from PySide6.QtCore import Signal
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex

# application modules
from App import session
from App.Database import ovfield
from App.Database.Exceptions import PyAppDBError
from App.Database.Exceptions import PyAppDBConcurrencyError
from App.Database.Psycopg import DEFAULT
from App.Database.Connect import appconn
from App.Database.Company import company_is_in_use
#from App.Database.Menus import get_menu_tree
#from App.Database.CodeDescriptionList import department_cdl
#from App.Database.CodeDescriptionList import event_cdl
#from App.Database.CodeDescriptionList import item_salable_cdl
from App.Core.L10n import _tr


UPDATED, INSERTED, DELETED = range(3)

FIELD, DESCRIPTION, RO, TYPE = range(4) # field columns attributes


class QueryModel(QAbstractTableModel):
    """A read-only model class that execute select sql statement and returns
    the results to view classes.
    The selected rows are stored in a [row, column] = value dictionary.
    The sql script dynamicaly created from table name adding where/order by/group by/having/limit clauses
    """

    def __init__(self, parent: QObject|None = None) -> None:
        "On init only set some empty objects"
        super().__init__(parent)
        self.dataSet: dict[tuple[int, int], str|int|float|QDate|QDateTime|None] = dict()  # a dict of (row, column) = value
        self.rows = 0 # number of record fetched updated by select method
        self.whereCondition: list[tuple[str, int|float|str]] = []  # list of (condition, argument) for where clause
        self.orderByExpression: list[str] = [] # list of strings
        self.groupByExpression: list[str] = [] # list of field names for group by
        self.havingCondition: list[tuple[str, int|float|str]] = []  # list of (condition, argument) for having clause
        self.limitCondition: int = 999_999_999  # limit clause integer
        self.filterCondition: list[tuple[str, int|float|str|QDate|QDateTime|None]] = []  # reference key condition before where conditions
        self.repr = 'Generic query model' # printable representation of the object,
        # subclass must define this
        self.selectQuery = '' # subclass must define this
        self.columns: tuple[Any]|None = None # subclass must define this
        self.isEditable = False # used in forms
        self.isCompanyTable = False # True if is a company table
        self.companyField = 'company_id' # company_id field name, subclass can modifie this if use table alias
        self.hasTotalsRow = False  # used for sorting
        self.recordType = None  # list of field:value key for record type
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr
        
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        "Always return readonly flag"
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex|QPersistentModelIndex = QModelIndex(), role: int = Qt.ItemDataRole.DisplayRole) -> str|int|float|QDate|QDateTime|None:
        "Returns the required data from dataSet"
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            if (index.row(), index.column()) in self.dataSet:
                return self.dataSet[index.row(), index.column()]
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # numbers aligned right anything else aligned left
            if isinstance(index.data(), (int, decimal.Decimal, QDate, QDateTime)):
                return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> str|None:
        "Returns header data for row (field header)/column (columns number) headers"
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self.columns[section][DESCRIPTION] # section = column number
            else:
                return None
        if orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return super().headerData(section, orientation, role)
            else:
                return None
        return None

    def rowCount(self, index: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the rows number of the dataSet"
        return self.rows

    def columnCount(self, index: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the columns number of the dataSet"
        return len(self.columns or [])  # sometimes columns are not yet set

    def sort(self, column: int, order: int = Qt.SortOrder.AscendingOrder) -> None:
        "One column inplace sorting of the model, manage null values base on declared data time"
        # convert data dict to a list of lists
        data = []
        for r in range(self.rowCount() - self.hasTotalsRow): # True = 1 line False = 0 line
            row = []
            for c in range(self.columnCount()):
                row.append(self.dataSet[r, c])
            data.append(row)
        # manage Null values
        dt = self.columns[column][TYPE]
        nv = {'int': 0,
              'str': "",
              'float': 0.0,
              'decimal2': 0,
              'decimal': 0,
              'bool': False,
              'date': QDate(),
              'time': QTime(),
              'datetime': QDateTime()}[dt]
        # inplace list sorting
        if order == Qt.SortOrder.AscendingOrder:
            data.sort(key=lambda x: x[column] or nv)
        else:
            data.sort(key=lambda x: x[column] or nv, reverse=True)
        # convert ordered list to dict
        for i, record in enumerate(data):
            for j, field in enumerate(record):
                self.dataSet[i, j] = field
        # notify of changed
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])

    def addWhere(self, condition: str, value: int|float|str) -> None:
        "Add where conditions before select"
        self.whereCondition.append((condition, value))

    def addOrderBy(self, expression: list | tuple) -> None:
        "Add order by expression before select"
        if isinstance(expression, (list, tuple)):
            self.orderByExpression += list(expression)
        elif isinstance(expression, str):
            self.orderByExpression.append(expression)
        else:
            raise TypeError("Order by expression must be string or list/tuple of strings")

    def addGroupBy(self, expression: list | tuple) -> None:
        "Add group by conditions before select"
        if isinstance(expression, (list, tuple)):
            self.groupByExpression += list(expression)
        elif isinstance(expression, str):
            self.groupByExpression.append(expression)
        else:
            raise TypeError("Group by expression must be string or list/tuple of strings")

    def addHaving(self, condition: str, value: int | str) -> None:
        "Add having conditions before select"
        self.havingCondition.append((condition, value))
        
    def addLimit(self, limit: int) -> None:
        "Add limit clause before select"
        self.limitCondition = limit
        
    def filter(self, column: int|None = None, value: str|int|float|QDate|QDateTime|None = None) -> None:
        "Filter records on a master/detail logic, this model is for detail"
        self.filterCondition.clear()
        if column is None: # empty master table or new record
            self.filterCondition.append(('True = %s', False))
        else:
            field = f"{self.columns[column][FIELD]}"
            self.filterCondition.append((f'{field} = %s', value))
        self.select()

    def select(self) -> None:
        "Fetch rows from database and fill the dataSet"
        args = None
        # remove trailing ; if present
        script = self.selectQuery.strip()
        script = script if script[-1] != ';' else script[:-1]
        # add where and order by clause
        args = []
        where = [] # (condition, value)
        if self.isCompanyTable:
            where += [(f'{self.companyField} = %s', session['current_company'])]
        if self.recordType:
            where += [(f'{i} = %s', f'{self.recordType[i]}') for i in self.recordType]
        if self.filterCondition:
            where += self.filterCondition
        if self.whereCondition:
            where += self.whereCondition
        if where:
            script += "\nWHERE " + f"{' AND '.join([i[0] for i in where])}"
            args += [i[1] for i in where]
        if self.groupByExpression:
            script += f"\nGROUP BY {', '.join([i for i in self.groupByExpression])}"
        if self.havingCondition:
            script += f"\nHAVING {self.havingCondition}"
        if self.orderByExpression:
            script += f"\nORDER BY {', '.join([i for i in self.orderByExpression])}"
        if self.limitCondition:
            script += f"\nLIMIT {self.limitCondition}"
        script += ";"
        logging.info(f"**** {self.repr} SELECT script ****\n{script}")
        logging.info(f"**** {self.repr} SELECT args ****\n{args}")
        self.layoutAboutToBeChanged.emit()
        self.dataSet.clear()
        try:
            with appconn.cursor() as cur:
                cur.execute(script, args)
                self.rows = cur.rowcount
                for i, record in enumerate(cur):
                    for j, field in enumerate(record):
                        self.dataSet[i, j] = field
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, str(er))
        # notify about changes
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        self.layoutChanged.emit()

    def revertAll(self) -> None:
        self.select()


class QueryWithParamsModel(QAbstractTableModel):
    """A read-only model class that execute select sql statement with keyword
    parameters and returns the results to view classes.
    The selected rows are stored in a [row, column] = value dictionary.
    The sql script is provided with parameters by subclasses 
    and is not changed, only a parameter substitution is applied
    """

    def __init__(self, parent: QObject | None = None) -> None:
        "On init only set some empty objects"
        super().__init__(parent)
        self.dataSet: dict = {}  # a dict of (row, column) = value
        self.rows = 0 # updated by select method
        self.parameter: dict = {} # dictionary of parameters
        self.repr = 'Generic query with params model' # printable representation of the object,
        # subclass must define this
        self.selectQuery = None # subclass must define this
        self.columns = None # subclass must define this
        self.isEditable = False # used in forms
        self.hasTotalsRow = False  # used for sorting
        self.limitCondition = None
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr
        
    def flags(self, index: QModelIndex|QPersistentModelIndex) -> Qt.ItemFlag:
        "Always return readonly flag"
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex|QPersistentModelIndex = QModelIndex(), role: int = Qt.ItemDataRole.DisplayRole) -> str|int|float|QDate|QDateTime|None:
        "Returns the required data from dataSet"
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            if (index.row(), index.column()) in self.dataSet:
                return self.dataSet[index.row(), index.column()]
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # numbers aligned right anything else aligned left
            if isinstance(index.data(), (int, decimal.Decimal, QDate, QDateTime)):
                return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        else:
            return None

    def headerData(self, section: int, orientation: int, role: int = Qt.ItemDataRole.DisplayRole) -> str|None:
        "Returns header data for row (field header)/column (columns number) headers"
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self.columns[section][DESCRIPTION]
            else:
                return None
        if orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return super().headerData(section, orientation, role)
            else:
                return None

    def rowCount(self, index: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the rows number of the dataSet"
        return self.rows

    def columnCount(self, index: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the columns number of the dataSet"
        return len(self.columns)

    def sort(self, column: int, order: int = Qt.SortOrder.AscendingOrder) -> None:
        "One column inplace sorting of the model, manage null values base on declared data time"
        # convert data dict to a list of lists
        if not self.dataSet:
            return
        data = []
        for r in range(self.rowCount() - self.hasTotalsRow): # True = 1 line False = 0 line
            row = []
            for c in range(self.columnCount()):
                row.append(self.dataSet[r, c])
            data.append(row)
        # manage Null values
        dt = self.columns[column][TYPE]
        nv = {'int': 0,
              'str': "",
              'float': 0.0,
              'decimal2': 0,
              'decimal': 0,
              'bool': False,
              'date': QDate(),
              'time': QTime(),
              'datetime': QDateTime()}[dt]
        # inplace list sorting
        if order == Qt.SortOrder.AscendingOrder:
            data.sort(key=lambda x: x[column] or nv)
        else:
            data.sort(key=lambda x: x[column] or nv, reverse=True)
        # convert ordered list to dict
        for i, record in enumerate(data):
            for j, field in enumerate(record):
                self.dataSet[i, j] = field
        # notify of changed
        self.dataChanged.emit(self.createIndex(0, 0), 
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])

    def setParameter(self, parameter: str, value: int|str|QDate|QDateTime|None) -> None:
        "Set the value of a parameter in prams dictionaty"
        self.parameter[parameter] = value

    def select(self) -> None:
        "Fetch rows from database and fill the dataSet"
        self.layoutAboutToBeChanged.emit()
        script = self.selectQuery.strip()
        logging.info(f"**** {self.repr} SELECT script ****\n{script}")
        logging.info(f"**** {self.repr} SELECT params ****\n{self.parameter}")
        try:
            with appconn.cursor() as cur:
                cur.execute(script, self.parameter)
                self.rows = cur.rowcount
                for i, record in enumerate(cur):
                    for j, field in enumerate(record):
                        self.dataSet[i, j] = field
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, str(er))
        # notify about changes
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        self.layoutChanged.emit()

    def revertAll(self) -> None:
        self.select()


class TableModel(QAbstractTableModel):
    """Generic table model for managing one sql table
    
    Structure:
    dataSet is a list of dictionaries, each dictionary is a record of a table
    the dictionary key is the column number of the model
    additional keys are the pkey for primary key dictionary
    and object_version for the concurrency management
    """
    userDataChanged = Signal()  # can not use dataChanged because is emitted even on select
    rowCountChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        "Initialize some empty or default data structure"
        super().__init__(parent)
        self.dataSet: list[dict] = [] # a list of dict (integer key = record column/field,
        #                                   'pkey' = primary key tuple,
        #                                   'object_version' = int)
        self.rows = 0 # automatic updated on select
        self.cols = 0 # updated on select
        self.whereCondition: list[tuple] = []  # list of (condition, argument)
        self.orderByExpression: list[str] = [] # list of string
        self.filterMapping: dict = {}
        self.toInsert: list[int] = []  # list of row number of any inserted row
        self.toModify: dict = {}  # dict of dict row number / column number of any modified field
        self.toDelete: list[dict] = []  # list of dict for any cancelled row (need to store pkey and object_version)
        # subclasses must define this properties
        self.table = None # table or view name - string, subclass must define this
        self.isCompanyTable = False # True if is a company table
        self.columns: tuple = () # model columns definition (field, description, readonly, type)
        self.primaryKey: list = [] # primary key fields name - sequence, subclass must define this
        self.automaticPKey = False  # set pkey filds at DEFAULT value on insert
        self.recordType = None  # list of field:value key for record type (a table with different record type)
        self.newRecordDefault: dict = {} # a record dictionary with default values for some field on insert
        self.filterCondition: list[tuple] = []  # reference key condition before where conditions, map master row to detail row
        self.limitCondition = None
        self.isDirty = False # setted on data changed
        self.isEditable = True # used in forms
        self.repr = 'Generic editable table model' # printable representation of the object
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr

    def flags(self, index: QModelIndex|QPersistentModelIndex) -> Qt.ItemFlag:
        "Return standard flags or readonly for some columns"
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        flags = QAbstractTableModel.flags(self, index)|Qt.ItemFlag.ItemIsEditable
        if self.columns[index.column()][RO]:
            flags = flags ^ Qt.ItemFlag.ItemIsEditable
        return flags

    def data(self, index: QModelIndex|QPersistentModelIndex = QModelIndex(), role: int = Qt.ItemDataRole.DisplayRole) -> str|int|float|QDate|QDateTime|None:
        # sometimes dataSet could be empty
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return None
        row = index.row()
        col = index.column()
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            if len(self.dataSet) <= row:
                return None
            if not col in self.dataSet[row]:
                return None
            result = self.dataSet[row][col]
            return result
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # numbers aligned right anything else aligned left
            if isinstance(index.data(), (int, decimal.Decimal, QDate, QDateTime)):
                return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            else:
                return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        else:
            return None

    def setData(self, index: QModelIndex|QPersistentModelIndex = QModelIndex(), value: str|int|float|QDate|QDateTime|None = None, role: int = Qt.ItemDataRole.EditRole) -> bool:
        "Set data in dataSet and mark row as modified"
        # sanity checks
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return False
        row = index.row()
        col = index.column()
        if role == Qt.ItemDataRole.EditRole:
            # check if different from before
            if self.dataSet[row][col] == value:
                return False
            # save the row/column of the modified cell
            if (row not in self.toModify and row not in self.toInsert):
                self.toModify[row] = {}
            if (row in self.toModify and col not in self.toModify[row]):
                self.toModify[row][col] = None
            # modify the model
            if isinstance(value, str):
                value = value or None # convert empty strings in Sql Null
            self.dataSet[row][col] = value
            self.isDirty = True
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            self.userDataChanged.emit()
            return True
        return False

    def blindSetData(self, row: int, column: int, value: str|int|float|QDate|QDateTime|None) -> None:
        "Set data without emitting dataChanged signal"
        row = self.filterMapping[row]
        self.dataSet[row][column] = value

    def submit(self) -> bool:
        # used only for commit on row changed, do nothing on manual submit
        # BUT is needed for proper DataWidgetMapper use
        return True

    def submitAll(self, column: int|None = None, value: str|int|float|QDate|QDateTime|None = None) -> bool:
        "Update database: insert/delete/update rows"
        # if a referenceKey is provided fill all the rows with reference value
        if not column is None :
            for row in self.dataSet:
                row[column] = value

        cols = len([i[FIELD] for i in self.columns if i[FIELD]]) # only column of master table need insert/update/delete
        pkcols = range(cols, cols + len(self.primaryKey))
        ovcol = cols + len(self.primaryKey)
        self.sqlCheck = (f"SELECT {', '.join(self.primaryKey)}\n"
                         f"FROM {self.table}\n"
                         f"WHERE {' AND '.join(
                             [f'{i} = %({i})s' for i in self.primaryKey + (ovfield,)])};")
        try:
            with appconn.cursor() as cur: # manual submit, no commit (form can save multiple table models)

                # *** UPDATE ***
                for row in self.toModify:
                    if row in self.toInsert: # skip row to be inserted first
                        continue
                    # check if record was already modified
                    pkey = self.dataSet[row]['pkey'].copy() # primary key is unchanged on update
                    args = pkey.copy()
                    #if self.isCompanyTable:
                    #    args['company_id'] = session['current_company']
                    args[ovfield] = self.dataSet[row][ovfield]
                    logging.info(f"**** {self.repr} SELECT CHECK script ****\n{self.sqlCheck}")
                    logging.info(f"**** {self.repr} SELECT CHEK  args   ****\n{args}")
                    cur.execute(self.sqlCheck, args)
                    if cur.rowcount == 0:
                        logging.error(f"**** {self.repr}: row modified before update ****")
                        raise PyAppDBConcurrencyError()
                    # update record
                    fields = ", ".join([f"{self.columns[i][FIELD]} = %({self.columns[i][FIELD]})s" for i in self.toModify[row]])
                    if not fields: # no real fields need update
                        continue
                    where = " AND ".join([f"{i} = %({i})s" for i in pkey])
                    fieldsback = ", ".join([i[FIELD] for i in self.columns if i[FIELD]] + [ovfield])
                    script = (f"UPDATE {self.table}\n"
                              f"SET {fields}\n"
                              f"WHERE {where}\n"
                              f"RETURNING {fieldsback};")
                    args = {self.columns[i][FIELD]: self.dataSet[row][i] for i in self.toModify[row] if self.columns[i][FIELD]}
                    args.update({k: pkey[k] for k in pkey})
                    logging.info(f"**** {self.repr} UPDATE script ****\n{script}")
                    logging.info(f"**** {self.repr} UPDATE args   ****\n{args}")
                    cur.execute(script, args)
                    # repopulate the modified row
                    for record in cur:
                        # selected fields
                        for index in range(self.cols):
                            self.dataSet[row][index] = record[index]
                        # row object version
                        self.dataSet[row][ovfield] = record[-1] # ovfield is always the last onefield
                    self.dataChanged.emit(self.createIndex(row, 0),
                                          self.createIndex(row, cols),
                                          [Qt.DisplayRole, Qt.EditRole]) # if any trigger modify de record
                # clear modified record list
                self.toModify.clear()

                # *** DELETE ***
                for dd in self.toDelete:
                    # check if record was modified
                    pkey = dd['pkey'].copy()  # self.toDelete[row]['pkey'].copy()
                    args = pkey.copy()
                    if self.isCompanyTable:
                        args['company_id'] = session['current_company']
                    args[ovfield] = dd[ovfield]
                    logging.info(f"**** {self.repr} SELECT CHECK script ****\n{self.sqlCheck}")
                    logging.info(f"**** {self.repr} SELECT CHEK  args   ****\n{args}")
                    cur.execute(self.sqlCheck, args)
                    if cur.rowcount == 0:
                        logging.error(f"**** {self.repr} row modified before update ****")
                        raise PyAppDBConcurrencyError()
                    # delete record
                    where = " AND ".join([f"{i} = %({i})s" for i in pkey])
                    script = (f"DELETE FROM {self.table}\n"
                              f"WHERE {where};")
                    args.update({k: pkey[k] for k in pkey})
                    logging.info(f"**** {self.repr} DELETE script ****\n{script}")
                    logging.info(f"**** {self.repr} DELETE args   ****\n{args}")
                    cur.execute(script, args)
                # clear deleted record list
                self.toDelete.clear()

                # *** INSERT ***
                for row in self.toInsert:
                    fieldList = [i[FIELD]for i in self.columns if i[FIELD] and not i[RO]] 
                    # calculated fields have None as field name
                    # read only fields can not be inserted
                    if self.automaticPKey:
                        # remove primary key fields if present
                        for i in self.primaryKey:
                            if i in fieldList:
                                fieldList.remove(i)
                    valueList = [f"%({i})s" for i in fieldList]
                    if self.recordType:
                        fieldList += [i for i in self.recordType]
                        valueList += [f"'{self.recordType[i]}'" for i in self.recordType]  # record type must be string
                    fields = ", ".join(fieldList)
                    values = ", ".join(valueList)
                    fieldsback = ", ".join([i[FIELD] or 'Null' for i in self.columns] + list(self.primaryKey) + [ovfield])
                    args = {c[FIELD]: self.dataSet[row][i] for i, c in enumerate(self.columns) if c[FIELD] and not c[RO]}
                    if self.recordType:
                        for i in self.recordType:
                            args[i] = self.recordType[i]
                    # set company after anything else, company_id may not be present in self.columns
                    if self.isCompanyTable:
                        fields += ', company_id'
                        values += ', %(company_id)s'
                        args['company_id'] = session['current_company']
                    script = (f"INSERT INTO {self.table}\n"
                              f"({fields})\n"
                              f"VALUES ({values})\n"
                              f"RETURNING {fieldsback};")
                    logging.info(f"**** {self.repr} INSERT script ****\n{script}")
                    logging.info(f"**** {self.repr} INSERT args   ****\n{args}")
                    try:
                        cur.execute(script, args)
                    except psycopg.Warning as er:
                        raise PyAppDBError(0, str(er))
                    # repopulate the inserted row
                    #for record in cur: # must be one record
                    #    pkey = record
                    #where = " AND ".join([f'{k} = %({k})s' for k in self.primaryKey])
                    #args = {k: v for k, v in zip(self.primaryKey, pkey)}
                    #fields = ", ".join([f"{i[FIELD]}" for i in self.columns] +
                    #       [f"{i}" for i in self.primaryKey] +
                    #       [ovfield])
                    #script = f"SELECT {fields}\nFROM {self.table}"
                    #script += f"\nWHERE {where};"
                    #logging.info(f"**** {self.repr} SELECT INSERT repopulate script ****\n{script}")
                    #logging.info(f"**** {self.repr} SELECT INSERT repopulate args   ****\n{args}")
                    #cur.execute(script, args)
                    for record in cur:
                        # selected fields
                        for index in range(self.cols):
                            self.dataSet[row][index] = record[index]
                        # primary key
                        self.dataSet[row]['pkey'] = {self.primaryKey[i - cols]: record[i] for i in pkcols}
                        # object version
                        self.dataSet[row][ovfield] = record[ovcol]
                    self.dataChanged.emit(self.createIndex(row, 0),
                                          self.createIndex(row, cols),
                                          [Qt.DisplayRole, Qt.EditRole]) # if any trigger modify record
                # clear insert record list
                self.toInsert.clear()
                
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er)
        self.isDirty = False
        return True

    def revertAll(self) -> None:
        self.toModify.clear()
        self.toDelete.clear()
        self.toInsert.clear()
        self.isDirty = False
        self.select()

    def clearData(self) -> None:
        "Clear all the content of model"
        self.dataSet.clear()
        self.toModify.clear()
        self.toDelete.clear()
        self.toInsert.clear()
        self.isDirty = False
        self.rows = 0 # usually updated by select
        self.cols = len(self.columns) # usually updated by select

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> str|None:
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self.columns[section][DESCRIPTION]
            else:
                return None
        if orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return super().headerData(section, orientation, role)
            else:
                return None

    def rowCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the rows number of the dataSet"
        return self.rows

    def columnCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the columns number of the dataSet"
        return self.cols

    def insertRows(self, position: int, count: int, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> bool:
        "Insert rows in model"
        self.beginInsertRows(parent, position, position + count - 1)
        for i in range(position, position + count):
            self.dataSet.insert(i, {i:self.newRecordDefault.get(j[FIELD]) for i, j in enumerate(self.columns)})
            self.toInsert.append(i)
        self.rows += count
        self.endInsertRows()
        self.userDataChanged.emit()
        self.rowCountChanged.emit(self.rows)
        return True

    def removeRows(self, position: int, count: int, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> bool:
        "Remove rows from model"
        if self.rowCount() < 1:
            return True
        # for removed rows we can't use row number because it is renumbered
        # every time a row is removed. Also inserted/modified rows have to be
        # renumbered when a row before is removed
        self.beginRemoveRows(parent, position, position + count - 1)
        for i in range(position, position + count):
            # if row to be deleted was just inserted and not saved yet delete from toInsert
            if i in self.toInsert:
                self.toInsert.remove(i)
            # if row to be deleted was just modified and not saved yet delete from toModify
            if i in self.toModify:
                del self.toModify[i]
            # save the deleted record primary key and object version
            if self.dataSet[i].get('pkey'):  # could happend if insert/delete before save
                self.toDelete.append({'pkey': self.dataSet[i]['pkey'].copy(),
                                      ovfield: self.dataSet[i][ovfield]})
            # if row deleted is before an inserted/modified adjust row number (-1)
            self.toInsert.sort()
            self.toInsert = [ri - 1 if ri > i else ri for ri in self.toInsert]
            rm = list(self.toModify.keys())
            rm.sort()
            for r in rm:
                if r > i:
                    self.toModify[r - 1] = self.toModify[r]
                    del self.toModify[r]
        # modify the model
        del self.dataSet[position: position + count]
        self.rows -= count
        self.endRemoveRows()
        self.userDataChanged.emit()
        self.rowCountChanged.emit(self.rows)
        return True

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        "Inplace sorting of the model, manage null values base on declared data time"
        # manage Null values
        dt = self.columns[column][TYPE]
        nv = {'int': 0,
              'str': "",
              'float': 0.0,
              'decimal': 0,
              'bool': False,
              'date': QDate(),
              'time': QTime(),
              'datetime': QDateTime()}[dt]
        # inplace list sorting
        if order == Qt.SortOrder.AscendingOrder:
            self.dataSet.sort(key=lambda x: x[column] or nv)
        else:
            self.dataSet.sort(key=lambda x: x[column] or nv, reverse=True)
        # notify about changes
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])

    def filter(self, column: int|None = None, value: str|int|float|QDate|QDateTime|None = None) -> None:
        "Filter records on a master/detail logic, this model is for detail"
        self.filterCondition.clear()
        if column is None: # empty master table or new record
            self.filterCondition.append(('True = %s', False))
        else:
            field = f"{self.columns[column][FIELD]}"
            self.filterCondition.append((f'{field} = %s', value))
        self.select()

    def filterMasterRow(self, row: int) -> None:
        "Filter dataset based on master row creating a dictionary of mapped rows"
        self.layoutAboutToBeChanged.emit()
        self.filterMapping.clear()
        # for n, i in enumerate(self.dataSet):
        #     if i['master_row'] == row:
        #         self._filterMapping[len(self._filterMapping)] = n
        self.filterMapping = {len(self.filterMapping): n for n, i in enumerate(self.dataSet) if  i['master_row'] == row}
        self.rows = len(self.filterMapping)
        # notify of changes
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        self.layoutChanged.emit()
        self.rowCountChanged.emit(self.rows)
    
    def addWhere(self, condition: str, value: str|int|float|QDate|QDateTime|None) ->None:
        "Add where conditions before select"
        self.whereCondition.append((condition, value))

    def addOrderBy(self, expression: str|list|tuple) -> None:
        "Add order by expression before select"
        if isinstance(expression, (list, tuple)):
            self.orderByExpression += list(expression)
        elif isinstance(expression, str):
            self.orderByExpression.append(expression)
        else:
            raise TypeError("Order by expression must be string or list/tuple of strings")

    def primaryKey(self, row: int) -> str|None:
        if row < 0:
            return
        return self.dataSet[row].get('pkey')

    def fieldName(self, column: int) -> str:
        "Return field name for column number"
        return self.columns[column][FIELD]

    def fieldColumn(self, fieldName: str) -> int:
        "Return column number for field name"
        i = self.columns.index([i for i in self.columns if i[FIELD] == fieldName][0]) # index the list of tuple with 1 element, [0] returns the tuple (no list)
        return i

    def select(self, column: int|None = None, value: str|int|float|QDate|QDateTime|None = None) -> None:
        "Fetch rows from DB creating the sql select statement and filling the dataset"
        # select fields + primary key fields + object version field
        # None fields (usually calculated fields) are converted to Null string
        fields = ", ".join([f"{i[FIELD] or 'Null'}" for i in self.columns]
                           + [f"{i}" for i in self.primaryKey]
                           + [ovfield])

        script = f"SELECT {fields}\nFROM {self.table}\n"
        args = []
        where = []
        if self.isCompanyTable:
            where.append(("company_id = %s", session['current_company']))
        if self.recordType:
            where += [(f'{i} = %s', f'{self.recordType[i]}') for i in self.recordType]
        if self.filterCondition:
            where += self.filterCondition
        if self.whereCondition:
            where += self.whereCondition
        if where:
            script += f"\nWHERE {' AND '.join([i[0] for i in where])}"
            args += [i[1] for i in where if '%s' in i[0]] # argument if required
        if self.orderByExpression:
            script += f"\nORDER BY {', '.join([i for i in self.orderByExpression])}"
        if self.limitCondition:
            script += f"\nLIMIT {self.limitCondition}"
        script += ";"
        #print("* Script *\n", script)
        #print("* Args *\n", args)
        cols = len(self.columns)
        pkcols = range(cols, cols + len(self.primaryKey))
        ovcol = cols + len(self.primaryKey)
        self.layoutAboutToBeChanged.emit()
        try:
            with appconn.cursor() as cur:
                cur.execute(script, args)
                self.rows = cur.rowcount
                #print("Selected rows:", self.rows)
                self.cols = cols
                self.dataSet.clear()
                for record in cur:
                    # selected fields
                    item = {i:record[i] for i in range(cols)}    
                    # primary key fields
                    item['pkey'] = {self.primaryKey[i - cols]: record[i] for i in pkcols}
                    # discard item with Null primary key
                    if item['pkey'][self.primaryKey[0]] is None:
                        continue
                    # master column
                    item['master_row'] = record[1] # master row number
                    # row object version
                    item[ovfield] = record[ovcol]
                    # append on record list
                    #print("Item:", item)
                    self.dataSet.append(item)
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, str(er))
        # create an unfiltered master row mapping
        self.filterMapping = {i: i  for i in range(len(self.dataSet))}
        # notify of changes
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), self.columnCount()),
                              [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        self.layoutChanged.emit()
        self.rowCountChanged.emit(self.rows)
        
       
class PandasModel(QAbstractTableModel):
    """A read-only model to interface a database view with pandas pivot dataframe"""

    def __init__(self,parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._dataframe = None
        self._pivot = None
        self.table = None # table or view name - string, subclass must define this
        self.isCompanyTable = False # True if is a company table, subclass must define this
        self.columns = () # model columns definition, subclass must define this
        # Number of rows needed for column headers
        #self.col_levels = dataframe.columns.nlevels if hasattr(dataframe.columns, 'nlevels') else 1
        self.col_levels = 0
        # Number of columns needed for row headers (index)
        self.row_levels = 0 # updated by createPivot
        
    def select(self) -> None:
        "Fetch rows from DB creating the sql select statement and filling the dataset"
        # create a reverse dictionary for columns translation
        self.trcolumns = {self.columns[i][0]: i for i in self.columns}
        #print("Columns translation:", self.trcolumns)
        script = f"SELECT {', '.join(self.columns.keys())}\nFROM {self.table}"
        if self.isCompanyTable:
            script += "\nWHERE company_id = system.pa_current_company();"
        else:
            script += ";"
        print("**** PandasModel SELECT script ****\n", script)
        try:
            with appconn.cursor() as cur:
                cur.execute(script)
                df = pd.DataFrame(cur.fetchall(),
                                  columns=[self.columns[i[0]][0] for i in cur.description])
                #print(df.head())
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, str(er))   
        # force correct data types
        f = {self.columns[i][0]: self.columns[i][3] for i in self.columns if self.columns[i][3]}
        self._dataframe = df.astype(f)
        print(f"Dataframe loaded with {len(self._dataframe)} rows and {len(self._dataframe.columns)} columns")
        print("DTypes:", self._dataframe.dtypes)
        
        # Number of columns needed for row headers (index)
        #self.row_levels = df.index.nlevels if hasattr(df.index, 'nlevels') else 1
        #print('Columns:', self._dataframe.columns)
        
    def filterEvent(self, value: str) -> None:
        "Filter dataframe for a specific event description"
        # re-generate dataframe from DB, undo previous filters
        self.select()
        if self._dataframe is None:
            return
        self._dataframe = self._dataframe[self._dataframe[self.columns['event'][0]] == value]
        
    def filterLike(self, column: str, value: str) -> None:
        "Filter dataframe for a specific column value using like operator"
        if self._dataframe is None:
            return
        if column not in self._dataframe.columns:
            return
        self._dataframe = self._dataframe[self._dataframe[column].astype(str).str.contains(value, na=False, case=False)]
        
    def getEvents(self) -> list:
        "Return a list of distinct events description"
        if self._dataframe is None:
            return []
        c = (self.columns.get('event') or (None,))[0] # index are translated for pivot use
        return self._dataframe[c].dropna().unique().tolist()

    def createPivot(self, rows: list, columns: list, values: list, aggfunc: dict, totals: bool) -> None:
        "Create a pivot table from the dataframe"
        if self._dataframe is None:
            return
        #print(self._dataframe.head())
        self._pivot = pd.pivot_table(self._dataframe,
                                    index=rows,
                                    columns=columns,
                                    values=values,
                                    aggfunc=aggfunc,
                                    fill_value=0.0,
                                    margins=totals,
                                    margins_name=_tr('Statistics','Totale Generale'))
        logging.info(f"Pivot table created with {len(self._pivot)} rows and {len(self._pivot.columns)} columns")
        print(self._pivot.head())
        print(self._pivot.columns)
        print(self._pivot.index.names)
        #print(self._pivot.info())
        # update col_levels
        #self.col_levels = self._pivot.columns.nlevels if hasattr(self._pivot.columns, 'nlevels') else 1
        #self.col_levels += totals
        # update row_levels
        self.row_levels = self._pivot.index.nlevels if hasattr(self._pivot.index, 'nlevels') else 1
        self.row_levels += totals

    def rowCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        return self._pivot.shape[0] + self.col_levels

    def columnCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        return self._pivot.shape[1] + self.row_levels

    def data(self, index: QModelIndex|QPersistentModelIndex = QModelIndex(), role: int = Qt.ItemDataRole.DisplayRole) -> str|int|float|QDate|QDateTime|None:
        if not index.isValid():
            return None
        header = self.headerData(index.column(), Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        header = header.split('\n')[0]  # in case of multi-line header
        fm = self.columns[self.trcolumns[header]][4]  # (name, format)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if fm in ('int', 'float', 'decimal2'):   
                return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        
        if role == Qt.ItemDataRole.DisplayRole:
            r, c = index.row(), index.column()
            dt = self._pivot.iloc[r - self.col_levels, c - self.row_levels] if r >= self.col_levels and c >= self.row_levels else None
            # CASE 1: Top-Left Empty Corner
            if r < self.col_levels and c < self.row_levels:
                return ""
            # CASE 2: Column Headers (Top rows)
            if r < self.col_levels:
                label = self._pivot.columns[c - self.row_levels]
                return str(label[r]) if isinstance(label, tuple) else str(label)
            # CASE 3: Row Headers (Left columns)
            if c < self.row_levels:
                label = self._pivot.index[r - self.col_levels]
                outstr = label[c] if isinstance(label, tuple) else label
                if fm == 'int':
                    return session['qlocale'].toString(int(outstr or 0))
                elif fm in ('float', 'decimal2'):
                    return session['qlocale'].toString(float(outstr or 0.0), 'f', 2)
                elif fm == 'date':
                    if pd.isna(outstr):
                        return ""
                    return outstr.strftime('%d/%m/%Y')
                else:
                    return str(outstr)
            # CASE 4: Actual Data Values
            if fm == 'int':
                return session['qlocale'].toString(int(dt or 0))
            elif fm in ('float', 'decimal2'):
                return session['qlocale'].toString(float(dt or 0.0), 'f', 2)
            elif fm == 'date':
                if pd.isna(dt):
                    return ""
                return dt.strftime('%d/%m/%Y')
            else:
                return str(dt)
        
        return None

    def headerData(self, section, orientation, role: int =Qt.ItemDataRole.DisplayRole) -> str|None:
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section < self.row_levels:
                    #print('Index;', self._pivot.index)
                    return self._pivot.index.names[section]
                # Column Names
                col_label = self._pivot.columns[section - self.row_levels]
                # If MultiIndex, join levels
                return "\n".join(map(str, col_label)) if isinstance(col_label, tuple) else str(col_label)
            
            if orientation == Qt.Orientation.Vertical:
                return None
        return None

