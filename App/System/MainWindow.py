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

"""Main window

This module is the main user interface, manage tabs and actions

"""

# standard library
import sys
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QLocale
from PySide6.QtCore import QRectF
from PySide6.QtCore import QSettings
from PySide6.QtCore import QEvent
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QAction
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QPainter
from PySide6.QtGui import QColor
from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QComboBox
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QWidgetAction
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QFrame
from PySide6.QtWidgets import QToolBar
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMenuBar
from PySide6.QtWidgets import QTabWidget

# application modules
from App import session
from App import actionDefinition
from App import currentAction
from App import currentIcon
from App import APPNAME
from App.Core.L10n import _tr
from App.System.Login import ChangeCompanyDialog
from App.System.Action import createActionDictionary
from App.Database.Connect import appconn
from App.Database.Gui import get_actions
from App.Database.Gui import get_menu
from App.Database.Gui import get_toolbar
from App.System.Preferences import tool_button_style
from App.System.Preferences import tab_position

from App.Ui.GoToDialog import Ui_GoToDialog

# logger
logger = logging.getLogger(__name__)


# default navigation status, when no tab is open nothing is available
NSEMPTY = (False,) * 15

COUNTER_NORMAL = ("QLineEdit {border: 1px solid; "
                  "border-radius: 3px; "
                  "border-color: grey;};")

COUNTER_LIMIT = ("QLineEdit {border: 1px solid; "
                 "border-radius: 3px; "
                 "color: red; "
                 "border-color: grey;};")

# action definition fields
DESC = 0 # description
SLOT = 1 # slot
CHCK = 2 # checkable
ICON = 3 # icon name
SHCT = 4 # shortcut
TOOL = 5 # tooltip
STAT = 6 # status tip
WHAT = 7 # what's this
MERO = 8 # menu role


# create actions (main window)

def createActions(mainWindow: MainWindow) -> None:
    # create available actions
    createActionDictionary(mainWindow)
    action: QAction|QWidgetAction
    # create active actions for user's profile
    for act, aut in get_actions(): # base
        if act not in actionDefinition:
            continue
        if act == 'edit_counter':
            # widgetAction for record counter current
            action = QWidgetAction(mainWindow)
            action.setDefaultWidget(mainWindow.counter)
        else:
            # regular action for anything else
            action = QAction(actionDefinition[act][DESC], mainWindow)  # description
        
        action.setMenuRole(actionDefinition[act][MERO])
        
        action.setData(aut) # authorization

        if actionDefinition[act][SLOT]:  # slot, passing qaction
            action.triggered.connect(actionDefinition[act][SLOT])
        if actionDefinition[act][CHCK]:  # chackable
            action.setCheckable(True)
        if actionDefinition[act][ICON]:  # icon
            action.setIcon(currentIcon[actionDefinition[act][ICON]])
        if actionDefinition[act][SHCT]:  # standard key shortcut
            action.setShortcut(actionDefinition[act][SHCT])
        if actionDefinition[act][TOOL]:  # tooltip
            action.setToolTip(actionDefinition[act][TOOL])
        if actionDefinition[act][STAT]:  # statustip
            action.setStatusTip(actionDefinition[act][STAT])
        if actionDefinition[act][WHAT]:  # whatsthis
            action.setWhatsThis(actionDefinition[act][WHAT])
        
        mainWindow.addAction(action)
        currentAction[act] = action
        

# create menu

def addMenuItems(item: str, menu: QMenuBar|QMenu) -> None:
    "Add action or submenu to menu"
    for child, itemType, description, action in get_menu(item):
        if itemType == 'S':
            menu.addSeparator()
        elif itemType == 'M':
            subMenu = menu.addMenu(description)
            addMenuItems(child, subMenu)
        else:
            if action in currentAction:
                menu.addAction(currentAction[action])

def createMenuBar(mainWindow: QMainWindow) -> None:
    "Create menu bar adding menus"
    menuBar = QMenuBar() # for MAC we need to create a menubar and set later
    for child, itemType, description, action in get_menu(session['menu']):
        menu = menuBar.addMenu(description or "EMPTY MENU")
        addMenuItems(child, menu)
    mainWindow.setMenuBar(menuBar)

# create toolbars

