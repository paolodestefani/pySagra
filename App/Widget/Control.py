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
from decimal import Decimal
from typing import Callable
from typing import Any

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
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import QEvent
from PySide6.QtCore import QObject
from PySide6.QtCore import QTimerEvent
from PySide6.QtCore import QRectF
from PySide6.QtGui import QKeyEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QPaintEvent
from PySide6.QtGui import QResizeEvent
from PySide6.QtGui import QBrush
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtGui import QColor
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPen
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetrics
from PySide6.QtGui import QStandardItemModel
from PySide6.QtGui import QStandardItem
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QDoubleSpinBox
from PySide6.QtWidgets import QDateTimeEdit
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QDataWidgetMapper
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QStyleOptionButton
from PySide6.QtWidgets import QStyle
from PySide6.QtCore import QRect
from PySide6.QtGui import QLinearGradient
from PySide6.QtNetwork import QHostInfo

# application modules
from App import currentIcon
from App.Common.L10n import _tr


class LabelImage(QLabel):
    "A QLabel used for display/store and return an image"

    imageChanged=Signal()

    def _get_imageBytearray(self) -> QByteArray|None:
        "Return imgage bytearray from label"
        ba = QByteArray()
        buf = QBuffer(ba)
        buf.open(QIODeviceBase.OpenModeFlag.WriteOnly)
        if self.pixmap().save(buf, "PNG"):
            buf.close()
            return ba
        return None

    def _set_imageBytearray(self, ba: QByteArray|None) -> None:
        "Set/display an image on label"
        if ba and not ba.isEmpty():
            pix = QPixmap()
            if pix.loadFromData(ba):
                super().setPixmap(pix)
            else:
                super().clear()
                self.setText(_tr("Controls", "INVALID IMAGE"))
        else:
            super().clear()
            self.setText(_tr("Controls", "NO IMAGE"))
        self.imageChanged.emit()

    imageBytearray = Property(QByteArray, 
                              fget=_get_imageBytearray,
                              fset=_set_imageBytearray,
                              notify=imageChanged,
                              user=True)

    def clear(self) -> None:
        "Clear the label"
        super().clear()
        self.setText(_tr("Controls", "NO IMAGE"))
        self.imageChanged.emit()
        

class SpinBoxDecimal(QDoubleSpinBox):
    "Custom doublespinbox for show decimal values with None option"

    customValueChanged=Signal(Decimal)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setSpecialValueText("--")
        self.setMinimum(-999999999999.99) # specialValueText is shown when value = minimum
        self.setRange(-999999999999.99, 999999999999.99)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)

    def _get_modelDataDecimal(self) -> Decimal|None:
        if self.value() == self.minimum():
            return None
        else:
            return Decimal(str(self.value())) # float to string to decimal for keep rounded values

    def _set_modelDataDecimal(self, value: Decimal|None) -> None:
        if value is None:
            self.setValue(self.minimum())
        else:
            self.setValue(float(value))

    modelDataDecimal = Property(object,
                                fget=_get_modelDataDecimal,
                                fset=_set_modelDataDecimal,
                                notify=customValueChanged,
                                user=True)


class SpinBoxInt(QSpinBox):
    "Custom spinbox for show integer with None option"

    customValueChanged=Signal(int)

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

    modelDataInt = Property(object,
                            fget=_get_modelDataInt,
                            fset=_set_modelDataInt,
                            notify=customValueChanged,
                            user=True)


class CheckBox(QCheckBox):
    "Custom checkbox for boolean with None option"

    customCheckStateChanged=Signal()

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
    
    modelDataState = Property(object,
                              fget=_get_modelDataState, 
                              fset=_set_modelDataState,
                              notify=customCheckStateChanged,
                              user=True)


class DateEdit(QLineEdit):
    "A line edit for date input with None option"

    dateChanged=Signal()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setInputMask('00/00/0000;_')

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

    modelDataDate = Property(QDate, 
                             fget=_get_modelDataDate,
                             fset=_set_modelDataDate, 
                             notify=dateChanged, 
                             user=True)


