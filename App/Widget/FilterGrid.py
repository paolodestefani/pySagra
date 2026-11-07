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

"""Filter grid

This module contains the rows of filters shared by SortFilterDialog and
PrintDialog. Each row has a field, a negate check box, an operator and an
operand widget that depends on the operator.

The dialogs own a FilterGrid and tell it which fields are available: the grid
knows nothing about models or reports.

"""

# standard library
import logging
from dataclasses import dataclass
from enum import IntEnum
from functools import partial
from typing import Any
from typing import Callable

# PySide6
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QObject
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import Qt
from PySide6.QtCore import QTime
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QDateEdit
from PySide6.QtWidgets import QDateTimeEdit
from PySide6.QtWidgets import QDoubleSpinBox
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QTimeEdit
from PySide6.QtWidgets import QWidget

# application modules
from App.Common.L10n import _tr
from App.Widget.Control import CheckableComboBox


# logger
logger = logging.getLogger(__name__)

# filter rows
FILTER_ROWS = 30

# types of the reports stored in the database that use the filters of another type
FILTER_TYPE_ALIAS = {'float': 'decimal'}


# filter fields, these are the columns of the layout
class ff(IntEnum):
    FIELD       = 0
    NEGATE      = 1
    OPERATOR    = 2
    OPERAND     = 3


def filterOperators() -> dict[str, list[tuple]]:
    """Return the operators of each field type, translated at runtime
    Each operator is (operator, description, format, widget)
    format:
    0 = require operand argument (field operator %s - args)
    1 = no require operand (field operator)
    2 = operand included in operator with argument as list (field operator - args)
    3 = operand included in operator with argument literal
    The LIST widget is available only for fields that have a list of values"""
    return {
        # integer
        'int': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', 'From list'), 0, 'LIST'), # list of reference values
            ('=', _tr('Operator', '='), 0, 'SB'), # spinbox
            ('<', _tr('Operator', '<'), 0, 'SB'),
            ('<=', _tr('Operator', '<='), 0, 'SB'),
            ('>', _tr('Operator', '>'), 0, 'SB'),
            ('>=', _tr('Operator', '>='), 0, 'SB'),
            ('= ANY(%s)', _tr('Operator', 'In'), 2, 'LEI'), # line edit int list
            ('IS NULL', _tr('Operator', 'Is Null'), 1, None),
            ],
        # decimal number
        'decimal': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', '='), 0, 'DSB'), # double spinbox
            ('<', _tr('Operator', '<'), 0, 'DSB'),
            ('<=', _tr('Operator', '<='), 0, 'DSB'),
            ('>', _tr('Operator', '>'), 0, 'DSB'),
            ('>=', _tr('Operator', '>='), 0, 'DSB'),
            ('= ANY(%s)', _tr('Operator', 'In'), 2, 'LED'), # line edit decimal list
            ('IS NULL', _tr('Operator', 'Is Null'), 1, None)
            ],
        # boolean
        'bool': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', '='), 0, 'CB'), # checkbox
            ('IS NULL', _tr('Operator', 'Is null'), 1, None)
            ],
        # string
        'str': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', 'From list'), 0, 'LIST'), # list of reference values
            ('=', _tr('Operator', '='), 0, 'LE'), # line edit
            ("ilike '%%'||%s||'%%'", _tr('Operator', 'Contains'), 3, 'LE'),
            ("ilike %s||'%%'", _tr('Operator', 'Starts with'), 3, 'LE'),
            ("ilike '%%'||%s", _tr('Operator', 'Ends with'), 3, 'LE'),
            ('ILIKE ANY(%s)', _tr('Operator', 'In'), 2, 'LES'), # line edit string list case insensitive
            ('IS NULL', _tr('Operator', 'Is null'), 1, None)
            ],
        # date
        'date': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', '='), 0, 'DE'), # date edit
            ('<', _tr('Operator', '<'), 0, 'DE'),
            ('<=', _tr('Operator', '<='), 0, 'DE'),
            ('>', _tr('Operator', '>'), 0, 'DE'),
            ('>=', _tr('Operator', '>='), 0, 'DE'),
            ('IS NULL', _tr('Operator', 'Is Null'), 1, None)
            ],
        # date time
        'datetime': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', '='), 0, 'DTE'), # date time edit
            ('<', _tr('Operator', '<'), 0, 'DTE'),
            ('<=', _tr('Operator', '<='), 0, 'DTE'),
            ('>', _tr('Operator', '>'), 0, 'DTE'),
            ('>=', _tr('Operator', '>='), 0, 'DTE'),
            ('IS NULL', _tr('Operator', 'Is Null'), 1, None)
            ],
         # time
        'time': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', '='), 0, 'TE'), # date time edit
            ('<', _tr('Operator', '<'), 0, 'TE'),
            ('<=', _tr('Operator', '<='), 0, 'TE'),
            ('>', _tr('Operator', '>'), 0, 'TE'),
            ('>=', _tr('Operator', '>='), 0, 'TE'),
            ('IS NULL', _tr('Operator', 'Is Null'), 1, None)
            ],
        # reference field / list
        'refstr': [
            ('', '', 0, None),  # first row means no data
            ('=', _tr('Operator', '='), 0, 'SCB'), # standard combo box
            ('= ANY(%s)', _tr('Operator', 'In'), 2, 'CCB'), # checkable combo box
            ('IS NULL', _tr('Operator', 'Is Null'), 1, None)
            ]
        }