def createToolBar(mainWindow: QMainWindow) -> None:
    "Create toolbars"
    for child, itemType, description, action in get_toolbar(session['toolbar']):
        toolBar = QToolBar(description)
        toolBar.setObjectName(description)
        toolBar.setToolButtonStyle(tool_button_style[session['tool_button_style'] or 'I'])
        for child2, itemType2, description2, action2 in get_toolbar(child):
            if itemType2 == 'S':
                toolBar.addSeparator()
            else:
                if action2 in currentAction:
                    a = currentAction[action2]
                    sc = a.shortcut()
                    if sc:
                        t = a.toolTip()
                        s = sc.toString()
                        a.setToolTip(t + f" [{s}]")
                    toolBar.addAction(a)
        mainWindow.addToolBar(toolBar)

# custom tab widget

class TabWidget(QTabWidget):

    def __init__(self, mainWin: MainWindow) -> None:
        super().__init__(mainWin)
        self.appimage = QPixmap(f":/{APPNAME}")
        # close current tab
        #act = QAction(_tr('MainWindow', "Close current tab"), self)
        #act.setShortcut("Ctrl+K")
        #act.triggered.connect(mainWin.closeTab)
        #self.addAction(act)
        # close all tabs
        aca = QAction(_tr('MainWindow', "Close all tabs"), self)
        aca.setShortcut("Ctrl+Shift+K")
        aca.triggered.connect(mainWin.closeAllTabs)
        self.addAction(aca)
        # show/hide tabbar
        ast = QAction(_tr('MainWindow', "Show tabbar"), self)
        ast.setCheckable(True)
        ast.setChecked(True)
        ast.triggered.connect(mainWin.hideTabBar)
        self.addAction(ast)
        #self.setStyleSheet(None)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        if self.count() != 0:
            return
        if session['event_image'] or session['company_image']:
            img = QPixmap()
            img.loadFromData(session['event_image'] or session['company_image'])
        else:
            img = self.appimage
        painter = QPainter(self)
        # colors
        if QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Light:
            color1 = QColor('#BBBBBB')
            color2 = QColor('#221155')
        else:
            color1 = QColor('#777722')
            color2 = QColor('#F0F040')
        # company
        x = (self.width() - img.width()) // 2
        y = (self.height() - img.height()) // 2
        painter.drawPixmap(x, y, img)
        painter.setPen(color1)
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold, True))
        painter.drawText(QRectF(3,   # x
                                50, # y
                                self.width(), # width
                                60), # height
                         Qt.AlignmentFlag.AlignCenter,
                         session['company_description'][:40])
        painter.setPen(color2)
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold, True))
        painter.drawText(QRectF(0,   # x
                                47, # y
                                self.width(), # width
                                60), # height
                         Qt.AlignmentFlag.AlignCenter,
                         session['company_description'][:40])
        # event
        msg = _tr('MainWindow', 'No event available')
        evds = f"{session['event_description'] or msg}"
        painter.setPen(color1)
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold, True))
        painter.drawText(QRectF(3,   # x
                                self.height() - 150,  # y
                                self.width(),  # width
                                60),  # height
                         Qt.AlignmentFlag.AlignCenter,
                         evds)
        painter.setPen(color2)
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold, True))
        painter.drawText(QRectF(0,   # x
                                self.height() - 153,  # y
                                self.width(),  # width
                                60),  # height
                         Qt.AlignmentFlag.AlignCenter,
                         evds)



# -------------------------------------------------------------------------- #
# --  MAIN  WINDOW
# -------------------------------------------------------------------------- #