class DateTimeEdit(QDateTimeEdit):
    "A QDateTimeEdit class with None option"

    customValueChanged = Signal(QDateTime) 

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setSpecialValueText(" ")
        self.setMinimumDateTime(QDateTime(1800, 1, 1, 0, 0, 0))
        self.dateTimeChanged.connect(self.customValueChanged.emit)

    def _get_modelDataDateTime(self) -> QDateTime:
        if self.dateTime() <= self.minimumDateTime():
            return QDateTime() 
        return self.dateTime()

    def _set_modelDataDateTime(self, value: QDateTime|None) -> None:
        self.blockSignals(True)
        if value is None or not value.isValid() or value.isNull():
            self.setDateTime(self.minimumDateTime())
        else:
            self.setDateTime(value)
        self.blockSignals(False)
        self.customValueChanged.emit(self.dateTime())

    modelDataDateTime = Property(QDateTime, 
                                 fget=_get_modelDataDateTime, 
                                 fset=_set_modelDataDateTime, 
                                 notify=customValueChanged, 
                                 user=True)
    

class RelationalComboBox(QComboBox):
    """QComboBox that uses userData + itemText for key-value foreign key
    or set/get items from a (k, v) list. Can be None. If available can use icon too"""

    itemChanged=Signal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.sqlFunc: Callable|None = None
        self.nullable = False
        self.currentIndexChanged.connect(self._on_index_changed)

    def _on_index_changed(self, index: int) -> None:
        # If the index is -1 it means that the combo has been emptied by code (e.g. clear)
        # We don't need to output the signal to the mapper in this case
        if index != -1:
            self.itemChanged.emit(index)

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
        if data:
            self._addItems([(None, None)] + data if self.nullable else data)

    def setItemList(self, items: list) -> None:
        self.blockSignals(True)
        self.clear()
        self._addItems(items)
        self.blockSignals(False)

    def _addItems(self, items: list) -> None:
        "Add (value, text) or (icon, value, text) items"
        for item in items:
            if len(item) == 3:
                icon, value, text = item
                self.addItem(icon, text, value)
            else:
                value, text = item
                self.addItem(text, value)

    def showPopup(self) -> None:
        "Update key/value list before show popup request"
        if self.sqlFunc:
            self.blockSignals(True)
            current = self.currentData()
            self.updateList()
            # updateList moves to the first item: go back to the selected one
            self.setCurrentIndex(self.findData(current))
            self.blockSignals(False)
        super().showPopup()

    def _get_modelDataInt(self) -> int|None:
        val = self.currentData(Qt.ItemDataRole.UserRole)
        return int(val) if val is not None else None # must return a number even if null

    def _set_modelDataInt(self, data: int|None) -> None:
        if data is None:
            self.setCurrentIndex(0) # set to null item if nullable, otherwise to first item
            return
        index = self.findData(data)
        self.setCurrentIndex(index if index >= 0 else 0)


    modelDataInt = Property(int, # NO object, break datawidgetmapper mapping
                            fget=_get_modelDataInt,
                            fset=_set_modelDataInt,
                            notify=itemChanged,
                            user=False)

    def _get_modelDataStr(self) -> str|None:
        val = self.currentData(Qt.ItemDataRole.UserRole)
        return str(val) if val is not None else "" # must return a string even if null

    def _set_modelDataStr(self, data: str|None) -> None:
        if data is None:
            self.setCurrentIndex(0) # set to null item if nullable, otherwise to first item
            return
        index = self.findData(data, Qt.ItemDataRole.UserRole, Qt.MatchFlag.MatchExactly|Qt.MatchFlag.MatchCaseSensitive)
        self.setCurrentIndex(index if index >= 0 else 0) # can be -1 on New

    modelDataStr = Property(str, # NO object, break datawidgetmapper mapping
                            fget=_get_modelDataStr, 
                            fset=_set_modelDataStr, 
                            notify=itemChanged,
                            user=True)
        

