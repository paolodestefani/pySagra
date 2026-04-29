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
import logging
import decimal
from typing import Any, cast, Callable

# PySide6
from PySide6.QtCore import Qt
#from PySide6.QtCore import QObject
from PySide6.QtCore import QTimer
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QSettings
from PySide6.QtCore import Slot
from PySide6.QtCore import QRectF
#from PySide6.QtGui import QPalette
from PySide6.QtGui import QColor
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPainterPath
from PySide6.QtGui import QFont
from PySide6.QtGui import QAction 
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QButtonGroup
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QSizePolicy

# application modules
from App import session
from App import currentIcon
from App.Core.L10n import fromCurrency
from App.Core.L10n import toCurrency
from App.Database.Exceptions import PyAppDBError
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
#from App.Database.WebOrder import get_web_order_header
#from App.Database.WebOrder import get_web_order_details
#from App.Database.WebOrder import set_web_order_processed
from App.Database.Order import Order
from App.Database.Order import get_orders_issued
from App.Report.Order import printOrderReport
from App.Report.Order import printOrderCoverReport
from App.Report.Order import printOrderDepartmentReport
from App.Report.Order import printStockUnloadReport
from App.Core.L10n import _tr
from App.Widget.Dialog import DateTimeInputDialog
from App.Ui.DepartmentNoteDialog import Ui_DepartmentNoteDialog
from App.Ui.ChooseVariantsDialog import Ui_ChooseVariantsDialog


ID, VARIANTS, DESC, QTY, PRICE, AMOUNT = range(6)

ORDER, TABLE = range(2)


