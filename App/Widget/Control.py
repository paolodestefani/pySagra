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

"""Controls

This module groups general customized controls used in forms


"""

# standard library
import os
import decimal
from typing import Callable, Any

# PySide6
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QBuffer
from PySide6.QtCore import QIODeviceBase
from PySide6.QtCore import Property
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtCore import QLocale
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QSize
from PySide6.QtCore import QPoint
from PySide6.QtCore import QUuid
from PySide6.QtCore import QUrl
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import QEvent
from PySide6.QtCore import QObject
from PySide6.QtCore import QTimerEvent
from PySide6.QtGui import QKeyEvent
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtGui import QResizeEvent
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QImage
from PySide6.QtGui import QIcon
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPen
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetrics
from PySide6.QtGui import QFontDatabase
from PySide6.QtGui import QTextDocument
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtGui import QCursor
from PySide6.QtGui import QAction
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QCompleter
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QDoubleSpinBox
from PySide6.QtWidgets import QDateEdit
from PySide6.QtWidgets import QDateTimeEdit
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QFontComboBox
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QDataWidgetMapper
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QToolBar
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QWidget

# application modules
from App import session
from App import currentIcon
from App.Core.L10n import _tr
from App.Core.Cryptography import string_encode
from App.Core.Cryptography import string_decode



class LabelImage(QLabel):

    imageChanged=Signal()

    def _get_imageBytearray(self) -> QByteArray|None:
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        if self.pixmap():
            self.pixmap().save(buf, "PNG")
            return buf.data()
        else:
            return None

    def _set_imageBytearray(self, ba: QByteArray|None) -> None:
        #print(type(ba))
        if ba:
            pix = QPixmap()
            pix.loadFromData(ba)
            super().setPixmap(pix)
        else:
            self.clear()

    imageBytearray = Property(QByteArray, fget=_get_imageBytearray, fset=_set_imageBytearray, notify=imageChanged)

    def clear(self) -> None:
        super().clear()
        self.setText(_tr("Controls", "NO IMAGE"))


class SpinBoxDecimal(QDoubleSpinBox):

    valueChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setSpecialValueText("--")
        self.setMinimum(-999999999999.99) # specialValueText is shown when value = minimum
        self.setRange(-999999999999.99, 999999999999.99)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    # def fixup(self, text: str) -> None:
    #     # if input is invalid set specialValueText = Null
    #     self.setValue(self.minimum())

    def _get_modelDataDecimal(self) -> decimal.Decimal|None:
        if self.value() == self.minimum():
            return None
        else:
            return decimal.Decimal(str(self.value())) # floaf to string to decimal for keep rounded values

    def _set_modelDataDecimal(self, value: decimal.Decimal|None) -> None:
        if value is None:
            self.setValue(self.minimum())
        else:
            self.setValue(float(value))

    modelDataDecimal = Property(object, fget=_get_modelDataDecimal, fset=_set_modelDataDecimal, notify=valueChanged)


class SpinBoxInt(QSpinBox):

    valueChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setSpecialValueText("--")
        self.setMinimum(-999999999) # specialValueText is shown when value = minimum
        self.setRange(-999999999, 999999999)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def _get_modelDataInt(self) -> int|None:
        if self.value() == self.minimum():
            return None
        else:
            return self.value()

    def _set_modelDataInt(self, value: int|None) -> None:
        if value is None:
            value = self.minimum()
        self.setValue(int(value))

    modelDataInt = Property(object, fget=_get_modelDataInt, fset=_set_modelDataInt, notify=valueChanged)


class CheckBox(QCheckBox):

    checkStateChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setTristate(True)

    def _get_modelDataState(self) -> bool|None:
        if self.checkState() == Qt.CheckState.Checked:
            return True
        elif self.checkState() == Qt.CheckState.Unchecked:
            return False
        else:
            return None

    def _set_modelDataState(self, value: bool|None) -> None:
        if value is True:
            self.setCheckState(Qt.CheckState.Checked)
        elif value is False:
            self.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.setCheckState(Qt.CheckState.PartiallyChecked)
    modelDataState = Property(object, fget=_get_modelDataState, fset=_set_modelDataState, notify=checkStateChanged)