def parseList(text: str, convert: Callable) -> list:
    "Return the valid values of a comma separated list, saved filters can hold invalid ones"
    values = []
    for value in text.split(','):
        try:
            values.append(convert(value.strip()))
        except ValueError:
            continue
    return values


class RowComboBox(QComboBox):
    "Custom combo box for store row number and set currentData"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.row: int|None = None

    def setCurrentData(self, data: Any) -> None:
        "Set current index based on data"
        idx = self.findData(data)
        if idx >= 0:
            self.setCurrentIndex(idx)
        else:
            self.setCurrentIndex(0)

    def setCurrentOperator(self, operator: str) -> None:
        "Set current index based on operator string inside a tuple stored in userData"
        for idx in range(self.count()):
            tuple_data = self.itemData(idx)
            if tuple_data and tuple_data[0] == operator:
                self.setCurrentIndex(idx)
                return
        self.setCurrentIndex(0)

    def currentOperator(self) -> str|None:
        "Return the operator string inside a tuple stored in userData"
        tuple_data = self.currentData()
        return tuple_data[0] if tuple_data else None

    def currentFormat(self) -> int|None:
        "Return the format code inside a tuple stored in userData"
        tuple_data = self.currentData()
        return tuple_data[2] if tuple_data else None

    def currentWidgetType(self) -> str|None:
        "Return the widget type string inside a tuple stored in userData"
        tuple_data = self.currentData()
        return tuple_data[3] if tuple_data else None

    def currentOperatorKey(self) -> str:
        "Key saved in the DB: SQL operator + widget type (ex. '=#SB', '=#LIST')"
        data = self.currentData()
        return f"{data[0]}#{data[3] or ''}" if data else ''

    def setCurrentOperatorKey(self, key: str) -> None:
        "Select the operator from its key; old keys without '#' use the first match"
        if '#' not in key:
            self.setCurrentOperator(key)    # data saved before the change
            return
        for idx in range(self.count()):
            data = self.itemData(idx)
            if data and f"{data[0]}#{data[3] or ''}" == key:
                self.setCurrentIndex(idx)
                return
        self.setCurrentIndex(0)


class RowCheckBox(QCheckBox):
    "Custom checkbox for storeing row number"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.row: int|None = None


class SpacerWidget(QWidget):
    "Custom widget for storeing field type"


class LineEditStrings(QLineEdit):
    "Custom line edit for list of string values separated by comma"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)

    def value(self) -> list:
        "Return the list of values separated by comma for ues in SQL ILIKE ANY(%s) operator"
        return [f'%{v.strip()}%' for v in self.text().split(',') if v.strip()]


