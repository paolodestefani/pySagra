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

"""Connection

Management of current connections and connection history

"""

# standard library
import logging

# PySide6
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QVBoxLayout

# application modules
from App import session
from App import currentIcon
from App.Database.Exceptions import PyAppDBError
from App.Database.Connections import kill_client
from App.Database.Connections import delete_connection_history
from App.Database.System import pa_setting
from App.Database.System import pa_setting_set
from App.Database.Models import ConnectionModel
from App.Database.Models import ConnectionHistoryModel
from App.Ui.ConnectionWidget import Ui_ConnectionWidget
from App.Ui.ConnectionHistoryWidget import Ui_ConnectionHistoryWidget
from App.Core.L10n import _tr
from App.Widget.Form import FormViewManager
from App.Core.ExceptionHandler import gui_exception_context


# logger
logger = logging.getLogger(__name__)


def connection(action: QAction, checked: bool = False) -> None:
    "Show/Edit curent connections"
    logger.info('Starting connections Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('CashDesk', 'No access right to this archive'))
        return
    cw = ConnectionForm(mw, title, auth)
    cw.applySortFilter()
    mw.addTab(title, cw)
    logger.info('Connections Form added to main window')


def connectionHistory(action: QAction, checked: bool = False) -> None:
    "Show connections history, clear history"
    logger.info('Starting connections history Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('CashDesk', 'No access right to this archive'))
        return
    cw = ConnectionHistoryForm(mw, title, auth)
    cw.applySortFilter()
    mw.addTab(title, cw)
    logger.info('Connections history Form added to main window')


class ConnectionForm(FormViewManager):
    "Current connections form"

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = ConnectionModel()
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        self.reloadConfirmation = False
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, True, True, True, True,
                                True, False, False, True)
        self.ui = Ui_ConnectionWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        # button icons
        self.ui.tableView.setLayoutName('CurrentConnection')  # must be set AFTER model
        self.ui.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # signal slot connections
        self.ui.killClientButton.clicked.connect(self.killClient)
     
    def killClient(self) -> None:
        "Kills selected client PID"
        if not self.view:
            return
        cir = self.view.selectionModel().currentIndex().row()
        pid = self.model.index(cir, 0).data() # pid on column 0
        if pid is None:
            QMessageBox.warning(self,
                                _tr('MessageDialog', 'Warning'),
                                _tr('Connection', "You must select a connection record first"),
                                QMessageBox.StandardButton.NoButton)
            return
        if pid == session['session_id']:
            QMessageBox.warning(self,
                                _tr('MessageDialog', 'Warning'),
                                _tr('Connection', "Cant't kill current connection"),
                                QMessageBox.StandardButton.NoButton)
            return
        msg = _tr('Connection', "Are you sure you want to kill PID")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}: {pid} ?",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            with gui_exception_context(self, _tr('Connection', "Kill client")):
                kill_client(pid)

    def export(self) -> None:
        "Export current connections list to file"
        self.ui.tableView.exportView()


class ConnectionHistoryForm(FormViewManager):
    "Connections History form"

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = ConnectionHistoryModel()
        self.setModel(model)
        self.tabName = title
        self.helpLink = None
        self.reloadConfirmation = False
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, True, True, True, True, True,
                                True, False, False, True)
        self.ui = Ui_ConnectionHistoryWidget()
        self.ui.setupUi(self)
        self.setView(self.ui.tableView)  # required for formviewmanager
        self.ui.tableView.setModel(model)
        self.ui.tableView.setLayoutName("ConnectionsHistory")
        # set read only view
        self.ui.tableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # automatic setting initial value
        days = pa_setting('clear_connection_history')
        if days is None:
            self.ui.checkBoxAutomaticDeletion.setChecked(False)
        else:
            self.ui.checkBoxAutomaticDeletion.setChecked(True)
            self.ui.spinBoxDays.setEnabled(True)
            self.ui.spinBoxDays.setValue(int(days))
        # button icons
        self.ui.pushButtonDeleteOlder.setIcon(currentIcon['record_delete'])
        self.ui.pushButtonDeleteAll.setIcon(currentIcon['record_delete'])
        self.ui.pushButtonDeleteSetting.setIcon(currentIcon['setting_update'])
        # delete buttons signal - slot
        self.ui.pushButtonDeleteOlder.clicked.connect(self.deleteOlder)
        self.ui.pushButtonDeleteAll.clicked.connect(self.deleteAll)
        self.ui.pushButtonDeleteSetting.clicked.connect(self.deleteSetting)
        #self.updateList()

    def deleteOlder(self) -> None:
        "Delete records of log history table"
        days, ok = QInputDialog.getInt(self,
                                        _tr('Connection', 'Delete older records'),
                                        _tr('Connection', 'Number of days for deletion'),
                                        180,
                                        0,
                                        2147483647,
                                        1)
        if not ok:
            return
        with gui_exception_context(self, _tr('Connection', 'Delete older records')):
            delete_connection_history(days)
            self.reload()
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'information'),
                                    _tr('Connection', 'Older records deletion completed'))

    def deleteAll(self) -> None:
        "Delete records of log history table"
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('Connection', "Are you sure you want to delete ALL records ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        with gui_exception_context(self, _tr('Connection', 'Delete all records')):
            delete_connection_history(0)
            self.reload()
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'information'),
                                    _tr('Connection', 'Log records deletion completed'))

    def deleteSetting(self) -> None:
        "Set automatic deletion settings for connection history"
        days = self.ui.spinBoxDays.value()
        if not self.ui.checkBoxAutomaticDeletion.isChecked():
            days = None
        with gui_exception_context(self, _tr('Connection', 'Set automatic deletion settings')):
            pa_setting_set('clear_connection_history', days)
            self.reload()
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Connection', 'Configuration updated'))

    def export(self) -> None:
        "Export connections history list to file"
        self.ui.tableView.exportView()