# launch main order entry dialog
def orderEntry(action: QAction, checked: bool = False) -> None:
    "Open order dialog"
    logging.info('Starting order entry dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
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
    # class OrderDialog(BaseOrderDialog, Ui_OrderDialog):
    #     pass
    #
    dlg = BaseOrderDialog(mw, Ui_OrderDialog)
    dlg.show()
    logging.info('Order entry dialog shown')


class DepartmentNoteDialog(QDialog):
    "Dialog for entering and editing department note"

    def __init__(self, parent: QWidget, dep: str, note: str) -> None:
        super().__init__(parent)
        self.ui = Ui_DepartmentNoteDialog()
        self.ui.setupUi(self)
        self.ui.lb_department.setText(_tr("OrderDialog", "Note for {}").format(dep))
        self.ui.le_note.setText(note)

# item variant selection

class VariantCheckBox(QCheckBox):
    def __init__(self, parent, desc, priced):
        super().__init__(parent)
        self.priceDelta = priced
        if priced > 0:
            self.setText(f"{desc} (+{toCurrency(priced)})")
        else:
            self.setText(desc)

class ChooseVariantDialog(QDialog):
    "Dialog for item variants selection"
    def __init__(self, parent: QWidget, item: str, variants: list):
        super().__init__(parent)
        self.ui = Ui_ChooseVariantsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(item)
        self.bg = QButtonGroup(self)
        self.bg.setExclusive(False)
        for variant, delta in variants:
            v = VariantCheckBox(self, variant, delta)
            self.bg.addButton(v)
            self.ui.layout.addWidget(v)

    def getVariants(self):
        "Rwturn a string of variants ad a price delta"
        variants = []
        priceDelta = 0
        # get variants and price delta
        for i in self.bg.buttons():
            if i.isChecked():
                variants.append(i.text())
                priceDelta += i.priceDelta
        # free variants
        if self.ui.lineEditFreeVariant.text():
            variants.append(self.ui.lineEditFreeVariant.text())
        return " ".join(variants), priceDelta

# a button of the list. It's a push button subclass with some more attribute

class ButtonList(QPushButton):
    "Push button for item list"

    def __init__(self, text: str, textColor: str, backgroundColor: str, parent: BaseOrderDialog) -> None:
        super().__init__(parent)
        self.setting = parent.setting
        self.description = text
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.caption = text.replace(' ', '\n')
        self.setText(self.caption)
        self.id = None
        self.sc = None # boolean stock control
        self.price = None
        self.hasVariants = False
        self.setAutoFillBackground(True)
        self.setFont(QFont(self.setting['order_list_font_family'], self.setting['order_list_font_size'], QFont.Weight.Bold))
        self.setMinimumWidth(65)
        #####
        # for colors use stylesheet to avoid problem with platform themes
        #####
        # for variants indicator
        self.variantIndicatorIcon = currentIcon['order_flag'].pixmap(25, 25)
        
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'level':
            self.setEnabled(True)  # disabled if level = 0 below
            if self.sc:
                value = value or 0 # avoid None values
                if not self.sc or (self.sc and not self.setting['always_show_stock_inventory']):
                    self.setText(self.caption)
                else:
                    self.setText(self.caption + f"\n({self.level})")
                # normal level
                if value >= self.setting['warning_stock_level']:
                    ss = f"background-color: {self.backgroundColor}; color: {self.textColor}"
                # warning level
                elif self.setting['critical_stock_level'] < value < self.setting['warning_stock_level']:
                    ss = f"background-color: {self.setting['warning_background_color']}; color: {self.setting['warning_text_color']}"
                # critical level
                elif 0 < value <= self.setting['critical_stock_level']:
                    ss = f"background-color: {self.setting['critical_background_color']}; color: {self.setting['critical_text_color']}"
                # disabled: value = 0
                else:
                    ss = f"background-color: {self.setting['disabled_background_color']}; color: {self.setting['disabled_text_color']}"
                    self.setDisabled(True)
            else:
                # no level control -> always normal
                ss = f"background-color: {self.backgroundColor}; color: {self.textColor}"
            self.setStyleSheet(ss)

    def paintEvent(self, event=None):
        QPushButton.paintEvent(self, event)
        if self.hasVariants:
            painter = QPainter(self)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.drawPixmap(5, 5, self.variantIndicatorIcon)
            painter.end()

    def showLevel(self):
        if self.sc:
            self.setText(self.caption + f"\n({self.level})")

    def hideLevel(self):
        if self.sc:
            self.setText(self.caption)


#---------------------#
#-- main dialog box --#
#---------------------#

class BaseOrderDialog(QDialog):
    "Order dialog"

    def __init__(self, parent: QWidget, uidialog: Callable) -> None:
        super().__init__(parent)
        self.ui = uidialog()
        self.ui.setupUi(self)
        #global setting
        self.setting = Setting()
        # restore geometry
        st = QSettings()
        if st.value("OrderDialogGeometry"):
            self.restoreGeometry(st.value("OrderDialogGeometry"))
        # window flags
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowType.Dialog|
                            Qt.WindowType.WindowMinMaxButtonsHint|
                            Qt.WindowType.WindowCloseButtonHint)
        # dialog icons
        self.ui.pushButtonTablesSwitch.setIcon(currentIcon['order_switch'])
        self.ui.pushButtonConfirm.setIcon(currentIcon['order_ok'])
        self.ui.pushButtonCancel.setIcon(currentIcon['order_cancel'])
        self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Order'))
        # idle time control
        if self.setting['check_inactivity']:
            self.idleTimer = QTimer(self)
            self.idleTimer.timeout.connect(self.resetAdvice)
            self.idleTimer.start(self.setting['inactivity_time'] * 1000)
        # delivery button group
        self.ui.buttonGroupDelivery = QButtonGroup(self)
        self.ui.buttonGroupDelivery.addButton(self.ui.radioButtonTable)
        self.ui.buttonGroupDelivery.addButton(self.ui.radioButtonTakeAway)
        # qty button group
        self.ui.buttonGroupQuantity = QButtonGroup(self)
        for i in (self.ui.radioButton1, self.ui.radioButton5, self.ui.radioButton10):
            self.ui.buttonGroupQuantity.addButton(i)
        # set departments tab position
        self.ui.tabWidgetList.setTabPosition({'N': QTabWidget.TabPosition.North,
                                              'S': QTabWidget.TabPosition.South,
                                              'E': QTabWidget.TabPosition.East,
                                              'W': QTabWidget.TabPosition.West}[self.setting['order_list_tab_position']])
        # order list tablewidget
        self.ui.list_rows = self.setting['order_list_rows']
        self.ui.list_columns = self.setting['order_list_columns']
        self.ui.tables_list_rows = self.setting['table_list_rows']
        self.ui.tables_list_columns = self.setting['table_list_columns']
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
        self.ui.tabWidgetOrder.hideColumn(ID)
        self.ui.tabWidgetOrder.hideColumn(VARIANTS)
        self.ui.tabWidgetOrder.setColumnWidth(DESC, 250)
        self.ui.tabWidgetOrder.setColumnWidth(QTY, 70)
        self.ui.tabWidgetOrder.setColumnWidth(PRICE, 70)
        self.ui.tabWidgetOrder.setColumnWidth(AMOUNT, 70)
        self.ui.doubleSpinBoxTotal.setValue(0.0)
        # departments note buttons and dictionary
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
        # buttons for tables
        self.ui.bgt = QButtonGroup(self)
        self.ui.bgt.setExclusive(False)
        gl = QGridLayout()
        gl.setSpacing(10)
        for tt, tr, tc, ttc, tbc in table_list():
            b = QPushButton(tt, self) # item description
            b.setFont(QFont(self.setting['table_list_font_family'], self.setting['table_list_font_size'], QFont.Weight.Bold))
            b.setStyleSheet(f"color: {ttc}; background-color: {tbc};")
            b.setMinimumWidth(50)
            b.setMinimumHeight(40)
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.ui.bgt.addButton(b)
            gl.addWidget(b, tr, tc)
        # fill the remaining cells of gl with an empty button
        for r in range(1, self.ui.tables_list_rows + 1):
            for c in range(1, self.ui.tables_list_columns + 1):
                if gl.itemAtPosition(r, c) is None:
                    w = QWidget(self)
                    #w.setMinimumWidth(5)
                    w.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
                    gl.addWidget(w, r, c)
        self.ui.frameTables.setLayout(gl)
        # list button group
        self.ui.bgt.buttonClicked.connect(self.tableButtonClicked)
        # signal/slot
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
        # add change date/event dialog shortcut
        ced = QAction('Change Event and date', self)
        ced.setShortcut('Ctrl+F12')
        ced.triggered.connect(self.changeEventDate)
        self.addAction(ced)
        self.dateTimeDiff = None # date time difference for event date change in seconds (int)
        sfb = QAction('Ser focus on web order input', self)
        sfb.setShortcut('Ctrl+F11')
        sfb.triggered.connect(lambda: self.ui.lineEditBarCode.setFocus())
        self.addAction(sfb)
        # clock
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()
        # initialize window and cash desk description
        self.updateWindowTile()
        # initialize
        self.resetDialog()
        
    def updateWindowTile(self):
        "Update window title and cash desk description"
        cd = get_cash_desk_description()
        if not cd:
            cd = _tr('OrderDialog', 'cash desk name to set')
        self.ui.labelCashDeskDescription.setText(cd)
        txt = _tr('OrderDialog', "Company: ") # mind the space
        txt += session['company_description'] + ' '
        txt += _tr('OrderDialog', 'User: ') # mind the space
        txt += session['app_user_code'] + ' '
        txt += _tr('OrderDialog', 'Event: ') # mind the space
        txt += session['event_description'] + ' '
        txt += _tr('OrderDialog', "Cash Desk: ") # mind the space
        txt += cd + '    '
        txt += _tr('OrderDialog', '[Press ESC to quit]')
        self.setWindowTitle(txt)
        
    def changeEventDate(self):
        "Change current date/event"
        dateTime, ok = DateTimeInputDialog(_tr('OrderDialog', 'Select the date for event selection:'))
        if not ok:
            return
        # set datediff
        #print("New Event", get_event_from_date(dateTime))
        if dateTime.isValid():
            self.dateTimeDiff = QDateTime.currentDateTime().secsTo(dateTime)
        else:
            self.dateTimeDiff = None
        dt = QDateTime.currentDateTime()
        dt = dt.addSecs(self.dateTimeDiff or 0) # consider date time difference
        session['event_id'], session['event_description'] = get_event_from_date(dt)
        self.updateWindowTile()

    def tableTakeAway(self, state):
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

    def resetAdvice(self):
        "Reset dialog advice from idle timer"
        message = _tr("OrderDialog", "Warning: No order inserted since {} seconds.\n"
                      "It is recommended to update the window data, "
                      "Update it now ?").format(self.setting['inactivity_time'])
        if QMessageBox.question(self,
                                _tr("OrderDialog", "Question"),
                                message,
                                QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            self.resetDialog()
        self.idleTimer.start()  # restart timer anyway

    def showTime(self):
        "Show time on a fixed format"
        dt = QDateTime.currentDateTime()
        dt = dt.addSecs(self.dateTimeDiff or 0) # consider date time difference
        if (dt.time().second() % 2) == 0: # flashing ':'
            text = dt.toString('dd.MM.yyyy  hh:mm')
        else:
            text = dt.toString('dd.MM.yyyy  hh mm')
        self.ui.lcdNumberTime.display(text)

    def checkCovers(self, value):
        if value > self.setting['max_covers']:
            QMessageBox.warning(self,
                                _tr("OrderDialog", "Warning"),
                                _tr("OrderDialog", "Warning: the number of covers is greater than {}").format(self.setting['max_covers']))
            self.ui.spinBoxCovers.setFocus()

    def tablesOrder(self):
        if not self.setting['use_table_list']:
            return
        if self.ui.stackedWidgetTableOrder.currentIndex() == 0:
            self.ui.stackedWidgetTableOrder.setCurrentIndex(1)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Order'))
        else:
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
            self.ui.pushButtonTablesSwitch.setText(_tr('OrderDialog', 'Tables'))

    def toggleLevel(self, toggled):
        "Hide/unhide level in list buttons"
        for b in self.ui.bgi.buttons():
            if toggled:
                b.showLevel()
            else:
                b.hideLevel()

    def resetDialog(self):
        "Setup initial dialog's values"
        # exit if no event available for the current date (changed event table)
        if not session['event_id']:
            QMessageBox.warning(session['mainwin'],
                                _tr('MessageDialog', 'Warning'),
                                _tr('OrderDialog', 'No event available, for order entry '
                                    'is necessary to setup an event for the current date'))
            # save geometry
            st = QSettings()
            st.setValue("OrderDialoGeometry", self.saveGeometry())
            QDialog.reject(self)
        # warns if have any item already selected
        if self.ui.tabWidgetOrder.rowCount() != 0:
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    _tr('OrderDialog', "There are items already entered, "
                                        "the item list will be cleared, proceed anyway ?"),
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No) == QMessageBox.No:
                return
        #get_current_event()  # update current event, don't need this as File\Events updates everything
        if self.setting['default_delivery_type'] == 'T': # tables
            self.ui.radioButtonTable.setChecked(True)
            self.ui.lineEditTable.setEnabled(True)
            self.ui.lineEditTable.clear()
            self.ui.lineEditCustomerName.setEnabled(True)
            self.ui.lineEditCustomerName.clear()
            self.ui.spinBoxCovers.setEnabled(True)
            self.ui.spinBoxCovers.setValue(0)
            if self.setting['use_table_list']:
                self.ui.pushButtonTablesSwitch.setEnabled(True)
                self.ui.stackedWidgetTableOrder.setCurrentIndex(1)
            else:
                self.ui.pushButtonTablesSwitch.setDisabled(True)
                self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
        else:  # takeaway
            self.ui.radioButtonTakeAway.setChecked(True)
            self.ui.lineEditTable.setDisabled(True)
            self.ui.lineEditTable.clear()
            self.ui.lineEditCustomerName.setEnabled(True)
            self.ui.lineEditCustomerName.clear()
            self.ui.spinBoxCovers.setEnabled(False)
            self.ui.spinBoxCovers.setValue(0)
            self.ui.pushButtonTablesSwitch.setDisabled(True)
            self.ui.stackedWidgetTableOrder.setCurrentIndex(0)
        # electronic payment check
        if self.setting['default_payment_type'] == 'E':
            self.ui.checkBoxElectronicPayment.setChecked(True)
        else:
            self.ui.checkBoxElectronicPayment.setChecked(False)
        # remove all item buttons
        while self.ui.tabWidgetList.count() != 0:
            self.ui.tabWidgetList.widget(self.ui.tabWidgetList.currentIndex()).close()
            self.ui.tabWidgetList.removeTab(self.ui.tabWidgetList.currentIndex())
        # remove all rows in order
        for i in range(self.ui.tabWidgetOrder.rowCount(), -1, -1):
            self.ui.tabWidgetOrder.removeRow(i)
        # disable show variants button on automatic popup
        if self.setting['automatic_show_variants']:
            self.ui.pushButtonVariants.setDisabled(True)
        # disable show level on always show stock
        if self.setting['always_show_stock_inventory']:
            self.ui.pushButtonShowLevel.setDisabled(True)
        self.ui.radioButton1.setChecked(True)
        self.ui.doubleSpinBoxSubTotal.setValue(0.0)
        self.ui.doubleSpinBoxDiscount.setValue(0.0)
        self.ui.doubleSpinBoxTotal.setValue(0.0)
        self.ui.doubleSpinBoxCash.setValue(0.0)
        self.ui.doubleSpinBoxChange.setValue(0.0)
        # tabs and buttons for items
        self.ui.bgi = QButtonGroup(self)
        self.ui.bgi.setExclusive(False)
        for i, dep in department_list(include_menu=True):
            ti = self.ui.tabWidgetList.addTab(QWidget(), dep)
            gl = QGridLayout()
            gl.setSpacing(self.setting['order_list_spacing'])
            for ji, jd, jp, jr, jc, jl, jx, jtc, jbc, jv, js in item_list(session['event_id'], i):
                # check item position
                if not jr or not jc:
                    message = _tr('OrderDialog', "Item '{}' lacks of position settings, will not be created").format(jd)
                    QMessageBox.information(self, "Attenzione", message)
                    continue
                b = ButtonList(jd, jtc, jbc, self) # item description
                b.id = ji # item id
                b.price = jp # item price
                b.sc = jl # has stock control
                b.hasVariants = jv # has variants
                b.level = js # current level
                b.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                self.ui.bgi.addButton(b, ji)  # assign an id = item id for find button later
                gl.addWidget(b, jr, jc)
            # fill the remaining cells of gl with an empty buttonlist
            for r in range(1, self.ui.list_rows + 1):
                for c in range(1, self.ui.list_columns + 1):
                    if gl.itemAtPosition(r, c) is None:
                        w = QWidget(self)
                        w.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                        gl.addWidget(w, r, c)
            self.ui.tabWidgetList.widget(ti).setLayout(gl)
        # enable/disable tabs
        if self.ui.radioButtonTakeAway.isChecked():
            for i in range(self.ui.tabWidgetList.count()):
                if self.ui.tabWidgetList.tabText(i) in department_takeaway_list():
                    self.ui.tabWidgetList.widget(i).setEnabled(True)
                else:
                    self.ui.tabWidgetList.widget(i).setDisabled(True)
        # list button group
        self.ui.bgi.buttonClicked.connect(self.buttonClicked)
        # clear notes
        self.ui.depnote.clear()
        for button in self.ui.bgnotes.buttons():
            button.setIcon(currentIcon['empty'])
        # idle control
        if self.setting['check_inactivity']:
            self.idleTimer.start()
        # focus on covers
        self.ui.lineEditTable.setFocus()
        # test for get list of buttons an item id
        #for i in self.bgi.buttons():
            #print(i.id)

    def buttonClicked(self, button, ivars = "",  priced = decimal.Decimal(0.0)): # price delta
        "React to button clicked. If provided vars and price delta don't lookup in database"
        # variants
        if button.hasVariants:
            if not ivars:
                if (not self.ui.pushButtonVariants.isEnabled()) or self.ui.pushButtonVariants.isChecked():
                    dlg = ChooseVariantDialog(self, button.description, get_variants(button.id))
                    rv = dlg.exec_()
                    if rv:
                        ivars, priced = dlg.getVariants()
                    dlg.close()
                    if not rv:
                        return
                if self.ui.pushButtonVariants.isEnabled():
                    self.ui.pushButtonVariants.setChecked(False)
        if not button.isEnabled():  # button.sc and button.level == 0:
            return
        qty = int(self.ui.buttonGroupQuantity.checkedButton().text())
        self.ui.radioButton1.setChecked(True)
        # look for same item in grid (item and variants)
        for i in range(self.ui.tabWidgetOrder.rowCount()):
            if (button.id == int(self.ui.tabWidgetOrder.item(i, ID).data(Qt.DisplayRole))
                    and ivars == self.ui.tabWidgetOrder.item(i, VARIANTS).data(Qt.DisplayRole)):
                old_qty = int(self.ui.tabWidgetOrder.item(i, QTY).data(Qt.DisplayRole))
                if button.sc and (button.level - qty < 0):
                    return #skip if go underzero (zero allowed)
                self.ui.tabWidgetOrder.item(i, QTY).setData(Qt.DisplayRole, old_qty + qty)
                # update amount
                price = fromCurrency(self.ui.tabWidgetOrder.item(i, PRICE).data(Qt.DisplayRole) or 0.0)
                self.ui.tabWidgetOrder.item(i, AMOUNT).setData(Qt.DisplayRole, toCurrency((old_qty + qty) * price))
                self.recalcTotals()
                # update button.level value
                if button.sc:
                    button.level = button.level - qty
                return
        # not found, insert new row
        row = self.ui.tabWidgetOrder.rowCount()
        self.ui.tabWidgetOrder.insertRow(row)
        cell = QTableWidgetItem(str(button.id))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tabWidgetOrder.setItem(row, ID, cell)
        cell = QTableWidgetItem(ivars)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tabWidgetOrder.setItem(row, VARIANTS, cell)
        cell = QTableWidgetItem(button.description + " " + ivars)
        cell.setToolTip(button.description + " " + ivars)
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.ui.tabWidgetOrder.setItem(row, DESC, cell)
        cell = QTableWidgetItem(str(qty))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.tabWidgetOrder.setItem(row, QTY, cell)
        cell = QTableWidgetItem(toCurrency(button.price + priced))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        cell.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.ui.tabWidgetOrder.setItem(row, PRICE, cell)
        cell = QTableWidgetItem(toCurrency(qty * (button.price + priced)))
        cell.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        cell.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.tabWidgetOrder.setItem(row, AMOUNT, cell)
        self.ui.tabWidgetOrder.scrollToBottom()
        self.recalcTotals()
        # update button.level value
        if button.sc:
            button.level = button.level - qty

    def tableButtonClicked(self, button):
        self.ui.lineEditTable.setText(button.text())
        #self.stackedWidgetTableOrder.setCurrentIndex(0)
        self.tablesOrder()

    def orderCellClicked(self, row, column):
        qty = int(self.ui.buttonGroupQuantity.checkedButton().text())
        self.ui.radioButton1.setChecked(True)
        old_qty = int(self.ui.tabWidgetOrder.item(row, QTY).data(Qt.DisplayRole))
        self.ui.tabWidgetOrder.item(row, QTY).setData(Qt.DisplayRole, old_qty - qty)
        # update amount
        price = fromCurrency((self.ui.tabWidgetOrder.item(row, PRICE).data(Qt.DisplayRole)))
        self.ui.tabWidgetOrder.item(row, AMOUNT).setData(Qt.DisplayRole, toCurrency((old_qty - qty) * price))
        # look for item in list for correct level value
        for b in self.ui.bgi.buttons():
            if b.id == int(self.ui.tabWidgetOrder.item(row, ID).data(Qt.DisplayRole)):
                if b.sc:
                    b.level = b.level + qty
        if (old_qty - qty) <= 0:
            self.ui.tabWidgetOrder.removeRow(row)
        self.recalcTotals()

    def bgNotesClicked(self, button):
        bid = self.ui.bgnotes.id(button)
        txt = self.ui.depnote.get(bid)
        text, ok = QInputDialog.getMultiLineText(self,
                                                 _tr("OrderDialog", "Department note"),
                                                 _tr("OrderDialog", "Message text for {}".format(get_department_desc(bid))),
                                                 txt)
        if ok:
            self.ui.depnote[bid] = text or None
        if self.ui.depnote.get(bid):
            button.setIcon(currentIcon['order_note'])
        else:
            button.setIcon(currentIcon['empty'])

    #def importWebOrder(self):
        #"Import weborder data from QR Code identifier"
        #dlg = ImportWebOrderDialog(self)
        # dlg.exec_()

    # def processReturn(self):
    #     return

    @Slot()
    def processWebOrder(self):
        "Fill order form based on web order details or QRC data"
        # disconnect ditingFinished to avoid calling it 2 times (return pressed and lost focus)
        self.ui.lineEditBarCode.editingFinished.disconnect()
        try:
            # check if web order int or web order QRC
            value = self.ui.lineEditBarCode.text()
            if not value:  # can happend when loosing focus without insert enything
                return
            #****************************
            # manage weborder QR Code
            # start resetting the dialog
            self.resetDialog()
            # parse QRC data
            try:
                
                qtype, qdelivery, qtable, qname, qcovers, qemail = value.split(';')[:6]
                itm = value.split(";")[6:][0::4] 
                var = value.split(";")[6:][1::4] 
                prd = value.split(";")[6:][2::4]
                qty = value.split(";")[6:][3::4]
            except Exception as er:
                msg = _tr('OrderDialog', f"Unrecognized QRC structure:") + f"\n{str(er)}"
                QMessageBox.critical(self,
                                    _tr("MessageDialog", "Critical"),
                                    _tr('OrderDialog', msg))
                self.ui.lineEditBarCode.clear()
                return
            # sanity checkes
            err = []
            if qtype != 'PSQRC':
                err.append(_tr('OrderDialog', f'Unrecognized QRC format:') + f" {qtype}")
            if qdelivery not in ('T', 'A'):
                err.append(_tr('OrderDialog', f'Unrecognized delivery option:') + f" {qdelivery}")
            if qcovers:
                if not qcovers.isdigit():
                    err.append(_tr('OrderDialog', f'Unrecognized covers number:') + f" {qcovers}")
            if err:
                msg = _tr('OrderDialog', f'Unrecognized parameters:') + f"\n{'\n'.join(err)}"
                QMessageBox.critical(self,
                                    _tr("MessageDialog", "Critical"),
                                    _tr('OrderDialog', msg))
                return           
            # move to order widget
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
            unavailable = dict()
        
            for i, v, p, q in zip(itm, var, prd, qty):
                # order line sanity checks
                if not i.isdigit():
                    msg = _tr('OrderDialog', f'Unrecognized item id:') + f" {i}"
                    QMessageBox.critical(self,
                                    _tr("MessageDialog", "Critical"),
                                    _tr('OrderDialog', msg))
                    return
                if not q.isdigit():   
                    msg = _tr('OrderDialog', f"Unrecognized quantity:") + f" {q}"
                    QMessageBox.critical(self,
                                    _tr("MessageDialog", "Critical"),
                                    _tr('OrderDialog', msg))
                    return        
                for j in range(int(q)): # repeat until quantity reached
                    b = self.ui.bgi.button(int(i)) # Returns the button with the specified id
                    if b is None:
                        QMessageBox.critical(self,
                                            _tr("MessageDialog", "Critical"),
                                            _tr('OrderDialog', "Item NOT available in buttons' grid, web order skipped"))
                        return
                    if b.isEnabled():
                        self.buttonClicked(b, v, decimal.Decimal(p))
                    else:
                        unavailable[b.text()] = unavailable.get(b.text(), 0) + 1
            # warn of anavailable items
            if unavailable:
                msg = _tr("OrderDialog", "These items are not available and not "
                        "included in the order:\n")
                msg += "\n".join(["{:>2}  {:<20}".format(q, i).replace('\n', ' ')
                                for i, q in unavailable.items()])
                QMessageBox.warning(self,
                                    _tr("MessageDialog", "Warning"),
                                    msg)
        finally:
            # clear barcode line edit
            self.ui.lineEditBarCode.clear()
            # riconnect signal
            self.ui.lineEditBarCode.editingFinished.connect(self.processWebOrder)


    def electronicPaymentToggled(self, checked):
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

    def recalcTotals(self):
        subtotal = decimal.Decimal(0.0)
        for i in range(self.ui.tabWidgetOrder.rowCount()):
            amount = fromCurrency(self.ui.tabWidgetOrder.item(i, AMOUNT).data(Qt.DisplayRole) or 0.0)
            subtotal += amount
        self.ui.doubleSpinBoxSubTotal.setValue(subtotal)
        discount = decimal.Decimal(self.ui.doubleSpinBoxDiscount.value())
        cash = decimal.Decimal(self.ui.doubleSpinBoxCash.value())
        self.ui.doubleSpinBoxTotal.setValue(subtotal - discount)
        self.ui.doubleSpinBoxChange.setValue(max(cash - subtotal + discount, 0))


    def accept(self):
        "Generate, save and print the order"
        #-------------------------#
        #-- SANITY CHECKS FIRST --#
        #-------------------------#
        # no items selected
        if self.ui.tabWidgetOrder.rowCount() == 0:
            msg = _tr('OrderDialog', "No item inserted!")
            QMessageBox.warning(self,
                                _tr('MessageDialog', "Warning"),
                                msg)
            return
        # mandatory table number
        if (self.setting['mandatory_table_number']
            and self.ui.radioButtonTable.isChecked()
                and not self.ui.lineEditTable.text().strip()):
            msg = _tr("OrderDialog", "The table number is missing!")
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                msg)
            self.ui.lineEditTable.setFocus()
            return
        # unknown table number
        if (self.setting['mandatory_table_number'] and self.setting['use_table_list']
            and self.ui.radioButtonTable.isChecked()):
            if not table_exists(self.ui.lineEditTable.text().strip()):
                msg = _tr("OrderDialog", "The table number does not exist, use it anyway ?")
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        msg,
                                        QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
                    self.ui.lineEditTable.setFocus()
                    return
        # no customer name for a takeaway order
        if self.ui.radioButtonTakeAway.isChecked() and not self.ui.lineEditCustomerName.text():
            msg = _tr("OrderDialog", "Customer's name is missing!")
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                msg)
            self.ui.lineEditCustomerName.setFocus()
            return
        # no covers for table delivery
        if self.ui.radioButtonTable.isChecked() and not self.ui.spinBoxCovers.value():
            msg = _tr("OrderDialog", "Warning: there are no seats even "
                          "though delivery to the table has been indicated,\n"
                          "do you want to correct it?")
            if QMessageBox.question(self,
                                    _tr("MessageDialog", "Question"),
                                    msg,
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.ui.spinBoxCovers.setFocus()
                self.ui.spinBoxCovers.selectAll()
                return
        # discount > total amount
        if decimal.Decimal(self.ui.doubleSpinBoxDiscount.value()) > decimal.Decimal(self.ui.doubleSpinBoxSubTotal.value()):
            msg = _tr("OrderDialog", "Discount amount greater than the total amount!")
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                msg)
            self.ui.doubleSpinBoxDiscount.setFocus()
            self.ui.doubleSpinBoxDiscount.selectAll()
            return
        # if takeaway allow only items of the right department
        if self.ui.radioButtonTakeAway.isChecked():
            nogood = []
            for i in range(self.ui.tabWidgetOrder.rowCount()):
                item = int(self.ui.tabWidgetOrder.item(i, ID).data(Qt.DisplayRole))
                if not is_for_takeaway(item):
                    nogood.append(get_item_desc(item))
            if nogood:
                msg = _tr('OrderDialog', "Warning: the following items are not available for take away:\n"
                              "- {}\n\nDo i proceed anyway ?".format("\n- ".join(nogood)))
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        msg,
                                        QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                    return

        #-----------------#
        #-- ok, proceed --#
        #-----------------#
        order = Order()
        order.header['date_time'] = QDateTime.currentDateTime().addSecs(self.dateTimeDiff or 0)
        # event, statistic date and day part are set in Order.insert()
        order.header['cash_desk'] = self.ui.labelCashDeskDescription.text()
        order.header['delivery'] = 'T' if self.ui.radioButtonTable.isChecked() else 'A' # (T)able or take (A)way
        order.header['is_electronic_payment'] =  self.ui.checkBoxElectronicPayment.isChecked()
        order.header['is_from_web'] =  self.ui.checkBoxWebOrder.isChecked()
        order.header['table_num'] = self.ui.lineEditTable.text().strip() or None
        order.header['customer_name'] = self.ui.lineEditCustomerName.text() or None
        order.header['customer_contact'] = self.ui.lineEditCustomerContact.text() or None
        order.header['covers'] = int(self.ui.spinBoxCovers.value())
        order.header['total_amount'] = decimal.Decimal(self.ui.doubleSpinBoxSubTotal.value())
        order.header['discount'] = decimal.Decimal(self.ui.doubleSpinBoxDiscount.value())
        order.header['cash'] = decimal.Decimal(self.ui.doubleSpinBoxCash.value())
        order.header['change'] = decimal.Decimal(self.ui.doubleSpinBoxChange.value())
        for i in range(self.ui.tabWidgetOrder.rowCount()):
            line = dict()
            line['item_id'] = int(self.ui.tabWidgetOrder.item(i, ID).data(Qt.DisplayRole))
            line['variants'] = self.ui.tabWidgetOrder.item(i, VARIANTS).data(Qt.DisplayRole) or None
            line['quantity'] = int(self.ui.tabWidgetOrder.item(i, QTY).data(Qt.DisplayRole))
            line['price'] = fromCurrency(self.ui.tabWidgetOrder.item(i, PRICE).data(Qt.DisplayRole))
            line['amount'] = fromCurrency(self.ui.tabWidgetOrder.item(i, AMOUNT).data(Qt.DisplayRole))
            order.lines.append(line)
        # check out of stock item
        ofsi = order.out_of_stock()
        if ofsi:
            msg = (_tr('OrderDialog', "Warning: these items are unavailable "
                           "for the curent order:\n\n"
                           "- {0}\n\nDo i proceed anyway ?").format("\n- ".join(ofsi)))
            if QMessageBox.question(self,
                                    _tr('MessageDialog', "Question"),
                                    msg,
                                    QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return
        # notes
        order.depnote.update(self.ui.depnote)
        # SAVE
        try:
            ti, used_dep = order.insert()  # ti = order header id
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
            return
        # PRINT ORDER
        # customer copy
        if self.setting['print_customer_copy']:
            printer = get_printer_name(self.setting['customer_printer_class'], session['hostname'])
            try:
                printOrderReport(ti, printer)
            except Exception as er:
                QMessageBox.critical(self,
                                     _tr("MessageDialog", "Critical"),
                                     _tr('OrderDialog', "Unable to print order customer copy:\n{}").format(er))   
        # covers copy
        if self.setting['print_cover_copy'] and order.header['delivery'] == 'T':
            printer = get_printer_name(self.setting['cover_printer_class'], session['hostname'])
            try:
                printOrderCoverReport(ti, printer)
            except Exception as er:
                QMessageBox.critical(self,
                                     _tr("MessageDialog", "Critical"),
                                     _tr('OrderDialog', "Unable to print order cover copy:\n{}").format(er))   
                
        # departments copies
        if self.setting['print_department_copy']:
            for i in used_dep:
                prncls = get_department_printer_class(i)
                if not prncls:
                    continue
                printer = get_printer_name(prncls, session['hostname'])
                try:
                    printOrderDepartmentReport(ti, i, printer)
                except Exception as er:
                    QMessageBox.critical(self,
                                         _tr("MessageDialog", "Critical"),
                                         _tr('OrderDialog', "Unable to print order department copy:\n{}").format(er)) 
        # check stock unload report
        if self.setting['print_ordered_delivered_report']:
            # get orders issued in the half day from last inserted order header
            n = get_orders_issued(order.header['event_id'],
                                  order.header['stat_order_date'],
                                  order.header['stat_order_day_part'])
            printer = get_printer_name(self.setting['ordered_delivered_printer_class'], session['hostname'])
            try:
                printStockUnloadReport(self.setting['ordered_delivered_report'],
                                        session['l10n'],
                                        printer,
                                        self.setting['ordered_delivered_copies'],
                                        order.header['event'],
                                        order.header['stat_order_date'],
                                        order.header['stat_order_day_part'])
            except Exception as er:
                QMessageBox.critical(self,
                                        _tr("MessageDialog", "Critical"),
                                        _tr('OrderDialog', "Unable to print stock unload report:\n{}").format(er)) 
                        
        # clear order list before reset otherwise save + reset = reset
        for i in range(self.ui.tabWidgetOrder.rowCount(), -1, -1):
            self.ui.tabWidgetOrder.removeRow(i)
        self.resetDialog()

    def reject(self):
        "Close the dialog"
        msg = _tr("OrderDialog", "Do you want to exit the order entry?")
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                msg,
                                QMessageBox.Yes|QMessageBox.No, # butons
                                QMessageBox.No # default botton
                                ) == QMessageBox.Yes:
            # save geometry
            st = QSettings()
            st.setValue("OrderDialogGeometry", self.saveGeometry())
            QDialog.reject(self)


# EOF
