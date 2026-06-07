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

"""Items

This module provides items form management

"""

# standard library
from enum import IntEnum
import logging
from typing import cast
from typing import Any

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentIcon
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Core.Gui import COLORS
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import ColorComboDelegate
from App.Widget.Delegate import QuantityDelegate
from App.Widget.Delegate import AmountDelegate
from App.Widget.Delegate import GenericDelegate
from App.Widget.Form import FormIndexManager
from App.Widget.Dialog import PrintDialog
from App.Database.Models import ItemIndexModel  
from App.Database.Models import ItemModel
from App.Database.Models import ItemVariantModel
from App.Database.Models import KitPartModel
from App.Database.Models import MenuPartModel
from App.Database.Models import PriceListItemModel
from App.Database.Setting import Setting
from App.Database.Lookup import item_with_variant_lookup
from App.Database.Lookup import kit_part_lookup
from App.Database.Lookup import menu_part_lookup
from App.Database.Lookup import department_lookup
from App.Database.Lookup import price_list_lookup
from App.Database.Item import get_variants
from App.Ui.ItemWidget import Ui_ItemWidget
from App.Ui.ChooseItemDialog import Ui_ChooseItemDialog


# logger
logger = logging.getLogger(__name__)


class iti(IntEnum): # item index
    ID            = 0
    TYPE          = 1
    DESCRIPTION   = 2
    DEPARTMENT    = 3
    SORTING       = 4
    ROW           = 5
    COLUMN        = 6
    TXT_COLOR     = 7
    BCK_COLOR     = 8
    STOCK         = 9
    UNLOAD        = 10
    VARIANTS      = 11
    KIT_PART      = 12
    MENU_PART     = 13
    SALABLE       = 14
    WEB_AVAILABLE = 15
    WEB_SORTING   = 16
    OBSOLETE      = 17
    USER_INS      = 18
    DATE_INS      = 19
    USER_UPD      = 20
    DATE_UPD      = 21

class itm(IntEnum): # item
    ID            = 0
    TYPE          = 1
    DESCRIPTION   = 2
    CUSTOMER_DESC = 3
    DEPARTMENT    = 4
    SORTING       = 5
    ROW           = 6
    COLUMN        = 7
    TXT_COLOR     = 8
    BCK_COLOR     = 9
    STOCK         = 10
    DELIVERED     = 11
    VARIANTS      = 12
    KIT_PART      = 13
    MENU_PART     = 14
    SALABLE       = 15
    WEB_AVAILABLE = 16
    WEB_SORTING   = 17
    OBSOLETE      = 18

class vnt(IntEnum): # variant
    ID            = 0
    ITEM          = 1
    DESC          = 2
    SORT          = 3
    PRICE         = 4
    USER_INS      = 5
    DATE_INS      = 6
    USER_UPD      = 7
    DATE_UPD      = 8
    
class kit(IntEnum): # kit part
    ID            = 0
    KIT           = 1 
    PART          = 2 
    QTA           = 3
    USER_INS      = 4 
    DATE_INS      = 5
    USER_UPD      = 6
    DATE_UPD      = 7
    
class men(IntEnum): # menu part
    ID            = 0
    MENU          = 1
    PART          = 2
    QTA           = 3
    USER_INS      = 4
    DATE_INS      = 5
    USER_UPD      = 6
    DATE_UPD      = 7
    
class prc(IntEnum): # price
    ID            = 0
    LIST          = 1
    ITEM          = 2
    PRICE         = 3 
    USER_INS      = 4
    DATE_INS      = 5
    USER_UPD      = 6
    DATE_UPD      = 7

TABVAR, TABCOM, TABMEN, TABPRI = range(4)


def itemType() -> list:
    return [('I', _tr('Item', 'Item')),
            ('K', _tr('Item', 'Kit')),
            ('M', _tr('Item', 'Menu'))]