class DateEdit(QLineEdit):
    "A line edit for date input that accepts Null values"

    dateChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setInputMask('00/00/0000;_')
        #self.textEdited.connect(self.adjustDate)

    def keyPressEvent(self, keyEvent: QKeyEvent) -> None:
        if keyEvent.text() in ('d', 'D'):
            self.setDate(QDate().currentDate())
        elif keyEvent.text() == '+':
            if date := self.date():
                self.setDate(date.addDays(1))
        elif keyEvent.text() == '-':
            if date := self.date():
                self.setDate(date.addDays(-1))
        else:
            super().keyPressEvent(keyEvent)

    def date(self) -> QDate|None:
        "Returns a date object or None, autocomplete month and year if omitted"
        date = self.text()
        if date == '//':  # no date entered
            return None
        d, m, y = date.split('/')
        if not d:
            di = 0
        else:
            di = int(d)
        if not m:
            mi = QDate().currentDate().month()
        else:
            mi = int(m)
        if not y:
            yi = QDate().currentDate().year()
        else:
            yi = int(y)
        outDate = QDate(yi, mi, di)
        if outDate.isValid():
            return outDate
        else:
            self.setText('//')
            return None

    def setDate(self, date: QDate|None) -> None:
        "Set date in the line edit"
        if date:
            self.setText(date.toString(QLocale.system().toString(date, QLocale.FormatType.ShortFormat)))
        else:
            self.setText("")

    def _get_modelDataDate(self) -> QDate|None:
        return self.date()

    def _set_modelDataDate(self, value: QDate|None) -> None:
        self.setDate(value)

    modelDataDate = Property(object, fget=_get_modelDataDate, fset=_set_modelDataDate, notify=dateChanged)


class DateTimeEdit(QDateTimeEdit):
    "A QDateTimeEdit class that accepts Null values"

    dateTimeChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setSpecialValueText(" ")
        self.setMinimumDateTime(QDateTime(1800, 1, 1, 0, 0, 0))
        self.setDateTime(QDateTime.currentDateTime())

    # def fixup(self, text: str) -> None:
    #     # if input is invalid set specialValueText = Null
    #     self.setDateTime(self.minimumDateTime())

    def _get_modelDataDateTime(self) -> QDateTime|None:
        if self.dateTime() == self.minimumDateTime():
            return None
        else:
            return self.dateTime()

    def _set_modelDataDateTime(self, value: QDateTime|None) -> None:
        if value is None:
            self.setDateTime(QDateTime(1800, 1, 1, 0, 0, 0)) # minimum date
        else:
            self.setDateTime(value)

    modelDataDateTime = Property(object, fget=_get_modelDataDateTime, fset=_set_modelDataDateTime, notify=dateTimeChanged)


class RelationalComboBox(QComboBox):
    """QComboBox that uses userData + itemText for key-value foreign key
    or set/get items from a (k, v) list. Can be Null. If available can use icon too"""

    itemChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.sqlFunc: Callable|None = None
        self.nullable = False
        self.currentIndexChanged.connect(self.itemChanged.emit)

    def setNullable(self, nullable: bool) -> None:
        self.nullable = nullable

    def setFunction(self, sqlFunc: Callable) -> None:
        "Store key/value function and update the list"
        self.sqlFunc = sqlFunc
        self.updateList()

    def updateList(self) -> None:
        self.clear()
        if not self.sqlFunc:
            return
        data = self.sqlFunc()
        #print(data)
        if data:
            if len(data[0]) == 3:  # items with icon
                if self.nullable:
                    for i, v, k in [(QIcon(), None, None)] + data:
                        self.addItem(i, k, v)
                else:
                    for i, v, k in data:
                        self.addItem(i, k, v)
            else:                  # items without icon
                if self.nullable:
                    for v, k in [(None, None)] + data:
                        self.addItem(k, v)
                else:
                    for v, k in data:
                        self.addItem(k, v)

    def setItemList(self, items: list) -> None:
        self.clear()
        if items:
            if len(items[0]) == 3:  # items with icon
                for i, v, k in items:
                    self.addItem(i, k, v)
            else:                   # items without icon
                for v, k in items:
                    self.addItem(k, v)

    def showPopup(self) -> None:
        "Update key/value list before show popup request"
        if self.sqlFunc:
            self.updateList()
        super().showPopup()

    def _get_modelDataInt(self) -> int|None:
        val = self.currentData(Qt.ItemDataRole.UserRole)
        return int(val) if val is not None else -1 # must return a number even if null

    def _set_modelDataInt(self, data: int|None) -> None:
        index = self.findData(data)
        self.setCurrentIndex(index if index >= 0 else 0) # can be -1 on New

    modelDataInt = Property(int, fget=_get_modelDataInt, fset=_set_modelDataInt, notify=itemChanged)

    def _get_modelDataStr(self) -> str|None:
        val = self.currentData(Qt.ItemDataRole.UserRole)
        return str(val) if val is not None else "" # must return a string even if null

    def _set_modelDataStr(self, data: str|None) -> None:
        index = self.findData(data, Qt.ItemDataRole.UserRole, Qt.MatchFlag.MatchExactly|Qt.MatchFlag.MatchCaseSensitive)
        self.setCurrentIndex(index if index >= 0 else 0) # can be -1 on New

    modelDataStr = Property(str, fget=_get_modelDataStr, fset=_set_modelDataStr, notify=itemChanged)
        

