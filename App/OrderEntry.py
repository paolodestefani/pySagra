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
import copy
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
from App.Core.Gui import get_tab_positions
from App.Database.Setting import Setting
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
from App.Database.Item import get_item_parts
from App.Database.Printer import get_printer_name
from App.Database.Item import get_variants
from App.Database.Order import Order
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

class vw(IntEnum):
    TABLE = 0
    ORDER = 1

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
    title = action.text()
    auth = action.data()
    if not auth[2]: # no execute permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderEntry', 'No access right to this feature'))
        return
    # exit if no event available
    if not session['event_id']:
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('OrderEntry', 'No event available, for order entry '
                                'is necessary to setup an event for the current date'))
        return
    setting = Setting()
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
    """
    Custom QCheckBox that carries an associated price adjustment stored in integer
    """
    
    def __init__(self, parent: Optional[QWidget], desc: str, price_delta: int, decimals: int) -> None:
        super().__init__(parent)
        # Store the clean raw properties directly in memory as integer cents
        self.variant_desc = desc
        self.price_delta = price_delta

        if price_delta > 0:
            displayed_price = session['qlocale'].toString(float(price_delta / 10 ** decimals), 'f', decimals)
            self.setText(f"{desc} (+{displayed_price})")
        else:
            self.setText(desc)


class ChooseVariantDialog(QDialog):
    """
    Dialog for item variants selection utilizing integer calculations
    """
    
    def __init__(self, parent: QWidget, item: str, variants: list, decimals) -> None:
        super().__init__(parent)
        self._decimals = decimals
        self.ui = Ui_ChooseVariantsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(item)
        self.ui.doubleSpinBoxPriceDelta.setDecimals(decimals)
        
        # Initialize button group to track variant checkboxes
        self.bg = QButtonGroup(self)
        self.bg.setExclusive(False)
        
        # price_delta is already an integer
        for variant_name, price_delta in variants:
            v = VariantCheckBox(None, variant_name, price_delta, decimals)   
            self.bg.addButton(v)
            self.ui.layout.addWidget(v)

    def getVariants(self) -> tuple[str, int]:
        """Return a string of selected variant names and the accumulated price delta in Decimal"""
        selected_descriptions: list[str] = []
        total_price_delta = 0
        
        # gather selected variants and aggregate integer price adjustments
        for btn in self.bg.buttons():
            checkbox = cast(VariantCheckBox, btn)
            if checkbox.isChecked():
                selected_descriptions.append(checkbox.variant_desc)
                total_price_delta += checkbox.price_delta
                
        # append free-text custom variants and price delta if provided by the user
        free_text = self.ui.lineEditFreeVariant.text().strip()
        total_price_delta += int(round(self.ui.doubleSpinBoxPriceDelta.value() * 10 ** self._decimals))
        if free_text:
            selected_descriptions.append(free_text)
            
        return " ".join(selected_descriptions), total_price_delta


