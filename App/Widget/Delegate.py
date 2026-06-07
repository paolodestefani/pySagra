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
from typing import Any
from typing import cast

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QRectF
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
from PySide6.QtGui import QMouseEvent, QPen
from PySide6.QtGui import QKeyEvent
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from PySide6.QtGui import QColor
from PySide6.QtGui import QColorConstants
from PySide6.QtGui import QBrush
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget   
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QStyledItemDelegate
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
from App.Core.L10n import _tr
from App.Database.AbstractModels.TableModel import QueryModel, TableModel
from App.Database.Setting import Setting
from App.Widget.Control import ColorComboBox
from App.Widget.Dialog import SelectImageDialog


# class GenericDelegate(QStyledItemDelegate):
#     """A Delegate for view that automatically choose the editor type 
#     based on the field type, and format the display of values"""

#     def paint(self, 
#               painter: QPainter,
#               option: QStyleOptionViewItem, 
#               index: QModelIndex|QPersistentModelIndex) -> None:
#         styleOption: QStyleOptionViewItem = QStyleOptionViewItem(option)
#         self.initStyleOption(styleOption, index)
#         value = index.data(Qt.ItemDataRole.DisplayRole)
#         match value:
#             case bool():
#                  styleOption.text = ''
#             case int():
#                 styleOption.text = str(value)
#                 styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
#             case QDate()|QDateTime()|QTime():
#                 styleOption.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
#                 styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
#             case Decimal():
#                 styleOption.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
#                 styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
#             case _:
#                 styleOption.text = str(value or '')  # for null values
#                 styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
#         font = index.model().data(index, Qt.ItemDataRole.FontRole)
#         if font:
#             styleOption.font = font
#         # draw
#         widget = option.widget
#         style = widget.style() if widget else QApplication.style()
#         style.drawControl(QStyle.ControlElement.CE_ItemViewItem, styleOption, painter, widget)
        
#     def createEditor(self, 
#                      parent: QWidget,
#                      option: QStyleOptionViewItem,
#                      index: QModelIndex | QPersistentModelIndex
#                      ) -> QWidget:
#         abstract_model = index.model()
#         model = cast(QueryModel|TableModel, abstract_model)
#         fieldType = cast(str, model.columns[index.column()][3])
#         widget: QWidget | QSpinBox | QDateEdit | QDateTimeEdit | QDoubleSpinBox | QLineEdit | None
#         match fieldType:
#             case 'bool':  # must be checked before int (bool is subclass of int)
#                 widget = QWidget(parent)
#             case 'int':
#                 widget = QSpinBox(parent)
#                 widget.setRange(0, 999999999)
#             case 'date':
#                 widget = QDateEdit(parent)
#                 #widget.setToolTip('Inserire 01/01/0001 per indicare nessuna data')
#                 #widget.setDateRange(QDate(1, 1, 1), QDate(3000, 12, 31))
#                 #widget.setDisplayFormat('dd/MM/yyyy')
#                 #widget.setSpecialValueText(' ')
#                 # widget.setCalendarPopup(True)
#             case 'datetime':
#                 widget = QDateTimeEdit(parent)
#                 # widget.setDisplayFormat('dd.MM.yyyy')
#                 #widget.setDateRange(QDate(2000, 1, 1), QDate(3000, 12, 31))
#                 # widget.setCalendarPopup(True)
#             case 'decimal':
#                 widget = QDoubleSpinBox(parent)
#                 widget.setDecimals(2)
#             case _: # all remaining types are considered stings
#                 widget = QLineEdit(parent)
#         return widget

#     def setEditorData(self, 
#                       editor: QWidget, 
#                       index: QModelIndex|QPersistentModelIndex
#                       ) -> None:
#         val = index.data()
#         if val is None:
#             return
#         match editor:
#             case QCheckBox() as cb:
#                 cb.setChecked(bool(val))
#             case QSpinBox() as sb:
#                 sb.setValue(int(val))
#             case QDateEdit() as de:
#                 de.setDate(val)
#             case QDateTimeEdit() as dte:
#                 dte.setDateTime(val)
#             case QDoubleSpinBox() as dsb:
#                 dsb.setValue(val)
#             case QLineEdit() as le:
#                 le.setText(str(val))
#             case QWidget():  # dummy editor for boolean fields, toggle value
#                 pass
#             case _:
#                 raise TypeError(f"Unsupported editor type: {type(editor)}")