class DataWidgetMapper(QDataWidgetMapper):
    "Subclass of QDataWidgetMapper that commit data on combobox change, workaround for comboboxes on MacOS that not get focusOut event properly"

    def addMapping(self, widget: QWidget, section: int, propertyName: QByteArray|bytes|bytearray|memoryview|None = None) -> None:
        # Match the overloads of QDataWidgetMapper.addMapping
        if propertyName is None:
            super().addMapping(widget, section)
        else:
            super().addMapping(widget, section, propertyName)
        if isinstance(widget, QComboBox):
            delegate = self.itemDelegate()
            widget.currentIndexChanged.connect(lambda: delegate.commitData.emit(widget))


class ColorComboBox(QComboBox):
    """QComboBox that uses userData + itemText for key-value foreign key
    or set/get items from a (k, v) list"""

    itemChanged=Signal()

    def setColorList(self, colors: list) -> None:
        self.clear()
        for v, k in colors:
            pix = QPixmap(24, 24)
            pix.fill(QColor(v))
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            painter.drawRect(pix.rect())
            self.addItem(QIcon(pix), k, v)
            painter.end()
            
    def currentColor(self) -> QColor:
        return self.currentData(Qt.ItemDataRole.UserRole)
    
    def setCurrentColor(self, color: QColor) -> None:
        index = self.findData(color)
        self.setCurrentIndex(index if index >= 0 else 0)  # can be -1 on New

    def _get_modelDataStr(self) -> str|None:
        return self.currentData(Qt.ItemDataRole.UserRole)

    def _set_modelDataStr(self, data: str|None) -> None:
        index = self.findData(data)
        self.setCurrentIndex(index if index >= 0 else 0)  # can be -1 on New

    modelDataStr = Property(str, fget=_get_modelDataStr, fset=_set_modelDataStr, notify=itemChanged)


