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

"""Delegates

This module contains custom general delegates


"""

# standard library
from decimal import Decimal
from typing import Any, cast

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QBuffer
from PySide6.QtCore import QIODevice
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QEvent
from PySide6.QtCore import QLocale
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QSize
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QKeyEvent
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QColor
from PySide6.QtGui import QBrush
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget   
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QAbstractItemDelegate
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QItemDelegate
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QSpinBox
from PySide6.QtWidgets import QDoubleSpinBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QDateEdit
from PySide6.QtWidgets import QDateTimeEdit
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QStyleOptionButton
from PySide6.QtWidgets import QStyleOptionViewItem
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QColorDialog

# application modules
from App import session
from App import actionDefinition
from App.Core.Cryptography import string_encode
from App.Core.Cryptography import string_decode
from App.Database.AbstractModels.TableModel import QueryModel, TableModel
from App.Database.Setting import SettingClass
from App.Widget.Control import ColorComboBox
from App.Widget.Control import RelationalComboBox
from App.Widget.Dialog import SelectImageDialog



class GenericDelegate(QStyledItemDelegate):
    """A Delegate for view that automatically choose the editor type 
    based on the field type, and format the display of values"""

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem, 
              index: QModelIndex|QPersistentModelIndex) -> None:
        value = index.data(Qt.ItemDataRole.DisplayRole)
        styleOption: QStyleOptionViewItem = QStyleOptionViewItem(option)
        self.initStyleOption(styleOption, index)
        match value:
            case bool():
                styleOption.text = ''
            case int():
                styleOption.text = str(value)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            case QDate()|QDateTime()|QTime():
                styleOption.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
            case Decimal():
                styleOption.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            case _:
                styleOption.text = str(value or '')  # for null values
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        font = index.model().data(index, Qt.ItemDataRole.FontRole)
        if font:
            styleOption.font = font
        # call base class to draw the item with the modified style option
        super().paint(painter, styleOption, index)
        
    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QWidget:
        abstract_model = index.model()
        model = cast(QueryModel|TableModel, abstract_model)
        fieldType = cast(str, model.columns[index.column()][3])
        widget: QWidget|QSpinBox|QDateEdit|QDateTimeEdit|QDoubleSpinBox|QLineEdit
        match fieldType:
            case 'bool':  # must be checked before int (bool is subclass of int)
                widget = QWidget(parent)
            case 'int':
                widget = QSpinBox(parent)
                widget.setRange(0, 999999999)
            case 'date':
                widget = QDateEdit(parent)
                #widget.setToolTip('Inserire 01/01/0001 per indicare nessuna data')
                #widget.setDateRange(QDate(1, 1, 1), QDate(3000, 12, 31))
                #widget.setDisplayFormat('dd/MM/yyyy')
                #widget.setSpecialValueText(' ')
                # widget.setCalendarPopup(True)
            case 'datetime':
                widget = QDateTimeEdit(parent)
                # widget.setDisplayFormat('dd.MM.yyyy')
                #widget.setDateRange(QDate(2000, 1, 1), QDate(3000, 12, 31))
                # widget.setCalendarPopup(True)
            case 'decimal':
                widget = QDoubleSpinBox(parent)
                widget.setDecimals(2)
            case _: # all remaining types are considered stings
                widget = QLineEdit(parent)
        return widget

    def setEditorData(self, 
                      editor: QWidget, 
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        val = index.data()
        if val is None:
            return
        match editor:
            case QCheckBox() as cb:
                cb.setChecked(bool(val))
            case QSpinBox() as sb:
                sb.setValue(int(val))
            case QDateEdit() as de:
                de.setDate(val)
            case QDateTimeEdit() as dte:
                dte.setDateTime(val)
            case QDoubleSpinBox() as dsb:
                dsb.setValue(val)
            case QLineEdit() as le:
                le.setText(str(val))
            case QWidget():  # dummy editor for boolean fields, toggle value
                pass
            case _:
                raise TypeError(f"Unsupported editor type: {type(editor)}")

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        match editor:
            case QCheckBox():
                model.setData(index, editor.isChecked())
            case QSpinBox():
                model.setData(index, editor.value())
            case QDateEdit():
                #date = editor.date()
                #if date == QDate(1, 1, 1):
                    #date = None
                model.setData(index, editor.date())
            case QDateTimeEdit():
                model.setData(index, editor.dateTime())
            case QDoubleSpinBox():
                model.setData(index, editor.value())
            case QLineEdit():
                model.setData(index, editor.text())
            case QWidget()|None:  # dummy editor for boolean fields, toggle value
                current_val = index.data(Qt.ItemDataRole.EditRole)
                if current_val is None:
                    current_val = index.data(Qt.ItemDataRole.DisplayRole)
                model.setData(index, not bool(current_val), Qt.ItemDataRole.EditRole)
            case _:
                raise TypeError(f"Unsupported editor type: {editor}")
  

class ColorDelegate(QStyledItemDelegate):
    "Color delegate"

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QWidget:
        color = QColor(index.data(Qt.ItemDataRole.DisplayRole))
        if not color.isValid():
            color = QColor(Qt.GlobalColor.green)
        newcolor = QColorDialog.getColor(color, parent)
        if newcolor.isValid():
            index.model().setData(index, newcolor.name(), Qt.ItemDataRole.EditRole)
        return QWidget(parent)  # dummy editor, not used

    def paint(self,
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex) -> None:
        color = QColor(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        painter.save()
        styleOption = QStyleOptionViewItem(option)
        styleOption.backgroundBrush = QBrush(color)
        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                         styleOption,
                                         painter)
        painter.restore()


class ColorComboDelegate(QStyledItemDelegate):
    "Color delegate select from combobox"

    def __init__(self, parent: QWidget, colors: list[tuple[str, str]]) -> None:
        super().__init__(parent)
        self.colors = colors

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QWidget:
        color = QColor(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        if not color.isValid():
            color = QColor(Qt.GlobalColor.white)
        cb = ColorComboBox(parent)
        cb.setColorList(self.colors)
        return cb

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        color_editor = cast(ColorComboBox, editor)
        cbi = color_editor.findData(index.data())
        color_editor.setCurrentIndex(cbi if cbi >= 0 else 0)  # can be -1 on New

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        ccb = cast(ColorComboBox, editor)
        model.setData(index, ccb.currentData(Qt.ItemDataRole.UserRole), Qt.ItemDataRole.EditRole)

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        color = QColor(index.data(Qt.ItemDataRole.DisplayRole))
        painter.save()
        styleOption = QStyleOptionViewItem(option)
        styleOption.backgroundBrush = QBrush(color)
        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                         styleOption,
                                         painter)
        painter.restore()


class ImageDelegate(QStyledItemDelegate):
    "Image delegate"

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        "Paint a scaled pixmap"
        imageba = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        painter.save()
        if option.state & QStyle.StateFlag.State_Selected:  # selected
            if option.state & QStyle.StateFlag.State_Active:  # selected active
                painter.fillRect(option.rect, option.palette.highlight())
                option.backgroundBrush = option.palette.highlight()
            else:  # selected not active
                if option.features & QStyleOptionViewItem.ViewItemFeature.Alternate:
                    painter.fillRect(option.rect, option.palette.alternateBase())
                    option.backgroundBrush = option.palette.alternateBase()
                else:
                    painter.fillRect(option.rect, option.palette.base())
                    option.backgroundBrush = option.palette.base()
        else:  # not selected
            if option.features & QStyleOptionViewItem.ViewItemFeature.Alternate:
                painter.fillRect(option.rect, option.palette.alternateBase())
                option.backgroundBrush = option.palette.alternateBase()
            else:
                painter.fillRect(option.rect, option.palette.base())
                option.backgroundBrush = option.palette.base()
        if imageba:
            pix = QPixmap()
            pix.loadFromData(imageba)
            painter.drawPixmap(option.rect, pix, pix.rect())
        painter.restore()

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QWidget:
        dd = SelectImageDialog(parent)
        ba = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if ba:
            pix = QPixmap()
            pix.loadFromData(ba)
            dd.setImage(pix)
        if dd.exec_() == QDialog.DialogCode.Accepted:
            px = dd.getImage()
            ba = QByteArray()
            buf = QBuffer(ba)
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            if px:
                px.save(buf, "PNG")
            index.model().setData(index, ba, Qt.ItemDataRole.EditRole)
        return QWidget(parent)  # dummy editor, not used

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        imgdlg = cast(SelectImageDialog, editor)
        QStyledItemDelegate.setEditorData(self, imgdlg, index)


class HideTextDelegate(QStyledItemDelegate):
    "A delegate for (not) display text (password)"

    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(parent)
        self.text = text

    def paint(self, 
              painter: QPainter, 
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        "Paint a text string instead of model data"
        painter.save()
        if option.state & QStyle.StateFlag.State_Selected:  # selected
            if option.state & QStyle.StateFlag.State_Active:  # selected active
                painter.fillRect(option.rect, option.palette.highlight())
                option.backgroundBrush = option.palette.highlight()
            else:  # selected not active
                if option.features & QStyleOptionViewItem.ViewItemFeature.Alternate:
                    painter.fillRect(option.rect, option.palette.alternateBase())
                    option.backgroundBrush = option.palette.alternateBase()
                else:
                    painter.fillRect(option.rect, option.palette.base())
                    option.backgroundBrush = option.palette.base()
        else:  # not selected
            if option.features & QStyleOptionViewItem.ViewItemFeature.Alternate:
                painter.fillRect(option.rect, option.palette.alternateBase())
                option.backgroundBrush = option.palette.alternateBase()
            else:
                painter.fillRect(option.rect, option.palette.base())
                option.backgroundBrush = option.palette.base()
        painter.drawText(option.rect,
                         Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter,
                         self.text)  # '\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF')
        painter.restore()

    def createEditor(self, parent, option, index):
        return None

    def setEditorData(self, editor, index):
        return

    def setModelData(self, editor, model, index):
        return


class BooleanDelegate(QStyledItemDelegate):
    """A delegate for boolean values with a checkbox centered in the cell
    Actually obsolete, because the same can be achieved with GenericDelegate
    that used model data end check state role"""

    def createEditor(self, 
                     parent: QWidget, 
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QWidget:
        "Important, otherwise an editor is created if the user clicks in this cell."
        return QWidget(parent)  # dummy editor, not used

    def paint(self, 
          painter: QPainter,
          option: QStyleOptionViewItem,
          index: QModelIndex|QPersistentModelIndex) -> None:
        "Draw a checkbox centered in the cell, with state based on the model data and enabled/disabled based on the item flags"
        opts = QStyleOptionViewItem(option)
        self.initStyleOption(opts, index)
        painter.save()
        # draw background (selection, hover, alternate background)
        QApplication.style().drawPrimitive(
            QStyle.PrimitiveElement.PE_PanelItemViewItem, opts, painter, opts.widget
        )
        # configure CheckBox
        checkBoxStyleOption = QStyleOptionButton()
        checkBoxStyleOption.rect = self.getCheckBoxRect(opts)
        # sync state (Enabled, Selected, etc.)
        checkBoxStyleOption.state = opts.state & ~QStyle.StateFlag.State_HasFocus  # remove focus state to avoid dotted border
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        if bool(val):
            checkBoxStyleOption.state |= QStyle.StateFlag.State_On
        else:
            checkBoxStyleOption.state |= QStyle.StateFlag.State_Off
        # if not modifyable add ReadOnly
        if not (index.flags() & Qt.ItemFlag.ItemIsEditable):
            checkBoxStyleOption.state |= QStyle.StateFlag.State_ReadOnly
        # draw CheckBox
        QApplication.style().drawControl(
            QStyle.ControlElement.CE_CheckBox,
            checkBoxStyleOption,
            painter
        )
        painter.restore()

    def getCheckBoxRect(self, option: QStyleOptionViewItem) -> QRect:
        checkBoxStyleOption = QStyleOptionButton()
        checkBoxRect = QApplication.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, checkBoxStyleOption, None)
        checkBoxPoint = QPoint(option.rect.x() + option.rect.width() // 2 - checkBoxRect.width() // 2,
                               option.rect.y() + option.rect.height() // 2 - checkBoxRect.height() // 2)
        return QRect(checkBoxPoint, checkBoxRect.size())

    def editorEvent(self, 
                    event: QEvent, 
                    model: QAbstractItemModel, 
                    option: QStyleOptionViewItem, 
                    index: QModelIndex|QPersistentModelIndex
                    ) -> bool:
    
        if not (index.flags() & Qt.ItemFlag.ItemIsEditable) or not (index.flags() & Qt.ItemFlag.ItemIsEnabled):
            return False

        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, QEvent.Type.MouseButtonDblClick):
            mouse_event = cast(QMouseEvent, event) # Importa cast da typing per Mypy
            
            if mouse_event.button() != Qt.MouseButton.LeftButton or \
            not self.getCheckBoxRect(option).contains(mouse_event.pos()):
                return False
            
            if event.type() == QEvent.Type.MouseButtonRelease:
                self.setModelData(None, model, index)
                return True
            
            # avoid double toggle on double click
            return True 

        elif event.type() == QEvent.Type.KeyPress:
            key_event = cast(QKeyEvent, event)
            if key_event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Select):
                self.setModelData(None, model, index)
                return True

        return False

    def setModelData(self, editor, model, index):
        current_val = index.data(Qt.ItemDataRole.EditRole)
        if current_val is None:
            current_val = index.data(Qt.ItemDataRole.DisplayRole)
        model.setData(index, not bool(current_val), Qt.ItemDataRole.EditRole)


class ItemsDelegate(QStyledItemDelegate):
    "A delegate (combo box) for choose a value from a list"

    def __init__(self, parent: QWidget, items) -> None:
        super().__init__(parent)
        self.data = items

    def sizeHint(self, 
                 option: QStyleOptionViewItem,
                 index: QModelIndex|QPersistentModelIndex
                 ) -> QSize:
        # ignore flags, add a little more margin
        size = QApplication.fontMetrics().size(0, str(self.data[index.data()]))
        size.setWidth(size.width() + 10)
        return size

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        opt = QStyleOptionViewItem(option)
        opt.text = index.data()
        opt.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        super().paint(painter, opt, index)

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QComboBox:
        cb = QComboBox(parent)
        cb.addItems(self.data)
        return cb

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        cb = cast(QComboBox, editor)
        cb.setCurrentText(index.data())

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        cb = cast(QComboBox, editor)
        model.setData(index, cb.currentText())


class PrintersDelegate(ItemsDelegate):
    "A delegate (combo box) for choose a printer of the current computer"

    def __init__(self, parent: QWidget, items: list, hostName: str) -> None:
        super().__init__(parent, items)
        self.hostName = hostName

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QComboBox:
        # avoid editing of printers of another computer
        # computer name must be in the preceeding column of the same row
        if index.model().index(index.row(), index.column() - 1).data() != self.hostName:
            return QComboBox(parent)
        cb = QComboBox(parent)
        cb.addItems(self.data)
        return cb


class RelationDelegate(QStyledItemDelegate):
    "A delegate (combo box) for referenced table fields"

    def __init__(self, parent: QWidget, function) -> None:
        super().__init__(parent)
        self.function = function
        self.updateItems()

    def updateItems(self) -> None:
        self.data = dict(self.function())

    def sizeHint(self, 
                 option: QStyleOptionViewItem,
                 index: QModelIndex|QPersistentModelIndex
                 ) -> QSize:
        # ignore flags, add a little more margin
        size = QApplication.fontMetrics().size(0, str(self.data.get(index.data())))
        size.setWidth(size.width() + 10)
        return size

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        "Paint the delegate"
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = self.data.get(index.data()) or '---'  # for item actually unavailable
        opt.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        painter.save()
        if option.state & QStyle.StateFlag.State_Selected:  # selected
            if option.state & QStyle.StateFlag.State_Active:  # selected active
                opt.backgroundBrush = option.palette.highlight()
        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                         opt,
                                         painter)
        painter.restore()

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex) -> QComboBox:
        self.updateItems()
        cb = QComboBox(parent)
        for k, v in self.data.items():
            cb.addItem(v, k)
        return cb

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex) -> None:
        if not index.data():
            return None
        cb = cast(QComboBox, editor)
        cb.setCurrentText(self.data.get(index.data()) or '')

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        cb = cast(QComboBox, editor)
        model.setData(index, cb.currentData())

    def getRelationData(self, index: QModelIndex) -> Any:
        return self.data.get(index.data())