class MainWindow(QMainWindow):
    """Application Main Window"""

    def __init__(self, parent: QWidget|None = None) -> None:
        """Initialization"""
        super().__init__(parent)
        # window title
        self.setWindowTitle(APPNAME + ' - ' + session['company_description'])
        # create main window central widget
        # tab widget = central widget
        self.tabWidget = TabWidget(self)
        self.tabWidget.setTabPosition(tab_position[session['tab_position'] or 'N'])
        self.tabWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideRight)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tabWidget)
        # change tab action
        self.tabWidget.currentChanged.connect(self.tabChanged)
        # setup UI
        self.updateActionMenuToolbar()
        # setup status bar
        # create status bar
        self.status_bar = self.statusBar()
        self.status_user = QLabel()
        #self.status_profile = QLabel()
        self.status_company = QLabel()
        self.status_user.setFrameShape(QFrame.Shape.Panel)
        self.status_user.setFrameShadow(QFrame.Shadow.Sunken)
        self.status_company.setFrameShape(QFrame.Shape.Panel)
        self.status_company.setFrameShadow(QFrame.Shadow.Sunken)
        self.status_bar.addPermanentWidget(self.status_user)
        #self.status_bar.addPermanentWidget(self.status_profile)
        self.status_bar.addPermanentWidget(self.status_company)
        # set user
        user_desc = f"{session['app_user_code']}"
        if len(user_desc) > 32:
            user_desc = user_desc[:29] + "..."
        txt1 = _tr('MainWindow', "User")
        txt2 = f"<b>{txt1}:</b> {user_desc}"
        self.status_user.setText(txt2)
        self.updateStatusBar()
        # finally restore window sate
        st = QSettings()
        if st.value("MainWindowGeometry"):
            self.restoreGeometry(st.value("MainWindowGeometry"))
        else:  # useful default
            self.setGeometry(50, 50, 800, 600)
        # center windows
        self.setGeometry(QStyle.alignedRect(Qt.LayoutDirection.LeftToRight,
                                            Qt.AlignmentFlag.AlignCenter,
                                            self.size(),
                                            QGuiApplication.primaryScreen().availableGeometry()))
        if st.value("MainWindowState"):
            self.restoreState(st.value("MainWindowState"), 1)
        # and set initial edit status
        self.updateEditStatus(NSEMPTY, -1, -1, None)

    def updateActionMenuToolbar(self) -> None:
        "Delete/recreate actions/menus/toolbars on access/change company"
        # delete everything already in place
        currentAction.clear() # clear action dictionary
        # toolbars
        for i in self.findChildren(QToolBar):
            i.clear() # clear toolbar button
            self.removeToolBar(i) # remove toolbar from main window
        # menu bar
        if self.menuBar():
            self.menuBar().clear() # clear menu from menu bar
        # actions
        for a in self.actions():
            self.removeAction(a) # remove actions from main window
            a.deleteLater() # delete old actions
        # create new UI
        # record counter, must be set after connection, user can change font
        self.counter = QLineEdit("-- / --", self)
        self.counter.setStatusTip(_tr('MainWindow', "Current view's record "
                                      "counter, shows current record number and total records count"))
        self.counter.setToolTip(_tr('MainWindow', "Current view's record counter"))
        font = QFont()
        font.setBold(True)
        self.counter.setFont(font)
        self.counter.setStyleSheet(COUNTER_NORMAL)
        self.counter.setFixedWidth(120)
        self.counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter.setReadOnly(True)
        # actions
        createActions(self)
        # create menu' and toolbars
        createMenuBar(self)
        createToolBar(self)

    def updateEditStatus(self, status: tuple, current: int, total: int, limit: int|None = None) -> None:
        "Enable/disable navigation buttons and update counter"
        # status must be a tuple of 12 boolena values, current and total integers
        for i in range(12):
            currentAction[('edit_new',
                           'edit_save',
                           'edit_delete',
                           'edit_reload',
                           'edit_first',
                           'edit_previous',
                           'edit_next',
                           'edit_last',
                           'edit_filter',
                           'edit_change_view',
                           'edit_print',
                           'edit_export')[i]].setEnabled(status[i])
        # set counter status
        if current >= 0:
            self.counter.setText(f"{QLocale().toString(current)}/{QLocale().toString(total)}")
        else:
            self.counter.setText("-- / --")
        # show if limit was reached
        if limit and total == limit:
            self.counter.setStyleSheet(COUNTER_LIMIT)
        else:
            self.counter.setStyleSheet(COUNTER_NORMAL)

    def updateStatusBar(self) -> None:
        "Set status bar text on change company"
        # set company
        company_desc = f"{session['company_description']}"
        if len(company_desc) > 40:
            company_desc = company_desc[:37] + "..."
        txt1 = _tr('MainWindow', 'Company')
        txt2 = f"<b>{txt1}:</b> {company_desc}"
        self.status_company.setText(txt2)

    def addTab(self, tabname: str, widget: QWidget) -> None:
        "Add a new tab"
        # already exists
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == tabname:
                self.tabWidget.setCurrentIndex(i)
                return
        # not exists, create
        t = self.tabWidget.addTab(widget, tabname)
        self.tabWidget.setCurrentIndex(t)

    def closeTab(self, index: int) -> bool:
        "Close current tab"
        w = self.tabWidget.widget(index)
        if not w:
            return False
        if w.close():
            self.tabWidget.removeTab(index)
            # empty tab widget
            if self.tabWidget.count() == 0:
                self.updateEditStatus(NSEMPTY, -1, -1)
            return True
        return False

    def closeAllTabs(self) -> None:
        "Close all tabs"
        while self.tabWidget.count():
            if not self.closeTab(self.tabWidget.currentIndex()):
                break

    def hideTabBar(self) -> None:
        "Hide tabbar"
        if self.tabWidget.tabBar().isVisible():
            self.tabWidget.tabBar().setVisible(False)
        else:
            self.tabWidget.tabBar().setVisible(True)

    def tabChanged(self, tn: int) -> None:
        "Update edit status on tab change"
        if tn == -1:
            self.updateEditStatus(NSEMPTY, -1, -1, None)
        else:
            t = self.tabWidget.widget(tn)
            if t and hasattr(t, 'updateEditStatus'):
                t.updateEditStatus()
            else:
                self.updateEditStatus(NSEMPTY, -1, -1, None)

    # main action's slot redirection

    def new(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'new'):
            w.new()

    def save(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'save'):
            w.save()

    def delete(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'delete'):
            w.delete()

    def reload(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'reload'):
            if hasattr(w, 'reloadConfirmation') and w.reloadConfirmation:
                # confirmation request
                if QMessageBox.question(self,
                                        _tr("MessageDialog", "Question"),
                                        _tr("Form", "Undo changes and reload data ?"),
                                        QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,
                                        QMessageBox.StandardButton.No
                                        ) == QMessageBox.StandardButton.No:
                    return
                w.reload()

    # def addChild(self) -> None:
    #     w = self.tabWidget.currentWidget()
    #     if w and hasattr(w, 'addChild'):
    #         w.addChild()

    def add(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'add'):
            w.add()

    def remove(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'remove'):
            w.remove()

    def toFirst(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'toFirst'):
            w.toFirst()

    def toPrevious(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'toPrevious'):
            w.toPrevious()

    def toNext(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'toNext'):
            w.toNext()

    def toLast(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'toLast'):
            w.toLast()

    def changeView(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'changeView'):
            w.changeView()

    def setFilters(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'setFilters'):
            w.setFilters()

    def print(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'print'):
            w.print()

    def export(self) -> None:
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'export'):
            w.export()

    def disconnected(self, error: str) -> None:
        "Disconnected from db server, call by check notification"
        # _tr function can't be inside an f-string as it will not be recognized
        msg1 = _tr('MainWindow', "The connection is not active with the following error message:")
        msg2 = _tr('MainWindow', "Quitting the application...")
        QMessageBox.critical(self,
                             _tr('MessageDialog', "Critical"),
                             f"<p><b>{msg1}</b></p><pre><tt>{error}</tt></pre><b>{msg2}</b>",
                             QMessageBox.StandardButton.Ok)
        sys.exit(0)

    def changeCompany(self) -> None:
        "Change working company"
        # As is necessary to close tab on company change it'is better to put
        # this in main window
        if self.tabWidget.count() != 0:
            if QMessageBox.question(self,
                                    _tr('MessageDialog', "Question"),
                                    _tr('MainWindow', "Warning: open tabs will "
                                        "be closed, continue anyway ?"),
                                    QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                    QMessageBox.StandardButton.No  # default botton
                                    ) == QMessageBox.StandardButton.No:
                return
        # close all open tabs
        self.closeAllTabs()
        dlg = ChangeCompanyDialog(self)
        if dlg.exec() == QDialog.DialogCode.Rejected:
            return
        # update user interface
        self.updateActionMenuToolbar()
        self.setWindowTitle(APPNAME + ' - ' + session['company_description'])
        self.updateEditStatus(NSEMPTY, -1, -1, None)
        # update status bar
        self.updateStatusBar()

    def closeEvent(self, event: QEvent) -> None:
        "Confirm exiting request on closing"
        # _tr function can't be inside an f-string as it will not be recognized
        msg = _tr('MainWindow', 'Are you sure you want to quit')
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg} <b>{APPNAME}</b> ?",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.Yes:
            # save window state
            st = QSettings()
            st.setValue("MainWindowGeometry", self.saveGeometry())
            st.setValue("MainWindowState", self.saveState(1))
            # disconnect
            logger.info("DB disconnection")
            appconn.close()
            event.accept()
            logger.info('Closing the application')
            logger.info('****************************************')
        else:
            event.ignore()

    def helpLink(self) -> str:
        "Return contect help link if available"
        w = self.tabWidget.currentWidget()
        if w and hasattr(w, 'helpLink'):
            return w.helpLink
        else:
            return "help/main.html"