class DataWidgetMapper(QDataWidgetMapper):
    """
    Optimized version of a QDataWidgetMapper: Uses standard behavior but forces immediate commit
    for widgets that don't lose focus correctly on macOS.
    """
    
    def addMapping(self, widget: QWidget, section: int, propertyName: QByteArray|bytes|bytearray|memoryview|None = None) -> None:
        if propertyName is None:
            super().addMapping(widget, section)
        else:
            super().addMapping(widget, section, propertyName)
        
        delegate = self.itemDelegate()
        
        if isinstance(widget, QComboBox):
            widget.activated.connect(lambda: delegate.commitData.emit(widget))
            
        elif isinstance(widget, QCheckBox):
            # this forces the commit immediatly for checkboxes, 
            # which otherwise on macOS would not lose focus and commit until another widget is focused
            widget.clicked.connect(lambda: delegate.commitData.emit(widget))


class ColorComboBox(QComboBox):
    """A QComboBox compatible with QDataWidgetMapper and psycopg.
    Accepts QColor/QColorConstants internally but communicates with the 
    outside (Property) via hex strings to match database expectations."""

    itemChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Fixed TypeError issue using lambda in currentIndexChanged connection by defining a separate method
        self.currentIndexChanged.connect(lambda index: self.itemChanged.emit())

    def setColorList(self, colors: list[tuple[Any, str]]) -> None:
        """Receives a list of tuples (color, color_name), where color can be a 
        hex string or a QColor/QColorConstants, and populates the combo box with colored icons."""
        self.clear()
        
        # Define a fixed corner radius for the color icons
        corner_radius = 5.0 
        
        for color_input, name in colors:
            color = QColor(color_input)
            if not color.isValid():
                continue
            # 1. create an empty pixmap with transparent background
            pix = QPixmap(24, 24)
            pix.fill(Qt.GlobalColor.transparent)
            # 2. initialize a QPainter to draw on the pixmap
            painter = QPainter(pix)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            # 3. Set the fill color and light black border
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            # 4. Draw the rounded rectangle
            # We use 0.5 as offset to avoid the 1px border from being cut off
            rect = QRectF(0.5, 0.5, 23.0, 23.0)
            painter.drawRoundedRect(rect, corner_radius, corner_radius)
            painter.end()
            
            # save the color in userData for later retrieval and matching with database values
            self.addItem(QIcon(pix), name, color)

            
    def currentColor(self) -> QColor | None:
        """Returns the currently selected QColor object"""
        return self.currentData(Qt.ItemDataRole.UserRole)
    
    def setCurrentColor(self, color_input: Any) -> None:
        """Sets the current color accepting a hex string or QColor"""
        color = QColor(color_input)
        index = self.findData(color)
        self.setCurrentIndex(index if index >= 0 else 0)

    # --- data binding methods for QDataWidgetMapper --- #

    def _get_modelDataStr(self) -> str:
        """
        Extracts the current color and returns it as a hex string used by psycopg.
        If no valid color is selected, returns an empty string.
        """
        color = self.currentColor()
        return color.name() if color and color.isValid() else ""

    def _set_modelDataStr(self, data: str | None) -> None:
        """
        Receives the string from the database via the mapper and updates the interface.
        """
        if data:
            self.setCurrentColor(data)
        else:
            self.setCurrentIndex(0)

    # this property is used by the mapper to get/set the color as a hex string, 
    # while the combo box internally works with QColor objects
    modelDataStr = Property(str, 
                            fget=_get_modelDataStr,
                            fset=_set_modelDataStr,
                            notify=itemChanged,
                            user=True)


