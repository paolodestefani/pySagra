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

"""Order entry

This module provides order entry dialog and required subcalsses/funtions

"""

# standard library
from enum import IntEnum
import logging
import warnings 
from decimal import Decimal 
from typing import Any
from typing import cast
from typing import Callable
from typing import Optional

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QSettings
from PySide6.QtCore import Slot
from PySide6.QtGui import QFont
from PySide6.QtGui import QAction 
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QButtonGroup
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QSizePolicy

# application modules
from App import session
from App import currentIcon
from App.Core.ExceptionHandler import gui_exception_context
from App.Core.L10n import fromCurrency
from App.Core.L10n import toCurrency
from App.Core.Gui import TP
from App.Database.Setting import Setting
from App.Database.Setting import SettingClass
from App.Database.Event import get_event_from_date
from App.Database.CashDesk import get_cash_desk_description
from App.Database.Department import department_list
from App.Database.Department import get_department_printer_class
from App.Database.Department import department_takeaway_list
from App.Database.Department import get_department_desc
from App.Database.SeatMap import table_list
from App.Database.SeatMap import table_exists
from App.Database.Item import item_list
from App.Database.Item import is_for_takeaway
from App.Database.Item import get_item_desc
from App.Database.Printer import get_printer_name
from App.Database.Item import get_variants
from App.Database.Order import Order
from App.Database.Order import get_orders_issued
from App.Report.Order import printOrderReport
from App.Report.Order import printOrderCoverReport
from App.Report.Order import printOrderDepartmentReport
from App.Report.Order import printStockUnloadReport
from App.Core.L10n import _tr
from App.Widget.Dialog import DateTimeInputDialog
from App.Widget.Control import ButtonSeat
from App.Widget.Control import ButtonItem
from App.Ui.ChooseVariantsDialog import Ui_ChooseVariantsDialog



# logger
logger = logging.getLogger(__name__)


class two(IntEnum):
    ID = 0
    VARIANTS = 1
    DESCRIPTION = 2
    QUANTITY = 3
    PRICE = 4
    AMOUNT = 5


# launch main order entry dialog
def orderEntry(action: QAction, checked: bool = False) -> None:
    "Open order dialog"
    logger.info('Starting order entry dialog')
    mw = session['mainwin']
    # exit if no event available
    if not session['event_id']:
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderDialog', 'No event available, for order entry '
                                'is necessary to setup an event for the current date'))
        return
    setting = SettingClass()
    Ui_OrderDialog: Callable
    if setting['order_entry_ui'] == 0:
        from App.Ui.OrderDialog0 import Ui_OrderDialog0 as Ui_OrderDialog
    elif setting['order_entry_ui'] == 1:
        from App.Ui.OrderDialog1 import Ui_OrderDialog1 as Ui_OrderDialog
    elif setting['order_entry_ui'] == 2:
        from App.Ui.OrderDialog2 import Ui_OrderDialog2 as Ui_OrderDialog
    else:
        return
    dlg = BaseOrderDialog(mw, Ui_OrderDialog)
    dlg.show()
    logger.info('Order entry dialog shown')


# item variant selection

class VariantCheckBox(QCheckBox):
    """Custom QCheckBox that carries an associated price adjustment."""
    
    def __init__(self, parent: Optional[QWidget], desc: str, priced: float) -> None:
        super().__init__(parent)
        self.priceDelta = priced
        if priced > 0.0:
            self.setText(f"{desc} (+{toCurrency(priced)})")
        else:
            self.setText(desc)


class ChooseVariantDialog(QDialog):
    """Dialog for item variants selection."""
    
    def __init__(self, parent: QWidget, item: str, variants: list) -> None:
        super().__init__(parent)
        self.ui = Ui_ChooseVariantsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(item)
        self.bg = QButtonGroup(self)
        self.bg.setExclusive(False)
        for variant, delta in variants:
            # Pass None as parent since the layout will manage the ownership hierarchy
            v = VariantCheckBox(None, variant, float(delta)) # delta from db is Decimal  
            self.bg.addButton(v)
            self.ui.layout.addWidget(v)

    def getVariants(self) -> tuple[str, float]:
        """Return a string of selected variants and the total price delta."""
        variants: list[str] = []
        price_delta = 0.0
        # Gather selected variants and aggregate price adjustments
        for i in self.bg.buttons():
            button_instance = cast(Any, i)
            if button_instance.isChecked():
                variants.append(button_instance.text())
                price_delta += button_instance.priceDelta
        # Append free-text variants if provided by the user
        if self.ui.lineEditFreeVariant.text().strip():
            variants.append(self.ui.lineEditFreeVariant.text().strip())
            
        return " ".join(variants), price_delta


#---------------------#
#-- main dialog box --#
#---------------------#