class LineEditInts(QLineEdit):
    "Custom line edit for list of int values separated by comma"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.setValidator(QRegularExpressionValidator(
            QRegularExpression(r'\s*[+-]?\d*(\s*,\s*[+-]?\d*)*\s*'), self))

    def value(self) -> list:
        "Return the list of values separated by comma"
        return parseList(self.text(), int)


class LineEditDecimals(QLineEdit):
    "Custom line edit for list of decimal values separated by comma"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.setValidator(QRegularExpressionValidator(
            QRegularExpression(r'\s*[+-]?\d*\.?\d*(\s*,\s*[+-]?\d*\.?\d*)*\s*'), self))

    def value(self) -> list:
        "Return the list of values separated by comma"
        return parseList(self.text(), float)


def operandValue(widget: QWidget) -> Any:
    "Return the value of an operand widget as a query argument"
    match widget:
        case CheckableComboBox(): # before QComboBox: it is a subclass
            return widget.currentData() # list
        case QComboBox():
            return widget.currentData()
        case LineEditStrings()|LineEditInts()|LineEditDecimals(): # before QLineEdit: they are subclasses
            return widget.value()
        case QLineEdit():
            return widget.text()
        case QSpinBox()|QDoubleSpinBox():
            return widget.value()
        case QDateEdit():
            return widget.date()
        case QTimeEdit(): # before QDateTimeEdit: it is a subclass
            return widget.time()
        case QDateTimeEdit():
            return widget.dateTime()
        case QCheckBox():
            return widget.isChecked()
        case _:
            return None


def operandText(widget: QWidget) -> Any:
    "Return the value of an operand widget as it is saved in the database"
    match widget:
        case CheckableComboBox(): # before QComboBox: it is a subclass
            return '|'.join(str(x) for x in widget.currentData())
        case QComboBox():
            return str(widget.currentData())
        case QLineEdit():
            return widget.text()
        case QSpinBox()|QDoubleSpinBox():
            return widget.value()
        case QDateEdit():
            return widget.date().toString(Qt.DateFormat.ISODate)
        case QTimeEdit(): # before QDateTimeEdit: it is a subclass
            return widget.time().toString(Qt.DateFormat.ISODate)
        case QDateTimeEdit():
            return widget.dateTime().toString(Qt.DateFormat.ISODate)
        case QCheckBox():
            return widget.isChecked()
        case _:
            return None


def setOperandText(widget: QWidget, text: str) -> None:
    "Set an operand widget from the value saved in the database"
    match widget:
        case CheckableComboBox(): # before QComboBox: it is a subclass
            widget.setCheckedData([x for x in text.split('|') if x])
        case QComboBox():
            # saved as data; old saves contain the index
            idx = next((i for i in range(widget.count())
                        if str(widget.itemData(i)) == text), -1)
            if idx < 0 and text.isdigit() and int(text) < widget.count():
                idx = int(text)
            widget.setCurrentIndex(idx)
        case QLineEdit():
            widget.setText(text)
        case QSpinBox():
            widget.setValue(int(float(text or 0)))
        case QDoubleSpinBox():
            widget.setValue(float(text or 0.0))
        case QDateEdit():
            widget.setDate(QDate.fromString(text, Qt.DateFormat.ISODate))
        case QTimeEdit(): # before QDateTimeEdit: it is a subclass
            widget.setTime(QTime.fromString(text, Qt.DateFormat.ISODate))
        case QDateTimeEdit():
            widget.setDateTime(QDateTime.fromString(text, Qt.DateFormat.ISODate))
        case QCheckBox():
            widget.setChecked(text == 'True')


@dataclass
class FilterRow:
    "The widgets of a row of the grid"
    field: RowComboBox
    negate: RowCheckBox
    operator: RowComboBox
    operand: QWidget


