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
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QColor
from PySide6.QtGui import QBrush
from PySide6.QtGui import QPalette
from PySide6.QtGui import QPainter
#from PySide6.QtGui import QKeySequence
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
#from PySide6.QtWidgets import QKeySequenceEdit

# application modules
from App import session
from App import actionDefinition
from App.Core.Cryptography import string_encode
from App.Core.Cryptography import string_decode
from App.Database.Setting import SettingClass
from App.Widget.Control import ColorComboBox
from App.Widget.Control import RelationalComboBox
from App.Widget.Dialog import SelectImageDialog



class GenericDelegate(QStyledItemDelegate):
    "Delegate for view"

    def paint(self, 
              painter: QPainter,
              option: QStyleOptionViewItem, 
              index: QModelIndex|QPersistentModelIndex) -> None:
        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        #print('GenericDelegate.paint:', value, type(value))
        styleOption: QStyleOptionViewItem = QStyleOptionViewItem(option)
        self.initStyleOption(styleOption, index)

        if isinstance(value, bool):
            styleOption = QStyleOptionButton()
            styleOption.state |= QStyle.StateFlag.State_On if value else QStyle.StateFlag.State_Off
            styleOption.rect = self.getCheckBoxRect(option)
            #style.drawControl(QStyle.CE_CheckBox,
            #                    styleOption,
            #                   painter)
        elif isinstance(value, int):
            styleOption.text = str(value)
            styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        elif isinstance(value, (QDate, QDateTime, QTime)):
            styleOption.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
            styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
        elif isinstance(value, Decimal):
            styleOption.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
            styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        else:
            styleOption.text = str(value or '')  # for null values
            styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

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

    def getCheckBoxRect(self, option: QStyleOptionViewItem) -> QRect:
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(int(option.rect.x() + option.rect.width() / 2 - check_box_rect.width() / 2),
                                 int(option.rect.y() + option.rect.height() / 2 - check_box_rect.height() / 2))
        return QRect(check_box_point, check_box_rect.size())

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QWidget:
        model = index.model()
        fieldType = model.columns[index.column()][3]
        widget: QCheckBox|QSpinBox|QDateEdit|QDateTimeEdit|QDoubleSpinBox|QLineEdit
        match fieldType:
            case 'bool':  # must be checked before int (bool is subclass of int)
                widget = QCheckBox(parent)
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
        if not index.data():
            return
        match editor:
            case QCheckBox():
                editor.setChecked(index.data())
            case QSpinBox():
                editor.setValue(index.data())
            case QDateEdit():
                editor.setDate(index.data())
            case QDateTimeEdit():
                editor.setDateTime(index.data())
            case QDoubleSpinBox():
                editor.setValue(index.data())
            case QLineEdit():
                editor.setText(str(index.data()))
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

    def __init__(self, parent: QWidget, colors: list[str]) -> None:
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
                      editor: ColorComboBox,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        cbi = editor.findData(index.data())
        editor.setCurrentIndex(cbi if cbi >= 0 else 0)  # can be -1 on New

    def setModelData(self, 
                     editor: ColorComboBox,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        model.setData(index, editor.currentData(Qt.ItemDataRole.UserRole), Qt.ItemDataRole.EditRole)

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
            # pix is scaled anyway
            #pix = pix.scaled(option.rect.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
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
            pix = dd.getImage()
            ba = QByteArray()
            buf = QBuffer(ba)
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            pix.save(buf, "PNG")
            index.model().setData(index, ba, Qt.ItemDataRole.EditRole)
        return QWidget(parent)  # dummy editor, not used

    def setEditorData(self, 
                      editor: SelectImageDialog,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        QStyledItemDelegate.setEditorData(self, editor, index)


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
        "Paint a checkbox without the label."
        checked = bool(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        check_box_style_option = QStyleOptionButton()
        painter.save()
        if option.state & QStyle.StateFlag.State_Selected:  # selected
            if option.state & QStyle.StateFlag.State_Active:  # selected active
                painter.fillRect(option.rect, option.palette.highlight())
            else:  # selected not active
                if option.features & QStyleOptionViewItem.ViewItemFeature.Alternate:
                    painter.fillRect(option.rect, option.palette.alternateBase())
                else:
                    painter.fillRect(option.rect, option.palette.base())
        else:  # not selected
            if option.features & QStyleOptionViewItem.ViewItemFeature.Alternate:
                painter.fillRect(option.rect, option.palette.alternateBase())
            else:
                painter.fillRect(option.rect, option.palette.base())
        if (option.state & QStyle.StateFlag.State_Selected):
            check_box_style_option.state |= QStyle.StateFlag.State_Selected
        if option.state & QStyle.StateFlag.State_Enabled:
            check_box_style_option.state |= QStyle.StateFlag.State_Enabled
        if checked:
            check_box_style_option.state |= QStyle.StateFlag.State_On
        else:
            check_box_style_option.state |= QStyle.StateFlag.State_Off
        check_box_style_option.rect = self.getCheckBoxRect(option)
        if not index.flags() & Qt.ItemFlag.ItemIsEditable:
            check_box_style_option.state |= QStyle.StateFlag.State_ReadOnly
        QApplication.style().drawControl(QStyle.ControlElement.CE_CheckBox,
                                         check_box_style_option,
                                         painter)
        painter.restore()

    def getCheckBoxRect(self, option: QStyleOptionViewItem) -> QRect:
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(option.rect.x() + option.rect.width() // 2 - check_box_rect.width() // 2,
                                 option.rect.y() + option.rect.height() // 2 - check_box_rect.height() // 2)
        return QRect(check_box_point, check_box_rect.size())

    def editorEvent(self, 
                    event: QEvent, 
                    model: QAbstractItemModel, 
                    option: QStyleOptionViewItem, 
                    index: QModelIndex|QPersistentModelIndex
                    ) -> bool   :
        """Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        """
        # if int(not index.flags() & Qt.ItemIsEditable) > 0:
        if not (index.flags() & Qt.ItemFlag.ItemIsEditable):
            return False
        # do nothing if view is not editable. Parent of the delegate must be the view
        if hasattr(self.parent(), 'editTriggers'):
            if self.parent().editTriggers() == QAbstractItemView.EditTrigger.NoEditTriggers:
                return False
        # Do not change the checkbox-state
        if event.type() == QEvent.Type.MouseButtonRelease or event.type() == QEvent.Type.MouseButtonDblClick:
            if event.button() != Qt.MouseButton.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QEvent.Type.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.Type.KeyPress:
            if event.key() != Qt.Key.Key_Space and event.key() != Qt.Key.Key_Select:
                return False
        else:
            return False
        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        "The user wanted to change the old state in the opposite."
        newValue = not bool(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        model.setData(index, newValue, Qt.ItemDataRole.EditRole)

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
                      editor: QComboBox,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        editor.setCurrentText(index.data())

    def setModelData(self, 
                     editor: QComboBox,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        model.setData(index, editor.currentText())


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

    #def setEditorData(self, editor, index):
        #if not index.data():
            #return
        #editor.setCurrentText(index.data())

    #def setModelData(self, editor, model, index):
        #model.setData(index, editor.currentText())


class RelationDelegate(QStyledItemDelegate):
    "A delegate (combo box) for referenced table fields"

    def __init__(self, parent: QWidget, function) -> None:
        super().__init__(parent)
        # define a model used for paint and combobox editor
        # (field, relational field)
        #self.model = QStandardItemModel(len(fields), 2)
        #for r, (f, rf) in enumerate(fields):
            #fd = QStandardItem(f)
            #rfd = QStandardItem(rf)
            #self.model.setItem(r, 0, fd)
            #self.model.setItem(r, 1, rfd)
        self.function = function
        self.updateItems()

    def updateItems(self) -> None:
        self.data = dict(self.function())
        #self.reverseData = {v:k for k, v in self.data.items()}


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
            #else:  # selected not active
                #if option.features & QStyleOptionViewItem.Alternate:
                    #opt.backgroundBrush = option.palette.alternateBase()
                #else:
                    #opt.backgroundBrush = option.palette.base()
        #else:  # not selected
            #if option.state & QStyle.State_Active:  # not selected active
                #if option.features & QStyleOptionViewItem.Alternate:
                    #opt.backgroundBrush = option.palette.base()
                #else:
                    #opt.backgroundBrush = option.palette.alternateBase()
            #else:  # not selected not active
                #if option.features & QStyleOptionViewItem.Alternate:
                    #opt.backgroundBrush = option.palette.alternateBase()
                #else:
                    #opt.backgroundBrush = option.palette.base()
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
        editor.setCurrentText(self.data.get(index.data()))

    def setModelData(self, 
                     editor: QWidget,
                     model: QAbstractItemModel, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        # if editor.currentText(): # can happend in insert row
        #print("Editor data", editor.currentData())
        model.setData(index, editor.currentData())

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
        option.text = str(index.data()) #str(int(index.data() or 0)  # can be null on insert row
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        if self.bold:
            option.font.setWeight(QFont.Weight.Bold)
        if index.data(Qt.ItemDataRole.FontRole):
            if index.data(Qt.ItemDataRole.FontRole).bold():
                option.font.setWeight(QFont.Weight.Bold)

        super().paint(painter, option, index)
        #painter.save()

        #if option.state & QStyle.State_Selected:  # selected
            #if option.state & QStyle.State_Active:  # selected active
                #painter.fillRect(option.rect, option.palette.highlight())
                #option.backgroundBrush = option.palette.highlight()
            #else:  # selected not active
                #if option.features & QStyleOptionViewItem.Alternate:
                    #painter.fillRect(option.rect, option.palette.alternateBase())
                    #option.backgroundBrush = option.palette.alternateBase()
                #else:
                    #painter.fillRect(option.rect, option.palette.base())
                    #option.backgroundBrush = option.palette.base()
        #else:  # not selected
            #if option.features & QStyleOptionViewItem.Alternate:
                #painter.fillRect(option.rect, option.palette.alternateBase())
                #option.backgroundBrush = option.palette.alternateBase()
            #else:
                #painter.fillRect(option.rect, option.palette.base())
                #option.backgroundBrush = option.palette.base()

        #QApplication.style().drawControl(QStyle.CE_ItemViewItem, option, painter)
        #painter.restore()

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QSpinBox:
        sb = QSpinBox(parent)
        sb.setMaximum(999999999)
        return sb

    def setEditorData(self, 
                      editor: QSpinBox, 
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        editor.setValue(index.data())

    def setModelData(self, 
                     editor: QSpinBox,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        model.setData(index, editor.value())


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

        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem, option, painter)
        painter.restore()

    def createEditor(self, 
                     parent: QWidget,
                     option: QStyleOptionViewItem,
                     index: QModelIndex|QPersistentModelIndex) -> QDoubleSpinBox:
        sb = QDoubleSpinBox(parent)
        sb.setDecimals(self.prec)
        sb.setMaximum(self.maximum)
        return sb

    def setEditorData(self, 
                      editor: QDoubleSpinBox,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        editor.setValue(index.data())

    def setModelData(self, 
                     editor: QDoubleSpinBox,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex) -> None:
        model.setData(index, editor.value())

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

    #def createEditor(self, parent, option, index):
    #    dsb = QDoubleSpinBox(parent)
    #    dsb.setDecimals(setting['quantity_decimal_places'])
    #    dsb.setMaximum(999999)
    #    return dsb

    def setEditorData(self, 
                      editor: QDoubleSpinBox,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        model = index.model()
        stockIndex = model.createIndex(index.row(), self.STOCK)
        newLoads = model.data(stockIndex) or 0.0
        editor.setValue(newLoads)

    def setModelData(self, 
                     editor: QDoubleSpinBox,
                     model: QAbstractItemModel,
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        # update loads
        loadsIndex = model.createIndex(index.row(), self.LOAD)
        unloadsIndex = model.createIndex(index.row(), self.UNLOAD)
        unloads = model.data(unloadsIndex) or Decimal(0)
        model.setData(loadsIndex, Decimal(editor.value()) + unloads)
        # update stock
        stockIndex = model.createIndex(index.row(), self.STOCK)
        stock = Decimal(editor.value())
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
        option.text = session['qlocale'].toString(float(index.data() or 0.0), 'f', self.prec)  # can be null on insert row
        value = index.data() or 0  # could be None
        option.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
        option.font.setWeight(QFont.Weight.Bold)
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
        # check color
        if value >= self.warning_level:
            option.palette.setColor(QPalette.ColorRole.Text, self.normalColor)
        elif self.critical_level < value < self.warning_level:
            option.palette.setColor(QPalette.ColorRole.Text, self.warningColor)
        elif 0 < value <= self.critical_level:
            option.palette.setColor(QPalette.ColorRole.Text, self.criticalColor)
        else:  # out of stock
            option.palette.setColor(QPalette.ColorRole.Text, self.outOfStockColor)
        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                         option,
                                         painter)
        painter.restore()


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
        opt = QStyleOptionViewItem(option)
        #model = index.model()
        #ni = model.index(index.row(), index.column())
        #d = ni.data(Qt.DisplayRole)
        d = index.data(Qt.ItemDataRole.DisplayRole)
        if d:
            #opt.text = self.action.get(d)
            opt.text = d
        painter.save()
        # selected on focus
        if (option.state & QStyle.StateFlag.State_Selected):
            painter.fillRect(option.rect, option.palette.highlight())
            opt.backgroundBrush = option.palette.highlight()
        #elif (option.state & QStyle.State_Active):
            #print("***")
        # standard alternate
        elif (option.features & QStyleOptionViewItem.ViewItemFeature.Alternate):
            painter.fillRect(option.rect, option.palette.alternateBase())
        # standard
        elif (option.features & QStyleOptionViewItem.ViewItemFeature.None_):
            painter.fillRect(option.rect, option.palette.base())

        QApplication.style().drawControl(QStyle.ControlElement.CE_ItemViewItem,
                                         opt,
                                         painter)
        painter.restore()

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
                      editor: QComboBox,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        editor.setCurrentText(self.action.get(index.data()))

    def setModelData(self, 
                     editor: QComboBox, 
                     model: QAbstractItemModel, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        #print(editor.currentData())
        model.setData(index, editor.currentData())


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
                         '\u25CF\u25CF\u25CF\u25CF\u25CF\u25CF')
        painter.restore()

    def createEditor(self, 
                     parent: QWidget, 
                     option: QStyleOptionViewItem, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> QLineEdit:
        le = QLineEdit(parent)
        le.setEchoMode(QLineEdit.EchoMode.Password)
        return le

    def setEditorData(self, 
                      editor: QLineEdit,
                      index: QModelIndex|QPersistentModelIndex
                      ) -> None:
        if not index.data():
            return
        editor.setText(string_decode(index.data()))

    def setModelData(self, 
                     editor: QLineEdit, 
                     model: QAbstractItemModel, 
                     index: QModelIndex|QPersistentModelIndex
                     ) -> None:
        model.setData(index, string_encode(editor.text()))


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
            case QDate(), QDateTime():
                styleOption.text = session['qlocale'].toString(value, QLocale.FormatType.ShortFormat)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter
            case Decimal():
                styleOption.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter
            case _:
                styleOption.text = str(value or '')  # for null values
                styleOption.displayAlignment = Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter

        font = index.model().data(index, Qt.Weight.WFontRole)
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
        
        
# class PandasDelegate(QStyledItemDelegate):
#     "Read only delegate for a tableview with pandas model"

#     def paint(self, painter, option, index):
#         if index.isValid() is False:
#             return
#         model = index.model()
#         header = model.headerData(index.column(), Qt.Horizontal, Qt.DisplayRole)
#         header = header.split('\n')[0]  # in case of multi-line header
#         dt = model.columns[model.trcolumns[header]][2]  # (name, type)
#         value = index.data() # index.model().data(index, Qt.DisplayRole)
#         print("Val", value, "Type", type(value), "DT", dt)
#         #type = index.model().columns[index.column()][1]  # (name, type)
#         styleOption = QStyleOptionViewItem(option)
#         self.initStyleOption(styleOption, index)

#         if dt == 'decimal2':
#             styleOption.text = session['qlocale'].toString(float(value or 0.0), 'f', 2)
#             styleOption.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
#         elif dt == 'int':
#             styleOption.text = str(int(float(value) or 0))
#             styleOption.displayAlignment = Qt.AlignRight | Qt.AlignVCenter
#         elif dt == 'str':
#             styleOption.text = str(value or '')  # for null values
#             styleOption.displayAlignment = Qt.AlignLeft | Qt.AlignVCenter
#         else:
#             styleOption.text = str(value or '')  # for null values
#             styleOption.displayAlignment = Qt.AlignLeft | Qt.AlignVCenter

#         font = index.model().data(index, Qt.FontRole)
#         if font:
#             styleOption.font = font
#         painter.save()
#         if option.state & QStyle.State_Selected:  # selected
#             if option.state & QStyle.State_Active:  # selected active
#                 styleOption.backgroundBrush = option.palette.highlight()

#         QApplication.style().drawControl(QStyle.CE_ItemViewItem,
#                                          styleOption,
#                                          painter)
#         painter.restore()

#     def getCheckBoxRect(self, option):
#         check_box_style_option = QStyleOptionButton()
#         check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
#         check_box_point = QPoint(option.rect.x() +
#                                  option.rect.width() / 2 -
#                                  check_box_rect.width() / 2,
#                                  option.rect.y() +
#                                  option.rect.height() / 2 -
#                                  check_box_rect.height() / 2)
#         return QRect(check_box_point, check_box_rect.size())

#     def createEditor(self, parent, option, index):
#         "Important, otherwise an editor is created if the user clicks in this cell."
#         return None