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

"""Settings

This module provides application setting dialog


"""

# standard library
import logging

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor
from PySide6.QtGui import QFont
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QColorDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QPushButton

# application modules
from App import session
from App import currentAction
from App.Database.Exceptions import PyAppDBError
from App.Database.Exceptions import PyAppDBConcurrencyError
from App.Database.Setting import Setting
from App.Database.CodeDescriptionList import printer_class_cdl
from App.Database.CodeDescriptionList import customer_order_report_cdl
from App.Database.CodeDescriptionList import department_order_report_cdl
from App.Database.CodeDescriptionList import cover_order_report_cdl
from App.Database.CodeDescriptionList import stock_unload_report_cdl
from App.Ui.SettingsDialog import Ui_SettingsDialog
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod
from App.Item import COLORS



COMP_ID, COMP_DESC, COMP_SCHEMA, COMP_SYSTEM, COMP_IMAGE = range(5)
(UC_COMPANY, UC_USER, UC_PROFILE, UC_MENU, UC_TOOLBAR, UC_USER_INS,
 UC_DATE_INS, UC_USER_UPD, UC_DATE_UPD) = range(9)


def settings() -> None:
    "Application settings"
    logging.info('Starting settings dialog')
    mw = session['mainwin']
    title = currentAction['app_file_setting'].text()
    auth = currentAction['app_file_setting'].data()
    sd = SettingsDialog(mw, title, auth)
    sd.exec_()
    logging.info('Settings dialog shown')


