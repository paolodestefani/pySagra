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

This module contains items form management classes and functions


"""

# standard library
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentAction
from App import currentIcon
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import ColorComboDelegate
from App.Widget.Delegate import BooleanDelegate
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
from App.Database.Setting import SettingClass
from App.Database.CodeDescriptionList import item_with_variant_cdl
from App.Database.CodeDescriptionList import kit_part_cdl
from App.Database.CodeDescriptionList import menu_part_cdl
from App.Database.CodeDescriptionList import department_cdl
from App.Database.CodeDescriptionList import price_list_cdl
from App.Database.Item import get_variants
from App.Ui.ItemWidget import Ui_ItemWidget
from App.Ui.ChooseItemDialog import Ui_ChooseItemDialog


(I_ID, I_TYPE, I_DESCRIPTION, I_DEPARTMENT, I_SORTING, I_ROW, I_COLUMN,
 I_NORMALTXTCOLOR, I_NORMALBCKCOLOR, I_STOCK, I_UNLOAD, I_VARIANTS, I_KITPART, I_MENUPART,
 I_SALABLE, I_WEBAVAILABLE, I_WEBSORTING, I_OBSOLETE,
 I_USER_INS, I_DATE_INS, I_USER_UPD, I_DATE_UPD) = range(22)

(ID, TYPE, DESCRIPTION, CUSTOMER_DESCRIPTION, DEPARTMENT, SORTING, ROW, COLUMN,
 NORMALTXTCOLOR, NORMALBCKCOLOR, STOCK, DELIVERED, VARIANTS, KITPART, MENUPART,
 SALABLE, WEBAVAILABLE, WEBSORTING, OBSOLETE) = range(19)

(VID, VITEM, VDESC, VSORT, VPRICE, VUINS, VDINS, VUUPG, VDUPG) = range(9)
(KID, KKIT, KPART, KQTA, KUINS, KDINS, KUUPG, KDUPG) = range(8)
(MID, MMENU, MPART, MQTA, MUINS, MDINS, MUUPG, MDUPG) = range(8)
(PID, PLIST, PITEM, PPRICE, PUINS, PDINS, PUUPG, PDUPG) = range(8)

TABVAR, TABCOM, TABMEN, TABPRI = range(4)


# colors for color combo box
COLORS = [('#FF0000', _tr('Item', 'Red')),
          ('#FF7700', _tr('Item', 'Orange')),
          ('#00FF00', _tr('Item', 'Green')),
          ('#0000FF', _tr('Item', 'Blue')),
          ('#4141C5', _tr('Item', 'Light blue')),
          ('#000000', _tr('Item', 'Black')),
          ('#535353', _tr('Item', 'Gray')),
          ('#FFFFFF', _tr('Item', 'White')),
          ('#FFFF00', _tr('Item', 'Yellow')),
          ('#770000', _tr('Item', 'Dark red')),
          ('#007700', _tr('Item', 'Dark green')),
          ('#000077', _tr('Item', 'Dark blue'))]


def itemType() -> list:
    return [('I', _tr('Item', 'Item')),
            ('K', _tr('Item', 'Kit')),
            ('M', _tr('Item', 'Menu'))]


def item() -> None:
    "Manage items"
    logging.info('Starting items Form')
    mw = session['mainwin']
    title = currentAction['app_file_item'].text()
    auth = currentAction['app_file_item'].data()
    iw = ItemForm(mw, title, auth)
    iw.reload()
    mw.addTab(title, iw)
    logging.info('Items Form added to main window')


class ChooseItemDialog(QDialog):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_ChooseItemDialog()
        self.ui.setupUi(self)
        for k, v in item_with_variant_cdl():
            self.ui.comboBoxItems.addItem(v, k)


class ItemForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = ItemModel(self)
        idxModel = ItemIndexModel(self)
        modelv = ItemVariantModel(self)
        modelk = KitPartModel(self)
        modelm = MenuPartModel(self)
        modelp = PriceListItemModel(self)
        self.setModel(model, idxModel)
        self.addDetailRelation(modelv, ID, VITEM)
        self.addDetailRelation(modelk, ID, KKIT)
        self.addDetailRelation(modelm, ID, MMENU)
        self.addDetailRelation(modelp, ID, PITEM)
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
        setting = SettingClass()
        # signal slot connections
        self.ui.checkBoxVariants.toggled[bool].connect(self.ui.tabVariants.setEnabled)
        self.ui.comboBoxType.currentIndexChanged.connect(self.itemTypeChanged)
        # tableView
        # set index view
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('item')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_TYPE, RelationDelegate(self, itemType))
        self.ui.tableView.setItemDelegateForColumn(I_DEPARTMENT, RelationDelegate(self, department_cdl))
        self.ui.tableView.setItemDelegateForColumn(I_STOCK, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_VARIANTS, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_UNLOAD, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_KITPART, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_MENUPART, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_SALABLE, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_WEBAVAILABLE, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_OBSOLETE, BooleanDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(I_NORMALBCKCOLOR, ColorComboDelegate(self, [(setting['normal_background_color'] or '', _tr('Item', 'default'))] + COLORS))
        self.ui.tableView.setItemDelegateForColumn(I_NORMALTXTCOLOR, ColorComboDelegate(self, [(setting['normal_text_color'] or '', _tr('Item', 'default'))] + COLORS))
        # mapper mappings
        self.ui.comboBoxType.setFunction(itemType)
        self.mapper.addMapping(self.ui.comboBoxType, TYPE, b"modelDataStr")
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        self.mapper.addMapping(self.ui.lineEditCustomerDescription, CUSTOMER_DESCRIPTION)
        self.ui.comboBoxDepartment.setFunction(department_cdl)
        self.mapper.addMapping(self.ui.comboBoxDepartment, DEPARTMENT, b"modelDataInt")
        self.mapper.addMapping(self.ui.spinBoxRow, ROW)
        self.mapper.addMapping(self.ui.spinBoxColumn, COLUMN)
        self.mapper.addMapping(self.ui.spinBoxSorting, SORTING)
        #self.mapper.addMapping(self.ui.doubleSpinBoxPrice, PRICE, b"modelDataDecimal")
        self.mapper.addMapping(self.ui.comboBoxNormalTextColor, NORMALTXTCOLOR, b"modelDataStr")
        self.mapper.addMapping(self.ui.comboBoxNormalBackgroundColor, NORMALBCKCOLOR, b"modelDataStr")
        self.mapper.addMapping(self.ui.checkBoxVariants, VARIANTS)
        self.mapper.addMapping(self.ui.checkBoxInventoryControl, STOCK)
        self.mapper.addMapping(self.ui.checkBoxDeliveredControl, DELIVERED)
        self.mapper.addMapping(self.ui.checkBoxKitPart, KITPART)
        self.mapper.addMapping(self.ui.checkBoxMenuPart, MENUPART)
        self.mapper.addMapping(self.ui.checkBoxSalable, SALABLE)
        self.mapper.addMapping(self.ui.checkBoxWebAvailable, WEBAVAILABLE)
        self.mapper.addMapping(self.ui.spinBoxWebSorting, WEBSORTING)
        self.mapper.addMapping(self.ui.checkBoxObsolete, OBSOLETE)
        # tabwidget tabs and tableview
        self.ui.tableViewVariants.setModel(modelv)
        self.ui.tableViewVariants.setLayoutName('itemVariant')
        self.ui.tableViewVariants.setItemDelegateForColumn(VPRICE, AmountDelegate(self))
        self.ui.tableViewVariants.setItemDelegateForColumn(VDESC, GenericDelegate(self))
        self.ui.tableViewVariants.setItemDelegateForColumn(VSORT, GenericDelegate(self))
        self.ui.tableViewComponents.setModel(modelk)
        self.ui.tableViewComponents.setLayoutName('itemComponent')
        self.ui.tableViewComponents.setItemDelegateForColumn(KPART, RelationDelegate(self, kit_part_cdl))
        self.ui.tableViewComponents.setItemDelegateForColumn(KQTA, QuantityDelegate(self))
        self.ui.tableViewMenuItems.setModel(modelm)
        self.ui.tableViewMenuItems.setLayoutName('itemMenu')
        self.ui.tableViewMenuItems.setItemDelegateForColumn(MPART, RelationDelegate(self, menu_part_cdl))
        self.ui.tableViewMenuItems.setItemDelegateForColumn(MQTA, QuantityDelegate(self))
        self.ui.tableViewPrices.setModel(modelp)
        self.ui.tableViewPrices.setLayoutName('itemPrice')
        self.ui.tableViewPrices.setItemDelegateForColumn(PLIST, RelationDelegate(self, price_list_cdl))
        self.ui.tableViewPrices.setItemDelegateForColumn(PPRICE, AmountDelegate(self))
        # self.toFirst() not here because we need to set models first
        self.ui.checkBoxVariants.stateChanged.connect(self.hasVariantsStateChanged)
        self.ui.pushButtonCopyVariants.clicked.connect(self.copyVariants)
        self.ui.lineEditDescription.editingFinished.connect(self.copyDescription)
        self.ui.checkBoxSalable.toggled.connect(self.salableToggled)
        self.ui.checkBoxWebAvailable.toggled.connect(self.ui.spinBoxWebSorting.setEnabled)
        # set colors
        self.ui.comboBoxNormalTextColor.setColorList([(setting['normal_text_color'], _tr('Item', 'default'))] + COLORS)
        self.ui.comboBoxNormalBackgroundColor.setColorList([(setting['normal_background_color'], _tr('Item', 'default'))] + COLORS)
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
            model.setData(model.createIndex(modelRow, VDESC), vd)
            model.setData(model.createIndex(modelRow, VSORT), so)
            model.setData(model.createIndex(modelRow, VPRICE), pd)

    def itemTypeChanged(self, index):
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

    # def add(self):
    #     if self.ui.tabWidget.currentIndex() == TABVAR:
    #         if self.ui.tableViewVariants.isEnabled():
    #             self.ui.tableViewVariants.add()
    #     elif self.ui.tabWidget.currentIndex() == TABCOM:
    #         if self.ui.tableViewComponents.isEnabled():
    #             self.ui.tableViewComponents.add()
    #     elif self.ui.tabWidget.currentIndex() == TABMEN:
    #         if self.ui.tableViewMenuItems.isEnabled():
    #             self.ui.tableViewMenuItems.add()
    #     elif self.ui.tabWidget.currentIndex() == TABPRI:
    #         self.ui.tableViewPrices.add()
    #     else:
    #         pass

    # def remove(self):
    #     if self.ui.tabWidget.currentIndex() == TABVAR:
    #         self.ui.tableViewVariants.remove()
    #     elif self.ui.tabWidget.currentIndex() == TABCOM:
    #         self.ui.tableViewComponents.remove()
    #     elif self.ui.tabWidget.currentIndex() == TABMEN:
    #         self.ui.tableViewMenuItems.remove()
    #     elif self.ui.tabWidget.currentIndex() == TABPRI:
    #         self.ui.tableViewPrices.remove()
    #     else:
    #         pass

    @scriptMethod
    def new(self):
        "Set focus on item descriptionon new record"
        super().new()
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