class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):

        def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex|QPersistentModelIndex) -> QSize:
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        lineEdit = self.lineEdit()
        if lineEdit is not None:
            lineEdit.setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        #palette = QApplication.palette(QPushButton())
        #palette.setBrush(QPalette.Base, palette.button())
        #self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        lineEdit = self.lineEdit()
        if lineEdit is not None:
            lineEdit.installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event: QResizeEvent) -> None:
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object: QObject, event: QEvent) -> bool:

        if object == self.lineEdit():
            if event.type() == QEvent.Type.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.Type.MouseButtonRelease:
                from PySide6.QtGui import QMouseEvent
                from PySide6.QtGui import QStandardItemModel
                mouse_event = event if isinstance(event, QMouseEvent) else None
                if mouse_event:
                    index = self.view().indexAt(mouse_event.pos())
                    model = self.model()
                    if isinstance(model, QStandardItemModel):
                        item = model.item(index.row())

                        if item.checkState() == Qt.CheckState.Checked:
                            item.setCheckState(Qt.CheckState.Unchecked)
                        else:
                            item.setCheckState(Qt.CheckState.Checked)
                return True
        return False

    def showPopup(self) -> None:
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self) -> None:
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event: QTimerEvent) -> None:
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self) -> None:
        texts = []
        model = self.model()
        if isinstance(model, QStandardItemModel):
            for i in range(model.rowCount()):
                if model.item(i).checkState() == Qt.CheckState.Checked:
                    texts.append(model.item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        lineEdit = self.lineEdit()
        if lineEdit is not None:
            metrics = QFontMetrics(lineEdit.font())
            elidedText = metrics.elidedText(text, Qt.TextElideMode.ElideRight, lineEdit.width())
            lineEdit.setText(elidedText)

    def addItem(self, *args, **kwargs) -> None:
        """
        Overloaded addItem for CheckableComboBox.
        Matches QComboBox.addItem(self, str, Any = None) and QComboBox.addItem(self, QIcon, str, Any = None) signatures.
        """
        # Handle addItem(str, userData)
        if len(args) == 1 or (len(args) == 2 and not isinstance(args[0], QIcon)):
            text = args[0]
            userData = args[1] if len(args) > 1 else None
            item = QStandardItem()
            item.setText(text)
            if userData is None:
                item.setData(text, Qt.ItemDataRole.UserRole)
            else:
                item.setData(userData, Qt.ItemDataRole.UserRole)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            model = self.model()
            if isinstance(model, QStandardItemModel):
                model.appendRow(item)
        # Handle addItem(QIcon, str, userData)
        elif len(args) >= 2 and isinstance(args[0], QIcon):
            icon = args[0]
            text = args[1]
            userData = args[2] if len(args) > 2 else None
            item = QStandardItem()
            item.setIcon(icon)
            item.setText(text)
            if userData is None:
                item.setData(text, Qt.ItemDataRole.UserRole)
            else:
                item.setData(userData, Qt.ItemDataRole.UserRole)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            model = self.model()
            if isinstance(model, QStandardItemModel):
                model.appendRow(item)
        else:
            raise TypeError("Invalid arguments for addItem")

    # The addItemWithIcon method is now redundant and can be removed.

    def addItems(self, texts) -> None:
        # Overriding QComboBox.addItems(self, Iterable[str])
        # If you want to support datalist, use a separate method or call addItem in a loop externally.
        for text in texts:
            self.addItem(text)

    def currentData(self, role: int = Qt.ItemDataRole.UserRole) -> list[object]:
        # Return the list of selected items data for the given role
        res = []
        model = self.model()
        if isinstance(model, QStandardItemModel):
            for i in range(model.rowCount()):
                if model.item(i).checkState() == Qt.CheckState.Checked:
                    res.append(model.item(i).data(role))
        return res

    def deselectAll(self) -> None:
        model = self.model()
        if isinstance(model, QStandardItemModel):
            for i in range(model.rowCount()):
                model.item(i).setCheckState(Qt.CheckState.Unchecked)


class PasswordLineEdit(QLineEdit):
    """A QLineEdit that encrypt text"""

    textChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.setClearButtonEnabled(True)
        self.setPlaceholderText(_tr("controls", "Type the password here"))

    def _get_modelDataEncrypt(self) -> str:
        return string_encode(self.text())

    def _set_modelDataEncrypt(self, data: str) -> None:
        if data:
            self.setText(string_decode(data))

    modelDataEncrypt = Property(str, fget=_get_modelDataEncrypt, fset=_set_modelDataEncrypt, notify=textChanged)


class ColorSetComboBox(QComboBox):
    "A combobox with a predefined set of colors"

    currentColorChanged = Signal(QColor)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.colors = ((Qt.GlobalColor.transparent, _tr("Controls", "Transparent")),
                       (Qt.GlobalColor.black, _tr("Controls", "Black")),
                       (Qt.GlobalColor.red, _tr("Controls", "Red")),
                       (Qt.GlobalColor.darkRed, _tr("Controls", "Dark red")),
                       (Qt.GlobalColor.green, _tr("Controls", "Green")),
                       (Qt.GlobalColor.darkGreen, _tr("Controls", "Dark green")),
                       (Qt.GlobalColor.blue, _tr("Controls", "Blue")),
                       (Qt.GlobalColor.darkBlue, _tr("Controls", "Dark blue")),
                       (Qt.GlobalColor.cyan, _tr("Controls", "Cyan")),
                       (Qt.GlobalColor.darkCyan, _tr("Controls", "Dark cyan")),
                       (Qt.GlobalColor.magenta, _tr("Controls", "Magenta")),
                       (Qt.GlobalColor.darkMagenta, _tr("Controls", "Dark magenta")),
                       (Qt.GlobalColor.yellow, _tr("Controls", "Yellow")),
                       (Qt.GlobalColor.darkYellow, _tr("Controls", "Dark yellow")),
                       (Qt.GlobalColor.gray, _tr("Controls", "Gray")),
                       (Qt.GlobalColor.darkGray, _tr("Controls", "Dark gray")),
                       (Qt.GlobalColor.lightGray, _tr("Controls", "Light gray")),
                       (Qt.GlobalColor.white, _tr("Controls", "White")))
        self.qtColors = tuple((i[0] for i in self.colors))
        for c, d in self.colors:
            pix = QPixmap(32, 24)
            pix.fill(QColor(c))
            # painter = QPainter(pix)
            # painter.setRenderHint(QPainter.Antialiasing)
            # painter.setPen(QPen(Qt.black, 1))
            # r = pix.rect()
            # painter.drawRect(r)
            self.addItem(QIcon(pix), d, c)
            # painter.end()
        self.currentIndexChanged.connect(self.emitColor)
        
    def setCurrentColor(self, color: QColor) -> None:
        if color in self.qtColors:
            self.setCurrentIndex(self.qtColors.index(color))

    def emitColor(self, index: int) -> None:
        color = QColor(self.qtColors[self.currentIndex()])
        self.currentColorChanged.emit(color)

# End of file Control.py