#     def setModelData(self, 
#                      editor: QWidget,
#                      model: QAbstractItemModel,
#                      index: QModelIndex|QPersistentModelIndex
#                      ) -> None:
#         match editor:
#             case QCheckBox():
#                 model.setData(index, editor.isChecked())
#             case QSpinBox():
#                 model.setData(index, editor.value())
#             case QDateEdit():
#                 #date = editor.date()
#                 #if date == QDate(1, 1, 1):
#                     #date = None
#                 model.setData(index, editor.date())
#             case QDateTimeEdit():
#                 model.setData(index, editor.dateTime())
#             case QDoubleSpinBox():
#                 model.setData(index, editor.value())
#             case QLineEdit():
#                 model.setData(index, editor.text())
#             case QWidget():  # dummy editor for boolean fields, toggle value
#                 current_val = index.data(Qt.ItemDataRole.EditRole)
#                 if current_val is None:
#                     current_val = index.data(Qt.ItemDataRole.DisplayRole)
#                 model.setData(index, not bool(current_val), Qt.ItemDataRole.EditRole)
#             case _:
#                 raise TypeError(f"Unsupported editor type: {editor}")
  


class GenericDelegate(QStyledItemDelegate):
    """A Delegate for view that automatically choose the editor type 
    based on the field type, and format the display of values"""

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt load the basic model data (including fonts, colors, and selection)
        super().initStyleOption(option, index)
        
        # retrieves the value to display
        value = index.data(Qt.ItemDataRole.DisplayRole)
        
        # format text, alignment, and native checkboxes based on data type
        match value:
            case bool():  # boolean check must precede int (bool is a subclass of int)
                option.text = ""
                option.features |= QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator
                option.checkState = Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
                option.displayAlignment = Qt.AlignmentFlag.AlignCenter
            case int():
                option.text = str(value)
                option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            case QDate() | QDateTime() | QTime():
                option.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
                option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            case Decimal():
                option.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
                option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            case _:
                option.text = str(value) if value is not None else ""
                option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QWidget:
        abstract_model = index.model()
        model = cast(QueryModel | TableModel, abstract_model)
        fieldType = cast(str, model.columns[index.column()][3])
        widget: QWidget | QSpinBox | QDateEdit | QDateTimeEdit|QDoubleSpinBox
        match fieldType:
            case 'bool':  
                # empty QWidget as placeholder: actual toggling is done on click
                return QWidget(parent)
            case 'int':
                widget = QSpinBox(parent)
                widget.setRange(0, 999999999)
                return widget
            case 'date':
                return QDateEdit(parent)
            case 'datetime':
                return QDateTimeEdit(parent)
            case 'decimal':
                widget = QDoubleSpinBox(parent)
                widget.setDecimals(2)
                widget.setRange(-999999999.0, 999999999.0) # Gestisce anche i negativi
                return widget
            case _: 
                return QLineEdit(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
            
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
                dsb.setValue(float(val))
            case QLineEdit() as le:
                le.setText(str(val))
            case QWidget():  
                pass
            case _:
                raise TypeError(f"Unsupported editor type: {type(editor)}")

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        match editor:
            case QCheckBox():
                model.setData(index, editor.isChecked(), Qt.ItemDataRole.EditRole)
            case QSpinBox():
                model.setData(index, editor.value(), Qt.ItemDataRole.EditRole)
            case QDateEdit():
                model.setData(index, editor.date(), Qt.ItemDataRole.EditRole)
            case QDateTimeEdit():
                model.setData(index, editor.dateTime(), Qt.ItemDataRole.EditRole)
            case QDoubleSpinBox():
                model.setData(index, editor.value(), Qt.ItemDataRole.EditRole)
            case QLineEdit():
                model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
            case QWidget():  
                # fixed getting the current value for the boolean toggle
                current_val = index.data(Qt.ItemDataRole.EditRole)
                if current_val is None:
                    current_val = index.data(Qt.ItemDataRole.DisplayRole)
                model.setData(index, not bool(current_val), Qt.ItemDataRole.EditRole)
            case _:
                raise TypeError(f"Unsupported editor type: {type(editor)}")

    
class ColorDelegate(QStyledItemDelegate):
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index) -> None:
        # retrieve color from model data, if invalid use white as default
        color_val = index.data(Qt.ItemDataRole.DisplayRole)
        color = QColor(color_val) if color_val else QColor(Qt.GlobalColor.white)
        
        painter.save()
        opts = QStyleOptionViewItem(option)
        self.initStyleOption(opts, index)
        # 1. remove text to avoid drawing it, we will draw only the colored rectangle
        opts.text = ""
        # 2. let the style draw the system background (handling selection and focus)
        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem, opts, painter)
        # 3. draw the colored rectangle if the color is valid (non-empty string)
        if color.isValid():
            # use antialiasing for smoother edges on the rounded rectangle
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            # same margin for all sides to create a gap between the colored rectangle and the cell borders
            margin = 3.0
            rect = QRectF(
                option.rect.x() + margin,
                option.rect.y() + margin,
                option.rect.width() - (margin * 2),
                option.rect.height() - (margin * 2)
            )
            # set the brush to fill the rectangle with the color and a pen for the border 
            # (optional, can be set to NoPen if no border is desired)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            # same corner radius of 4 pixels
            corner_radius = 4.0
            painter.drawRoundedRect(rect, corner_radius, corner_radius)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        # using MouseButtonRelease because it's the standard across Win/Mac
        # to avoid issues with MouseButtonDblClick that can cause double toggling of the color on double click
        if event.type() == QEvent.Type.MouseButtonRelease:
            if event.button() == Qt.MouseButton.LeftButton:
                current_str = index.data(Qt.ItemDataRole.DisplayRole)
                current_color = QColor(current_str) if current_str else QColor(Qt.GlobalColor.green)
                # open color dialog with current color as default
                new_color = QColorDialog.getColor(current_color, option.widget, _tr('Delegate', 'Select Color'))
                if new_color.isValid():
                    # update model with new color as hex string, using EditRole to store the actual value
                    model.setData(index, new_color.name(), Qt.ItemDataRole.EditRole)
                    return True
        return False

    def createEditor(self, parent, option, index):
        # mandatory return None to avoid creating an editor, we will handle editing in editorEvent
        return None


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
            color = QColor(QColorConstants.White)
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
            index: QModelIndex | QPersistentModelIndex
            ) -> None:
        
        color = QColor(index.data(Qt.ItemDataRole.DisplayRole))
        
        painter.save()
        # draw the default item view background (selection, hover, alternate background) without text
        styleOption = QStyleOptionViewItem(option)
        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                        styleOption,
                                        painter)
        
        # if color is valid, draw a filled rounded rectangle with the color, leaving a margin from the cell borders
        if color.isValid():
            # use antialiasing for smoother edges on the rounded rectangle
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            # define a margin of 3 pixels on all sides to create a gap between the colored rectangle and the cell borders
            margin = 3.0
            rect = QRectF(
                option.rect.x() + margin,
                option.rect.y() + margin,
                option.rect.width() - (margin * 2),
                option.rect.height() - (margin * 2)
            )
            # use the color for filling and a light black border (you can use Qt.PenStyle.NoPen if you don't want a border)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.GlobalColor.black, 1))
            # corner radius for the rounded rectangle
            corner_radius = 4.0
            painter.drawRoundedRect(rect, corner_radius, corner_radius)
            
        painter.restore()