class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):

        def sizeHint(self, 
                     option: QStyleOptionViewItem, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QSize:
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
                mouse_event = event if isinstance(event, QMouseEvent) else None
                if mouse_event:
                    index = self.view().indexAt(mouse_event.position().toPoint())
                    model = self.model()
                    if isinstance(model, QStandardItemModel):
                        item = model.item(index.row())
                        if item is None:  # click outside of the items
                            return True

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
                
    def setCheckedData(self, values) -> None:
        "Check the items whose data is in values, uncheck the others"
        wanted = {str(v) for v in values}
        model = self.model()
        if isinstance(model, QStandardItemModel):
            for i in range(model.rowCount()):
                item = model.item(i)
                checked = str(item.data(Qt.ItemDataRole.UserRole)) in wanted
                item.setCheckState(Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked)

        
class Button3D(QPushButton):
    """A QPushButton painted with a 3D gradient and custom colors.
    Subclasses can change the base color with paintColor() and draw on top of
    the button with paintOverlay()"""

    def __init__(self,
                 parent: QWidget,
                 textColor: QColor|str = QColorConstants.Black,
                 backgroundColor: QColor|str = QColorConstants.Svg.lightgreen) -> None:
        super().__init__(parent)
        self.textColor = QColor(textColor)
        self.backgroundColor = QColor(backgroundColor)
        self.setMinimumWidth(65)

    def setTextColor(self, color: QColor|str) -> None:
        self.textColor = QColor(color)
        self.update()

    def setBackgroundColor(self, color: QColor|str) -> None:
        self.backgroundColor = QColor(color)
        self.update()

    def paintColor(self) -> QColor:
        "Return the base color of the gradient"
        return self.backgroundColor

    def paintOverlay(self, painter: QPainter, rect: QRect) -> None:
        "Draw on top of the button, rect is the visible area of the button"

    def paintEvent(self, event: QPaintEvent) -> None:
        "Draw the gradient, the border, the top edge light and the text"
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            option = QStyleOptionButton()
            self.initStyleOption(option)
            margin = 5
            rect = option.rect.adjusted(margin, margin, -margin, -margin)
            color = self.paintColor()
            pressed = bool(option.state & QStyle.StateFlag.State_Sunken)
            gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
            if pressed:
                gradient.setColorAt(0, color.darker(120))
                gradient.setColorAt(1, color.darker(110))
            else:
                gradient.setColorAt(0, color.lighter(115))
                gradient.setColorAt(0.5, color)
                gradient.setColorAt(1, color.darker(110))
            painter.setBrush(gradient)
            painter.setPen(QPen(color.darker(150), 1))
            painter.drawRoundedRect(rect, 6, 6)
            if self.isEnabled() and not pressed:
                painter.setPen(QPen(color.lighter(130), 1))
                painter.drawLine(rect.left() + 5, rect.top() + 1, rect.right() - 5, rect.top() + 1)
            painter.setPen(self.textColor)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, self.text())
            self.paintOverlay(painter, rect)


class ButtonSeat(Button3D):
    "A 3D button for seat selection in order dialog or seat map management"

    def __init__(self,
                 parent: QWidget,
                 text: str,
                 font: QFont,
                 textColor: str,
                 backgroundColor: str,
                 unavailable: bool) -> None:
        super().__init__(parent, textColor, backgroundColor)
        self.setText(text)
        self.setFont(font)
        self.setMinimumWidth(80)
        self.setMinimumHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.unavailable = unavailable