def item(action: QAction, checked: bool = False) -> None:
    "Manage items"
    logger.info('Starting items Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('Inventory', 'No access right to this archive'))
        return
    iw = ItemForm(mw, title, auth)
    iw.applySortFilter()
    mw.addTab(title, iw)
    logger.info('Items Form added to main window')


class ChooseItemDialog(QDialog):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_ChooseItemDialog()
        self.ui.setupUi(self)
        for k, v in item_with_variant_lookup():
            self.ui.comboBoxItems.addItem(v, k)


class ItemForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = ItemModel(self)
        idxModel = ItemIndexModel(self)
        modelv = ItemVariantModel(self)
        modelk = KitPartModel(self)
        modelm = MenuPartModel(self)
        modelp = PriceListItemModel(self)
        self.setModel(model, idxModel)
        self.addDetailRelation(modelv, itm.ID, vnt.ITEM)
        self.addDetailRelation(modelk, itm.ID, kit.KIT)
        self.addDetailRelation(modelm, itm.ID, men.MENU)
        self.addDetailRelation(modelp, itm.ID, prc.ITEM)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, True)
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        # icons for add/remove buttons
        self.ui.pushButtonAddVar.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemoveVar.setIcon(currentIcon['edit_remove'])
        self.ui.pushButtonAddKit.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemoveKit.setIcon(currentIcon['edit_remove'])
        self.ui.pushButtonAddMen.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemoveMen.setIcon(currentIcon['edit_remove'])
        self.ui.pushButtonAddPri.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemovePri.setIcon(currentIcon['edit_remove'])
        # setting
        self.setting = Setting()
        # signal slot connections
        self.ui.checkBoxVariants.toggled[bool].connect(self.ui.tabVariants.setEnabled)
        self.ui.comboBoxType.currentIndexChanged.connect(self.itemTypeChanged)
        # tableView
        # set index view
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('ItemIndex')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(iti.TYPE, RelationDelegate(self, itemType))
        self.ui.tableView.setItemDelegateForColumn(iti.DEPARTMENT, RelationDelegate(self, department_lookup))
        self.ui.tableView.setItemDelegateForColumn(iti.BCK_COLOR, ColorComboDelegate(self, 
                                                                                        cast(list[Any], [(self.setting['normal_background_color'] or '', _tr('Item', 'default'))] 
                                                                                        + COLORS)))
        self.ui.tableView.setItemDelegateForColumn(iti.TXT_COLOR, ColorComboDelegate(self, 
                                                                                        cast(list[Any], [(self.setting['normal_text_color'] or '', _tr('Item', 'default'))] 
                                                                                        + COLORS)))
        # mapper mappings
        self.ui.comboBoxType.setFunction(itemType)
        self.mapper.addMapping(self.ui.comboBoxType, itm.TYPE)
        self.mapper.addMapping(self.ui.lineEditDescription, itm.DESCRIPTION)
        self.mapper.addMapping(self.ui.lineEditCustomerDescription, itm.CUSTOMER_DESC)
        self.ui.comboBoxDepartment.setFunction(department_lookup)
        self.mapper.addMapping(self.ui.comboBoxDepartment, itm.DEPARTMENT)
        self.mapper.addMapping(self.ui.spinBoxRow, itm.ROW)
        self.mapper.addMapping(self.ui.spinBoxColumn, itm.COLUMN)
        self.mapper.addMapping(self.ui.spinBoxSorting, itm.SORTING)
        self.mapper.addMapping(self.ui.comboBoxNormalTextColor, itm.TXT_COLOR)
        self.mapper.addMapping(self.ui.comboBoxNormalBackgroundColor, itm.BCK_COLOR)
        self.mapper.addMapping(self.ui.checkBoxVariants, itm.VARIANTS)
        self.mapper.addMapping(self.ui.checkBoxInventoryControl, itm.STOCK)
        self.mapper.addMapping(self.ui.checkBoxDeliveredControl, itm.DELIVERED)
        self.mapper.addMapping(self.ui.checkBoxKitPart, itm.KIT_PART)
        self.mapper.addMapping(self.ui.checkBoxMenuPart, itm.MENU_PART)
        self.mapper.addMapping(self.ui.checkBoxSalable, itm.SALABLE)
        self.mapper.addMapping(self.ui.checkBoxWebAvailable, itm.WEB_AVAILABLE)
        self.mapper.addMapping(self.ui.spinBoxWebSorting, itm.WEB_SORTING)
        self.mapper.addMapping(self.ui.checkBoxObsolete, itm.OBSOLETE)
        # tabwidget tabs and tableview
        self.ui.tableViewVariants.setModel(modelv)
        self.ui.tableViewVariants.setLayoutName('ItemVariant')
        self.ui.tableViewVariants.setItemDelegateForColumn(vnt.PRICE, AmountDelegate(self))
        self.ui.tableViewVariants.setItemDelegateForColumn(vnt.DESC, GenericDelegate(self))
        self.ui.tableViewVariants.setItemDelegateForColumn(vnt.SORT, GenericDelegate(self))
        self.ui.tableViewComponents.setModel(modelk)
        self.ui.tableViewComponents.setLayoutName('ItemComponent')
        self.ui.tableViewComponents.setItemDelegateForColumn(kit.PART, RelationDelegate(self, kit_part_lookup))
        self.ui.tableViewComponents.setItemDelegateForColumn(kit.QTA, QuantityDelegate(self))
        self.ui.tableViewMenuItems.setModel(modelm)
        self.ui.tableViewMenuItems.setLayoutName('ItemMenu')
        self.ui.tableViewMenuItems.setItemDelegateForColumn(men.PART, RelationDelegate(self, menu_part_lookup))
        self.ui.tableViewMenuItems.setItemDelegateForColumn(men.QTA, QuantityDelegate(self))
        self.ui.tableViewPrices.setModel(modelp)
        self.ui.tableViewPrices.setLayoutName('ItemPrice')
        self.ui.tableViewPrices.setItemDelegateForColumn(prc.LIST, RelationDelegate(self, price_list_lookup))
        self.ui.tableViewPrices.setItemDelegateForColumn(prc.PRICE, AmountDelegate(self))
        # self.toFirst() not here because we need to set models first
        self.ui.checkBoxVariants.checkStateChanged.connect(self.hasVariantsStateChanged)
        self.ui.pushButtonCopyVariants.clicked.connect(self.copyVariants)
        self.ui.lineEditDescription.editingFinished.connect(self.copyDescription)
        self.ui.checkBoxSalable.toggled.connect(self.salableToggled)
        self.ui.checkBoxWebAvailable.toggled.connect(self.ui.spinBoxWebSorting.setEnabled)
        # set colors
        self.ui.comboBoxNormalTextColor.setColorList(COLORS)
        self.ui.comboBoxNormalTextColor.setCurrentColor(self.setting['normal_text_color'])
        self.ui.comboBoxNormalBackgroundColor.setColorList(COLORS)
        self.ui.comboBoxNormalBackgroundColor.setCurrentColor(self.setting['normal_background_color'])
        # signal/slot connections for add/remove buttons
        self.ui.pushButtonAddVar.clicked.connect(self.ui.tableViewVariants.add)
        self.ui.pushButtonRemoveVar.clicked.connect(self.ui.tableViewVariants.remove)
        self.ui.pushButtonAddKit.clicked.connect(self.ui.tableViewComponents.add)
        self.ui.pushButtonRemoveKit.clicked.connect(self.ui.tableViewComponents.remove)
        self.ui.pushButtonAddMen.clicked.connect(self.ui.tableViewMenuItems.add)
        self.ui.pushButtonRemoveMen.clicked.connect(self.ui.tableViewMenuItems.remove)
        self.ui.pushButtonAddPri.clicked.connect(self.ui.tableViewPrices.add)
        self.ui.pushButtonRemovePri.clicked.connect(self.ui.tableViewPrices.remove)
         # scripting init
        self.script = scriptInit(self)
        # scripting init
        
    def copyDescription(self):
        "Copy item description to item customer description on editingFinished of description lineEdit"
        if not self.ui.lineEditCustomerDescription.text():
            self.ui.lineEditCustomerDescription.setText(self.ui.lineEditDescription.text())

    def hasVariantsStateChanged(self, state):
        if Qt.CheckState(state) == Qt.CheckState.Checked:
            self.ui.tableViewVariants.setEnabled(True)
            self.ui.pushButtonCopyVariants.setEnabled(True)
        else:
            self.ui.tableViewVariants.setEnabled(False)
            self.ui.pushButtonCopyVariants.setEnabled(False)

    def salableToggled(self, checked: bool) -> None:
        if checked:
            self.ui.spinBoxRow.setEnabled(True)
            self.ui.spinBoxColumn.setEnabled(True)
            self.ui.spinBoxSorting.setEnabled(True)
            self.ui.comboBoxNormalBackgroundColor.setEnabled(True)
            self.ui.comboBoxNormalTextColor.setEnabled(True)
        else:
            self.ui.spinBoxRow.setEnabled(False)
            self.ui.spinBoxColumn.setEnabled(False)
            self.ui.spinBoxSorting.setEnabled(False)
            self.ui.comboBoxNormalBackgroundColor.setEnabled(False)
            self.ui.comboBoxNormalTextColor.setEnabled(False)
            self.ui.spinBoxRow.setValue(0)
            self.ui.spinBoxColumn.setValue(0)
            self.ui.spinBoxSorting.setValue(0)

    @scriptMethod
    def copyVariants(self, checked: bool = False) -> None:
        # ask for item to use for variantsa source
        dlg = ChooseItemDialog(self)
        if dlg.exec_() == QDialog.DialogCode.Rejected:
            return
        # activate variants
        self.ui.checkBoxVariants.setChecked(True)
        # add variants
        model = self.ui.tableViewVariants.model()
        for so, (vd, pd) in enumerate(get_variants(dlg.ui.comboBoxItems.currentData()), 1):
            model.insertRows(model.rowCount(), 1)
            modelRow = model.rowCount() - 1
            model.setData(model.index(modelRow, vnt.DESC), vd)
            model.setData(model.index(modelRow, vnt.SORT), so)
            model.setData(model.index(modelRow, vnt.PRICE), pd)

    def itemTypeChanged(self, index):
        self.ui.comboBoxType.blockSignals(True)
        if self.ui.comboBoxType.modelDataStr == 'K':
            self.ui.tableViewComponents.setEnabled(True)
            self.ui.tableViewMenuItems.setDisabled(True)
            self.ui.tabWidget.setCurrentIndex(1)
            self.ui.checkBoxDeliveredControl.setChecked(False)
            self.ui.checkBoxDeliveredControl.setDisabled(False)
            self.ui.checkBoxKitPart.setChecked(False)
            self.ui.checkBoxKitPart.setDisabled(True)
            self.ui.checkBoxMenuPart.setEnabled(True)
        elif self.ui.comboBoxType.modelDataStr == 'M':
            self.ui.tableViewComponents.setDisabled(True)
            self.ui.tableViewMenuItems.setEnabled(True)
            self.ui.tabWidget.setCurrentIndex(2)
            self.ui.checkBoxDeliveredControl.setChecked(False)
            self.ui.checkBoxDeliveredControl.setDisabled(True)
            self.ui.checkBoxKitPart.setChecked(False)
            self.ui.checkBoxKitPart.setDisabled(True)
            self.ui.checkBoxMenuPart.setChecked(False)
            self.ui.checkBoxMenuPart.setDisabled(True)
        else:
            self.ui.tableViewComponents.setDisabled(True)
            self.ui.tableViewMenuItems.setDisabled(True)
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.checkBoxInventoryControl.setEnabled(True)
            self.ui.checkBoxDeliveredControl.setEnabled(True)
            self.ui.checkBoxKitPart.setEnabled(True)
            self.ui.checkBoxMenuPart.setEnabled(True)
        self.ui.comboBoxType.blockSignals(False)

    @scriptMethod
    def new(self):
        "Set focus on item descriptionon new record"
        super().new()
        self.ui.comboBoxNormalTextColor.setCurrentColor(self.setting['normal_text_color'])
        self.ui.comboBoxNormalBackgroundColor.setCurrentColor(self.setting['normal_background_color'])
        self.ui.lineEditDescription.setFocus()

    @scriptMethod
    def save(self):
        super().save()

    @scriptMethod
    def delete(self):
        msg = _tr('Item', 'Delete this item ?')
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{self.ui.lineEditDescription.text()}",
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        super().delete()

    @scriptMethod
    def reload(self):
        super().reload()

    @scriptMethod
    def print(self):
        "Items report"
        dialog = PrintDialog(self, 'ITEM')
        dialog.show()