class IntegerDelegate(QStyledItemDelegate):
    "A delegate for integer values"

    def __init__(self, parent: QWidget, bold=False):
        super().__init__(parent)
        self.bold = bold

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex) -> None:
        # first use EditRole (actual value, user inserted) then DisplayRole (formatted value)
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        option.text = str(val)
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        if self.bold:
            option.font.setWeight(QFont.Weight.Bold)
        if index.data(Qt.ItemDataRole.FontRole):
            if index.data(Qt.ItemDataRole.FontRole).bold():
                option.font.setWeight(QFont.Weight.Bold)
        super().paint(painter, option, index)
        
    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QSpinBox:
        sb = QSpinBox(parent)
        sb.setMaximum(999999999)
        return sb

    def setEditorData(self, 
                      editor: QWidget, 
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        sb = cast(QSpinBox, editor)
        sb.setValue(index.data())

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        sb = cast(QSpinBox, editor)
        model.setData(index, sb.value())


class DecimalDelegate(QStyledItemDelegate):
    "A delegate for decimal values or currency values"

    def __init__(self, parent: QWidget, prec=0, maximum=999.9, currency=False, bold=False):
        super().__init__(parent)
        self.prec = prec
        self.maximum = maximum
        self.currency = currency
        self.bold = bold

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem, 
              index: QModelIndex|QPersistentModelIndex) -> None:
        # first use EditRole (actual value, user inserted) then DisplayRole (formatted value)
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        if self.currency:
            option.text = session['qlocale'].toCurrencyString(float(index.data() or 0.0), ' ')  # no currency symbol
        else:
            option.text = session['qlocale'].toString(float(index.data() or 0.0), 'f', self.prec)  # can be null on insert row
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        if self.bold:
            option.font.setWeight(QFont.Weight.Bold)
        if index.data(Qt.ItemDataRole.FontRole):
            if index.data(Qt.ItemDataRole.FontRole).bold():
                option.font.setWeight(QFont.Weight.Bold)
        super().paint(painter, option, index)

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex) -> QDoubleSpinBox:
        sb = QDoubleSpinBox(parent)
        sb.setDecimals(self.prec)
        sb.setMaximum(self.maximum)
        return sb

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        dsb = cast(QDoubleSpinBox, editor)
        dsb.setValue(index.data())

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex) -> None:
        dsb = cast(QDoubleSpinBox, editor)
        model.setData(index, dsb.value())