class ButtonItem(Button3D):
    """
    A custom QPushButton representing a menu item.
    Features automated color-coding based on stock thresholds and visual
    indicator overlays for item variants.
    All monetary values and quantity balances are kept strictly as integers 
    to guarantee flawless arithmetic operations without rounding anomalies.
    """
    
    def __init__(self, parent: QWidget, text: str, textColor: str, backgroundColor: str, setting: dict) -> None:
        super().__init__(parent, textColor, backgroundColor)

        self.setting = setting
        self.description = text or ''
        self.caption = self.description.replace(' ', '\n')
        
        # Property initialization
        self._price: int = 0    
        self._stockLevel: int = 0 
        self.id: int | None = None
        self.hasInventory: bool = False 
        self.hasVariants: bool = False
        self._showLevel: bool = False
        
        self._quantityDecs = self.setting.get('quantity_decimal_places', 0)
        self._priceDecs = self.setting.get('price_decimal_places', 0)
        self._qty_factor = 10 ** self._quantityDecs
        self._price_factor = 10 ** self._priceDecs
        
        # Font settings and structural constraints
        font_family = self.setting.get('order_list_font_family', 'Arial')
        font_size = int(self.setting.get('order_list_font_size', 11))
        self.setFont(QFont(font_family, font_size, QFont.Weight.Bold))
        # Variant indicator icon fallback logic
        self.variantIndicatorIcon = currentIcon['order_flag'].pixmap(25, 25) if 'order_flag' in currentIcon else QPixmap()
        
        # Standard palette initialization
        self.default_bg = self.backgroundColor
        self.default_text = self.textColor
        
        self._color_cache = {
            'warning_bg': QColor(self.setting.get('warning_background_color', '#ffaa00')),
            'warning_tx': QColor(self.setting.get('warning_text_color', '#000000')),
            'critical_bg': QColor(self.setting.get('critical_background_color', '#ff2200')),
            'critical_tx': QColor(self.setting.get('critical_text_color', '#ffffff')),
            'disabled_bg': QColor(self.setting.get('disabled_background_color', '#dcdcdc')),
            'disabled_tx': QColor(self.setting.get('disabled_text_color', '#888888'))
        }

        # Initialize the button text display
        self.update_button_text()

    # --- PROPERTIES ---

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, value: int):
        self._price = value

    @property
    def stockLevel(self) -> int:
        return self._stockLevel

    @stockLevel.setter
    def stockLevel(self, value: int):
        self._stockLevel = value 
        self.recalculate_state_and_colors()
        self.update_button_text()

    @property
    def showLevel(self) -> bool:
        return self._showLevel

    @showLevel.setter
    def showLevel(self, value: bool):
        """Intercepts view changes to trigger immediate UI redraws"""
        self._showLevel = bool(value)
        self.update_button_text()  
        self.update()              

    # --- CORE METHODS ---

    def recalculate_state_and_colors(self):
        """Evaluates integer stock level thresholds and shifts active styling parameters"""
        if not self.hasInventory:
            self.backgroundColor = self.default_bg
            self.textColor = self.default_text
            self.setEnabled(True)
            return

        current_level = self._stockLevel
        
        warning_limit = self.setting.get('warning_stock_level', 10) * self._qty_factor
        critical_limit = self.setting.get('critical_stock_level', 5) * self._qty_factor
        
        # State assignment drawing straight from the optimized color cache
        if current_level >= warning_limit:
            bc, tc = self.default_bg, self.default_text
            self.setEnabled(True)
        elif critical_limit < current_level < warning_limit:
            bc, tc = self._color_cache['warning_bg'], self._color_cache['warning_tx']
            self.setEnabled(True)
        elif 0 < current_level <= critical_limit:
            bc, tc = self._color_cache['critical_bg'], self._color_cache['critical_tx']
            self.setEnabled(True)
        else:
            bc, tc = self._color_cache['disabled_bg'], self._color_cache['disabled_tx']
            self.setEnabled(False)
            
        self.backgroundColor = bc
        self.textColor = tc
        self.update() # Safe scheduling for an asymmetrical canvas refresh

    def update_button_text(self):
        """Formats the label string completely outside the paint loop to prevent recursion"""
        if self.hasInventory and self.showLevel:
            # extract integer and fractional strings directly.
            # avoids floating-point precision loss and messy string stripping (.rstrip).
            int_part, dec_part = divmod(abs(self._stockLevel), self._qty_factor)
            sign = '-' if self._stockLevel < 0 else ''

            if dec_part == 0:
                level_str = f"{sign}{int_part}"
            else:
                # handle zero padding safely based on dynamic configurations (e.g., 5 with 2 decs -> "05")
                decimals = str(dec_part).zfill(self._quantityDecs).rstrip('0')
                level_str = f"{sign}{int_part}{QLocale().decimalPoint()}{decimals}"
                
            self.setText(f"{self.caption}\n({level_str})")
        else:
            self.setText(self.caption)

    # --- PAINTING ---

    def paintColor(self) -> QColor:
        return self.backgroundColor if self.isEnabled() else self._color_cache['disabled_bg']

    def paintOverlay(self, painter: QPainter, rect: QRect) -> None:
        "Draw the variant indicator"
        if self.hasVariants and not self.variantIndicatorIcon.isNull():
            painter.drawPixmap(QRect(rect.right() - 18, rect.top() - 2, 24, 24), self.variantIndicatorIcon)