class BaseOrderDialog(QDialog):
    "Order dialog"
        
    def __init__(self, parent: QWidget, uidialog: Callable) -> None:
        super().__init__(parent)
        self.ui = uidialog()
        self.ui.setupUi(self)
        self.setting = Setting()
        # Restore window geometry
        st = QSettings()
        if st.value("OrderDialogGeometry"):
            self.restoreGeometry(st.value("OrderDialogGeometry"))
        # Window flags configuration
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog |
                            Qt.WindowType.WindowMinMaxButtonsHint |
                            Qt.WindowType.WindowCloseButtonHint)
        # Dialog static icons and translations
        self.ui.pushButtonTablesSwitch.setIcon(currentIcon['order_switch'])
        self.ui.pushButtonConfirm.setIcon(currentIcon['order_ok'])
        self.ui.pushButtonCancel.setIcon(currentIcon['order_cancel'])
        self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Order'))
        # Idle time control system
        if self.setting['check_inactivity']:
            self.idleTimer = QTimer(self)
            self.idleTimer.timeout.connect(self.resetAdvice)
            self.idleTimer.start(self.setting['inactivity_time'] * 1000)
        # Delivery mode radio button group
        self.ui.buttonGroupDelivery = QButtonGroup(self)
        self.ui.buttonGroupDelivery.addButton(self.ui.radioButtonTable)
        self.ui.buttonGroupDelivery.addButton(self.ui.radioButtonTakeAway)
        # Quantity selector button group
        self.ui.buttonGroupQuantity = QButtonGroup(self)
        for i in (self.ui.radioButton1, self.ui.radioButton5, self.ui.radioButton10):
            self.ui.buttonGroupQuantity.addButton(i)
        # Define department layout tabs orientation
        self.ui.tabWidgetList.setTabPosition(TP[self.setting['order_list_tab_position'] or 'N'][1])
        # Grid parameters and properties initialization
        self.ui.list_rows = self.setting['order_list_rows']
        self.ui.list_columns = self.setting['order_list_columns']
        self.ui.tables_list_rows = self.setting['table_list_rows']
        self.ui.tables_list_columns = self.setting['table_list_columns']
        # Order list table widget structural parameters
        self.ui.twheader = [_tr('OrderDialog', "ID"),
                            _tr('OrderDialog', "Variants"),
                            _tr('OrderDialog', "Item"),
                            _tr('OrderDialog', "Quantity"),
                            _tr('OrderDialog', "Price"),
                            _tr('OrderDialog', "Amount")]
        self.ui.tabWidgetOrder.setColumnCount(len(self.ui.twheader))
        self.ui.tabWidgetOrder.setSortingEnabled(False)
        self.ui.tabWidgetOrder.setHorizontalHeaderLabels(self.ui.twheader)
        self.ui.tabWidgetOrder.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ui.tabWidgetOrder.hideColumn(two.ID)
        self.ui.tabWidgetOrder.hideColumn(two.VARIANTS)
        self.ui.tabWidgetOrder.setColumnWidth(two.DESCRIPTION, 250)
        self.ui.tabWidgetOrder.setColumnWidth(two.QUANTITY, 70)
        self.ui.tabWidgetOrder.setColumnWidth(two.PRICE, 70)
        self.ui.tabWidgetOrder.setColumnWidth(two.AMOUNT, 70)
        self.ui.doubleSpinBoxTotal.setValue(0.0)
        # Department note buttons structural binding
        self.ui.depnote = dict()
        self.ui.bgnotes = QButtonGroup(self)
        for (b, (i, t)) in zip((self.ui.pushButtonDepartmentNote1,
                                self.ui.pushButtonDepartmentNote2,
                                self.ui.pushButtonDepartmentNote3,
                                self.ui.pushButtonDepartmentNote4,
                                self.ui.pushButtonDepartmentNote5),
                               department_list()):
            b.setEnabled(True)
            b.setText(t)
            self.ui.bgnotes.addButton(b, i)
        self.ui.bgnotes.buttonClicked.connect(self.bgNotesClicked)
        # TABLES LOGICAL CONTAINER (Will be populated exclusively inside resetDialog)
        self.ui.bgt = QButtonGroup(self)
        # Core signal/slot connections
        self.ui.radioButtonTakeAway.toggled[bool].connect(self.tableTakeAway)
        self.ui.spinBoxCovers.valueChanged.connect(self.checkCovers)
        self.ui.pushButtonTablesSwitch.clicked.connect(self.tablesOrder)
        self.ui.pushButtonShowLevel.toggled.connect(self.toggleLevel)
        self.ui.tabWidgetOrder.cellClicked.connect(self.orderCellClicked)
        self.ui.checkBoxElectronicPayment.toggled.connect(self.electronicPaymentToggled)
        self.ui.pushButtonConfirm.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.resetDialog)
        self.ui.doubleSpinBoxDiscount.valueChanged.connect(self.recalcTotals)
        self.ui.doubleSpinBoxCash.valueChanged.connect(self.recalcTotals)
        self.ui.lineEditBarCode.editingFinished.connect(self.processWebOrder)
        # System Actions and Keyboard Shortcuts
        ced = QAction(_tr('OrderDialog', 'Change Event and date'), self)
        ced.setShortcut('Ctrl+F12')
        ced.triggered.connect(self.changeEventDate)
        self.addAction(ced)
        self.dateTimeDiff: Optional[int] = None # date time difference for event date change in seconds (int)
        sfb = QAction(_tr('OrderDialog', 'Set focus on web order input'), self)
        sfb.setShortcut('Ctrl+F11')
        sfb.triggered.connect(lambda: self.ui.lineEditBarCode.setFocus())
        self.addAction(sfb)
        # System status clock
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        # Refresh window contextual assets
        self.updateWindowTitle()
        # Trigger the initial full population via resetDialog
        self.resetDialog()
    
    def updateWindowTitle(self) -> None:
        "Update window title and cash desk description"
        cd = get_cash_desk_description()
        if not cd:
            cd = _tr('OrderDialog', 'cash desk name to set')
        self.ui.labelCashDeskDescription.setText(cd)
        txt = _tr('OrderDialog', "Company: {} User: {} Event: {} Cash Desk: {}  [Press ESC to quit]").format(
            str(session.get('company_description') or ''),
            str(session.get('app_user_code') or ''),
            str(session.get('event_description') or ''),
            str(cd)
        )
        self.setWindowTitle(txt)
        
    def changeEventDate(self) -> None:
        "Change current date/event"
        dateTime, ok = DateTimeInputDialog(_tr('OrderDialog', 'Select the date for event selection:'))
        if not ok:
            return
        # set datedifference for current date and selected date, to show correct time in order dialog and print correct date in order report
        if dateTime and dateTime.isValid():
            self.dateTimeDiff = QDateTime.currentDateTime().secsTo(dateTime)
        else:
            self.dateTimeDiff = None
        dt = QDateTime.currentDateTime()
        dt = dt.addSecs(self.dateTimeDiff or 0) # consider date time difference
        session['event_id'], session['event_description'] = get_event_from_date(dt)
        self.updateWindowTitle()

    def tableTakeAway(self, state) -> None:
        "Enable/disable tab widget item (departments) for takeaway"
        if state is True: # = takeaway
            self.ui.lineEditTable.setText('')
            self.ui.lineEditTable.setDisabled(True)
            self.ui.spinBoxCovers.setDisabled(True)
            self.ui.pushButtonTablesSwitch.setDisabled(True)
            self.ui.lineEditCustomerName.setFocus()
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
            depta = department_takeaway_list()
            for i in range(self.ui.tabWidgetList.count()):
                if self.ui.tabWidgetList.tabText(i) in depta:
                    self.ui.tabWidgetList.widget(i).setEnabled(True)
                else:
                    self.ui.tabWidgetList.widget(i).setDisabled(True)
        else: # = table
            self.ui.lineEditTable.setEnabled(True)
            self.ui.spinBoxCovers.setEnabled(True)
            if self.setting['use_table_list']:
                self.ui.pushButtonTablesSwitch.setEnabled(True)
                self.ui.stackedWidgetTableOrder.setCurrentIndex(1)
            for i in range(self.ui.tabWidgetList.count()):
                self.ui.tabWidgetList.widget(i).setEnabled(True)

    def resetAdvice(self) -> None:
        "Reset dialog advice from idle timer"
        self.idleTimer.stop()
        message = _tr("OrderDialog", "Warning: No order inserted since {} seconds.\n"
                      "It is recommended to update the window data, "
                      "Update it now ?").format(self.setting['inactivity_time'])
        if QMessageBox.question(self,
                                _tr("OrderDialog", "Question"),
                                message,
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                ) == QMessageBox.StandardButton.Yes:
            self.resetDialog()
        self.idleTimer.start()  # restart timer anyway

    def showTime(self) -> None:
        "Show time on a fixed format"
        dt = QDateTime.currentDateTime()
        dt = dt.addSecs(self.dateTimeDiff or 0) # consider date time difference
        if (dt.time().second() % 2) == 0: # flashing ':'
            text = dt.toString('dd.MM.yyyy  hh:mm')
        else:
            text = dt.toString('dd.MM.yyyy  hh mm')
        self.ui.lcdNumberTime.display(text)

    def checkCovers(self, value) -> None:
        "Check covers value against max covers setting and show warning if exceeded"
        if value > self.setting['max_covers']:
            msg = _tr("OrderDialog", "Warning: the number of covers is greater than {}").format(self.setting['max_covers'])
            QMessageBox.warning(self,
                                _tr("OrderDialog", "Warning"),
                                msg)
            self.ui.spinBoxCovers.setFocus()

    def tablesOrder(self) -> None:
        "Switch between tables grid and order list"
        if not self.setting['use_table_list']:
            return
        if self.ui.stackedWidgetTableOrder.currentIndex() == 0:
            self.ui.stackedWidgetTableOrder.setCurrentIndex(1)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Order'))
        else:
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Tables'))

    def toggleLevel(self, toggled) -> None:
        "Hide/unhide stock level in list buttons"
        for b in self.ui.bgi.buttons():
            if toggled:
                b.showLevel()
            else:
                b.hideLevel()

    def resetDialog(self) -> None:
        """Setup initial dialog's values and regenerate dynamic UI elements."""
        # Exit if no event is available for the current date
        if not session['event_id']:
            QMessageBox.warning(session['mainwin'],
                                _tr('MessageDialog', 'Warning'),
                                _tr('OrderDialog', 'No event available. For order entry '
                                    'it is necessary to setup an event for the current date.'))
            st = QSettings()
            st.setValue("OrderDialogGeometry", self.saveGeometry())
            QDialog.reject(self)
            return  # Stop execution if validation fails
        # Warn the user if there are items already entered in the order
        if self.ui.tabWidgetOrder.rowCount() != 0:
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    _tr('OrderDialog', "There are items already entered, "
                                        "the item list will be cleared. Proceed anyway ?"),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                return
        # table grid buttons regeneration with new data from database
        # 1. Clear the previous table button group signals if they exists
        # Suppress the PySide6 RuntimeWarning during initial empty disconnects
        if hasattr(self.ui, 'bgt') and self.ui.bgt is not None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                try:
                    self.ui.bgt.buttonClicked.disconnect(self.tableButtonClicked)
                except (RuntimeError, TypeError):
                    pass
        # 2. Explicitly remove and destroy old table buttons/widgets from the grid layout
        if self.ui.gridLayoutTables is not None:
            while self.ui.gridLayoutTables.count() > 0:
                layout_item = self.ui.gridLayoutTables.takeAt(0)
                widget_to_remove = layout_item.widget()
                if widget_to_remove is not None:
                    widget_to_remove.deleteLater()
        # 3. Re-initialize the table button group
        self.ui.bgt = QButtonGroup(self)
        self.ui.bgt.setExclusive(True)  # Tables usually operate in exclusive selection mode
        # 4. Populate the grid with active tables from database/list
        success = False
        with gui_exception_context(self, _tr('OrderDialog', "Loading tables from database")):
            for table_title, row_pos, col_pos, text_color, bg_color, unavailable in table_list():
                if row_pos is None or col_pos is None:
                    continue
                table_font = QFont(self.setting['table_list_font_family'], 
                                   self.setting['table_list_font_size'], 
                               QFont.Weight.Bold if not unavailable else QFont.Weight.Normal)
                btn_seat = ButtonSeat(self, table_title, table_font, text_color, bg_color, unavailable)
                btn_seat.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                # Use a unique identifier if table_list() provides an ID, otherwise use a placeholder
                self.ui.bgt.addButton(btn_seat)  
                self.ui.gridLayoutTables.addWidget(btn_seat, row_pos, col_pos)
            # 5. Fill the remaining empty cells of the grid layout with spacer widgets
            for r in range(1, self.ui.tables_list_rows + 1):
                for c in range(1, self.ui.tables_list_columns + 1):
                    if self.ui.gridLayoutTables.itemAtPosition(r, c) is None:
                        empty_placeholder = QWidget(self)
                        empty_placeholder.setMinimumWidth(50)
                        empty_placeholder.setMinimumHeight(50)
                        empty_placeholder.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                        self.ui.gridLayoutTables.addWidget(empty_placeholder, r, c)
            success = True
        if not success:
            return  # Stop execution if loading tables fails
        # 6. Connect the new button group to our click handler
        self.ui.bgt.buttonClicked.connect(self.tableButtonClicked)
        # Setup input widgets based on the default delivery type
        if self.setting['default_delivery_type'] == 'T':  # Tables
            self.ui.radioButtonTable.setChecked(True)
            self.ui.lineEditTable.setEnabled(True)
            self.ui.lineEditTable.clear()
            self.ui.lineEditCustomerName.setEnabled(True)
            self.ui.lineEditCustomerName.clear()
            self.ui.spinBoxCovers.setEnabled(True)
            self.ui.spinBoxCovers.setValue(0)
            self.ui.pushButtonTablesSwitch.setEnabled(self.setting['use_table_list'])
            self.ui.stackedWidgetTableOrder.setCurrentIndex(1 if self.setting['use_table_list'] else 0)
        else:  # Takeaway
            self.ui.radioButtonTakeAway.setChecked(True)
            self.ui.lineEditTable.setDisabled(True)
            self.ui.lineEditTable.clear()
            self.ui.lineEditCustomerName.setEnabled(True)
            self.ui.lineEditCustomerName.clear()
            self.ui.spinBoxCovers.setEnabled(False)
            self.ui.spinBoxCovers.setValue(0)
            self.ui.pushButtonTablesSwitch.setDisabled(True)
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
        # Handle default payment type checkbox
        self.ui.checkBoxElectronicPayment.setChecked(self.setting['default_payment_type'] == 'E')
        # defaut web order flag
        self.ui.checkBoxWebOrder.setChecked(False)
        # 1. CLEANUP TABS CORRECTLY (Prevents memory leaks in PySide6)
        while self.ui.tabWidgetList.count() != 0:
            tab_widget = self.ui.tabWidgetList.widget(0)
            self.ui.tabWidgetList.removeTab(0)
            if tab_widget:
                tab_widget.deleteLater()
        # 2. FAST SQUASH OF ORDER TABLE ROWS
        self.ui.tabWidgetOrder.setRowCount(0)
        # Handle specific stock and variants setting combinations
        if self.setting['automatic_show_variants']:
            self.ui.pushButtonVariants.setDisabled(True)
        if self.setting['always_show_stock_inventory']:
            self.ui.pushButtonShowLevel.setDisabled(True)
        # Reset totals and financial spinboxes
        self.ui.radioButton1.setChecked(True)
        self.ui.doubleSpinBoxSubTotal.setValue(0.0)
        self.ui.doubleSpinBoxDiscount.setValue(0.0)
        self.ui.doubleSpinBoxTotal.setValue(0.0)
        self.ui.doubleSpinBoxCash.setValue(0.0)
        self.ui.doubleSpinBoxChange.setValue(0.0)
        # 3. DISCONNECT AND RE-INITIALIZE ITEM BUTTON GROUP
        # Suppress the PySide6 RuntimeWarning during initial empty disconnects
        if hasattr(self.ui, 'bgi') and self.ui.bgi is not None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                try:
                    self.ui.bgi.buttonClicked.disconnect(self.buttonClicked)
                except (RuntimeError, TypeError):
                    pass
        self.ui.bgi = QButtonGroup(self)
        self.ui.bgi.setExclusive(False)
        # Dynamic generation of departments and item buttons
        success = False
        with gui_exception_context(self, _tr('OrderDialog', "Loading items from database")):
            for dept_id, dept_name in department_list(include_menu=True):
                tab_pane = QWidget()
                grid_layout = QGridLayout()
                grid_layout.setSpacing(self.setting['order_list_spacing'])
                for (item_id, item_desc, item_price, row_pos, col_pos, has_stock, stock_val, txt_color, bg_color,
                     has_vars, current_lvl) in item_list(session['event_id'], dept_id):
                    if not row_pos or not col_pos:
                        message = _tr('OrderDialog', "Item '{}' lacks layout position settings, will not be created.").format(item_desc)
                        QMessageBox.information(self, _tr('OrderDialog', "Warning"), message)
                        continue
                    btn = ButtonItem(self, item_desc, txt_color, bg_color)
                    btn.id = item_id
                    btn.price = float(item_price) # from Decimal to float
                    btn.sc = has_stock
                    btn.hasVariants = has_vars
                    btn.level = float(current_lvl) # from Decimal to float
                    btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
                    self.ui.bgi.addButton(btn, item_id)
                    grid_layout.addWidget(btn, row_pos, col_pos)
                # Fill the remaining empty layout grid cells with generic spacer widgets
                for r in range(1, self.ui.list_rows + 1):
                    for c in range(1, self.ui.list_columns + 1):
                        if grid_layout.itemAtPosition(r, c) is None:
                            empty_widget = QWidget(self)
                            empty_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
                            grid_layout.addWidget(empty_widget, r, c)
                tab_pane.setLayout(grid_layout)
                self.ui.tabWidgetList.addTab(tab_pane, dept_name)
            success = True
        if not success:            
            return  # Stop execution if loading items fails
        # Connect click event handler to the newly generated item button group
        self.ui.bgi.buttonClicked.connect(self.buttonClicked)
        # Enable or disable tabs selectively for takeaway mode constraints
        if self.ui.radioButtonTakeAway.isChecked():
            takeaway_depts = department_takeaway_list()
            for i in range(self.ui.tabWidgetList.count()):
                is_takeaway_valid = self.ui.tabWidgetList.tabText(i) in takeaway_depts
                self.ui.tabWidgetList.widget(i).setEnabled(is_takeaway_valid)
        # Clear specific notes and reset operational icons
        self.ui.depnote.clear()
        for button in self.ui.bgnotes.buttons():
            button.setIcon(currentIcon['empty'])
        # Initialize or extend the application idle timer system
        if self.setting['check_inactivity']:
            self.idleTimer.start()
        # Establish window focus context on the primary table entry field
        self.ui.lineEditTable.setFocus()

    # def buttonClicked(self, button: Any, ivars: str = "", priced: float = 0.0, web: bool = False) -> None:
    #     """React to an item button click, manage variants, and update the order table."""
    #     btn = cast(Any, button)
    #     # 1. HANDLE ITEM VARIANTS
    #     if btn.hasVariants and not web: # orders from web has already variants and prices
    #         if not ivars:
    #             if (not self.ui.pushButtonVariants.isEnabled()) or self.ui.pushButtonVariants.isChecked():
    #                 item_description = getattr(btn, 'description', '')
    #                 dlg = ChooseVariantDialog(self, item_description, get_variants(btn.id))
    #                 rv = dlg.exec()
    #                 if rv:
    #                     ivars, variant_price = dlg.getVariants()
    #                     priced = variant_price or 0.0
    #                 dlg.deleteLater()  
    #                 if not rv:
    #                     return
    #             if self.ui.pushButtonVariants.isEnabled():
    #                 self.ui.pushButtonVariants.setChecked(False)
    #     if not btn.isEnabled():
    #         return
    #     # 2. DETERMINE QUANTITY TO ADD
    #     qty = float(self.ui.buttonGroupQuantity.checkedButton().text())
    #     self.ui.radioButton1.setChecked(True)
    #     # 3. LOOK FOR EXISTING SAME ITEM & VARIANT IN THE ORDER GRID
    #     for i in range(self.ui.tabWidgetOrder.rowCount()):
    #         order_item_id = self.ui.tabWidgetOrder.item(i, two.ID)
    #         order_item_vars = self.ui.tabWidgetOrder.item(i, two.VARIANTS)
    #         if order_item_id and order_item_vars:
    #             same_id = (btn.id == int(order_item_id.data(Qt.ItemDataRole.DisplayRole)))
    #             same_vars = (ivars == order_item_vars.data(Qt.ItemDataRole.DisplayRole))
    #             if same_id and same_vars:
    #                 qty_item = self.ui.tabWidgetOrder.item(i, two.QUANTITY)
    #                 price_item = self.ui.tabWidgetOrder.item(i, two.PRICE)
    #                 amount_item = self.ui.tabWidgetOrder.item(i, two.AMOUNT)
    #                 if qty_item and price_item and amount_item:
    #                     old_qty = float(qty_item.data(Qt.ItemDataRole.DisplayRole))
    #                     if btn.sc and (btn.level - qty < 0):
    #                         return 
    #                     # Update quantity
    #                     qty_item.setData(Qt.ItemDataRole.DisplayRole, old_qty + qty)
    #                     # Recalculate amount
    #                     raw_data = price_item.data(Qt.ItemDataRole.DisplayRole) # becausefromCurrency expects a string input
    #                     price_val = float(raw_data) if raw_data is not None else 0.0
    #                     price_decimal = price_val
    #                     qty_decimal = old_qty + qty
    #                     amount_item.setData(Qt.ItemDataRole.DisplayRole, toCurrency(qty_decimal * price_decimal))
    #                     self.recalcTotals()
    #                     if btn.sc:
    #                         btn.level = btn.level - qty
    #                     return
    #     # 4. ITEM NOT FOUND: INSERT NEW ROW INTO THE TABLE
    #     row = self.ui.tabWidgetOrder.rowCount()
    #     self.ui.tabWidgetOrder.insertRow(row)
    #     # Column: ID
    #     cell_id = QTableWidgetItem(str(btn.id))
    #     cell_id.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #     self.ui.tabWidgetOrder.setItem(row, two.ID, cell_id)
    #     # Column: VARIANTS
    #     cell_vars = QTableWidgetItem(ivars)
    #     cell_vars.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #     self.ui.tabWidgetOrder.setItem(row, two.VARIANTS, cell_vars)
    #     # Column: DESCRIPTION
    #     full_desc = btn.description + " " + ivars if hasattr(btn, 'description') else ivars
    #     cell_desc = QTableWidgetItem(full_desc)
    #     cell_desc.setToolTip(full_desc)
    #     cell_desc.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #     self.ui.tabWidgetOrder.setItem(row, two.DESCRIPTION, cell_desc)
    #     # Column: QUANTITY
    #     cell_qty = QTableWidgetItem(str(qty))
    #     cell_qty.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #     cell_qty.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    #     self.ui.tabWidgetOrder.setItem(row, two.QUANTITY, cell_qty)
    #     # Column: PRICE
    #     total_unit_price = btn.price + priced
    #     cell_price = QTableWidgetItem(toCurrency(total_unit_price))
    #     cell_price.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #     cell_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    #     self.ui.tabWidgetOrder.setItem(row, two.PRICE, cell_price)
    #     # Column: TOTAL AMOUNT
    #     cell_amount = QTableWidgetItem(toCurrency(float(qty) * total_unit_price))
    #     cell_amount.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #     cell_amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    #     self.ui.tabWidgetOrder.setItem(row, two.AMOUNT, cell_amount)
    #     # UI adjustments
    #     self.ui.tabWidgetOrder.scrollToBottom()
    #     self.recalcTotals()
    #     # 5. UPDATE STOCK LEVEL TRACKING ON THE BUTTON
    #     if btn.sc:
    #         btn.level = btn.level - qty
            
    def buttonClicked(self, button: Any, ivars: str = "", priced: float = 0.0, web: bool = False) -> None:
        """React to an item button click, manage variants, and update the order table."""
        btn = cast(Any, button)
        
        # 1. HANDLE ITEM VARIANTS
        if btn.hasVariants and not web: # orders from web has already variants and prices
            if not ivars:
                if (not self.ui.pushButtonVariants.isEnabled()) or self.ui.pushButtonVariants.isChecked():
                    item_description = getattr(btn, 'description', '')
                    dlg = ChooseVariantDialog(self, item_description, get_variants(btn.id))
                    rv = dlg.exec()
                    if rv:
                        ivars, variant_price = dlg.getVariants()
                        priced = variant_price or 0.0
                    dlg.deleteLater()  
                    if not rv:
                        return
                if self.ui.pushButtonVariants.isEnabled():
                    self.ui.pushButtonVariants.setChecked(False)
        if not btn.isEnabled():
            return
            
        # 2. DETERMINE QUANTITY TO ADD
        qty = float(self.ui.buttonGroupQuantity.checkedButton().text())
        self.ui.radioButton1.setChecked(True)
        
        # --- OTTIMIZZAZIONE GRAFICA: Congeliamo la tabella per evitare lag visivi ---
        self.ui.tabWidgetOrder.setUpdatesEnabled(False)
        self.ui.tabWidgetOrder.blockSignals(True)
        
        try:
            # 3. LOOK FOR EXISTING SAME ITEM & VARIANT IN THE ORDER GRID
            for i in range(self.ui.tabWidgetOrder.rowCount()):
                order_item_id = self.ui.tabWidgetOrder.item(i, two.ID)
                order_item_vars = self.ui.tabWidgetOrder.item(i, two.VARIANTS)
                
                if order_item_id and order_item_vars:
                    # Recuperiamo l'ID nativo (se salvato come int o stringa)
                    same_id = (btn.id == int(order_item_id.data(Qt.ItemDataRole.DisplayRole)))
                    same_vars = (ivars == order_item_vars.data(Qt.ItemDataRole.DisplayRole))
                    
                    if same_id and same_vars:
                        qty_item = self.ui.tabWidgetOrder.item(i, two.QUANTITY)
                        price_item = self.ui.tabWidgetOrder.item(i, two.PRICE)
                        amount_item = self.ui.tabWidgetOrder.item(i, two.AMOUNT)
                        
                        if qty_item and price_item and amount_item:
                            # Leggiamo la vecchia quantità dal UserRole (se presente) o dal DisplayRole
                            old_qty_raw = qty_item.data(Qt.ItemDataRole.UserRole)
                            old_qty = float(old_qty_raw) if old_qty_raw is not None else float(qty_item.data(Qt.ItemDataRole.DisplayRole))
                            
                            if btn.sc and (btn.level - qty < 0):
                                return 
                            
                            new_qty = old_qty + qty
                            
                            # Aggiorna QUANTITÀ nel UserRole (float) e DisplayRole (testo/numero)
                            qty_item.setData(Qt.ItemDataRole.UserRole, new_qty)
                            qty_item.setData(Qt.ItemDataRole.DisplayRole, str(new_qty)) # O mantieni il tuo formato visivo
                            
                            # Recupera il PREZZO dal UserRole (evita stringhe, virgole e localizzazione)
                            price_raw = price_item.data(Qt.ItemDataRole.UserRole)
                            if price_raw is not None:
                                price_val = float(price_raw)
                            else:
                                # Fallback se la riga era stata creata col vecchio metodo
                                raw_data = price_item.data(Qt.ItemDataRole.DisplayRole)
                                price_val = float(raw_data) if raw_data is not None else 0.0
                            
                            # Ricalcola l'IMPORTO TOTALE riga
                            new_amount = new_qty * price_val
                            
                            # Salva l'IMPORTO nel UserRole come float e nel DisplayRole formattato localizzato
                            amount_item.setData(Qt.ItemDataRole.UserRole, new_amount)
                            amount_item.setData(Qt.ItemDataRole.DisplayRole, toCurrency(new_amount))
                            
                            self.recalcTotals()
                            if btn.sc:
                                btn.level = btn.level - qty
                            return

            # 4. ITEM NOT FOUND: INSERT NEW ROW INTO THE TABLE
            row = self.ui.tabWidgetOrder.rowCount()
            self.ui.tabWidgetOrder.insertRow(row)
            
            # Column: ID
            cell_id = QTableWidgetItem(str(btn.id))
            cell_id.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.ui.tabWidgetOrder.setItem(row, two.ID, cell_id)
            
            # Column: VARIANTS
            cell_vars = QTableWidgetItem(ivars)
            cell_vars.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.ui.tabWidgetOrder.setItem(row, two.VARIANTS, cell_vars)
            
            # Column: DESCRIPTION
            full_desc = btn.description + " " + ivars if hasattr(btn, 'description') else ivars
            cell_desc = QTableWidgetItem(full_desc)
            cell_desc.setToolTip(full_desc)
            cell_desc.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.ui.tabWidgetOrder.setItem(row, two.DESCRIPTION, cell_desc)
            
            # Column: QUANTITY
            cell_qty = QTableWidgetItem(str(qty))
            cell_qty.setData(Qt.ItemDataRole.UserRole, qty) # <-- Salva float pulito
            cell_qty.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            cell_qty.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.ui.tabWidgetOrder.setItem(row, two.QUANTITY, cell_qty)
            
            # Column: PRICE
            total_unit_price = float(btn.price + priced)
            cell_price = QTableWidgetItem(toCurrency(total_unit_price))
            cell_price.setData(Qt.ItemDataRole.UserRole, total_unit_price) # <-- Salva float pulito (ignora la virgola di toCurrency)
            cell_price.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            cell_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.ui.tabWidgetOrder.setItem(row, two.PRICE, cell_price)
            
            # Column: TOTAL AMOUNT
            total_amount = qty * total_unit_price
            cell_amount = QTableWidgetItem(toCurrency(total_amount))
            cell_amount.setData(Qt.ItemDataRole.UserRole, total_amount) # <-- Salva float pulito
            cell_amount.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            cell_amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.ui.tabWidgetOrder.setItem(row, two.AMOUNT, cell_amount)
            
            # UI adjustments
            self.ui.tabWidgetOrder.scrollToBottom()
            self.recalcTotals()
            
            # 5. UPDATE STOCK LEVEL TRACKING ON THE BUTTON
            if btn.sc:
                btn.level = btn.level - qty

        finally:
            # --- RIPRISTINO GRAFICA: Sblocchiamo la tabella e aggiorniamo lo schermo in un colpo solo ---
            self.ui.tabWidgetOrder.blockSignals(False)
            self.ui.tabWidgetOrder.setUpdatesEnabled(True)
            self.ui.tabWidgetOrder.viewport().update()

            
    def tableButtonClicked(self, button) -> None:
        """When a table button is clicked, set the table number in the input field
        and switch to order view."""
        if button.unavailable:
            return
        self.ui.lineEditTable.setText(button.text())
        self.tablesOrder()

    # def orderCellClicked(self, row: int, column: int) -> None:
    #     """Decrease item quantity or remove row from order when a cell is clicked."""
    #     qty = float(self.ui.buttonGroupQuantity.checkedButton().text())
    #     self.ui.radioButton1.setChecked(True)
    #     # Safe extraction of table items
    #     qty_item = self.ui.tabWidgetOrder.item(row, two.QUANTITY)
    #     price_item = self.ui.tabWidgetOrder.item(row, two.PRICE)
    #     amount_item = self.ui.tabWidgetOrder.item(row, two.AMOUNT)
    #     id_item = self.ui.tabWidgetOrder.item(row, two.ID)
    #     if not (qty_item and price_item and amount_item and id_item):
    #         return  # Safety fallback if cells are not properly initialized
    #     old_qty = float(qty_item.data(Qt.ItemDataRole.DisplayRole))
    #     new_qty = old_qty - qty
    #     # 1. UPDATE STOCK LEVEL TRACKING ON BUTTONS FIRST
    #     item_id = int(id_item.data(Qt.ItemDataRole.DisplayRole))
    #     for b in self.ui.bgi.buttons():
    #         btn = cast(Any, b)
    #         if btn.id == item_id:
    #             if btn.sc:
    #                 btn.level = btn.level + qty
    #                 print(btn.level)
    #             break  # Found the item, no need to keep looping
    #     # 2. IF QUANTITY DROPS TO ZERO OR LESS, REMOVE ROW AND EXIT IMMEDIATELY
    #     if new_qty <= 0.0:
    #         self.ui.tabWidgetOrder.removeRow(row)
    #         self.recalcTotals()
    #         return  # Stop execution here to prevent reading from a deleted row
    #     # 3. OTHERWISE, AGGIOUPDATE CELL VALUES
    #     # Blocca i segnali per evitare che Qt ridisegni la tabella a ogni singola modifica
    #     self.ui.tabWidgetOrder.blockSignals(True)
    #     try:
    #         qty_item.setData(Qt.ItemDataRole.DisplayRole, new_qty)
    #         # Estrazione sicura della stringa
    #         raw_price_data = price_item.data(Qt.ItemDataRole.DisplayRole)
    #         price_float = float(raw_price_data) if raw_price_data is not None else 0.0
    #         # Chiama fromCurrency una sola volta per clic
    #         #price_decimal = fromCurrency(price_str)
    #         total_amount = new_qty * price_float
    #         # Aggiorna il totale visibile
    #         amount_item.setData(Qt.ItemDataRole.DisplayRole, total_amount)
    #     finally:
    #         # Riattiva i segnali per consentire un unico rendering visivo combinato
    #         self.ui.tabWidgetOrder.blockSignals(False)
            
    #     self.recalcTotals()


    def orderCellClicked(self, row: int, column: int) -> None:
        """Decrease item quantity or remove row from order when a cell is clicked."""
        qty = float(self.ui.buttonGroupQuantity.checkedButton().text())
        self.ui.radioButton1.setChecked(True)
        
        # Safe extraction of table items
        qty_item = self.ui.tabWidgetOrder.item(row, two.QUANTITY)
        price_item = self.ui.tabWidgetOrder.item(row, two.PRICE)
        amount_item = self.ui.tabWidgetOrder.item(row, two.AMOUNT)
        id_item = self.ui.tabWidgetOrder.item(row, two.ID)
        
        if not (qty_item and price_item and amount_item and id_item):
            return  # Safety fallback if cells are not properly initialized
            
        # --- OTTIMIZZAZIONE GRAFICA: Congeliamo l'interfaccia subito ---
        self.ui.tabWidgetOrder.setUpdatesEnabled(False)
        self.ui.tabWidgetOrder.blockSignals(True)
        
        try:
            # Leggiamo la vecchia quantità dal UserRole (se presente) o dal DisplayRole come fallback
            old_qty_raw = qty_item.data(Qt.ItemDataRole.UserRole)
            old_qty = float(old_qty_raw) if old_qty_raw is not None else float(qty_item.data(Qt.ItemDataRole.DisplayRole))
            
            new_qty = old_qty - qty
            
            # 1. UPDATE STOCK LEVEL TRACKING ON BUTTONS FIRST
            item_id = int(id_item.data(Qt.ItemDataRole.DisplayRole))
            for b in self.ui.bgi.buttons():
                btn = cast(Any, b)
                if btn.id == item_id:
                    if btn.sc:
                        btn.level = btn.level + qty
                        print(btn.level)
                    break  # Found the item, no need to keep looping
                    
            # 2. IF QUANTITY DROPS TO ZERO OR LESS, REMOVE ROW AND EXIT IMMEDIATELY
            if new_qty <= 0.0:
                self.ui.tabWidgetOrder.removeRow(row)
                self.recalcTotals()
                return  # Stop execution here to prevent reading from a deleted row
                
            # 3. OTHERWISE, UPDATE CELL VALUES
            # Aggiorna QUANTITÀ nel UserRole (float) e DisplayRole (testo)
            qty_item.setData(Qt.ItemDataRole.UserRole, new_qty)
            qty_item.setData(Qt.ItemDataRole.DisplayRole, str(new_qty))
            
            # Recupera il PREZZO dal UserRole (evita stringhe, virgole e localizzazione)
            price_raw = price_item.data(Qt.ItemDataRole.UserRole)
            if price_raw is not None:
                price_float = float(price_raw)
            else:
                # Fallback se la riga era stata creata col vecchio metodo
                raw_price_data = price_item.data(Qt.ItemDataRole.DisplayRole)
                price_float = float(raw_price_data) if raw_price_data is not None else 0.0
                
            # Calcola il nuovo importo totale di riga
            total_amount = new_qty * price_float
            
            # Salva l'IMPORTO nel UserRole come float e nel DisplayRole formattato localizzato
            amount_item.setData(Qt.ItemDataRole.UserRole, total_amount)
            amount_item.setData(Qt.ItemDataRole.DisplayRole, toCurrency(total_amount))
            
            self.recalcTotals()
            
        finally:
            # --- RIPRISTINO GRAFICA: Sblocchiamo tutto alla fine ---
            self.ui.tabWidgetOrder.blockSignals(False)
            self.ui.tabWidgetOrder.setUpdatesEnabled(True)
            self.ui.tabWidgetOrder.viewport().update()

    
    def bgNotesClicked(self, button: Any) -> None:
        """Open a multi-line input dialog to edit department-specific notes."""
        # Get the internal ID assigned to the clicked button
        bid = self.ui.bgnotes.id(button)
        # Safe extraction: fallback to an empty string if no note exists yet (prevents PySide6 crash)
        txt = self.ui.depnote.get(bid) or ""
        # Prompt the user with a multi-line text input dialog
        text, ok = QInputDialog.getMultiLineText(
            self,
            _tr("OrderDialog", "Department note"),
            _tr("OrderDialog", "Message text for {}").format(get_department_desc(bid)),
            txt
        )
        if ok:
            # Store the note, or set to None if the user cleared the text area
            self.ui.depnote[bid] = text.strip() or None
        # Update the button icon dynamically based on whether a note is currently active
        if self.ui.depnote.get(bid):
            button.setIcon(currentIcon['order_note'])
        else:
            button.setIcon(currentIcon['empty'])

    @Slot()
    def processWebOrder(self) -> None:
        """Fill order form based on web order details or QRC data parsed from barcode scanner"""
        # Disconnect editingFinished to avoid calling it 2 times (return pressed and lost focus)
        try:
            self.ui.lineEditBarCode.editingFinished.disconnect(self.processWebOrder)
        except (RuntimeError, TypeError):
            pass  # Fail-safe if it wasn't connected
        try:
            value = self.ui.lineEditBarCode.text().strip()
            if not value:  # Can happen when losing focus without inserting anything
                return
            # Reset the dialog container state
            self.resetDialog()
            # Parse QRC CSV structural segments
            try:
                segments = value.split(';')
                qtype, qdelivery, qtable, qname, qcovers, qemail = segments[:6]
                # Extract repeating item attributes from index 6 onwards
                items_part = segments[6:]
                itm = items_part[0::4] 
                var = items_part[1::4] 
                prd = items_part[2::4]
                qty = items_part[3::4]
            except Exception as er:
                msg = _tr('OrderDialog', "Unrecognized QRC structure:") + f"\n{str(er)}"
                QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                return
            # Sanity checks for fundamental parameters
            err: list[str] = []
            if qtype != 'PSQRC':
                err.append(_tr('OrderDialog', "Unrecognized QRC format:") + f" {qtype}")
            if qdelivery not in ('T', 'A'):
                err.append(_tr('OrderDialog', "Unrecognized delivery option:") + f" {qdelivery}")
            if qcovers and not qcovers.isdigit():
                err.append(_tr('OrderDialog', "Unrecognized covers number:") + f" {qcovers}") 
            if err:
                msg = _tr('OrderDialog', "Unrecognized parameters:") + f"\n{'\n'.join(err)}"
                QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                return           
            # Move UI layout to order view widget
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Tables'))
            if qdelivery == 'T':
                self.ui.radioButtonTable.setChecked(True)
            else:
                self.ui.radioButtonTakeAway.setChecked(True)
            self.ui.lineEditTable.setText(qtable or '')
            self.ui.lineEditCustomerName.setText(qname or '')
            self.ui.spinBoxCovers.setValue(int(qcovers or 0))
            self.ui.lineEditCustomerContact.setText(qemail or '')
            unavailable: dict[str, int] = dict()
            # matching the QR code loop constraints.
            self.ui.radioButton1.setChecked(True)
            # Iterate through extracted order lines
            for i, v, p, q in zip(itm, var, prd, qty):
                if not i.isdigit():
                    msg = _tr('OrderDialog', "Unrecognized item id:") + f" {i}"
                    QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                    return
                if not q.isdigit():   
                    msg = _tr('OrderDialog', "Unrecognized quantity:") + f" {q}"
                    QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                    return        
                # Repeat item insertion loop based on QR code quantity requirements
                for j in range(int(q)):
                    raw_button = self.ui.bgi.button(int(i))
                    if raw_button is None:
                        QMessageBox.critical(self,
                                            _tr("MessageDialog", "Critical"),
                                            _tr('OrderDialog', "Item NOT available in buttons' grid, web order skipped."))
                        return 
                    # Cast to Any to prevent mypy exceptions on custom attributes
                    btn = cast(Any, raw_button)
                    if btn.isEnabled():
                        self.buttonClicked(btn, v, float(p or '0.0'), web = True) # web = true -> avoid variant selection
                    else:
                        btn_text = str(btn.text())
                        unavailable[btn_text] = unavailable.get(btn_text, 0) + 1
            # Warn the operator of unavailable items that were skipped
            if unavailable:
                msg = _tr("OrderDialog", "These items are not available and not included in the order:\n")
                msg += "\n".join(["{:>2}  {:<20}".format(count, name).replace('\n', ' ')
                                 for name, count in unavailable.items()])
                QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
            # Set the digital weborder indicator flag to active
            self.ui.checkBoxWebOrder.setChecked(True)
        finally:
            # Always clean up inputs and re-establish the core signal hook
            self.ui.lineEditBarCode.clear()
            self.ui.lineEditBarCode.editingFinished.connect(self.processWebOrder)

    def electronicPaymentToggled(self, checked) -> None:
        "Enable/disable cash/change for electronic payment"
        if checked:
            self.ui.doubleSpinBoxCash.setValue(0.0)
            self.ui.doubleSpinBoxCash.setDisabled(True)
            self.ui.doubleSpinBoxChange.setValue(0.0)
            self.ui.doubleSpinBoxChange.setDisabled(True)
        else:
            self.ui.doubleSpinBoxCash.setValue(0.0)
            self.ui.doubleSpinBoxCash.setEnabled(True)
            self.ui.doubleSpinBoxChange.setValue(0.0)
            self.ui.doubleSpinBoxChange.setEnabled(True)

    # def recalcTotals(self) -> None:
    #     """Recalculate order subtotal, total, and change using Decimal precision for UI spinboxes."""
    #     subtotal = Decimal('0.0')
    #     # 1. SUM ALL ROW AMOUNTS FROM THE ORDER GRID
    #     for i in range(self.ui.tabWidgetOrder.rowCount()):
    #         amount_item = self.ui.tabWidgetOrder.item(i, two.AMOUNT)
    #         if amount_item:
    #             raw_amount_data = amount_item.data(Qt.ItemDataRole.DisplayRole)
    #             # Ensure str cast for fromCurrency to satisfy mypy
    #             amount_val = fromCurrency(str(raw_amount_data) if raw_amount_data is not None else '0.0')
    #             subtotal += Decimal(str(amount_val))
    #     # Update subtotal spinbox (cast Decimal to float for QDoubleSpinBox compatibility)
    #     self.ui.doubleSpinBoxSubTotal.setValue(float(subtotal))
    #     # 2. EXTRACT DISCOUNT AND CASH INPUT VALUES AS DECIMAL
    #     discount = Decimal(str(self.ui.doubleSpinBoxDiscount.value()))
    #     cash = Decimal(str(self.ui.doubleSpinBoxCash.value()))
    #     # 3. CALCULATE NET TOTAL AND CHANGE AMOUNT
    #     total = subtotal - discount
    #     # Ensure change doesn't drop below zero using Decimal comparison
    #     change = cash - total
    #     if change < Decimal('0.0'):
    #         change = Decimal('0.0')
    #     # 4. UPDATE THE REMAINING INTERFACE WIDGETS
    #     self.ui.doubleSpinBoxTotal.setValue(float(total))
    #     self.ui.doubleSpinBoxChange.setValue(float(change))


    # def recalcTotals(self) -> None:
    #     """Recalculate order subtotal, total, and change for UI spinboxes."""
    #     subtotal = 0.0
    #     # 1. SUM ALL ROW AMOUNTS FROM THE ORDER GRID
    #     for i in range(self.ui.tabWidgetOrder.rowCount()):
    #         amount_item = self.ui.tabWidgetOrder.item(i, two.AMOUNT)
    #         if amount_item:
    #             raw_amount_data = amount_item.data(Qt.ItemDataRole.DisplayRole)
    #             price_str = float(raw_amount_data) if raw_amount_data is not None else 0.0
    #             # accumulate directly using the Decimal returned by fromCurrency
    #             #subtotal += fromCurrency(price_str)
    #             subtotal += price_str
    #     # Update subtotal spinbox (cast Decimal to float for QDoubleSpinBox compatibility)
    #     self.ui.doubleSpinBoxSubTotal.setValue(subtotal)
    #     # 2. EXTRACT DISCOUNT AND CASH INPUT VALUES AS DECIMAL
    #     # Convertiamo direttamente il float restituito dallo spinbox in Decimal (senza str())
    #     discount = self.ui.doubleSpinBoxDiscount.value()
    #     cash = self.ui.doubleSpinBoxCash.value()
    #     # 3. CALCULATE NET TOTAL AND CHANGE AMOUNT
    #     total = subtotal - discount
    #     change = max(cash - total, 0.0)
    #     # 4. UPDATE THE REMAINING INTERFACE WIDGETS
    #     self.ui.doubleSpinBoxTotal.setValue(total)
    #     self.ui.doubleSpinBoxChange.setValue(change)

    def recalcTotals(self) -> None:
        """Recalculate order subtotal, total, and change for UI spinboxes."""
        subtotal = 0.0
        
        # 1. SUM ALL ROW AMOUNTS FROM THE ORDER GRID
        for i in range(self.ui.tabWidgetOrder.rowCount()):
            amount_item = self.ui.tabWidgetOrder.item(i, two.AMOUNT)
            if amount_item:
                # Recupera il float puro dal UserRole (immune a virgole, punti e toCurrency)
                raw_amount_data = amount_item.data(Qt.ItemDataRole.UserRole)
                if raw_amount_data is not None:
                    price_float = float(raw_amount_data)
                else:
                    # Fallback se la riga era stata creata col vecchio metodo
                    fallback_data = amount_item.data(Qt.ItemDataRole.DisplayRole)
                    price_float = float(fallback_data) if fallback_data is not None else 0.0
                    
                subtotal += price_float

        # Blocchiamo temporaneamente i segnali degli spinbox per velocizzare la scrittura
        self.ui.doubleSpinBoxSubTotal.blockSignals(True)
        self.ui.doubleSpinBoxTotal.blockSignals(True)
        self.ui.doubleSpinBoxChange.blockSignals(True)
        
        try:
            # Update subtotal spinbox
            self.ui.doubleSpinBoxSubTotal.setValue(subtotal)
            
            # 2. EXTRACT DISCOUNT AND CASH INPUT VALUES
            discount = self.ui.doubleSpinBoxDiscount.value()
            cash = self.ui.doubleSpinBoxCash.value()
            
            # 3. CALCULATE NET TOTAL AND CHANGE AMOUNT
            total = subtotal - discount
            change = max(cash - total, 0.0)
            
            # 4. UPDATE THE REMAINING INTERFACE WIDGETS
            self.ui.doubleSpinBoxTotal.setValue(total)
            self.ui.doubleSpinBoxChange.setValue(change)
            
        finally:
            # Sblocchiamo i segnali per ripristinare il normale comportamento della maschera
            self.ui.doubleSpinBoxSubTotal.blockSignals(False)
            self.ui.doubleSpinBoxTotal.blockSignals(False)
            self.ui.doubleSpinBoxChange.blockSignals(False)

    
    def accept(self) -> None:
        """Validate, generate, save, and print the completed order."""
        # ----------------------------------------------------------
        # SANITY CHECKS FIRST
        # ----------------------------------------------------------
        # Check if the order contains at least one item
        if self.ui.tabWidgetOrder.rowCount() == 0:
            msg = _tr('OrderDialog', "No item inserted!")
            QMessageBox.warning(self, _tr('MessageDialog', "Warning"), msg)
            return
        # Check for mandatory table number when table delivery is selected
        if (self.setting['mandatory_table_number']
                and self.ui.radioButtonTable.isChecked()
                and not self.ui.lineEditTable.text().strip()):
            msg = _tr("OrderDialog", "The table number is missing!")
            QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
            self.ui.lineEditTable.setFocus()
            return
        # Validate that the table number actually exists in the predefined list
        if (self.setting['mandatory_table_number'] and self.setting['use_table_list']
                and self.ui.radioButtonTable.isChecked()):
            if not table_exists(self.ui.lineEditTable.text().strip()):
                msg = _tr("OrderDialog", "The table number does not exist, use it anyway ?")
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        msg,
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                    self.ui.lineEditTable.setFocus()
                    return
        # Validate that a customer name is provided for takeaway operations
        if self.ui.radioButtonTakeAway.isChecked() and not self.ui.lineEditCustomerName.text().strip():
            msg = _tr("OrderDialog", "Customer's name is missing!")
            QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
            self.ui.lineEditCustomerName.setFocus()
            return
        # Double check if covers/seats are missing despite being a table order
        if self.ui.radioButtonTable.isChecked() and not self.ui.spinBoxCovers.value():
            msg = _tr("OrderDialog", "Warning: there are no seats even "
                                     "though delivery to the table has been indicated,\n"
                                     "do you want to correct it?")
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    msg,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.ui.spinBoxCovers.setFocus()
                self.ui.spinBoxCovers.selectAll()
                return
        # Prevent financial inconsistencies where discount exceeds subtotal
        subtotal_check = self.ui.doubleSpinBoxSubTotal.value()
        discount_check = self.ui.doubleSpinBoxDiscount.value()
        if discount_check > subtotal_check:
            msg = _tr("OrderDialog", "Discount amount greater than the total amount!")
            QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
            self.ui.doubleSpinBoxDiscount.setFocus()
            self.ui.doubleSpinBoxDiscount.selectAll()
            return
        # Filter out items that are restricted from takeaway delivery
        if self.ui.radioButtonTakeAway.isChecked():
            nogood: list[str] = []
            for i in range(self.ui.tabWidgetOrder.rowCount()):
                item_cell = self.ui.tabWidgetOrder.item(i, two.ID)
                if item_cell:
                    item_id = int(item_cell.data(Qt.ItemDataRole.DisplayRole))
                    if not is_for_takeaway(item_id):
                        nogood.append(get_item_desc(item_id))
            if nogood:
                msg = _tr('OrderDialog', "Warning: the following items are not available for take away:\n"
                                         "- {}\n\nDo i proceed anyway ?".format("\n- ".join(nogood)))
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        msg,
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                    return
        # ---------------------------------------------------------------------
        # VALIDATIONS PASSED: EXECUTE ORDER SUBMISSION
        # ---------------------------------------------------------------------
        order = Order()
        order.header['date_time'] = QDateTime.currentDateTime().addSecs(self.dateTimeDiff or 0)
        order.header['cash_desk'] = self.ui.labelCashDeskDescription.text()
        order.header['delivery'] = 'T' if self.ui.radioButtonTable.isChecked() else 'A'
        order.header['is_electronic_payment'] = self.ui.checkBoxElectronicPayment.isChecked()
        order.header['is_from_web'] = self.ui.checkBoxWebOrder.isChecked()
        order.header['table_num'] = self.ui.lineEditTable.text().strip() or None
        order.header['customer_name'] = self.ui.lineEditCustomerName.text().strip() or None
        order.header['customer_contact'] = self.ui.lineEditCustomerContact.text().strip() or None
        order.header['covers'] = int(self.ui.spinBoxCovers.value())
        # Safe extraction of float metrics to highly accurate Decimal formats
        order.header['total_amount'] = Decimal(str(self.ui.doubleSpinBoxSubTotal.value()))
        order.header['discount'] = Decimal(str(self.ui.doubleSpinBoxDiscount.value()))
        order.header['cash'] = Decimal(str(self.ui.doubleSpinBoxCash.value()))
        order.header['change'] = Decimal(str(self.ui.doubleSpinBoxChange.value()))
        # Extract structured items information from the layout grid rows
        for i in range(self.ui.tabWidgetOrder.rowCount()):
            id_cell = self.ui.tabWidgetOrder.item(i, two.ID)
            vars_cell = self.ui.tabWidgetOrder.item(i, two.VARIANTS)
            qty_cell = self.ui.tabWidgetOrder.item(i, two.QUANTITY)
            price_cell = self.ui.tabWidgetOrder.item(i, two.PRICE)
            amount_cell = self.ui.tabWidgetOrder.item(i, two.AMOUNT)
            if id_cell and vars_cell and qty_cell and price_cell and amount_cell:
                line: dict[str, Any] = dict()
                line['item_id'] = int(id_cell.data(Qt.ItemDataRole.DisplayRole))
                line['variants'] = vars_cell.data(Qt.ItemDataRole.DisplayRole) or None
                line['quantity'] = Decimal(qty_cell.data(Qt.ItemDataRole.DisplayRole))
                # Protect fromCurrency strings against mypy signature checks
                raw_price = price_cell.data(Qt.ItemDataRole.DisplayRole)
                raw_amount = amount_cell.data(Qt.ItemDataRole.DisplayRole)
                line['price'] = fromCurrency(raw_price if raw_price is not None else '0.0')
                line['amount'] = fromCurrency(raw_amount if raw_amount is not None else '0.0')
                order.lines.append(line)
        # Handle real-time stock allocation checks
        ofsi = order.out_of_stock()
        if ofsi:
            items = [str(item) for item in ofsi]
            msg = (_tr('OrderDialog', "Warning: these items are unavailable "
                                      "for the current order:\n\n"
                                      "- {0}\n\nDo i proceed anyway ?").format("\n- ".join(items)))
            if QMessageBox.question(self,
                                    _tr('MessageDialog', "Question"),
                                    msg,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                return
        # Map department situational notes context
        order.depnote.update(self.ui.depnote) 
        # ---------------------------------------------------------------------
        # DATABASE COMMIT OPERATION
        # ---------------------------------------------------------------------
        success = False
        with gui_exception_context(self, _tr('OrderDialog', "Saving order to database")):
            ti, used_dep = order.insert()  # ti = order header reference key ID
            success = True
        if not success:
            return
        # ---------------------------------------------------------------------
        # ASYNC ORDER PRINT REPORTS DISPATCH
        # ---------------------------------------------------------------------
        # Print customer receipt copy
        if self.setting['print_customer_copy']:
            with gui_exception_context(self, _tr('OrderDialog', "Printing order customer copy")):
                printer = get_printer_name(self.setting['customer_printer_class'], session['hostname'])
                printOrderReport(ti, printer)
        # covers copy
        if self.setting['print_cover_copy'] and order.header['delivery'] == 'T':
            with gui_exception_context(self, _tr('OrderDialog', "Printing order cover copy")):
                printer = get_printer_name(self.setting['cover_printer_class'], session['hostname'])
                printOrderCoverReport(ti, printer)
        # ---------------------------------------------------------------------
        # SEPARATE DEPARTMENT COPIES PRINT DISPATCH
        # ---------------------------------------------------------------------
        if self.setting['print_department_copy']:
            with gui_exception_context(self, _tr('OrderDialog', "Printing order department copies")):
                for dept_id in used_dep:
                    if dept_id is None:
                        continue  # Skip if department ID is not valid
                    prncls = get_department_printer_class(dept_id)
                    if not prncls:
                        continue
                    printer = get_printer_name(prncls, session['hostname'])
                    printOrderDepartmentReport(ti, dept_id, printer)
        # ---------------------------------------------------------------------
        # STOCK UNLOAD / ORDERED DELIVERED REPORT SYSTEM
        # ---------------------------------------------------------------------
        if self.setting['print_ordered_delivered_report']:
            with gui_exception_context(self, _tr('OrderDialog', "Printing ordered delivered report")):
                printer = get_printer_name(self.setting['ordered_delivered_printer_class'], session['hostname'])
                printStockUnloadReport(self.setting['ordered_delivered_report'],
                                       printer,
                                       self.setting['ordered_delivered_copies'],
                                       order.header['event'],
                                       order.header['stat_order_date'],
                                       order.header['stat_order_day_part'])
        # ---------------------------------------------------------------------
        # INTERFACE RESET AND CLEANUP
        # ---------------------------------------------------------------------
        # Fast, safe and clean squashing of all rows in the order table
        self.ui.tabWidgetOrder.setRowCount(0)
        # Trigger full interface and button grids rejuvenation
        self.resetDialog()
        
    def reject(self) -> None:
        "Close the dialog"
        msg = _tr("OrderDialog", "Do you want to exit the order entry?")
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                msg,
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, # butons
                                QMessageBox.StandardButton.No # default botton
                                ) == QMessageBox.StandardButton.Yes:
            # save geometry
            st = QSettings()
            st.setValue("OrderDialogGeometry", self.saveGeometry())
            super().reject()

# EOF