class QuantityDelegate(DecimalDelegate):
    "Delegate for quantity values"

    def __init__(self, parent: QWidget, bold=False):
        setting = SettingClass()
        super().__init__(parent,
                         setting['quantity_decimal_places'],
                         maximum=99999.9,
                         currency=False,
                         bold=bold)


class AmountDelegate(DecimalDelegate):
    "Delegate for currency values"

    def __init__(self, parent: QWidget):
        super().__init__(parent,
                         prec=2,
                         maximum=99999.9,
                         currency=True)


class NewStockDelegate(QuantityDelegate):
    """A delegate for insert new stock on stock_summary and recalc loads and balance
    """
    LOAD, UNLOAD, STOCK, ORDERED, AVAILABLE = range(3, 8)
    
    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        option.text = ""
        super().paint(painter, option, index)

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if index.data() is None:
            return
        model = index.model()
        stockIndex = model.createIndex(index.row(), self.STOCK)
        newLoads = model.data(stockIndex) or 0.0
        dsb = cast(QDoubleSpinBox, editor)
        dsb.setValue(newLoads)

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        dsb = cast(QDoubleSpinBox, editor)
        # update loads
        loadsIndex = model.createIndex(index.row(), self.LOAD)
        unloadsIndex = model.createIndex(index.row(), self.UNLOAD)
        unloads = model.data(unloadsIndex) or Decimal(0)
        model.setData(loadsIndex, Decimal(dsb.value()) + unloads)
        # update stock
        stockIndex = model.createIndex(index.row(), self.STOCK)
        stock = Decimal(dsb.value())
        model.setData(stockIndex, stock)
        # update available
        orderedIndex = model.createIndex(index.row(), self.ORDERED)
        ordered = model.data(orderedIndex) or Decimal(0)
        availableIndex = model.createIndex(index.row(), self.AVAILABLE)
        model.setData(availableIndex, stock - ordered)