class ImageDelegate(QStyledItemDelegate):
    "Image delegate"

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt draw the correct background (base, alternate, selected, active)
        super().initStyleOption(option, index)
        
        # get image binary data
        imageba = index.data(Qt.ItemDataRole.DisplayRole)
        
        # if the image exists, upload it and assign it as the option icon
        if imageba:
            pix = QPixmap()
            pix.loadFromData(imageba)
            # by passing the pixmap as an icon, Qt automatically scales and centers it in the cell
            option.icon = QIcon(pix)
            option.features |= QStyleOptionViewItem.ViewItemFeature.HasDecoration
            option.text = "" # hides any text to show only the image
            # remove the internal text margins that push the icon to the left
            option.decorationAlignment = Qt.AlignmentFlag.AlignCenter
            option.displayAlignment = Qt.AlignmentFlag.AlignCenter

    def createEditor(self,
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QWidget:
        dd = SelectImageDialog(parent)
        ba = index.data(Qt.ItemDataRole.DisplayRole)
        if ba:
            pix = QPixmap()
            pix.loadFromData(ba)
            dd.setImage(pix)
            
        if dd.exec() == QDialog.DialogCode.Accepted:
            px = dd.getImage()
            new_ba = QByteArray()
            buf = QBuffer(new_ba)
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            if px:
                px.save(buf, "PNG")
            index.model().setData(index, new_ba, Qt.ItemDataRole.EditRole)
            
        # We create a dummy QWidget, but never display it.
        # This is only to comply with the method signature required by PySide6 and Mypy.
        dummy = QWidget(parent)
        dummy.hide()
        return dummy


    # setEditorData and setModelData are NO longer needed and are removed altogether


class HideTextDelegate(QStyledItemDelegate):
    "A delegate for (not) display text (password)"

    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(parent)
        self.text = text

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt draw the correct background (base, alternate, selected, active)
        super().initStyleOption(option, index)
        
        # overwrite the actual text with the fixed string (e.g. 'HIDDEN TEXT')
        option.text = self.text
        
        # center text
        option.displayAlignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter

    def createEditor(self, 
                     parent: QWidget, 
                     option: QStyleOptionViewItem, 
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QWidget:
        # Returns an invisible widget to block editing
        dummy = QWidget(parent)
        dummy.hide()
        return dummy

     # setEditorData and setModelData are NO longer needed and are removed altogether



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

    def __init__(self, parent: QWidget, items: list[str]) -> None:
        super().__init__(parent)
        self.data = items

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt load the basic data from the model
        super().initStyleOption(option, index)
        
        # force text and alignment to the left
        val = index.data(Qt.ItemDataRole.DisplayRole)
        option.text = str(val) if val is not None else ""
        option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QSize:
        # retrieves the actual text in the cell to calculate the space needed
        val = index.data(Qt.ItemDataRole.DisplayRole)
        text = str(val) if val is not None else ""
        
        # calculate font size using the current option's fontMetrics (more accurate)
        size = option.fontMetrics.size(0, text)
        size.setWidth(size.width() + 10)
        return size

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QComboBox:
        cb = QComboBox(parent)
        cb.addItems(self.data)
        return cb

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
            
        if val is None:
            return
            
        cb = cast(QComboBox, editor)
        cb.setCurrentText(str(val))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        cb = cast(QComboBox, editor)
        model.setData(index, cb.currentText(), Qt.ItemDataRole.EditRole)


class PrintersDelegate(ItemsDelegate):
    "A delegate (combo box) for choose a printer of the current computer"

    def __init__(self, parent: QWidget, printers: list[str], hostName: str) -> None:
        super().__init__(parent, printers)
        self.hostName = hostName

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QComboBox:
        # prevent editing printers on another computer.
        # the computer name must appear in the previous column of the same line.
        row_host = index.model().index(index.row(), index.column() - 1).data()
        
        if row_host != self.hostName:
            # create a dummy widget and hide it immediately.
            # this stops editing in its tracks and leaves the data untouched.
            dummy = QComboBox(parent)
            dummy.hide()
            return dummy
            
        cb = QComboBox(parent)
        cb.addItems(self.data)
        return cb


class RelationDelegate(QStyledItemDelegate):
    "A delegate (combo box) for referenced table fields"

    def __init__(self, parent: QWidget, function) -> None:
        super().__init__(parent)
        self.function = function
        self.data: dict[Any, Any] = {}
        self.updateItems()

    def updateItems(self) -> None:
        self.data = dict(self.function())

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt load the basic data from the model
        super().initStyleOption(option, index)
        
        # retrieve the key (EditRole) and map it to the text description
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
            
        # sets the decoded text or a fallback if the key does not exist in the dictionary
        option.text = str(self.data.get(val, '---'))
        option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QSize:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
            
        text = str(self.data.get(val, '---'))
        
        # use the current fontMetrics option for pinpoint accuracy on the active font
        size = option.fontMetrics.size(0, text)
        size.setWidth(size.width() + 10)
        return size

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex) -> QComboBox:
        self.updateItems()
        cb = QComboBox(parent)
        for k, v in self.data.items():
            cb.addItem(str(v), k) # v is the description, k is the ID/key saved as userData
        return cb

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            return
            
        cb = cast(QComboBox, editor)
        # find the correct item by comparing the ID stored as UserData
        idx = cb.findData(val)
        if idx != -1:
            cb.setCurrentIndex(idx)
        else:
            cb.setCurrentText(str(self.data.get(val, '')))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        cb = cast(QComboBox, editor)
        # save the real ID (currentData) in the template, not the description string
        model.setData(index, cb.currentData(), Qt.ItemDataRole.EditRole)

    def getRelationData(self, index: QModelIndex) -> Any:
        val = index.data(Qt.ItemDataRole.EditRole)
        return self.data.get(val)


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

    def __init__(self, 
                 parent: QWidget,
                 prec: int      = 0, 
                 maximum: float = 999.9, 
                 currency: bool = False, 
                 bold: bool     = False
                 ) -> None:
        super().__init__(parent)
        self.prec = prec
        self.maximum = maximum
        self.currency = currency
        self.bold = bold

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt fill the option with the basic model data
        super().initStyleOption(option, index)
        # retrieve the raw numeric value
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        # format text if value exists
        if val is None:
            option.text = ""
        else:
            num_val = float(val)
            if self.currency:
                option.text = session['qlocale'].toCurrencyString(num_val, ' ')
            else:
                option.text = session['qlocale'].toString(num_val, 'f', self.prec)
        # apply alignment and visual styles
        option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        model_font = index.data(Qt.ItemDataRole.FontRole)
        if self.bold or (model_font and model_font.bold()):
            option.font.setBold(True)

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QWidget:
        sb = QDoubleSpinBox(parent)
        sb.setDecimals(self.prec)
        sb.setMaximum(self.maximum)
        return sb

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            return
        dsb = cast(QDoubleSpinBox, editor)
        dsb.setValue(float(val))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        dsb = cast(QDoubleSpinBox, editor)
        model.setData(index, dsb.value(), Qt.ItemDataRole.EditRole)


class QuantityDelegate(DecimalDelegate):
    "Delegate for quantity values"

    def __init__(self, parent: QWidget, bold: bool = False):
        setting = Setting()
        prec: int = setting['quantity_decimal_places']
        super().__init__(parent,
                         prec,
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
    """A delegate for insert new stock on stock_summary and recalc loads and balance"""
    
    LOAD, UNLOAD, STOCK, ORDERED, AVAILABLE = range(3, 8)
    
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt fill the option with the basic model data
        super().initStyleOption(option, index)
        # keeps the cell visually blank when not in edit mode
        option.text = ""        

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            return
            
        model = index.model()
        stock_index = model.index(index.row(), self.STOCK)
        
        # retrieve the value using EditRole and maintain consistency with Decimal/float
        stock_data = model.data(stock_index, Qt.ItemDataRole.EditRole)
        new_loads = float(stock_data) if stock_data is not None else 0.0
        
        dsb = cast(QDoubleSpinBox, editor)
        dsb.setValue(new_loads)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        dsb = cast(QDoubleSpinBox, editor)
        editor_value = dsb.value()
        
        stock_diff = Decimal(str(editor_value))
        
        # 1. Update loads
        unloads_index = model.index(index.row(), self.UNLOAD)
        unloads_data = model.data(unloads_index, Qt.ItemDataRole.EditRole)
        unloads = Decimal(str(unloads_data)) if unloads_data is not None else Decimal('0')
        
        loads_index = model.index(index.row(), self.LOAD)
        model.setData(loads_index, stock_diff + unloads, Qt.ItemDataRole.EditRole)
        
        # 2. Update stock
        stock_index = model.index(index.row(), self.STOCK)
        model.setData(stock_index, stock_diff, Qt.ItemDataRole.EditRole)
        
        # 3. Update availability
        ordered_index = model.index(index.row(), self.ORDERED)
        ordered_data = model.data(ordered_index, Qt.ItemDataRole.EditRole)
        ordered = Decimal(str(ordered_data)) if ordered_data is not None else Decimal('0')
        
        available_index = model.index(index.row(), self.AVAILABLE)
        model.setData(available_index, stock_diff - ordered, Qt.ItemDataRole.EditRole)


class StockLevelDelegate(QuantityDelegate):
    """A delegate for stock level with color based on quantity (green, orange, red, gray)"""

    def __init__(self, parent: QWidget, warning=10, critical=5, bold=True):
        super().__init__(parent, bold=bold)
        self.warning_level = warning
        self.critical_level = critical
        self.normalColor = QColorConstants.DarkGreen
        self.warningColor = QColorConstants.Svg.orange
        self.criticalColor = QColorConstants.Red
        self.outOfStockColor = QColorConstants.Gray

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt fill the option with the basic model data
        super().initStyleOption(option, index)
        
        # retrieve and validate the numeric value
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        
        try:
            num_val = float(val) if val is not None else 0.0
        except (ValueError, TypeError):
            num_val = 0.0

        # format text
        option.text = session['qlocale'].toString(num_val, 'f', self.prec)
        
        # alignment and font
        option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        
        model_font = index.data(Qt.ItemDataRole.FontRole)
        if self.bold or (model_font and model_font.bold()):
            option.font.setBold(True)

        # assign colors to the palette based on quantity
        # always set selected text to white (HighlightedText)
        option.palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        
        if num_val > self.warning_level:
            option.palette.setColor(QPalette.ColorRole.Text, self.normalColor)
        elif self.critical_level < num_val <= self.warning_level:
            option.palette.setColor(QPalette.ColorRole.Text, self.warningColor)
        elif 0 < num_val <= self.critical_level:
            option.palette.setColor(QPalette.ColorRole.Text, self.criticalColor)
        else:  # out of stock (<= 0)
            option.palette.setColor(QPalette.ColorRole.Text, self.outOfStockColor)


class ActionDelegate(QStyledItemDelegate):
    "A custom delegate for action code/description"

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        # extracts the first element of the tuple (the description in string format)
        self.action = {k: actionDefinition[k][0] for k in actionDefinition}

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        super().initStyleOption(option, index)
        
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            val = index.data(Qt.ItemDataRole.DisplayRole)
        
        if val in self.action:
            option.text = f"[{val}] {self.action[val]}"
        else:
            option.text = str(val) if val is not None else ""
            

        option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        
        model_font = index.data(Qt.ItemDataRole.FontRole)
        if model_font and model_font.bold():
            option.font.setBold(True)

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex | QPersistentModelIndex
                     ) -> QComboBox:
        cb = QComboBox(parent)
        for k, v in self.action.items(): 
            cb.addItem(f"[{k}] {v}", k)
        return cb

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        val = index.data(Qt.ItemDataRole.EditRole)
        if val is None:
            return
        
        cb = cast(QComboBox, editor)
        idx = cb.findData(val)
        if idx != -1:
            cb.setCurrentIndex(idx)
        else:
            cb.setCurrentText(self.action.get(val, ''))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        cb = cast(QComboBox, editor)
        model.setData(index, cb.currentData(), Qt.ItemDataRole.EditRole)


class GenericReadOnlyDelegate(QStyledItemDelegate):
    "Delegate for view with read only query model"

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt initialize basic data (including selection state, focus, and FontRole)
        super().initStyleOption(option, index)
        
        # retrieves the value to format
        value = index.data(Qt.ItemDataRole.DisplayRole)
        
        # format text and align based on data type.
        match value:
            case bool():  # boolean check must precede int (bool is a subclass of int)
                option.text = '\u26ab' if value else '\u26aa'
                option.displayAlignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            case int():
                option.text = str(value)
                option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            case QDate() | QDateTime() | QTime():
                option.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
                option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            case Decimal():
                option.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
                option.displayAlignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            case _:
                option.text = str(value) if value is not None else ""
                option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

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

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        # let Qt load the basic model data
        super().initStyleOption(option, index)
        
        # retrieve the value using DisplayRole
        val = index.data(Qt.ItemDataRole.DisplayRole)
        
        # check the type and format of the time string
        if isinstance(val, QTime):
            option.text = val.toString('HH:mm:ss')
        else:
            option.text = ''
            
        # sets alignment
        option.displayAlignment = Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter

        