#---------------------#
#-- main dialog box --#
#---------------------#
class BaseOrderDialog(QDialog):
    """
    Order dialog. Manages tables, items, and item availability. 
    Quantities and prices are in integer numbers with virtual decimal points.
    """
        
    def __init__(self, parent: QWidget, uidialog: Callable) -> None:
        super().__init__(parent)
        self.ui = uidialog()
        self.ui.setupUi(self)
        self.setting = Setting()
        
        # restore window geometry
        st = QSettings()
        if st.value("OrderEntry/Geometry"):
            self.restoreGeometry(st.value("OrderEntry/Geometry"))
            
        # window flags configuration
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog |
                            Qt.WindowType.WindowMinMaxButtonsHint |
                            Qt.WindowType.WindowCloseButtonHint)
                            
        # dialog static icons and translations
        self.ui.pushButtonTablesSwitch.setIcon(currentIcon['order_switch'])
        self.ui.pushButtonConfirm.setIcon(currentIcon['order_ok'])
        self.ui.pushButtonCancel.setIcon(currentIcon['order_cancel'])
        self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Order'))
        
        # idle time control system
        if self.setting['check_inactivity']:
            self.idleTimer = QTimer(self)
            self.idleTimer.timeout.connect(self.resetAdvice)
            self.idleTimer.start(self.setting['inactivity_time'] * 1000)
            
        # delivery mode radio button group
        self.ui.buttonGroupDelivery = QButtonGroup(self)
        self.ui.buttonGroupDelivery.addButton(self.ui.radioButtonTable)
        self.ui.buttonGroupDelivery.addButton(self.ui.radioButtonTakeAway)
        
        # quantity selector button group
        self.ui.buttonGroupQuantity = QButtonGroup(self)
        for i in (self.ui.radioButton1, self.ui.radioButton5, self.ui.radioButton10):
            self.ui.buttonGroupQuantity.addButton(i)
            
        # define department layout tabs orientation
        self.ui.tabWidgetList.setTabPosition(get_tab_positions()[self.setting['order_list_tab_position'] or 'N'][1])
        
        # grid parameters and properties initialization
        self.ui.list_rows = self.setting['order_list_rows']
        self.ui.list_columns = self.setting['order_list_columns']
        self.ui.tables_list_rows = self.setting['table_list_rows']
        self.ui.tables_list_columns = self.setting['table_list_columns']
        
        # order list table widget structural parameters
        self.ui.twheader = [_tr('OrderEntry', "ID"),
                            _tr('OrderEntry', "Variants"),
                            _tr('OrderEntry', "Item"),
                            _tr('OrderEntry', "Quantity"),
                            _tr('OrderEntry', "Price"),
                            _tr('OrderEntry', "Amount")]
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
        # usefull in mac, prevent the flicker effect on selecting a row
        self.ui.tabWidgetOrder.horizontalHeader().setHighlightSections(False)
        
        # department note buttons structural binding
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
        
        # core signal/slot connections
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
        self.ui.doubleSpinBoxDiscount.valueChanged.connect(self.onDiscountChanged)

        # system Actions and Keyboard Shortcuts
        ced = QAction(_tr('OrderEntry', 'Change Event and date'), self)
        ced.setShortcut('Ctrl+F12')
        ced.triggered.connect(self.changeEventDate)
        self.addAction(ced)
        self.dateTimeDiff: Optional[int] = None # date time difference for event date change in seconds (int)
        
        sfb = QAction(_tr('OrderEntry', 'Set focus on web order input'), self)
        sfb.setShortcut('Ctrl+F11')
        sfb.triggered.connect(lambda: self.ui.lineEditBarCode.setFocus())
        self.addAction(sfb)
        
        # system status clock
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        
        # refresh window contextual assets
        self.updateWindowTitle()
        
        # detail order items mapping container -> key structure: (item_id, variant_string)
        self.order_lines: dict[tuple[int, str | None], dict[str, Any]] = {}
        # totals and subtotals
        self.current_subtotal_int: int  = 0
        self.current_discount_int: int  = 0
        self.current_total_int: int     = 0
        self.current_cash_int: int      = 0
        self.current_change_int: int    = 0
        # decimals factor
        self._qty_factor: int       = 0 # updated in resetDialog
        self._price_factor: int     = 0 # updated in resetDialog
        self._amount_factor: int    = 0 # updated in resetDialog
        # local inventory
        self._original_inventory: dict[int, Any] = {} 
        self._inventory: dict[int, Any] = {} # current inventory
        
        # trigger the initial full population via resetDialog
        self.resetDialog()

    def updateWindowTitle(self) -> None:
        "Update window title and cash desk description"
        cd = get_cash_desk_description()
        if not cd:
            cd = _tr('OrderEntry', 'cash desk name to set')
        self.ui.labelCashDeskDescription.setText(cd)
        txt = _tr('OrderEntry', "Company: {} User: {} Event: {} Cash Desk: {}  [Press ESC to quit]").format(
            str(session.get('company_description') or ''),
            str(session.get('app_user_code') or ''),
            str(session.get('event_description') or ''),
            str(cd)
        )
        self.setWindowTitle(txt)
        
    def changeEventDate(self) -> None:
        "Change current date/event"
        dateTime, ok = DateTimeInputDialog(_tr('OrderEntry', 'Select the date for event selection:'))
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
        message = _tr("OrderEntry", "Warning: No order inserted since {} seconds.\n"
                      "It is recommended to update the window data, "
                      "Update it now ?").format(self.setting['inactivity_time'])
        if QMessageBox.question(self,
                                _tr("OrderEntry", "Question"),
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
            msg = _tr("OrderEntry", "Warning: the number of covers is greater than {}").format(self.setting['max_covers'])
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                msg)
            self.ui.spinBoxCovers.setFocus()

    def tablesOrder(self) -> None:
        "Switch between tables grid and order list"
        if not self.setting['use_table_list']:
            return
        if self.ui.stackedWidgetTableOrder.currentIndex() == 0:
            self.ui.stackedWidgetTableOrder.setCurrentIndex(1)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderEntry', 'Order'))
        else:
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderEntry', 'Tables'))

    def toggleLevel(self, toggled) -> None:
        "Hide/unhide stock level in list buttons"
        for b in self.ui.bgi.buttons():
            if toggled:
                b.showLevel = True
            else:
                b.showLevel = False

    def resetDialog(self) -> None:
        """Setup initial dialog's values and regenerate dynamic UI elements."""
        # exit if no event is available for the current date
        if not session.get('event_id', None):
            QMessageBox.warning(session['mainwin'],
                                _tr('MessageDialog', 'Warning'),
                                _tr('OrderEntry', 'No event available. For order entry '
                                    'it is necessary to setup an event for the current date.'))
            st = QSettings()
            st.setValue("OrderEntry/Geometry", self.saveGeometry())
            QDialog.reject(self)
            return  # stop execution if validation fails
            
        # warn the user if there are items already entered in the order
        if self.ui.tabWidgetOrder.rowCount() != 0:
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    _tr('OrderEntry', "There are items already entered, "
                                        "the item list will be cleared. Proceed anyway ?"),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                return
        # update settings used allaround
        self.setting.reload()
        # clear totals
        self.current_subtotal_int   = 0
        self.current_discount_int   = 0
        self.current_total_int      = 0
        self.current_cash_int       = 0
        self.current_change_int     = 0
        # decimal factors
        self._qty_factor    = 10 ** self.setting['quantity_decimal_places']
        self._price_factor  = 10 ** self.setting['price_decimal_places']
        self._amount_factor = 10 ** self.setting['amount_decimal_places']
        self.ui.doubleSpinBoxSubTotal.setDecimals(self.setting['amount_decimal_places'])
        self.ui.doubleSpinBoxDiscount.setDecimals(self.setting['amount_decimal_places'])
        self.ui.doubleSpinBoxTotal.setDecimals(self.setting['amount_decimal_places'])
        self.ui.doubleSpinBoxCash.setDecimals(self.setting['amount_decimal_places'])
        self.ui.doubleSpinBoxChange.setDecimals(self.setting['amount_decimal_places'])
        # detail order items mapping container -> key structure: (item_id, variant_string or None)
        self.order_lines.clear()

        # table grid buttons regeneration with new data from database
        # clear the previous table button group signals if they exist
        # suppress the PySide6 RuntimeWarning during initial empty disconnects
        if hasattr(self.ui, 'bgt') and self.ui.bgt is not None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                try:
                    self.ui.bgt.buttonClicked.disconnect(self.tableButtonClicked)
                except (RuntimeError, TypeError):
                    pass
                    
        # explicitly remove and destroy old table buttons/widgets from the grid layout
        if self.ui.gridLayoutTables is not None:
            while self.ui.gridLayoutTables.count() > 0:
                layout_item = self.ui.gridLayoutTables.takeAt(0)
                widget_to_remove = layout_item.widget()
                if widget_to_remove is not None:
                    widget_to_remove.deleteLater()
                    
        # re-initialize the table button group
        self.ui.bgt = QButtonGroup(self)
        self.ui.bgt.setExclusive(True)  # tables operate in exclusive selection mode
        
        # populate the grid with active tables from database/list
        success = False
        with gui_exception_context(self, _tr('OrderEntry', "Loading tables from database")):
            for table_title, row_pos, col_pos, text_color, bg_color, unavailable in table_list():
                if row_pos is None or col_pos is None:
                    continue
                table_font = QFont(self.setting['table_list_font_family'], 
                                   self.setting['table_list_font_size'], 
                                   QFont.Weight.Bold if not unavailable else QFont.Weight.Normal)
                btn_seat = ButtonSeat(self, table_title, table_font, text_color, bg_color, unavailable)
                btn_seat.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                self.ui.bgt.addButton(btn_seat)  
                self.ui.gridLayoutTables.addWidget(btn_seat, row_pos, col_pos)
                
            # fill the remaining empty cells of the grid layout with spacer widgets
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
            return  # stop execution if loading tables fails
            
        # connect the new button group to our click handler
        self.ui.bgt.buttonClicked.connect(self.tableButtonClicked)
        
        # setup input widgets based on the default delivery type
        # tables
        if self.setting['default_delivery_type'] == 'T':  
            self.ui.radioButtonTable.setChecked(True)
            self.ui.lineEditTable.setEnabled(True)
            self.ui.spinBoxCovers.setEnabled(True)
            self.ui.spinBoxCovers.setValue(0)
            self.ui.pushButtonTablesSwitch.setEnabled(self.setting['use_table_list'])
            self.ui.stackedWidgetTableOrder.setCurrentIndex(vw.ORDER if self.setting['use_table_list'] else vw.TABLE)
        # takeaway
        else: 
            self.ui.radioButtonTakeAway.setChecked(True)
            self.ui.lineEditTable.setDisabled(True)
            self.ui.spinBoxCovers.setEnabled(False)
            self.ui.spinBoxCovers.setValue(0)
            self.ui.pushButtonTablesSwitch.setDisabled(True)
            self.ui.stackedWidgetTableOrder.setCurrentIndex(vw.TABLE)
        
        # common default
        self.ui.lineEditTable.clear()
        self.ui.lineEditCustomerName.setEnabled(True)
        self.ui.lineEditCustomerName.clear()
        self.ui.lineEditCustomerContact.clear()
            
        # handle default payment type checkbox
        is_electronic = (self.setting['default_payment_type'] == 'E')
        self.ui.checkBoxElectronicPayment.setChecked(is_electronic)
        
        # default web order flag
        self.ui.checkBoxWebOrder.setChecked(False)
        
        # CLEANUP TABS CORRECTLY (prevents memory leaks in PySide6)
        while self.ui.tabWidgetList.count() != 0:
            tab_widget = self.ui.tabWidgetList.widget(0)
            self.ui.tabWidgetList.removeTab(0)
            if tab_widget:
                tab_widget.deleteLater()
                
        # FAST SQUASH OF ORDER TABLE ROWS
        self.ui.tabWidgetOrder.setRowCount(0)
        
        # handle specific stock and variants setting combinations
        if self.setting['automatic_show_variants']:
            self.ui.pushButtonVariants.setDisabled(True)
        if self.setting['always_show_stock_inventory']:
            self.ui.pushButtonShowLevel.setDisabled(True)
            
        # reset totals and financial spinboxes
        self.ui.radioButton1.setChecked(True)
        self.ui.doubleSpinBoxSubTotal.setValue(0.0)
        self.ui.doubleSpinBoxDiscount.setValue(0.0)
        self.ui.doubleSpinBoxTotal.setValue(0.0)
        self.ui.doubleSpinBoxCash.setValue(0.0)
        self.ui.doubleSpinBoxChange.setValue(0.0)
        
        # DISCONNECT AND RE-INITIALIZE ITEM BUTTON GROUP
        if hasattr(self.ui, 'bgi') and self.ui.bgi is not None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                try:
                    self.ui.bgi.buttonClicked.disconnect(self.buttonClicked)
                except (RuntimeError, TypeError):
                    pass
        self.ui.bgi = QButtonGroup(self)
        self.ui.bgi.setExclusive(False)
        
        # dynamic generation of departments and item buttons including inventory
        self._original_inventory.clear()
        success = False
        with gui_exception_context(self, _tr('OrderEntry', "Loading items from database")):
            for dept_id, dept_name in department_list(include_menu=True):
                tab_pane = QWidget()
                grid_layout = QGridLayout()
                grid_layout.setSpacing(self.setting['order_list_spacing'])
                
                # rebuild the grid layout populating item buttons per department
                for (is_salable, item_type, item_id, item_desc, item_price, row_pos, col_pos,
                     has_inventory, has_delivered, txt_color, bg_color, has_vars, available_qty
                     ) in item_list(session['event_id'], dept_id):
                    
                    qty = int(round(available_qty * self._qty_factor)) if available_qty is not None else 0
                        
                    # instantiate custom ButtonItem with native parameters for salable items
                    if is_salable:
                        if not row_pos or not col_pos:
                            message = _tr('OrderEntry', "Item '{}' lacks layout position settings, will not be created.").format(item_desc)
                            QMessageBox.information(self, _tr('OrderEntry', "Warning"), message)
                            continue
                        
                        btn_item = ButtonItem(self, item_desc, txt_color, bg_color, self.setting)
                        btn_item.id = item_id
                        btn_item.price = int(round(item_price * self._price_factor)) if item_price is not None else 0
                        btn_item.hasVariants = has_vars
                        
                        # SET THE CONTROL FLAG FIRST
                        btn_item.hasInventory = has_inventory  
                        
                        # CONVERT THE TRUE AVAILABLE QUANTITY TO INTEGER
                        # we read available_qty
                        if has_inventory:
                            self._original_inventory[item_id] = {'type': item_type, 'qty': qty, 'part':{}}
                            if item_type != 'I':
                                self._original_inventory[item_id]['part'] = {i: int(round(q * self._qty_factor)) for i, q in get_item_parts(item_id)}
                            btn_item.stockLevel = qty
                        
                        btn_item.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
                        self.ui.bgi.addButton(btn_item, item_id) # Register using item_id as the button group index
                        grid_layout.addWidget(btn_item, row_pos, col_pos)
                    else:
                        # not salable items are used for inventory
                        if has_inventory:
                            self._original_inventory[item_id] = {'type': item_type, 'qty': qty, 'part':{}}
                            if item_type != 'I':
                                self._original_inventory[item_id]['part'] = {i: int(round(q * self._qty_factor)) for i, q in get_item_parts(item_id)}                    
                        
                # fill the remaining empty layout grid cells with generic spacer widgets
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
            logger.error("Failed to re-populate order entry department grids layout view.")
            return

        # copy original_inventory to inventory recreating it
        self._inventory = copy.deepcopy(self._original_inventory)
        
        # connect click event handler to the newly generated item button group
        self.ui.bgi.buttonClicked.connect(self.buttonClicked)
        # enable or disable tabs selectively for takeaway mode constraints
        if self.ui.radioButtonTakeAway.isChecked():
            takeaway_depts = department_takeaway_list()
            for i in range(self.ui.tabWidgetList.count()):
                is_takeaway_valid = self.ui.tabWidgetList.tabText(i) in takeaway_depts
                self.ui.tabWidgetList.widget(i).setEnabled(is_takeaway_valid)
        # clear specific notes and reset operational icons
        self.ui.depnote.clear()
        for button in self.ui.bgnotes.buttons():
            button.setIcon(currentIcon['empty'])
        # initialize or extend the application idle timer system
        if self.setting['check_inactivity']:
            self.idleTimer.start()
        # establish window focus context on the primary table entry field
        self.ui.lineEditTable.setFocus()
        #print(self._inventory)
        
    def _explode_to_parts(self, item_id: int, multiplier: int = 1, flat_recipe: dict | None = None) -> dict:
        """
        Helper method to break down items. Safely ignores untracked components.
        """
        if flat_recipe is None:
            flat_recipe = {}
            
        if item_id not in self._inventory:
            return flat_recipe
            
        item = self._inventory[item_id]
        
        if item['type'] == 'I':
            flat_recipe[item_id] = flat_recipe.get(item_id, 0) + multiplier
        else:
            if 'part' in item and item['part']:
                for comp_id, req_qty in item['part'].items():
                    scaled_consumption = (int(req_qty) * int(multiplier)) // int(self._qty_factor)
                    self._explode_to_parts(comp_id, scaled_consumption, flat_recipe)
                    
        return flat_recipe


    def calculate_and_update_qty(self, item_id: int) -> int:
        """
        Recursive function to calculate real available quantity.
        Since self._inventory ONLY contains tracked items, missing IDs are skipped.
        """
        # If the main item isn't in the inventory, it's unmanaged (infinite)
        if item_id not in self._inventory:
            return 99999
            
        item = self._inventory[item_id]
        
        # CASE 1: Raw Ingredient ('I')
        if item['type'] == 'I':
            return int(item['qty'])
            
        # CASE 2: Kit ('K') or Menu ('M')
        if 'part' not in item or not item['part']:
            return 0
            
        component_limits = []
        
        for comp_id, required_qty in item['part'].items():
            # if the component is NOT in self._inventory, it's untracked
            # we skip it so it won't act as a bottleneck.
            if comp_id not in self._inventory:
                continue
                
            available_comp_qty = self.calculate_and_update_qty(comp_id)
            req_qty = int(required_qty)
            
            if req_qty > 0:
                possible_portions = available_comp_qty // req_qty
                component_limits.append(possible_portions)
            else:
                component_limits.append(0)
            
        # if all components were skipped, it's infinite.
        if not component_limits:
            plain_portions = 99999 if item['part'] else 0
        else:
            plain_portions = max(0, min(component_limits))
            
        # Scale back to fixed-point space only for actual limited quantities
        real_qty = plain_portions if plain_portions == 99999 else plain_portions * int(self._qty_factor)
        item['qty'] = real_qty
        
        return real_qty

    def refresh_inventory_and_ui(self) -> None:
        """
        Centralized pipeline: resets inventory to baseline, subtracts everything 
        currently inside self.order_lines, recalculates bottlenecks, and updates UI buttons.
        """
        # reset working inventory to the pristine original database snapshot
        self._inventory = copy.deepcopy(self._original_inventory)
        
        # explode and subtract EVERY line currently present in self.order_lines
        total_order_consumption: dict = {}
        for dict_key, line_data in self.order_lines.items():
            item_id = line_data["item_id"]
            qty_int = line_data["qty_int"]
            
            # Explode this specific order line into raw 'I' ingredients
            line_consumption = self._explode_to_parts(item_id, qty_int)
            for ing_id, needed_qty in line_consumption.items():
                total_order_consumption[ing_id] = total_order_consumption.get(ing_id, 0) + needed_qty
                
        # deduct line consumption from our working inventory
        for ing_id, total_to_deduct in total_order_consumption.items():
            if ing_id in self._inventory:
                self._inventory[ing_id]['qty'] -= total_to_deduct

        # recalculate Kit ('K') and Menu ('M') availability in the working inventory
        for item_id in list(self._inventory.keys()):
            self.calculate_and_update_qty(item_id)
            
        # push updated stock levels directly to item buttons
        for button in self.ui.bgi.buttons():
            btn = cast(ButtonItem, button)
            if btn.hasInventory:
                # if an item was completely unmanaged or stripped, guarantee safe readout
                if btn.id in self._inventory:
                    btn.stockLevel = self._inventory[btn.id]['qty']
                # else:
                #     # Fallback for unmanaged items if they somehow have the flag active
                #     btn.stockLevel = 99999 
                
        # initialize or extend the application idle timer system
        if self.setting['check_inactivity']:
            self.idleTimer.start()

    
    def buttonClicked(self, button: Any, ivars: str | None = "", variant_price: int = 0, web: bool = False) -> None:
        """React to an item button click, manage variants, and update the order lines structure using integers,
        recalculate inventory"""
        btn = cast(ButtonItem, button) # cast directly to our optimized custom class
        if not btn.id:
            raise TypeError(_tr('OrderEntry', "Any button must have an ID"))
        
        # HANDLE ITEM VARIANTS
        if btn.hasVariants and not web: # orders from web already have variants and prices and sum of this values is already in the order_lines
            if not ivars:
                if (not self.ui.pushButtonVariants.isEnabled()) or self.ui.pushButtonVariants.isChecked():
                    item_description = getattr(btn, 'description', '')
                    variants = [(vd,
                                 int(round(float(pd) * self._price_factor))
                                 ) for vd, pd in get_variants(btn.id)]
                    dlg = ChooseVariantDialog(self, item_description, variants, self.setting['price_decimal_places'])
                    rv = dlg.exec()
                    if rv:
                        ivars, variant_price = dlg.getVariants()
                    dlg.deleteLater()  
                    if not rv:
                        return
                if self.ui.pushButtonVariants.isEnabled():
                    self.ui.pushButtonVariants.setChecked(False)
                    
        if not btn.isEnabled():
            return
                
        # DETERMINE QUANTITY TO ADD
        qty_float = float(self.ui.buttonGroupQuantity.checkedButton().text())
        qty_int = int(round(qty_float * self._qty_factor))
        
        self.ui.radioButton1.setChecked(True)
        
        # VERIFY STOCK LEVEL ON THE BUTTON IN INTEGER SPACE
        if btn.hasInventory and (self._inventory[btn.id]['qty'] - qty_int < 0):
            QMessageBox.warning(self, _tr('OrderEntry', 'Warning'), _tr('OrderEntry', 'Not enough stock available.'))
            return 
            
        # CALCULATE TOTAL SINGLE UNIT PRICE IN INTEGER
        # btn.price is already an integer
        base_price = btn.price
        unit_price = base_price + variant_price
        
        # UPDATE PYTHON DATA STRUCTURE MEMORY (self.order_lines)
        dict_key: tuple[int, str | None]
        dict_key = (btn.id, ivars)
        
        if dict_key in self.order_lines:
            # increment the existing quantity
            self.order_lines[dict_key]["qty_int"] += qty_int
        else:
            # create a new line record from scratch in the dictionary
            self.order_lines[dict_key] = {
                "item_id": btn.id,
                "description": btn.description,
                "variant": ivars,
                "qty_int": qty_int,
                "price_int": unit_price
            }
            
        # REFRESH GRAPHICAL INTERFACE AND RECALCULATE TOTALS
        self.refresh_inventory_and_ui()
        self.renderOrderTable()
        
        
    def renderOrderTable(self) -> None:
        """
        Clear order grid layout view and rebuild rows from scratch using dynamic integer decimal memory configurations.
        Calculate and display totals.
        """
        # freeze graphic pipeline rendering to bypass performance bottlenecks on macOS/Windows
        self.ui.tabWidgetOrder.setUpdatesEnabled(False)
        self.ui.tabWidgetOrder.blockSignals(True)
            
        try:
            # wipe table rows clean
            self.ui.tabWidgetOrder.setRowCount(0)
            
            # re-populate data grid rows matching internal Python dictionary lines
            for dict_key, item in self.order_lines.items():
                row = self.ui.tabWidgetOrder.rowCount()
                self.ui.tabWidgetOrder.insertRow(row)
                
                # revert quantity back to standard float using the dynamic factor strictly for visual presentation
                actual_qty = item["qty_int"] / self._qty_factor
                
                # atomic multiplication using dynamic quantity factor to secure perfect math precision
                line_amount = (item["qty_int"] * item["price_int"]) / self._qty_factor / self._price_factor
                
                # format quantity string: handles dynamic decimals configurations nicely (e.g., 1.5 shows "1,5")
                qty_str = session['qlocale'].toString(float(actual_qty), 'f', self.setting['quantity_decimal_places'])
                actual_price = item["price_int"] / self._price_factor
                price_str = session['qlocale'].toString(float(actual_price), 'f', self.setting['price_decimal_places'])
                amount_str = session['qlocale'].toString(float(line_amount), 'f', self.setting['amount_decimal_places'])
                
                # prepare description formatting string (name + variant if present)
                full_description = item["description"]
                if item["variant"]:
                    full_description += f" {item['variant']}"
                    
                # populate row widgets items cell data blocks
                self.ui.tabWidgetOrder.setItem(row, two.ID, QTableWidgetItem(str(item["item_id"])))
                self.ui.tabWidgetOrder.setItem(row, two.VARIANTS, QTableWidgetItem(item["variant"]))
                self.ui.tabWidgetOrder.setItem(row, two.DESCRIPTION, QTableWidgetItem(full_description))
                
                cell_qty = QTableWidgetItem(qty_str)
                cell_qty.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                cell_qty.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.ui.tabWidgetOrder.setItem(row, two.QUANTITY, cell_qty)
                
                cell_price = QTableWidgetItem(price_str)
                cell_price.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                cell_price.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.ui.tabWidgetOrder.setItem(row, two.PRICE, cell_price)
                
                cell_amount = QTableWidgetItem(amount_str)
                cell_amount.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                cell_amount.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.ui.tabWidgetOrder.setItem(row, two.AMOUNT, cell_amount)
                
            # COMPREHENSIVE INTEGRITY FIX: Centralize mathematical evaluation inside recalcTotals.
            # this automatically populates self.current_subtotal_int and aligns all display fields!
            self.recalcTotals()
                
        finally:
            # then, restore the main table widget behavior safely
            self.ui.tabWidgetOrder.blockSignals(False)
            self.ui.tabWidgetOrder.setUpdatesEnabled(True)
            self.ui.tabWidgetOrder.viewport().update()
            self.ui.tabWidgetOrder.scrollToBottom()

            
    def tableButtonClicked(self, button) -> None:
        """When a table button is clicked, set the table number in the input field
        and switch to order view."""
        if button.unavailable:
            return
        self.ui.lineEditTable.setText(button.text())
        self.tablesOrder()


    def orderCellClicked(self, row: int, column: int) -> None:
        """Decrease item quantity or remove line from order using dynamic integer configurations when a row cell is clicked."""        
        # DETERMINE DECREMENT QUANTITY FROM SELECTOR
        qty_to_remove_float = float(self.ui.buttonGroupQuantity.checkedButton().text())
        qty_to_remove_int = int(round(qty_to_remove_float * self._qty_factor))
        
        self.ui.radioButton1.setChecked(True)
        
        # SAFE EXTRACTION OF CORE REFERENCE IDENTIFIERS FROM HIDDEN COLUMNS
        id_item = self.ui.tabWidgetOrder.item(row, two.ID)
        vars_item = self.ui.tabWidgetOrder.item(row, two.VARIANTS)
        
        if not (id_item and vars_item):
            return  # safety fallback if operational cell markers are missing or uninitialized
            
        item_id = int(id_item.text())
        variant_str = vars_item.text()
        dict_key = (item_id, variant_str)
        
        if not dict_key in self.order_lines:
            return
        
        current_ordered_qty = self.order_lines[dict_key]["qty_int"]
        
        # avoid restoring phantom stock, we can only return what was actually in the order line.
        actual_returned_qty_int = min(qty_to_remove_int, current_ordered_qty)
        
        # DECREMENT QUANTITY INSIDE MEMORY DICTIONARY MAP
        self.order_lines[dict_key]["qty_int"] -= actual_returned_qty_int
        
        # RESTORE STOCK LEVEL ON THE CORRESPONDING COUNTER BUTTON
        # explode the removed item to find which Raw Ingredients (Type 'I') it actually returns
        returned_ingredients = self._explode_to_parts(item_id, actual_returned_qty_int)
        
        # add quantities back ONLY to the Raw Ingredients inside the inventory
        for ing_id, total_qty_to_restore in returned_ingredients.items():
            if ing_id in self._inventory:
                self._inventory[ing_id]['qty'] += total_qty_to_restore
                
        # IF QUANTITY DROPS TO ZERO OR LESS, WIPE ITEM FROM CORE DICTIONARY STRUCTURE
        if self.order_lines[dict_key]["qty_int"] <= 0:
            del self.order_lines[dict_key]
            
        # UPDATE STOCK LEVEL ON THE BUTTON GROUP
        self.refresh_inventory_and_ui()
        # REFRESH CENTRALIZED GRAPHICAL VIEW DATA PIPELINE FROM MEMORY
        self.renderOrderTable()

    
    def bgNotesClicked(self, button: Any) -> None:
        """Open a multi-line input dialog to edit department-specific notes."""
        # get the internal ID assigned to the clicked button
        bid = self.ui.bgnotes.id(button)
        # safe extraction: fallback to an empty string if no note exists yet (prevents PySide6 crash)
        txt = self.ui.depnote.get(bid) or ""
        # prompt the user with a multi-line text input dialog
        text, ok = QInputDialog.getMultiLineText(
            self,
            _tr("OrderEntry", "Department note"),
            _tr("OrderEntry", "Message text for {}").format(get_department_desc(bid)),
            txt
        )
        if ok:
            # store the note, or set to None if the user cleared the text area
            self.ui.depnote[bid] = text.strip() or None
        # update the button icon dynamically based on whether a note is currently active
        if self.ui.depnote.get(bid):
            button.setIcon(currentIcon['order_note'])
        else:
            button.setIcon(currentIcon['empty'])

    @Slot()
    def processWebOrder(self) -> None:
        """
        Fill order form based on web order details or QRC data parsed from barcode scanner.
        """
        # disconnect editingFinished to avoid calling it 2 times (return pressed and lost focus)
        try:
            self.ui.lineEditBarCode.editingFinished.disconnect(self.processWebOrder)
        except (RuntimeError, TypeError):
            pass  # fail-safe if it wasn't connected
            
        try:
            value = self.ui.lineEditBarCode.text().strip()
            if not value:  # can happen when losing focus without inserting anything
                return
                
            # reset the dialog container state
            self.resetDialog()
            
            # parse QRC CSV structural segments
            try:
                segments = value.split(';')
                qtype, qdelivery, qtable, qname, qcovers, qemail = segments[:6]
                # extract repeating item attributes from index 6 onwards
                items_part = segments[6:]
                itm = items_part[0::4] 
                var = items_part[1::4] 
                prd = items_part[2::4]
                qty = items_part[3::4]
            except Exception as er:
                msg = _tr('OrderEntry', "Unrecognized QRC structure:") + f"\n{str(er)}"
                QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                return
                
            # sanity checks for fundamental parameters
            err: list[str] = []
            if qtype != 'PSQRC':
                err.append(_tr('OrderEntry', "Unrecognized QRC format:") + f" {qtype}")
            if qdelivery not in ('T', 'A'):
                err.append(_tr('OrderEntry', "Unrecognized delivery option:") + f" {qdelivery}")
            if qcovers and not qcovers.isdigit():
                err.append(_tr('OrderEntry', "Unrecognized covers number:") + f" {qcovers}") 
            if err:
                msg = _tr('OrderEntry', "Unrecognized parameters:") + f"\n{'\n'.join(err)}"
                QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                return           
                
            # move UI layout to order view widget
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderEntry', 'Tables'))
            
            if qdelivery == 'T':
                self.ui.radioButtonTable.setChecked(True)
            else:
                self.ui.radioButtonTakeAway.setChecked(True)
                
            self.ui.lineEditTable.setText(qtable or '')
            self.ui.lineEditCustomerName.setText(qname or '')
            self.ui.spinBoxCovers.setValue(int(qcovers or 0))
            self.ui.lineEditCustomerContact.setText(qemail or '')
            
            unavailable: dict[str, int] = dict()
            self.ui.radioButton1.setChecked(True)
            
            # iterate through extracted order lines
            for i, v, p, q in zip(itm, var, prd, qty):
                if not i.isdigit():
                    msg = _tr('OrderEntry', "Unrecognized item id:") + f" {i}"
                    QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                    return
                if not q.isdigit():   
                    msg = _tr('OrderEntry', "Unrecognized quantity:") + f" {q}"
                    QMessageBox.critical(self, _tr("MessageDialog", "Critical"), msg)
                    return        
                    
                # convert the incoming QR code price string safely into integer cents
                variant_float = float(p or '0.0')
                variant_price_cents = int(round(variant_float * 100))
                
                # repeat item insertion loop based on QR code quantity requirements
                for j in range(int(q)):
                    raw_button = self.ui.bgi.button(int(i))
                    if raw_button is None:
                        QMessageBox.critical(self,
                                            _tr("MessageDialog", "Critical"),
                                            _tr('OrderEntry', "Item NOT available in buttons' grid, web order skipped."))
                        return 
                        
                    # cast to Any to prevent mypy exceptions on custom attributes
                    btn = cast(Any, raw_button)
                    if btn.isEnabled():
                        # now calling buttonClicked passing the converted integer cents variant upcharge
                        self.buttonClicked(btn, v, variant_price_cents, web=True) # web=True bypasses manual dialogs
                    else:
                        btn_text = str(btn.text())
                        unavailable[btn_text] = unavailable.get(btn_text, 0) + 1
                        
            # warn the operator of unavailable items that were skipped
            if unavailable:
                msg = _tr("OrderEntry", "These items are not available and not included in the order:\n")
                msg += "\n".join(["{:>2}  {:<20}".format(count, name).replace('\n', ' ')
                                for name, count in unavailable.items()])
                QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
                
            # set the digital weborder indicator flag to active
            self.ui.checkBoxWebOrder.setChecked(True)
            
        finally:
            # always clean up inputs and re-establish the core signal hook
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
            
            
    def onDiscountChanged(self, value: float) -> None:
        """Triggered when the operator modifies the discount spinbox. 
        Converts the float to pure integer cents and forces a recalculation."""
        # update the internal state variable to integers before doing any calculations
        self.current_discount_int = int(round(value * self._price_factor))
        
        # recalculates totals so the entire screen realigns
        self.recalcTotals()


    def recalcTotals(self) -> None:
        """Recalculate order subtotal, total, and change indicators using dynamic integer memory mappings."""
        
        subtotal_int = 0
        
        # calculate the gross sum of all rows
        for item in self.order_lines.values():
            line_amount_int = int((item["qty_int"] / self._qty_factor) * 
                               (item["price_int"] / self._price_factor) *
                               self._amount_factor)
            subtotal_int += line_amount_int
        
        # freeze chart signals to avoid refresh loops
        self.ui.doubleSpinBoxSubTotal.blockSignals(True)
        self.ui.doubleSpinBoxTotal.blockSignals(True)
        self.ui.doubleSpinBoxChange.blockSignals(True)
        
        try:
            # extracts the discount and cash entered by the operator
            discount_int = int(round(self.ui.doubleSpinBoxDiscount.value() * self._amount_factor))
            cash_int = int(round(self.ui.doubleSpinBoxCash.value() * self._amount_factor))
            net_total_int = max(0, subtotal_int - discount_int)
            change_int = max(0, cash_int - net_total_int)
            
            # synchronize the values in the instance for next validation
            self.current_subtotal_int   = subtotal_int
            self.current_discount_int   = discount_int
            self.current_total_int      = net_total_int
            self.current_change_int     = change_int
            
            # update graphic widgets
            self.ui.doubleSpinBoxSubTotal.setValue(subtotal_int / self._amount_factor) 
            self.ui.doubleSpinBoxTotal.setValue(net_total_int / self._amount_factor) 
            self.ui.doubleSpinBoxChange.setValue(change_int / self._amount_factor) 
            
        finally:
            self.ui.doubleSpinBoxSubTotal.blockSignals(False)
            self.ui.doubleSpinBoxTotal.blockSignals(False)
            self.ui.doubleSpinBoxChange.blockSignals(False)

    
    def accept(self) -> None:
        """Validate, generate, save, and print the completed order using memory data mapping."""
        # ----------------------------------------------------------
        # SANITY CHECKS FIRST
        # ----------------------------------------------------------
        # check if the order contains at least one item
        if len(self.order_lines) == 0:
            msg = _tr('OrderEntry', "No item inserted!")
            QMessageBox.warning(self, _tr('MessageDialog', "Warning"), msg)
            return
            
        # check for mandatory table number when table delivery is selected
        if (self.setting['mandatory_table_number']
                and self.ui.radioButtonTable.isChecked()
                and not self.ui.lineEditTable.text().strip()):
            msg = _tr("OrderEntry", "The table number is missing!")
            QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
            self.ui.lineEditTable.setFocus()
            return
            
        # validate that the table number actually exists in the predefined list
        if (self.setting['mandatory_table_number'] and 
            self.setting['use_table_list'] and 
            self.ui.radioButtonTable.isChecked()):
            if not table_exists(self.ui.lineEditTable.text().strip()):
                msg = _tr("OrderEntry", "The table number does not exist, use it anyway ?")
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        msg,
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                        ) == QMessageBox.StandardButton.No:
                    self.ui.lineEditTable.setFocus()
                    return
                    
        # check for customer name (if mandatory) when table delivery is selected
        if (self.setting['mandatory_name_for_takeaway'] and
            self.ui.radioButtonTakeAway.isChecked() and 
            not self.ui.lineEditCustomerName.text().strip()):
            msg = _tr("OrderEntry", "Customer's name is missing! proced anyway?")
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    msg,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    ) == QMessageBox.StandardButton.No:
                self.ui.lineEditCustomerName.setFocus()
                return
            
        # double check if covers/seats are missing despite being a table order
        if self.ui.radioButtonTable.isChecked() and not self.ui.spinBoxCovers.value():
            msg = _tr("OrderEntry", "Warning: there are no covers even "
                                    "though delivery to the table has been indicated,\n"
                                    "do you want to correct it?")
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    msg,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    ) == QMessageBox.StandardButton.Yes:
                self.ui.spinBoxCovers.setFocus()
                self.ui.spinBoxCovers.selectAll()
                return
            
        # filter out items that are restricted from takeaway delivery
        if self.ui.radioButtonTakeAway.isChecked():
            nogood: list[str] = []
            # cycle through our clean memory order lines keys
            for dict_key in self.order_lines.keys():
                item_id = dict_key[0]  # first element of the tuple key is the item_id
                if not is_for_takeaway(item_id):
                    nogood.append(get_item_desc(item_id))
            if nogood:
                msg = _tr('OrderEntry', "Warning: the following items are not available for take away:\n"
                                        "- {}\n\nDo i proceed anyway ?".format("\n- ".join(nogood)))
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        msg,
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                        ) == QMessageBox.StandardButton.No:
                    return
                    
        # ---------------------------------------------------------------------
        # VALIDATIONS PASSED: EXECUTE ORDER SUBMISSION
        # --------------------------------------------------------------------- 
        # DISCOUNT CHECK: The discount cannot be greater than the order amount
        if self.current_discount_int > self.current_subtotal_int:
            msg = _tr("OrderEntry", "Discount amount greater than the total amount!")
            QMessageBox.warning(self, _tr("MessageDialog", "Warning"), msg)
            self.ui.doubleSpinBoxDiscount.setFocus()
            self.ui.doubleSpinBoxDiscount.selectAll()
            return

        # create the Order
        order = Order()
        order.header['order_date_time'] = QDateTime.currentDateTime().addSecs(self.dateTimeDiff or 0)
        order.header['cash_desk'] = self.ui.labelCashDeskDescription.text()
        order.header['delivery'] = 'T' if self.ui.radioButtonTable.isChecked() else 'A'
        order.header['is_electronic_payment'] = self.ui.checkBoxElectronicPayment.isChecked()
        order.header['is_from_web'] = self.ui.checkBoxWebOrder.isChecked()
        order.header['table_num'] = self.ui.lineEditTable.text().strip() or None
        order.header['customer_name'] = self.ui.lineEditCustomerName.text().strip() or None
        order.header['customer_contact'] = self.ui.lineEditCustomerContact.text().strip() or None
        order.header['covers'] = int(self.ui.spinBoxCovers.value()) or None
        
        order.header['total_amount'] = Decimal(self.current_subtotal_int) / Decimal(self._amount_factor)
        order.header['discount'] = Decimal(self.current_discount_int) / Decimal(self._amount_factor)
        order.header['cash'] = Decimal(self.current_cash_int) / Decimal(self._amount_factor)
        order.header['change'] = Decimal(self.current_change_int) / Decimal(self._amount_factor)

        # We safely map integers back to Decimals dynamically based on settings factors
        for item in self.order_lines.values():
            line: dict[str, Any] = dict()
            line['item_id'] = item['item_id']
            line['variants'] = item['variant'] or None
            
            # quantity representation conversion using dynamic factor
            line['quantity'] = Decimal(item['qty_int']) / Decimal(self._qty_factor)
            
            # direct atomic price calculations converted safely using dynamic factors
            price_decimal = Decimal(item['price_int']) / Decimal(self._price_factor)
            line_amount_cents = (item['qty_int'] * item['price_int']) // self._qty_factor
            amount_decimal = Decimal(line_amount_cents) / Decimal(self._price_factor)
            
            line['price'] = price_decimal
            line['amount'] = amount_decimal
            
            order.lines.append(line)
            
        # handle real-time stock allocation checks
        ofsi = order.out_of_stock()
        if ofsi:
            items = [str(item) for item in ofsi]
            msg = (_tr('OrderEntry', "Warning: these items are unavailable "
                                    "for the current order:\n\n"
                                    "- {0}\n\nDo i proceed anyway ?").format("\n- ".join(items)))
            if QMessageBox.question(self,
                                    _tr('MessageDialog', "Question"),
                                    msg,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
                return
                
        # Mmp department situational notes context directly from UI widgets
        order.depnote.update(self.ui.depnote)
        
        # ---------------------------------------------------------------------
        # DATABASE COMMIT OPERATION
        # ---------------------------------------------------------------------
        success = False
        with gui_exception_context(self, _tr('OrderEntry', "Saving order to database")):
            ti, used_dep = order.insert()  # ti = order header reference key ID
            success = True
        if not success:
            return
        # ---------------------------------------------------------------------
        # ASYNC ORDER PRINT REPORTS DISPATCH
        # ---------------------------------------------------------------------
        # print customer receipt copy
        if self.setting['print_customer_copy']:
            with gui_exception_context(self, _tr('OrderEntry', "Printing order customer copy")):
                printer = get_printer_name(self.setting['customer_printer_class'], session['hostname'])
                printOrderReport(ti, printer)
        # covers copy
        if self.setting['print_cover_copy'] and order.header['delivery'] == 'T' and order.header['covers']:
            with gui_exception_context(self, _tr('OrderEntry', "Printing order cover copy")):
                printer = get_printer_name(self.setting['cover_printer_class'], session['hostname'])
                printOrderCoverReport(ti, printer)
        # ---------------------------------------------------------------------
        # SEPARATE DEPARTMENT COPIES PRINT DISPATCH
        # ---------------------------------------------------------------------
        if self.setting['print_department_copy']:
            with gui_exception_context(self, _tr('OrderEntry', "Printing order department copies")):
                for dept_id in used_dep:
                    if dept_id is None:
                        continue  # skip if department ID is not valid
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
        # fast, safe and clean squashing of all rows in the order table
        self.ui.tabWidgetOrder.setRowCount(0)
        # Trigger full interface and button grids rejuvenation
        self.resetDialog()
        
    def reject(self) -> None:
        "Close the dialog"
        msg = _tr("OrderEntry", "Do you want to exit the order entry?")
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                msg,
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, # butons
                                QMessageBox.StandardButton.No # default botton
                                ) == QMessageBox.StandardButton.Yes:
            # save geometry
            st = QSettings()
            st.setValue("OrderEntry/Geometry", self.saveGeometry())
            super().reject()

# EOF
