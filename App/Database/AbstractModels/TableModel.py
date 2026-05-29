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
import decimal
import logging
from typing import Any, cast

# pandas
#import pandas as pd

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
from App.Database import OVFIELD
from App.Database.Exceptions import PyAppDBError
from App.Database.Exceptions import PyAppDBConcurrencyError
from App.Database.Connect import appconn
from App.Core.L10n import _tr

# logger
logger = logging.getLogger(__name__)


UPDATED, INSERTED, DELETED = range(3)

FIELD, DESCRIPTION, RO, TYPE = range(4) # field columns attributes



class QueryModel(QAbstractTableModel):
    """A read-only model class that execute select sql statement and returns
    the results to view classes.
    The selected rows are stored in a [row, column] = value dictionary.
    The sql script dynamicaly created from table name adding where/order by/group by/having/limit clauses
    """

    def __init__(self, parent: QObject | None = None) -> None:
        "On init only set some empty objects"
        super().__init__(parent)
        self.dataSet: Any = dict()  # a dict of (row, column) = value
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
        self.columns: tuple[Any, ...] = () # subclass must define this
        self.isEditable = False # used in forms
        self.isCompanyTable = False # True if is a company table
        self.companyField = 'company_id' # company_id field name, subclass can modifie this if use table alias
        self.hasTotalsRow = False  # used for sorting
        self.recordType: Any = None  # dict of field:value key for record type
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr
        
    def flags(self, index: QModelIndex|QPersistentModelIndex) -> Qt.ItemFlag:
        "Always return readonly flag"
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable

    def data(self,
             index: QModelIndex|QPersistentModelIndex = QModelIndex(),
             role: int = Qt.ItemDataRole.DisplayRole
             ) -> Any:
        "Returns the required data from dataSet"    
        # sometimes dataSet could be empty
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return None
        row = index.row()
        col = index.column()
        result = self.dataSet[row, col]
        match role:
            case Qt.ItemDataRole.DisplayRole:
                if isinstance(result, bool):
                    return None # do not return text for bool, checkbox is managed in CheckStateRole
                return result
            case Qt.ItemDataRole.TextAlignmentRole:
                # numbers aligned right anything else aligned left
                if isinstance(result, (int, decimal.Decimal, QDate, QDateTime)):
                    return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
                else:
                    return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
            case Qt.ItemDataRole.CheckStateRole:
                if isinstance(result, bool):
                    return Qt.CheckState.Checked if result else Qt.CheckState.Unchecked
                else:
                    return None
            case _:
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

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        """One column inplace sorting of the model, manage null values based on declared data type"""
        if not self.dataSet:
            return
        self.layoutAboutToBeChanged.emit()
        data: list[list[Any]] = []
        for r in range(self.rowCount() - int(self.hasTotalsRow)):
            row = [self.dataSet[r, c] for c in range(self.columnCount())]
            data.append(row)
        dt = self.columns[column][TYPE]
        null_map: dict[str, Any] = {
            'int': 0,
            'str': "",
            'float': 0.0,
            'decimal2': 0,
            'decimal': 0,
            'bool': False,
            'date': QDate(),
            'time': QTime(),
            'datetime': QDateTime()
        }
        nv = null_map.get(dt, "")
        is_reverse = (order == Qt.SortOrder.DescendingOrder)
        data.sort(
            key=lambda x: cast(Any, x[column] if x[column] is not None else nv),
            reverse=is_reverse
        )
        self.dataSet.clear()
        for i, record in enumerate(data):
            for j, field in enumerate(record):
                self.dataSet[i, j] = field
        self.layoutChanged.emit()

    def addWhere(self, condition: str, value: int|float|str) -> None:
        "Add where conditions before select"
        self.whereCondition.append((condition, value))

    def addOrderBy(self, expression: list | tuple | str) -> None:
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
        
    def filter(self, column: int|None = None, value: Any = None) -> None:
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
            self.whereCondition.clear() # clear where condition after use, they are intended for one select only
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
        logger.info(f"**** {self.repr} SELECT script ****\n{script}")
        logger.info(f"**** {self.repr} SELECT args ****\n{args}")
        self.beginResetModel()
        self.dataSet.clear()
        try:
            with appconn.cursor() as cur:
                cur.execute(script, args)
                self.rows = cur.rowcount
                for i, record in enumerate(cur):
                    for j, field in enumerate(record):
                        self.dataSet[i, j] = field
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
        self.endResetModel()
        
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
        self.dataSet: Any = dict()  # a dict of (row, column) = value
        self.rows = 0 # updated by select method
        self.parameter: dict = {} # dictionary of parameters
        self.repr = 'Generic query with parameters model' # printable representation of the object,
        # subclass must define this
        self.selectQuery: str = "" # subclass must define this
        self.columns: tuple[Any, ...] = () # subclass must define this
        self.isEditable = False # used in forms
        self.hasTotalsRow = False  # used for sorting
        self.limitCondition = None
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr
        
    def flags(self, index: QModelIndex|QPersistentModelIndex) -> Qt.ItemFlag:
        "Always return readonly flag"
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        return Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable

    def data(self,
             index: QModelIndex|QPersistentModelIndex = QModelIndex(),
             role: int = Qt.ItemDataRole.DisplayRole
             ) -> Any:
        "Returns the required data from dataSet"
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return None
        row = index.row()
        col = index.column()
        result = self.dataSet[row, col]
        match role:
            case Qt.ItemDataRole.DisplayRole:
                if isinstance(result, bool):
                    return None # do not return text for bool, checkbox is managed in CheckStateRole
                return result
            case Qt.ItemDataRole.TextAlignmentRole:
                # numbers aligned right anything else aligned left
                if isinstance(result, (int, decimal.Decimal, QDate, QDateTime)):
                    return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
                else:
                    return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
            case Qt.ItemDataRole.CheckStateRole:
                if isinstance(result, bool):
                    return Qt.CheckState.Checked if result else Qt.CheckState.Unchecked
                else:
                    return None
            case _:
                return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> str|None:
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
        return None

    def rowCount(self, index: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the rows number of the dataSet"
        return self.rows

    def columnCount(self, index: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the columns number of the dataSet"
        return len(self.columns)

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        "One column inplace sorting of the model, manage null values base on declared data time"
        if not self.dataSet:
            return
        self.layoutAboutToBeChanged.emit()
        data: list[list[Any]] = []
        for r in range(self.rowCount() - int(self.hasTotalsRow)):
            row = [self.dataSet[r, c] for c in range(self.columnCount())]
            data.append(row)
        dt = self.columns[column][TYPE]
        null_map: dict[str, Any] = {
            'int': 0,
            'str': "",
            'float': 0.0,
            'decimal2': 0,
            'decimal': 0,
            'bool': False,
            'date': QDate(),
            'time': QTime(),
            'datetime': QDateTime()
        }
        nv = null_map.get(dt, "")
        is_reverse = (order == Qt.SortOrder.DescendingOrder)
        data.sort(
            key=lambda x: cast(Any, x[column] if x[column] is not None else nv),
            reverse=is_reverse
        )
        self.dataSet.clear()
        for i, record in enumerate(data):
            for j, field in enumerate(record):
                self.dataSet[i, j] = field
        self.layoutChanged.emit() 

    def setParameter(self, parameter: str, value: int|str|QDate|QDateTime|None) -> None:
        "Set the value of a parameter in prams dictionaty"
        self.parameter[parameter] = value

    def select(self) -> None:
        "Fetch rows from database and fill the dataSet"
        self.beginResetModel()
        script = self.selectQuery.strip()
        logger.info(f"**** {self.repr} SELECT script ****\n{script}")
        logger.info(f"**** {self.repr} SELECT params ****\n{self.parameter}")
        try:
            with appconn.cursor() as cur:
                cur.execute(script, self.parameter)
                self.rows = cur.rowcount
                for i, record in enumerate(cur):
                    for j, field in enumerate(record):
                        self.dataSet[i, j] = field
        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
        self.endResetModel()

    def revertAll(self) -> None:
        """Revert all changes, in this model do nothing because is readonly,
        but is needed for proper DataWidgetMapper use"""
        self.select()
        
        
class Record(dict):
    def __init__(self, data: dict, pkey: dict|None, object_version: int, is_new: bool = False) -> None:
        # data is a dictionary {column_index: value}
        super().__init__(data)
        self.pkey = pkey
        self.object_version = object_version
        self.is_new = is_new
        self.is_modified = False
        self.is_deleted = False
                
    def __setitem__(self, key, value):
        """Override __setitem__ to mark the record as modified when a value is actuallychanged"""
        # if the value is the same do not mark as modified
        if key in self and self[key] == value:
            return
        super().__setitem__(key, value)
        # if the record is not new, mark as modified
        if not self.is_new:
            self.is_modified = True


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
        self.dataSet: list[Record] = [] 
        self.rows = 0 # automatic updated on select
        self.cols = 0 # updated on select
        self.whereCondition: list[tuple] = []  # list of (condition, argument)
        self.orderByExpression: list[str] = [] # list of string
        #self.filterMapping: dict = {}
        self.toDelete: list[dict[str, Any]] = []  # list of dict for any cancelled row (need to store pkey and object_version)
        # subclasses must define this properties
        self.table: str | None = None # table or view name - string, subclass must define this
        self.isCompanyTable = False # True if is a company table
        self.columns: tuple[Any, ...] = () # model columns definition (field, description, readonly, type)
        self.primaryKey: tuple[str, ...] = () # primary key fields name - sequence, subclass must define this
        self.automaticPKey = False  # set pkey filds at DEFAULT value on insert
        self.recordType: dict = {}  # list of field:value key for record type (a table with different record type)
        self.newRecordDefault: dict = {} # a record dictionary with default values for some field on insert
        self.filterCondition: list[tuple] = []  # reference key condition before where conditions, map master row to detail row
        self.limitCondition: int | None = None
        self.isDirty = False # setted on data changed
        self.isEditable = True # used in forms
        self.hasTotalsRow = False
        self.repr = 'Generic editable table model' # printable representation of the object
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr

    def flags(self, index: QModelIndex|QPersistentModelIndex) -> Qt.ItemFlag:
        "Return standard flags or readonly for some columns"
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        f = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        is_bool = self.columns[index.column()][TYPE] == 'bool'
        is_ro = self.columns[index.column()][RO]
        if not is_ro:
            f |= Qt.ItemFlag.ItemIsEditable
            if is_bool:
                f |= Qt.ItemFlag.ItemIsUserCheckable
        return f

    def data(self,
             index: QModelIndex | QPersistentModelIndex = QModelIndex(),
             role: int = Qt.ItemDataRole.DisplayRole
             ) -> Any:
        "Returns the required data from dataSet"
        # sometimes dataSet could be empty
        if (not index.isValid() 
            or index.row() > self.rowCount()
            or index.column() > self.columnCount()):
            return None
        row = index.row()
        col = index.column()
        if len(self.dataSet) <= row:
            return None
        if not col in self.dataSet[row]:
            return None
        result = self.dataSet[row][col]
        match role:
            case Qt.ItemDataRole.EditRole:
                return result
            case Qt.ItemDataRole.DisplayRole:
                if isinstance(result, bool):
                    return None # do not return text for bool, checkbox is managed in CheckStateRole
                return result
            case Qt.ItemDataRole.TextAlignmentRole:
                # numbers aligned right anything else aligned left
                if isinstance(result, (int, decimal.Decimal, QDate, QDateTime)):
                    return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
                else:
                    return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
            case Qt.ItemDataRole.CheckStateRole:
                if isinstance(result, bool):
                    return Qt.CheckState.Checked if result else Qt.CheckState.Unchecked
                return None
            case _:
                return None

    def setData(self, 
            index: QModelIndex | QPersistentModelIndex = QModelIndex(),
            value: Any = None,
            role: int = Qt.ItemDataRole.EditRole
            ) -> bool:
        """Set data in dataSet and mark row as modified"""
        if not index.isValid() or index.row() >= len(self.dataSet):
            return False
        row = index.row()
        col = index.column()
        record = self.dataSet[row]

        # for boolean value we use CheckStateRole and convert to bool, for any other value we use EditRole
        if role == Qt.ItemDataRole.CheckStateRole:
            new_value = (value == Qt.CheckState.Checked or value == Qt.CheckState.Checked.value)
            if record[col] == new_value:
                return False
            record[col] = new_value  # unleash Record.__setitem__
            self.isDirty = True
            self.dataChanged.emit(index, index, [role, Qt.ItemDataRole.DisplayRole])
            self.userDataChanged.emit()
            return True

        # for text and other value we use EditRole
        if role == Qt.ItemDataRole.EditRole:
            if record[col] == value:
                return False
            # empty string as Null value
            if isinstance(value, str):
                value = value or None
            # modify the data: Record.__setitem__ will set is_modified = True
            record[col] = value
            self.isDirty = True
            # notify the view that the data has changed
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            self.userDataChanged.emit()
            return True
        return False

    # def hiddenSetData(self, row: int, column: int, value: Any) -> None:
    #     "Set data without emitting dataChanged signal"
    #     row = self.filterMapping[row]
    #     self.dataSet[row][column] = value

    def submit(self) -> bool:
        "Update database: insert/delete/update rows, used only for commit on row changed, do nothing on manual submit"
        # used only for commit on row changed, do nothing on manual submit
        # BUT is needed for proper DataWidgetMapper use
        return True

    def submitAll(self, column: int|None = None, value: Any|None = None) -> bool:
        # if a referenceKey is provided fill all the rows with reference value
        record: Any
        if column is not None:
            for record in self.dataSet:
                record[column] = value
        sqlCheck = (f"SELECT {', '.join(self.primaryKey)}\n"
                    f"FROM {self.table}\n"
                    f"WHERE {' AND '.join([f'{i} = %({i})s' for i in self.primaryKey + (OVFIELD,)])};")
        try:
            with appconn.cursor() as cur:
                
                # *** DELETE ***
                # toDelete contains dict with pkey and object_version for each deleted record
                for record in self.toDelete:
                    args = record.pkey.copy()
                    args[OVFIELD] = record.object_version
                    # concurrency check
                    cur.execute(sqlCheck, args)
                    if cur.rowcount == 0:
                        raise PyAppDBConcurrencyError()
                    where = " AND ".join([f"{k} = %({k})s" for k in record.pkey])
                    script = f"DELETE FROM {self.table} WHERE {where};"
                    cur.execute(script, record.pkey)
                self.toDelete.clear()

                # *** UPDATE and INSERT ***
                # loop through all records, if is_new is True do insert, if is_modified is True do update, 
                # if both are False do nothing
                for record in self.dataSet:
                    if record.is_new and record.is_modified:
                        print("***** Record marked as NEW and MODIFIED, possible logical error! *****")
                    #print(f"Processing record: is_new={record.is_new}, is_modified={record.is_modified}, pkey={record.pkey}, object_version={record.object_version}")
                    #print(f"Record data: {record}")
                    # --- UPDATE ---
                    if record.is_modified and not record.is_new:
                        args = record.pkey.copy()
                        args[OVFIELD] = record.object_version
                        # concurrency check
                        cur.execute(sqlCheck, args)
                        if cur.rowcount == 0:
                            raise PyAppDBConcurrencyError()
                        # list of fields to update, only non read only fields with a field name
                        # (calculated fields have None as field name)
                        upd_fields = [c[FIELD] for c in self.columns if c[FIELD] and not c[RO]]
                        fields_str = ", ".join([f"{f} = %({f})s" for f in upd_fields])
                        where_str = " AND ".join([f"{k} = %({k})s" for k in record.pkey])
                        fieldsback = ", ".join([i[FIELD] for i in self.columns if i[FIELD]] + [OVFIELD])
                        
                        script = f"UPDATE {self.table} SET {fields_str} WHERE {where_str} RETURNING {fieldsback};"
                        
                        # mapping arguments for update, only non read only fields with a field name
                        upd_args = {self.columns[i][FIELD]: record[i] for i in range(len(self.columns)) if self.columns[i][FIELD]}
                        upd_args.update(record.pkey)
                        cur.execute(script, upd_args)
                        res = cur.fetchone()
                        if res:
                            # record is updated with returned values (in case of trigger modify the record)
                            for i in range(len(self.columns)): record[i] = res[i]
                            record.object_version = res[-1]
                            record.is_modified = False # Reset flag
                        # notify of changes
                        # calculate the index of the current row in the dataset
                        row_idx = self.dataSet.index(record) 
                        index_start = self.index(row_idx, 0) # index of the first column of the row
                        index_end = self.index(row_idx, self.columnCount() - 1) # index of the last column of the row
                        self.dataChanged.emit(index_start, index_end, [Qt.ItemDataRole.DisplayRole])

                    # --- INSERT ---
                    elif record.is_new:
                        fieldList = [i[FIELD] for i in self.columns if i[FIELD] and not i[RO]]
                        if self.automaticPKey:
                            for pk_f in self.primaryKey:
                                if pk_f in fieldList: 
                                    fieldList.remove(pk_f)
                        if self.recordType:
                            fieldList += [i for i in self.recordType]
                        args = {}
                        if self.recordType:
                            for i in self.recordType:
                                args[i] = self.recordType[i]
                        # set company after anything else, company_id may not be present in self.columns
                        if self.isCompanyTable:
                            fieldList += ['company_id']
                            args['company_id'] = session['current_company']
                        fields_str = ", ".join(fieldList)
                        placeholders = ", ".join([f"%({f})s" for f in fieldList])
                        fieldsback = ", ".join([i[FIELD] or 'Null' for i in self.columns] + list(self.primaryKey) + [OVFIELD])
                        
                        script = f"INSERT INTO {self.table} ({fields_str}) VALUES ({placeholders}) RETURNING {fieldsback};"
                        
                        # arguments for insert, only non read only fields with a field name
                        ins_args = {self.columns[i][FIELD]: record[i] for i in range(len(self.columns)) if self.columns[i][FIELD] and not self.columns[i][RO]}
                        ins_args.update(args)
                        #print(f"**** INSERT script ****\n{script}")
                        #print(f"**** INSERT args   ****\n{ins_args}")

                        cur.execute(script, ins_args)
                        res = cur.fetchone()
                        if res:
                            # repopulate the inserted record with returned values
                            for i in range(len(self.columns)): 
                                record[i] = res[i]
                            pk_start = len(self.columns)
                            record.pkey = {k: res[pk_start + i] for i, k in enumerate(self.primaryKey)}
                            record.object_version = res[-1]
                            record.is_new = False
                            record.is_modified = False
                        # notify of changes
                        # calculate the index of the current row in the dataset
                        row_idx = self.dataSet.index(record) 
                        index_start = self.index(row_idx, 0) # index of the first column of the row
                        index_end = self.index(row_idx, self.columnCount() - 1) # index of the last column of the row
                        self.dataChanged.emit(index_start, index_end, [Qt.ItemDataRole.DisplayRole])

            self.isDirty = False
            self.userDataChanged.emit()
            return True

        except psycopg.Error as er:
            raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


    def revertAll(self) -> None:
        self.toDelete.clear()
        self.isDirty = False
        self.select()

    def clearData(self) -> None:
        "Clear all the content of model"
        self.dataSet.clear()
        self.toDelete.clear()
        self.isDirty = False
        self.rows = 0 # usually updated by select
        self.cols = len(self.columns) # usually updated by select

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        "Returns header data for row (field header)/column (columns number) headers"
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.columns[section][DESCRIPTION]
        if orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return super().headerData(section, orientation, role)
        return None

    def rowCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the rows number of the dataSet"
        return len(self.dataSet)

    def columnCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
        "Returns the columns number of the dataSet"
        return len(self.columns)

    def insertRows(self, position: int, count: int, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> bool:
        "Insert rows in model"
        self.beginInsertRows(parent, position, position + count - 1)
        
        for i in range(position, position + count):
            data_dict = {idx: self.newRecordDefault.get(col[FIELD]) 
                        for idx, col in enumerate(self.columns)}
            new_record = Record(data_dict, pkey=None, object_version=0)
            new_record.is_new = True
            self.dataSet.insert(position, new_record)
            
        self.endInsertRows()
        self.isDirty = True
        self.userDataChanged.emit()
        self.rowCountChanged.emit(len(self.dataSet))
        return True

    def removeRows(self, position: int, count: int, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> bool:
        "Remove rows from model"
        if self.rowCount() < position + count:
            return False
        self.beginRemoveRows(parent, position, position + count - 1)
        
        rows_to_remove = self.dataSet[position : position + count]
        
        for record in rows_to_remove:
            if not record.is_new:
                self.toDelete.append(record)
        del self.dataSet[position : position + count]
        
        self.endRemoveRows()
        self.isDirty = True
        self.userDataChanged.emit()
        self.rowCountChanged.emit(len(self.dataSet))
        return True

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        "Inplace sorting of the model, manage null values base on declared data time"
        if not self.dataSet:
            return
        self.layoutAboutToBeChanged.emit()
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
            self.dataSet.sort(key=lambda x: x[column] or nv) # type: ignore
        else:
            self.dataSet.sort(key=lambda x: x[column] or nv, reverse=True) # type: ignore
        self.layoutChanged.emit()

    def filter(self, column: int|None = None, value: Any = None) -> None:
        "Filter records on a master/detail logic, this model is for detail"
        self.filterCondition.clear()
        if column is None: # empty master table or new record
            self.filterCondition.append(('True = %s', False))
        else:
            field = f"{self.columns[column][FIELD]}"
            self.filterCondition.append((f'{field} = %s', value))
        self.select()
 
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

    def getPrimaryKey(self, row: int) -> str|None:
        if row < 0:
            return None
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
                           + [OVFIELD])

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
            self.whereCondition.clear() # clear where condition after use, they are intended for one select only
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
        try:
            with appconn.cursor() as cur:
                cur.execute(script, args)
                
                self.beginResetModel()
                self.dataSet.clear()
                self.toDelete.clear()

                for record in cur:
                    data_dict = {i: record[i] for i in range(cols)}    
                    pkey_dict = {self.primaryKey[i - cols]: record[i] for i in pkcols}
                    # sanity check
                    if pkey_dict[self.primaryKey[0]] is None:
                        continue
                    new_record = Record(data_dict, pkey_dict, record[ovcol])
                    new_record['master_row'] = record[1]
                    new_record.is_modified = False
                    self.dataSet.append(new_record)
                    
                self.endResetModel()
                self.rowCountChanged.emit(len(self.dataSet))
                self.isDirty = False

        except psycopg.Error as er:
            self.endResetModel()
            raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
 
       
# class PandasModel(QAbstractTableModel):
#     """A read-only model to interface a database view with pandas pivot dataframe"""

#     def __init__(self,parent=None):
#         QAbstractTableModel.__init__(self, parent)
#         self._dataframe = None
#         self._pivot = None
#         self.table = None # table or view name - string, subclass must define this
#         self.isCompanyTable = False # True if is a company table, subclass must define this
#         self.columns = () # model columns definition, subclass must define this
#         # Number of rows needed for column headers
#         #self.col_levels = dataframe.columns.nlevels if hasattr(dataframe.columns, 'nlevels') else 1
#         self.col_levels = 0
#         # Number of columns needed for row headers (index)
#         self.row_levels = 0 # updated by createPivot
        
#     def select(self) -> None:
#         "Fetch rows from DB creating the sql select statement and filling the dataset"
#         # create a reverse dictionary for columns translation
#         self.trcolumns = {self.columns[i][0]: i for i in self.columns}
#         #print("Columns translation:", self.trcolumns)
#         script = f"SELECT {', '.join(self.columns.keys())}\nFROM {self.table}"
#         if self.isCompanyTable:
#             script += "\nWHERE company_id = system.pa_current_company();"
#         else:
#             script += ";"
#         #print("**** PandasModel SELECT script ****\n", script)
#         try:
#             with appconn.cursor() as cur:
#                 cur.execute(script)
#                 if cur.description:
#                     columns = [self.columns[i[0]][0] for i in cur.description]
#                 else:                    
#                     columns = []
#                 df = pd.DataFrame(cur.fetchall(), columns=columns)
#                 #print(df.head())
#         except psycopg.Error as er:
#             raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))   
#         # force correct data types
#         f = {self.columns[i][0]: self.columns[i][3] for i in self.columns if self.columns[i][3]}
#         self._dataframe = df.astype(f)
#         #print(f"Dataframe loaded with {len(self._dataframe)} rows and {len(self._dataframe.columns)} columns")
#         #print("DTypes:", self._dataframe.dtypes)
        
#         # Number of columns needed for row headers (index)
#         #self.row_levels = df.index.nlevels if hasattr(df.index, 'nlevels') else 1
#         #print('Columns:', self._dataframe.columns)
        
#     def filterEvent(self, value: str) -> None:
#         "Filter dataframe for a specific event description"
#         # re-generate dataframe from DB, undo previous filters
#         self.select()
#         if self._dataframe is None:
#             return
#         self._dataframe = self._dataframe[self._dataframe[self.columns['event'][0]] == value]
        
#     def filterLike(self, column: str, value: str) -> None:
#         "Filter dataframe for a specific column value using like operator"
#         if self._dataframe is None:
#             return
#         if column not in self._dataframe.columns:
#             return
#         self._dataframe = self._dataframe[self._dataframe[column].astype(str).str.contains(value, na=False, case=False)]
        
#     def getEvents(self) -> list:
#         "Return a list of distinct events description"
#         if self._dataframe is None:
#             return []
#         c = (self.columns.get('event') or (None,))[0] # index are translated for pivot use
#         return self._dataframe[c].dropna().unique().tolist()

#     def createPivot(self, rows: list, columns: list, values: list, aggfunc: dict, totals: bool) -> None:
#         "Create a pivot table from the dataframe"
#         if self._dataframe is None:
#             return
#         #print(self._dataframe.head())
#         self._pivot = pd.pivot_table(self._dataframe,
#                                     index=rows,
#                                     columns=columns,
#                                     values=values,
#                                     aggfunc=aggfunc,
#                                     fill_value=0.0,
#                                     margins=totals,
#                                     margins_name=_tr('Statistics','Totale Generale'))
#         logger.info(f"Pivot table created with {len(self._pivot)} rows and {len(self._pivot.columns)} columns")
#         #print(self._pivot.head())
#         #print(self._pivot.columns)
#         #print(self._pivot.index.names)
#         #print(self._pivot.info())
#         # update col_levels
#         #self.col_levels = self._pivot.columns.nlevels if hasattr(self._pivot.columns, 'nlevels') else 1
#         #self.col_levels += totals
#         # update row_levels
#         self.row_levels = self._pivot.index.nlevels if hasattr(self._pivot.index, 'nlevels') else 1
#         self.row_levels += totals

#     def rowCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
#         return self._pivot.shape[0] + self.col_levels

#     def columnCount(self, parent: QModelIndex|QPersistentModelIndex = QModelIndex()) -> int:
#         return self._pivot.shape[1] + self.row_levels

#     def data(self,
#              index: QModelIndex|QPersistentModelIndex = QModelIndex(),
#              role: int = Qt.ItemDataRole.DisplayRole
#              ) -> Any:
#         if not index.isValid():
#             return None
#         header = self.headerData(index.column(), Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
#         if header:
#             header = header.split('\n')[0]  # in case of multi-line header
#         fm = self.columns[self.trcolumns[header]][4]  # (name, format)
#         if role == Qt.ItemDataRole.TextAlignmentRole:
#             if fm in ('int', 'float', 'decimal2'):   
#                 return Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
#             return Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        
#         if role == Qt.ItemDataRole.DisplayRole:
#             r, c = index.row(), index.column()
#             dt = self._pivot.iloc[r - self.col_levels, c - self.row_levels] if r >= self.col_levels and c >= self.row_levels else None
#             # CASE 1: Top-Left Empty Corner
#             if r < self.col_levels and c < self.row_levels:
#                 return ""
#             # CASE 2: Column Headers (Top rows)
#             if r < self.col_levels:
#                 label = self._pivot.columns[c - self.row_levels]
#                 return str(label[r]) if isinstance(label, tuple) else str(label)
#             # CASE 3: Row Headers (Left columns)
#             if c < self.row_levels:
#                 label = self._pivot.index[r - self.col_levels]
#                 outstr = label[c] if isinstance(label, tuple) else label
#                 if fm == 'int':
#                     return session['qlocale'].toString(int(outstr or 0))
#                 elif fm in ('float', 'decimal2'):
#                     return session['qlocale'].toString(float(outstr or 0.0), 'f', 2)
#                 elif fm == 'date':
#                     if pd.isna(outstr):
#                         return ""
#                     return outstr.strftime('%d/%m/%Y')
#                 else:
#                     return str(outstr)
#             # CASE 4: Actual Data Values
#             if fm == 'int':
#                 return session['qlocale'].toString(int(dt or 0))
#             elif fm in ('float', 'decimal2'):
#                 return session['qlocale'].toString(float(dt or 0.0), 'f', 2)
#             elif fm == 'date':
#                 if pd.isna(dt):
#                     return ""
#                 return dt.strftime('%d/%m/%Y') if hasattr(dt, 'strftime') else str(dt)
#             else:
#                 return str(dt)
        
#         return None

#     def headerData(self, section, orientation, role: int =Qt.ItemDataRole.DisplayRole) -> str|None:
#         if role == Qt.ItemDataRole.DisplayRole:
#             if orientation == Qt.Orientation.Horizontal:
#                 if section < self.row_levels:
#                     #print('Index;', self._pivot.index)
#                     return self._pivot.index.names[section]
#                 # Column Names
#                 col_label = self._pivot.columns[section - self.row_levels]
#                 # If MultiIndex, join levels
#                 return "\n".join(map(str, col_label)) if isinstance(col_label, tuple) else str(col_label)
            
#             if orientation == Qt.Orientation.Vertical:
#                 return None
#         return None