class StockLevelDelegate(QuantityDelegate):

    def __init__(self, parent: QWidget, warning=10, critical=5):
        super().__init__(parent)
        self.warning_level = warning
        self.critical_level = critical
        self.normalColor = QColor('Green')
        self.warningColor = QColor('Yellow')
        self.criticalColor = QColor('Orange')
        self.outOfStockColor = QColor('Red')

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        # first use EditRole (actual value, user inserted) then DisplayRole (formatted value)
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        option.text = session['qlocale'].toString(float(val), 'f', self.prec)  # can be null on insert row
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        if self.bold:
            option.font.setWeight(QFont.Weight.Bold)
        if index.data(Qt.ItemDataRole.FontRole):
            if index.data(Qt.ItemDataRole.FontRole).bold():
                option.font.setWeight(QFont.Weight.Bold)
        super().paint(painter, option, index)
        

class BoldDelegate(QStyledItemDelegate):
    "A delegate for bold rendering of text"

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        option.font.setWeight(QFont.Weight.Bold)
        super().paint(painter, option, index)


class ActionDelegate(QStyledItemDelegate):
    "A custom delegate for action code/description"

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.action = {k: actionDefinition[k][0] for k in actionDefinition}

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        # first use EditRole (actual value, user inserted) then DisplayRole (formatted value)
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        option.text = str(val)
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        if index.data(Qt.ItemDataRole.FontRole):
            if index.data(Qt.ItemDataRole.FontRole).bold():
                option.font.setWeight(QFont.Weight.Bold)
        super().paint(painter, option, index)

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QComboBox:
        "Important, otherwise an editor is created if the user clicks in this cell."
        cb = QComboBox(parent)
        for k in self.action:
            cb.addItem(self.action[k], k)
        return cb

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        cb = cast(QComboBox, editor)
        cb.setCurrentText(self.action.get(index.data()) or '')

    def setModelData(self, 
                     editor: QWidget, 
                     model: QAbstractItemModel, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        #print(editor.currentData())
        cb = cast(QComboBox, editor)
        model.setData(index, cb.currentData())


class PasswordDelegate(QStyledItemDelegate):
    "A delegate for read/write encrypted password"

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem, 
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        "Paint *** string instead of model data"
        # first use EditRole (actual value, user inserted) then DisplayRole (formatted value)
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        option.text = '\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF'
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        if self.bold:
            option.font.setWeight(QFont.Weight.Bold)
        if index.data(Qt.ItemDataRole.FontRole):
            if index.data(Qt.ItemDataRole.FontRole).bold():
                option.font.setWeight(QFont.Weight.Bold)
        super().paint(painter, option, index)
        
    def createEditor(self, 
                     parent: QWidget, 
                     option: QStyleOptionViewItem, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QLineEdit:
        le = QLineEdit(parent)
        le.setEchoMode(QLineEdit.EchoMode.Password)
        return le

    def setEditorData(self, 
                      editor: QWidget,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        le = cast(QLineEdit, editor)
        le.setText(string_decode(index.data()))

    def setModelData(self, 
                     editor: QWidget, 
                     model: QAbstractItemModel, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        le = cast(QLineEdit, editor)
        model.setData(index, string_encode(le.text()))


class GenericReadOnlyDelegate(QStyledItemDelegate):
    "Delegate for view with read only query model"

    def paint(self, 
              painter: QPainter, 
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex
              ) -> None:
        if not index.isValid():
            return
        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        styleOption = QStyleOptionViewItem(option)
        self.initStyleOption(styleOption, index)
        match value:
            case bool():  # must be checked before int (bool is subclass of int)
                styleOption.text = '\u26ab' if value else '\u26aa' #'\u2714' '\u2611' '\u2610'
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter
            case int():
                styleOption.text = str(value)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            case QDate()|QDateTime()|QTime():
                styleOption.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
            case Decimal():
                styleOption.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            case _:
                styleOption.text = str(value or '')  # for null values
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter

        font = index.model().data(index, Qt.ItemDataRole.FontRole)
        if font:
            styleOption.font = font
        painter.save()
        if option.state & QStyle.StateFlag.State_Selected:  # selected
            if option.state & QStyle.StateFlag.State_Active:  # selected active
                styleOption.backgroundBrush = option.palette.highlight()

        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                         styleOption,
                                         painter)
        painter.restore()

    def createEditor(self, parent, option, index):
        "Important, otherwise an editor is created if the user clicks in this cell."
        return None


class ReadOnlyDelegate(QStyledItemDelegate):
    "Read only delegate"

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex) -> QWidget:
        "Important, otherwise an editor is created if the user clicks in this cell."
        return QWidget(parent)
    
    
class TimeDelegate(QStyledItemDelegate):
    "A delegate for QTime rendering in text"

    def paint(self, 
              painter: QPainter, 
              option: QStyleOptionViewItem,
              index: QModelIndex|QPersistentModelIndex) -> None:
        if isinstance(index.data(), QTime):
            option.text = index.data().toString('HH:mm:ss')
        else:
            option.text = ''
        super().paint(painter, option, index)
        