class FilterGrid(QObject):
    """The filter rows of a dialog, built inside an existing grid layout.
    Fields are set with setFields, the result can be read as query conditions
    with conditions, saved with settings and restored with restore"""

    def __init__(self, layout: QGridLayout, parent: QWidget) -> None:
        super().__init__(parent)
        self.gridLayout = layout
        self.owner = parent
        self.operators = filterOperators()
        self.fieldType: dict[Any, str] = {}
        self.fieldList: dict[Any, Callable|None] = {}
        self.rows: list[FilterRow] = []
        for row in range(FILTER_ROWS):
            self.rows.append(self._createRow(row))
        layout.setColumnStretch(ff.FIELD, 2)
        layout.setColumnStretch(ff.NEGATE, 0)
        layout.setColumnStretch(ff.OPERATOR, 1)
        layout.setColumnStretch(ff.OPERAND, 1)
        layout.setRowStretch(FILTER_ROWS, 1)

    def _createRow(self, row: int) -> FilterRow:
        "Create the widgets of a row"
        field = RowComboBox(self.owner)
        field.row = row
        field.addItem('', None) # item 0 for clear/reset
        field.currentIndexChanged.connect(partial(self._fieldChanged, row))
        negate = RowCheckBox(self.owner)
        negate.setDisabled(True)
        negate.row = row
        negate.setToolTip(_tr('SoftFilterDialog', 'Not'))
        operator = RowComboBox(self.owner)
        operator.setDisabled(True)
        operator.row = row
        operator.currentIndexChanged.connect(partial(self._operatorChanged, row))
        operand = SpacerWidget(self.owner) # position widget only
        self.gridLayout.addWidget(field, row, ff.FIELD)
        self.gridLayout.addWidget(negate, row, ff.NEGATE)
        self.gridLayout.addWidget(operator, row, ff.OPERATOR)
        self.gridLayout.addWidget(operand, row, ff.OPERAND)
        return FilterRow(field, negate, operator, operand)

    def setFields(self, fields: list[tuple[Any, str, str, Callable|None]]) -> None:
        """Set the available fields and clear the filters
        Each field is (field, description, type, function that returns the
        (key, description) values of the field or None)"""
        self.reset()
        self.fieldType = {f: t for f, d, t, l in fields}
        self.fieldList = {f: l for f, d, t, l in fields}
        for row in self.rows:
            row.field.blockSignals(True)
            row.field.clear()
            row.field.addItem('', None) # item 0 for clear/reset
            for f, d, t, l in fields:
                row.field.addItem(d, f)
            row.field.blockSignals(False)

    def reset(self) -> None:
        "Clear all the filters"
        for row in self.rows:
            row.field.setCurrentIndex(0)
            row.negate.setChecked(False)
            row.operator.setCurrentIndex(0)

    def _fieldChanged(self, row: int, index: int) -> None:
        "Set the negate check box and the available operators of a row"
        if index < 0:
            return
        filterRow = self.rows[row]
        filterRow.negate.setChecked(False)
        if index == 0:
            filterRow.negate.setDisabled(True)
            filterRow.operator.setCurrentIndex(0)
            filterRow.operator.setDisabled(True)
            return
        filterRow.negate.setEnabled(True)
        field = filterRow.field.currentData()
        ftype = self.fieldType.get(field)
        if not ftype:
            return
        filterRow.operator.setEnabled(True)
        filterRow.operator.clear()
        operators = self.operators.get(FILTER_TYPE_ALIAS.get(ftype, ftype))
        if operators is None:
            logger.warning("No filter operators for type %s of field %s", ftype, field)
            return
        for item in operators:
            if item[3] == 'LIST' and self.fieldList.get(field) is None:
                continue # skip if no list of values available
            filterRow.operator.addItem(item[1], item)

    def _operatorChanged(self, row: int, index: int) -> None:
        "Replace the operand widget of a row"
        if index < 0:
            return
        filterRow = self.rows[row]
        kind = filterRow.operator.currentWidgetType() if index > 0 else None
        widget = self._createOperand(kind, filterRow.field.currentData())
        self.gridLayout.removeWidget(filterRow.operand)
        filterRow.operand.deleteLater() # delete previous widget (MANDATORY)
        filterRow.operand = widget
        self.gridLayout.addWidget(widget, row, ff.OPERAND)

    def _createOperand(self, kind: str|None, field: Any) -> QWidget:
        "Return the operand widget for a kind of operator"
        widget: QWidget
        match kind:
            case 'SB': # spinbox
                widget = QSpinBox(self.owner)
                widget.setRange(0, 2147483647)
            case 'DSB': # double spinbox
                widget = QDoubleSpinBox(self.owner)
                widget.setDecimals(2)
                widget.setMaximum(99999999.99)
            case 'CB': # check box
                widget = QCheckBox(self.owner)
            case 'DE': # date edit
                widget = QDateEdit(QDate.currentDate(), self.owner)
                widget.setCalendarPopup(True)
                widget.setMinimumDate(QDate(1800, 1, 1))
                widget.setMaximumDate(QDate(3000, 12, 31))
                widget.setDate(QDate.currentDate())
            case 'DTE': # date time edit
                widget = QDateTimeEdit(self.owner)
                widget.setCalendarPopup(True)
                widget.setMinimumDate(QDate(1800, 1, 1))
                widget.setMaximumDate(QDate(3000, 12, 31))
                widget.setDate(QDate.currentDate())
            case 'TE': # time edit
                widget = QTimeEdit(QTime.currentTime(), self.owner)
            case 'LE': # line edit
                widget = QLineEdit(self.owner)
            case 'LES': # line edit string list
                widget = LineEditStrings(self.owner)
            case 'LEI': # line edit int list
                widget = LineEditInts(self.owner)
            case 'LED': # line edit decimal list
                widget = LineEditDecimals(self.owner)
            case 'LIST'|'SCB': # combo box
                widget = QComboBox(self.owner)
                self._fillList(widget, field)
            case 'CCB': # checkable combo box
                widget = CheckableComboBox(self.owner)
                self._fillList(widget, field)
            case _: # no widget required (is null)
                widget = SpacerWidget(self.owner)
        return widget

    def _fillList(self, widget: QComboBox, field: Any) -> None:
        "Fill a combo box with the values of a field"
        values = self.fieldList.get(field)
        if values is not None:
            for k, v in values():
                widget.addItem(v, k)

    def conditions(self) -> list[tuple[str, Any]]:
        "Return the (condition, argument) pairs of the filters to apply to a query"
        result: list[tuple[str, Any]] = []
        for row in self.rows:
            if row.field.currentIndex() <= 0 or row.operator.currentIndex() <= 0:
                continue
            field = row.field.currentData()
            operator = row.operator.currentOperator()
            value = operandValue(row.operand)
            argument: Any
            match row.operator.currentFormat():
                case 0:
                    # a date operand compares the day, the column can be a timestamp
                    column = f"({field})::date" if isinstance(row.operand, QDateEdit) else field
                    condition = f"{column} {operator} %s"
                    argument = value
                case 1:
                    condition = f"{field} {operator}"
                    argument = None
                case 2:
                    condition = f"{field} {operator}"
                    argument = value.split() if isinstance(value, str) else value
                case 3:
                    condition = f"{field} {operator}"
                    argument = value
                case _ as fmt:
                    raise ValueError(f"Unknown operator format: {fmt}")
            if row.negate.isChecked():
                condition = f"NOT {condition}"
            result.append((condition, argument))
        return result

    def settings(self) -> list[tuple[int, Any, bool, str, str]]:
        "Return the (row, field, negate, operator key, value) of the filters to save"
        return [(index, row.field.currentData(), row.negate.isChecked(),
                 row.operator.currentOperatorKey(), str(operandText(row.operand)))
                for index, row in enumerate(self.rows) if row.field.currentIndex() > 0]

    def restore(self, filters: list[tuple]) -> None:
        "Set the rows from the (type, row, field, negate, operator key, value) saved filters"
        for _, index, field, negate, operator, value in filters:
            if index >= FILTER_ROWS:
                continue
            row = self.rows[index]
            row.field.setCurrentData(field)
            row.negate.setChecked(negate)
            row.operator.setCurrentOperatorKey(operator)
            setOperandText(row.operand, value or '')