class SettingsDialog(QDialog):
    "Application settings dialog box for set/get application parameters"

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.setting = Setting()
        self.ui.spinBoxLunch.setValue(self.setting['lunch_start_time'])
        self.ui.horizontalSliderLunch.setValue(self.setting['lunch_start_time']) # initially slider/spinbox are not connected
        self.ui.spinBoxDinner.setValue(self.setting['dinner_start_time'])
        self.ui.horizontalSliderDinner.setValue(self.setting['dinner_start_time']) # initially slider/spinbox are not connected
        self.ui.comboBoxOrderUI.addItems([_tr('Setting', 'Standard'),
                                          _tr('Setting', 'Totals in one column'),
                                          _tr('Setting', 'Maximize items room')])
        self.ui.comboBoxOrderUI.setCurrentIndex(self.setting['order_entry_ui'])
        if self.setting['default_delivery_type'] == 'T':
            self.ui.radioButtonTable.setChecked(True)
        else:
            self.ui.radioButtonTakeaway.setChecked(True)
        if self.setting['default_payment_type'] == 'E':
            self.ui.radioButtonElectronic.setChecked(True)
        else:
            self.ui.radioButtonCash.setChecked(True)
        if self.setting['order_number_based_on'] == 'E':
            self.ui.radioButtonEventBased.setChecked(True)
        elif self.setting['order_number_based_on'] == 'D':
            self.ui.radioButtonDayBased.setChecked(True)
        else:
            self.ui.radioButtonDayPartBased.setChecked(True) # day (P)art based 
        for i, j in [('N', _tr('Setting', 'North')),
                     ('S', _tr('Setting', 'South')),
                     ('E', _tr('Setting', 'East')),
                     ('W', _tr('Setting', 'West'))]:
            self.ui.comboBoxTabPosition.addItem(j, i)
        self.ui.comboBoxTabPosition.setCurrentIndex(self.ui.comboBoxTabPosition.findData(self.setting['order_list_tab_position']))
        self.ui.spinBoxWarningLevel.setDecimals(self.setting['quantity_decimal_places'])
        self.ui.spinBoxWarningLevel.setValue(self.setting['warning_stock_level'])
        self.ui.spinBoxCriticalLevel.setDecimals(self.setting['quantity_decimal_places'])
        self.ui.spinBoxCriticalLevel.setValue(self.setting['critical_stock_level'])
        self.ui.spinBoxOrderListRows.setValue(self.setting['order_list_rows'])
        self.ui.spinBoxOrderListColumns.setValue(self.setting['order_list_columns'])
        self.ui.spinBoxOrderListSpacing.setValue(self.setting['order_list_spacing'])
        self.ui.fontComboBoxOrderList.setCurrentFont(QFont(self.setting['order_list_font_family']))
        self.ui.spinBoxOrderListFontSize.setValue(self.setting['order_list_font_size'])
        self.ui.spinBoxTableListRows.setValue(self.setting['table_list_rows'])
        self.ui.spinBoxTableListColumns.setValue(self.setting['table_list_columns'])
        self.ui.spinBoxTableListSpacing.setValue(self.setting['table_list_spacing'])
        self.ui.fontComboBoxTableList.setCurrentFont(QFont(self.setting['table_list_font_family']))
        self.ui.spinBoxTableListFontSize.setValue(self.setting['table_list_font_size'])
        self.ui.checkBoxUseTableList.setChecked(self.setting['use_table_list'])
        # colors
        # for many problems with platform themes i use stylesheet for setting colors
        self.ui.pushButtonWB.color = self.setting['warning_background_color']
        self.ui.pushButtonWB.setStyleSheet(f"background-color: {self.ui.pushButtonWB.color};")
        self.ui.pushButtonWT.color = self.setting['warning_text_color']
        self.ui.pushButtonWT.setStyleSheet(f"background-color: {self.ui.pushButtonWT.color};")
        self.ui.pushButtonCB.color = self.setting['critical_background_color']
        self.ui.pushButtonCB.setStyleSheet(f"background-color: {self.ui.pushButtonCB.color};")
        self.ui.pushButtonCT.color = self.setting['critical_text_color']
        self.ui.pushButtonCT.setStyleSheet(f"background-color: {self.ui.pushButtonCT.color};")
        self.ui.pushButtonDB.color = self.setting['disabled_background_color']
        self.ui.pushButtonDB.setStyleSheet(f"background-color: {self.ui.pushButtonDB.color};")
        self.ui.pushButtonDT.color = self.setting['disabled_text_color']
        self.ui.pushButtonDT.setStyleSheet(f"background-color: {self.ui.pushButtonDT.color};")
        self.updateExampleButtons()
        
        self.ui.checkBoxCustomerCopy.setChecked(self.setting['print_customer_copy'])
        self.ui.checkBoxDepartmentCopy.setChecked(self.setting['print_department_copy'])
        self.ui.checkBoxCoverCopy.setChecked(self.setting['print_cover_copy'])
        self.ui.spinBoxCustomerCopies.setValue(self.setting['customer_copies'] or 1)
        self.ui.spinBoxDepartmentCopies.setValue(self.setting['department_copies'] or 1)
        self.ui.spinBoxCoverCopies.setValue(self.setting['cover_copies'] or 1)
        self.ui.comboBoxCustomerReport.setFunction(customer_order_report_cdl)
        self.ui.comboBoxCustomerReport.setCurrentIndex(self.ui.comboBoxCustomerReport.findData(self.setting['customer_report']))
        self.ui.comboBoxDepartmentReport.setFunction(department_order_report_cdl)
        self.ui.comboBoxDepartmentReport.setCurrentIndex(self.ui.comboBoxDepartmentReport.findData(self.setting['department_report']))
        self.ui.comboBoxCoverReport.setFunction(cover_order_report_cdl)
        self.ui.comboBoxCoverReport.setCurrentIndex(self.ui.comboBoxCoverReport.findData(self.setting['cover_report']))
        self.ui.comboBoxCustomerPrinter.setFunction(printer_class_cdl)
        self.ui.comboBoxCustomerPrinter.setCurrentIndex(self.ui.comboBoxCustomerPrinter.findData(self.setting['customer_printer_class']))
        self.ui.comboBoxCoverPrinter.setFunction(printer_class_cdl)
        self.ui.comboBoxCoverPrinter.setCurrentIndex(self.ui.comboBoxCoverPrinter.findData(self.setting['cover_printer_class']))
        self.ui.spinBoxMaxCovers.setValue(self.setting['max_covers'])
        self.ui.checkBoxOrderProgress.setChecked(self.setting['manage_order_progress'])
        self.ui.checkBoxAutoVariants.setChecked(self.setting['automatic_show_variants'])
        self.ui.checkBoxShowInventory.setChecked(self.setting['always_show_stock_inventory'])
        self.ui.checkBoxMandatoryTableNumber.setChecked(self.setting['mandatory_table_number'])
        self.ui.checkBoxInactivity.setChecked(self.setting['check_inactivity'])
        self.ui.spinBoxInactivityTime.setValue(self.setting['inactivity_time'])
        self.ui.groupBoxOrderedDeliveredReport.setChecked(self.setting['print_ordered_delivered_report'])
        self.ui.spinBoxOrderedDeliveredCopies.setValue(self.setting['ordered_delivered_copies'] or 1)
        self.ui.comboBoxOrderedDeliveredReport.setFunction(stock_unload_report_cdl)
        self.ui.comboBoxOrderedDeliveredReport.setCurrentIndex(self.ui.comboBoxOrderedDeliveredReport.findData(self.setting['ordered_delivered_report']))
        self.ui.comboBoxOrderedDeliveredPrinterClass.setFunction(printer_class_cdl)
        self.ui.comboBoxOrderedDeliveredPrinterClass.setCurrentIndex(self.ui.comboBoxOrderedDeliveredPrinterClass.findData(self.setting['ordered_delivered_printer_class']))
        # items inventory
        self.ui.spinBoxInventoryWarningLevel.setDecimals(self.setting['quantity_decimal_places'])
        self.ui.spinBoxInventoryWarningLevel.setValue(self.setting['inventory_warning_stock_level'])
        self.ui.spinBoxInventoryCriticalLevel.setDecimals(self.setting['quantity_decimal_places'])
        self.ui.spinBoxInventoryCriticalLevel.setValue(self.setting['inventory_critical_stock_level'])
        self.ui.spinBoxQuantityDecimals.setValue(self.setting['quantity_decimal_places'])
        self.ui.lineEditCurrencySymbol.setText(self.setting['currency_symbol'])
        
        self.ui.colorComboBoxBackground.setColorList(COLORS)
        self.ui.colorComboBoxBackground.setCurrentColor(self.setting['normal_background_color'])
        self.ui.colorComboBoxText.setColorList(COLORS)
        self.ui.colorComboBoxText.setCurrentColor(self.setting['normal_text_color'])
        
        # set initial default for linked params
        if self.ui.checkBoxCustomerCopy.isChecked():
            self.ui.spinBoxCustomerCopies.setEnabled(True)
            self.ui.comboBoxCustomerReport.setEnabled(True)
            self.ui.comboBoxCustomerPrinter.setEnabled(True)
        if self.ui.checkBoxDepartmentCopy.isChecked():
            self.ui.spinBoxDepartmentCopies.setEnabled(True)
            self.ui.comboBoxDepartmentReport.setEnabled(True)
        if self.ui.checkBoxCoverCopy.isChecked():
            self.ui.spinBoxCoverCopies.setEnabled(True)
            self.ui.comboBoxCoverReport.setEnabled(True)
            self.ui.comboBoxCoverPrinter.setEnabled(True)
        if self.ui.checkBoxInactivity.isChecked():
            self.ui.labelInactivity.setEnabled(True)
            self.ui.spinBoxInactivityTime.setEnabled(True)
        # restore settings
        st = QSettings(self)
        if st.value("DialogGeometry/Settings"):
            self.restoreGeometry(st.value("DialogGeometry/Settings"))
        # signal/slot
        # slider/spinbox sincro
        self.ui.horizontalSliderLunch.valueChanged.connect(self.lunchSliderChanged)
        self.ui.spinBoxLunch.valueChanged.connect(self.ui.horizontalSliderLunch.setValue)
        self.ui.horizontalSliderDinner.valueChanged.connect(self.dinnerSliderChanged)
        self.ui.spinBoxDinner.valueChanged.connect(self.ui.horizontalSliderDinner.setValue)
        self.ui.spinBoxCriticalLevel.valueChanged.connect(self.criticalLevelChanged)
        self.ui.spinBoxWarningLevel.valueChanged.connect(self.warningLevelChanged)
        self.ui.colorComboBoxBackground.currentIndexChanged.connect(self.updateExampleNormalButton)
        self.ui.colorComboBoxText.currentIndexChanged.connect(self.updateExampleNormalButton)
        self.ui.pushButtonWB.clicked.connect(self.selectWarningBackground)
        self.ui.pushButtonWT.clicked.connect(self.selectWarningText)
        self.ui.pushButtonCB.clicked.connect(self.selectCriticalBackground)
        self.ui.pushButtonCT.clicked.connect(self.selectCriticalText)
        self.ui.pushButtonDB.clicked.connect(self.selectDisabledBackground)
        self.ui.pushButtonDT.clicked.connect(self.selectDisabledText)
        self.ui.buttonBox.clicked.connect(self.clicked)
        # initial example buttons
        self.updateExampleNormalButton()
        # scripting init
        self.script = scriptInit(self)

    def criticalLevelChanged(self, value: int) -> None:
        warningLevel = self.ui.spinBoxWarningLevel.value()
        if warningLevel <= value:
            self.ui.spinBoxWarningLevel.setValue(value + 1)

    def warningLevelChanged(self, value: int) -> None:
        criticalLevel = self.ui.spinBoxCriticalLevel.value()
        if criticalLevel >= value:
            self.ui.spinBoxCriticalLevel.setValue(value - 1)

    def lunchSliderChanged(self, value: int) -> None:
        if value > self.ui.horizontalSliderDinner.value():
            self.ui.horizontalSliderDinner.setValue(value)

    def dinnerSliderChanged(self, value: int) -> None:
        if value < self.ui.horizontalSliderLunch.value():
            self.ui.horizontalSliderLunch.setValue(value)

    def selectWarningBackground(self) -> None:
        color = QColorDialog.getColor(QColor(self.ui.pushButtonWB.palette().color(self.ui.pushButtonWB.backgroundRole())), self)
        if not color.isValid():
            return
        self.ui.pushButtonWB.color = color.name()
        self.ui.pushButtonWB.setStyleSheet(f"background-color: {self.ui.pushButtonWB.color};")
        self.updateExampleButtons()

    def selectWarningText(self) -> None:
        color = QColorDialog.getColor(QColor(self.ui.pushButtonWT.color), self)
        if not color.isValid():
            return
        self.ui.pushButtonWT.color = color.name()
        self.ui.pushButtonWT.setStyleSheet(f"background-color: {self.ui.pushButtonWT.color};")
        self.updateExampleButtons()

    def selectCriticalBackground(self) -> None:
        color = QColorDialog.getColor(QColor(self.ui.pushButtonCB.color), self)
        if not color.isValid():
            return
        self.ui.pushButtonCB.color = color.name()
        self.ui.pushButtonCB.setStyleSheet(f"background-color: {self.ui.pushButtonCB.color};")
        self.updateExampleButtons()

    def selectCriticalText(self) -> None:
        color = QColorDialog.getColor(QColor(self.ui.pushButtonCT.color), self)
        if not color.isValid():
            return
        self.ui.pushButtonCT.color = color.name()
        self.ui.pushButtonCT.setStyleSheet(f"background-color: {self.ui.pushButtonCT.color};")
        self.updateExampleButtons()

    def selectDisabledBackground(self) -> None:
        color = QColorDialog.getColor(QColor(self.ui.pushButtonDB.color), self)
        if not color.isValid():
            return
        self.ui.pushButtonDB.color = color.name()
        self.ui.pushButtonDB.setStyleSheet(f"background-color: {self.ui.pushButtonDB.color};")
        self.updateExampleButtons()

    def selectDisabledText(self) -> None:
        color = QColorDialog.getColor(QColor(self.ui.pushButtonDT.color), self)
        if not color.isValid():
            return
        self.ui.pushButtonDT.color = color.name()
        self.ui.pushButtonDT.setStyleSheet(f"background-color: {self.ui.pushButtonDT.color};")
        self.updateExampleButtons()

    def updateExampleButtons(self) -> None:
        "Update example buttons with new selected colors"
        # warning level
        ss = f"background-color: {self.ui.pushButtonWB.color}; color: {self.ui.pushButtonWT.color};"
        self.ui.pushButtonExampleWL.setStyleSheet(ss)
        # critical level
        ss = f"background-color: {self.ui.pushButtonCB.color}; color: {self.ui.pushButtonCT.color};"
        self.ui.pushButtonExampleCL.setStyleSheet(ss)
        # disabled level
        ss = f"background-color: {self.ui.pushButtonDB.color}; color: {self.ui.pushButtonDT.color};"
        self.ui.pushButtonExampleDL.setStyleSheet(ss)
        
    def updateExampleNormalButton(self) -> None:
        "Update example button with normal colors"
        # normal level
        ss = f"background-color: {self.ui.colorComboBoxBackground.currentColor()}; color: {self.ui.colorComboBoxText.currentColor()};"
        self.ui.pushButtonExampleNL.setStyleSheet(ss)

    def clicked(self, button: QPushButton) -> None:
        "Call Apply on clicked Ok or Apply button"
        if self.ui.buttonBox.standardButton(button) == QDialogButtonBox.Apply:
            self.apply()

    @scriptMethod
    def apply(self) -> None:
        self.setting['lunch_start_time'] = self.ui.spinBoxLunch.value()
        self.setting['dinner_start_time'] = self.ui.spinBoxDinner.value()
        if self.ui.radioButtonTable.isChecked():
            self.setting['default_delivery_type'] = 'T'
        else:
            self.setting['default_delivery_type'] = 'A'
        if self.ui.radioButtonElectronic.isChecked():
            self.setting['default_payment_type'] = 'E'
        else:
            self.setting['default_payment_type'] = 'C'
        if self.ui.radioButtonEventBased.isChecked():
            self.setting['order_number_based_on'] = 'E'
        elif self.ui.radioButtonDayBased.isChecked():
            self.setting['order_number_based_on'] = 'D'
        else:
            self.setting['order_number_based_on'] = 'P' # day (P)art based
        self.setting['order_entry_ui'] = self.ui.comboBoxOrderUI.currentIndex()
        self.setting['order_list_tab_position'] = self.ui.comboBoxTabPosition.currentData()
        self.setting['warning_stock_level'] = self.ui.spinBoxWarningLevel.value()
        self.setting['critical_stock_level'] = self.ui.spinBoxCriticalLevel.value()
        self.setting['order_list_rows'] = self.ui.spinBoxOrderListRows.value()
        self.setting['order_list_columns'] = self.ui.spinBoxOrderListColumns.value()
        self.setting['order_list_spacing'] = self.ui.spinBoxOrderListSpacing.value()
        self.setting['order_list_font_family'] = self.ui.fontComboBoxOrderList.currentFont().family()
        self.setting['order_list_font_size'] = self.ui.spinBoxOrderListFontSize.value()
        self.setting['table_list_rows'] = self.ui.spinBoxTableListRows.value()
        self.setting['table_list_columns'] = self.ui.spinBoxTableListColumns.value()
        self.setting['table_list_spacing'] = self.ui.spinBoxTableListSpacing.value()
        self.setting['table_list_font_family'] = self.ui.fontComboBoxTableList.currentFont().family()
        self.setting['table_list_font_size'] = self.ui.spinBoxTableListFontSize.value()
        self.setting['use_table_list'] = self.ui.checkBoxUseTableList.isChecked()
        # colors
        self.setting['normal_background_color'] = self.ui.colorComboBoxBackground.currentColor()
        self.setting['normal_text_color'] = self.ui.colorComboBoxText.currentColor()
        self.setting['warning_background_color'] = self.ui.pushButtonWB.color
        self.setting['warning_text_color'] = self.ui.pushButtonWT.color
        self.setting['critical_background_color'] = self.ui.pushButtonCB.color
        self.setting['critical_text_color'] = self.ui.pushButtonCT.color
        self.setting['disabled_background_color'] = self.ui.pushButtonDB.color
        self.setting['disabled_text_color'] = self.ui.pushButtonDT.color
        # reports
        self.setting['print_customer_copy'] = self.ui.checkBoxCustomerCopy.isChecked()
        self.setting['print_department_copy'] = self.ui.checkBoxDepartmentCopy.isChecked()
        self.setting['print_cover_copy'] = self.ui.checkBoxCoverCopy.isChecked()
        self.setting['customer_copies'] = self.ui.spinBoxCustomerCopies.value() if self.ui.spinBoxCustomerCopies.isEnabled() else None
        self.setting['department_copies'] = self.ui.spinBoxDepartmentCopies.value() if self.ui.spinBoxDepartmentCopies.isEnabled else None
        self.setting['cover_copies'] = self.ui.spinBoxCoverCopies.value() if self.ui.spinBoxCoverCopies.isEnabled() else None
        self.setting['customer_report'] = self.ui.comboBoxCustomerReport.currentData() if self.ui.comboBoxCustomerReport.isEnabled() else None
        self.setting['department_report'] = self.ui.comboBoxDepartmentReport.currentData() if self.ui.comboBoxDepartmentReport.isEnabled() else None
        self.setting['cover_report'] = self.ui.comboBoxCoverReport.currentData() if self.ui.comboBoxCoverReport.isEnabled() else None
        self.setting['customer_printer_class'] = self.ui.comboBoxCustomerPrinter.currentData() if self.ui.comboBoxCustomerPrinter.isEnabled() else None
        self.setting['cover_printer_class'] = self.ui.comboBoxCoverPrinter.currentData() if self.ui.comboBoxCoverPrinter.isEnabled() else None
        self.setting['max_covers'] = self.ui.spinBoxMaxCovers.value()
        self.setting['automatic_show_variants'] = self.ui.checkBoxAutoVariants.isChecked()
        self.setting['manage_order_progress'] = self.ui.checkBoxOrderProgress.isChecked()
        self.setting['always_show_stock_inventory'] = self.ui.checkBoxShowInventory.isChecked()
        self.setting['mandatory_table_number'] = self.ui.checkBoxMandatoryTableNumber.isChecked()
        self.setting['check_inactivity'] = self.ui.checkBoxInactivity.isChecked()
        self.setting['inactivity_time'] = self.ui.spinBoxInactivityTime.value()
        self.setting['ordered_delivered_automatic_update'] = self.ui.groupBoxAutomaticUpdate.isChecked()
        self.setting['ordered_delivered_update_interval'] = self.ui.spinBoxAutomaticUpdateInterval.value()
        self.setting['print_ordered_delivered_report'] = self.ui.groupBoxOrderedDeliveredReport.isChecked()
        self.setting['ordered_delivered_copies'] = self.ui.spinBoxOrderedDeliveredCopies.value() if self.ui.spinBoxOrderedDeliveredCopies.isEnabled() else None
        self.setting['ordered_delivered_report'] = self.ui.comboBoxOrderedDeliveredReport.currentData() if self.ui.comboBoxOrderedDeliveredReport.isEnabled() else None
        self.setting['ordered_delivered_printer_class'] = self.ui.comboBoxOrderedDeliveredPrinterClass.currentData() if self.ui.comboBoxOrderedDeliveredPrinterClass.isEnabled() else None
        self.setting['inventory_warning_stock_level'] = self.ui.spinBoxInventoryWarningLevel.value()
        self.setting['inventory_critical_stock_level'] = self.ui.spinBoxInventoryCriticalLevel.value()
        self.setting['quantity_decimal_places'] = self.ui.spinBoxQuantityDecimals.value()
        self.setting['currency_symbol'] = self.ui.lineEditCurrencySymbol.text()
        # sanity checks
        if self.setting['print_customer_copy']:
            if not self.setting['customer_report'] or not self.setting['customer_printer_class']:
                title = _tr("MessageDialog", "Critical")
                msg = _tr("Setting", "If print customer copy is selected you must provide a customer report and printer class")
                QMessageBox.critical(self, title, msg)
                return False # avoid dialog close
        if self.setting['print_department_copy']:
            if not self.setting['department_report']:
                title = _tr("MessageDialog", "Critical")
                msg = _tr("Setting", "If print department copy is selected you must provide a department report")
                QMessageBox.critical(self, title, msg)
                return False # avoid dialog close
        if self.setting['print_cover_copy']:
            if not self.setting['cover_report'] or not self.setting['cover_printer_class']:
                title = _tr("MessageDialog", "Critical")
                msg = _tr("Setting", "If print cover copy is selected you must provide a cover report and printer class")
                QMessageBox.critical(self, title, msg)
                return False # avoid dialog close
        try:
            self.setting.save()
        except PyAppDBConcurrencyError:
            title = _tr("MessageDialog", "Critical")
            msg = _tr("Setting", "Record modified before update, reload and modify again")
            QMessageBox.critical(self, title, msg)
        except PyAppDBError as er:
            title = _tr("MessageDialog", "Critical")
            msg = f"{er.code}\n{er.message}"
            QMessageBox.critical(self, title, msg)
        return True

    @scriptMethod
    def accept(self) -> None:
        if self.apply():
            # save settings
            st = QSettings(self)
            st.setValue("DialogGeometry/Settings", self.saveGeometry())
        QDialog.accept(self)