class ButtonItemExample(Button3D):
    "A pushbutton for settings example of color change on stock level value"

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setText(_tr("Controls", "Example Item"))


class ButtonColor(ButtonItemExample):
    "A button for showing example of color"


class PasswordLineEdit(QLineEdit):
    "A custom lineEdit with show/hide password feature"
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        
        # initialize the icons
        self.show_light = QIcon(":/eye_off_light")
        self.hide_light = QIcon(":/eye_light")
        self.show_dark = QIcon(":/eye_off_dark")
        self.hide_dark = QIcon(":/eye_dark")
        # action
        self.password_action = QAction(self)
        self.password_action.setToolTip(_tr('PasswordLineEdit', 'Press to show/hide the password'))
        self.addAction(self.password_action, QLineEdit.ActionPosition.TrailingPosition)
        # initialize the graphics
        self.update_icon()
        # signal slot
        self.password_action.triggered.connect(self.toggle_password)

    def update_icon(self):
        """Choose the correct preloaded icon by crossing Theme and EchoMode"""
        # dark mode or light mode
        is_dark = QApplication.instance().styleHints().colorScheme() == Qt.ColorScheme.Dark
        is_password = self.echoMode() == QLineEdit.EchoMode.Password
        if is_dark:
            icon = self.show_dark if is_password else self.hide_dark
        else:
            icon = self.show_light if is_password else self.hide_light
        self.password_action.setIcon(icon)

    def toggle_password(self):
        # Inverts the state of the text
        if self.echoMode() == QLineEdit.EchoMode.Password:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)
        # update icon
        self.update_icon()
            
    def changeEvent(self, event):
        # If the operating system changes theme at runtime, update the icon on the fly
        if event.type() == event.Type.PaletteChange:
            self.update_icon()
        super().changeEvent(event)


class HostNameLineEdit(QLineEdit):
    """A custom lineEdit that sets hostname on request with dynamic theme icons"""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setEchoMode(QLineEdit.EchoMode.Normal)
        # icons
        self.arrow_light = QIcon(":/arrow_circle_left_light")
        self.arrow_dark = QIcon(":/arrow_circle_left_dark")
        # action
        self.hostname_action = QAction(self)
        self.hostname_action.setToolTip(_tr('HostNameLineEdit', 'Press to set the current host name'))
        self.addAction(self.hostname_action, QLineEdit.ActionPosition.TrailingPosition)
        
        self.update_icon()
        
        self.hostname_action.triggered.connect(self.set_hostname)

    def update_icon(self):
        """Selects the correct preloaded icon based on the active system theme"""
        is_dark = QApplication.instance().styleHints().colorScheme() == Qt.ColorScheme.Dark
        icon = self.arrow_dark if is_dark else self.arrow_light
        self.hostname_action.setIcon(icon)

    def set_hostname(self):
        self.setText(QHostInfo.localHostName())
            
    def changeEvent(self, event):
        # if the operating system changes its theme at runtime while the cell is open, update it on the fly.
        if event.type() == event.Type.PaletteChange:
            self.update_icon()
        super().changeEvent(event)
