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

"""Profile

Management of user profiles

"""

# standard library
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QButtonGroup

# application modules
from App import session
from App import currentAction
from App import currentIcon
from App.Core.L10n import _tr
from App.Database.Exceptions import PyAppDBError
from App.Database.Profile import duplicate_profile
from App.Database.Models import ProfileIndexModel
from App.Database.Models import ProfileModel
from App.Database.Models import ProfileActionModel
from App.System.Action import actionDefinition
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import ActionDelegate
from App.Widget.Form import FormIndexManager
from App.Widget.Dialog import PrintDialog
from App.Ui.ProfileWidget import Ui_ProfileWidget
from App.Ui.DuplicateDialog import Ui_DuplicateDialog


# logger
logger = logging.getLogger(__name__)


CODE, DESCRIPTION, SYSTEM = range(3)

PROFILE, ACTION, AUTHORIZATION = range(3)


def authorizations() -> tuple[tuple[str, str], ...]:
    return (('R', _tr('Profile', 'Read')),
            ('W', _tr('Profile', 'Write')),
            ('X', _tr('Profile', 'Execute')))


def profile(action: QAction, checked: bool = False) -> None:
    "Show/Edit profiles"
    logger.info('Starting profiles Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    pw = ProfileForm(mw, title, auth)
    pw.applySortFilter()
    mw.addTab(title, pw)
    logger.info('Profiles Form added to main window')


class DuplicateProfileDialog(QDialog):
    "Dialog box for duplicate the current selected profile"
    
    def __init__(self, parent: QWidget, profile: str) -> None:  # no parent for tabwidget widget pages
        super().__init__(parent)
        self.ui = Ui_DuplicateDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(_tr('Profile', 'Duplicate profile'))
        self._fromProfile = profile

    def accept(self) -> None:
        "Duplicate profile"
        try:
            duplicate_profile(self._fromProfile,
                              self.ui.lineEditCode.text(),
                              self.ui.lineEditDescription.text())
        except PyAppDBError as er:
            logger.error("On duplicate profile: database error: %s %s", er.code, er.message)
            QMessageBox.critical(self,
                                 _tr('MessageDialog', "Critical"),
                                 f"{er.code} - {er.message}")
        else:
            logger.info("On duplicate profile: operation completed successfully")
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Profile', "Profile duplicated"))
        super().accept()


class ProfileForm(FormIndexManager):
    "Profile form management"
    
    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = ProfileModel(self)
        idxModel = ProfileIndexModel(self)
        paModel = ProfileActionModel(self)
        self.setModel(model, idxModel)
        self.addDetailRelation(paModel, 0, 0)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, False)
        self.ui = Ui_ProfileWidget()
        self.ui.setupUi(self)
        # icons for add/remove buttons
        self.ui.pushButtonAdd.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemove.setIcon(currentIcon['edit_remove'])
        # widget settings
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('profile')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.mapper.addMapping(self.ui.lineEditCode, CODE)
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        self.mapper.addMapping(self.ui.checkBoxSystem, SYSTEM)
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # detail tableview
        self.ui.tableViewActions.setModel(paModel)
        self.ui.tableViewActions.setLayoutName('profileAction')
        #self.ui.tableViewActions.setLayout()
        self.ui.tableViewActions.setItemDelegateForColumn(ACTION, ActionDelegate(self))
        self.ui.tableViewActions.setItemDelegateForColumn(AUTHORIZATION, RelationDelegate(self, authorizations))
        # authorization button group
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.ui.pushButtonRead)
        self.buttonGroup.addButton(self.ui.pushButtonWrite)
        self.buttonGroup.addButton(self.ui.pushButtonExecute)
        self.buttonGroup.buttonClicked.connect(self.authorizationButtonClicked)
        # signal/slot
        self.ui.pushButtonFillActions.clicked.connect(self.fillActions)
        self.ui.pushButtonDuplicate.clicked.connect(self.duplicate)
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)

    def fillActions(self) -> None:
        "Fill actions table view with all actions not already in"
        model = self.ui.tableViewActions.model()
        current = {model.data(model.index(i, ACTION)) for i in range(model.rowCount())}
        actions = {i for i in actionDefinition}
        difference = actions - current
        for i in difference:
            model.insertRow(model.rowCount())
            modelRow = model.rowCount() - 1
            model.setData(model.createIndex(modelRow, ACTION), i)
            model.setData(model.createIndex(modelRow, AUTHORIZATION), 'X')

    def authorizationButtonClicked(self, button: QPushButton) -> None:
        "Set all action to read/write/execute"
        if button == self.ui.pushButtonRead:
            auth = 'R'
        elif button == self.ui.pushButtonWrite:
            auth = 'W'
        else:
            auth = 'X'
        model = self.ui.tableViewActions.model()
        for row in range(model.rowCount()):
            model.setData(model.createIndex(row, AUTHORIZATION), auth)

    def delete(self) -> None:
        "Delete current profile"
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Profile', "Is not possible to delete a system profile"))
            return
        profile = self.ui.lineEditCode.text()
        description = self.ui.lineEditDescription.text()
        msg = _tr('Profile', "Are you sure you want to delete this profile ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{profile} - {description}",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()

    def new(self) -> None:
        "Inser a new profile"
        super().new()
        self.ui.lineEditCode.setEnabled(True)
        self.ui.lineEditCode.setFocus()

    def save(self) -> None:
        "Save data, set widgets to default state"
        self.ui.lineEditCode.setDisabled(True)
        super().save()

    def reload(self) -> None:
        "Reload data, set widgets to default state"
        self.ui.lineEditCode.setDisabled(True)
        super().reload()

    def add(self) -> None:
        "Add a row to detail view"
        # only on non system profile
        if not self.ui.checkBoxSystem.isChecked():
            self.ui.tableViewActions.add()

    def remove(self) -> None:
        "Remove current row from detail view"
        # only on non system profile
        if not self.ui.checkBoxSystem.isChecked():
            self.ui.tableViewActions.remove()

    def print(self) -> None:
        "Print profiles list"
        dialog = PrintDialog(self, 'PROFILE', session['l10n'])
        dialog.show()

    def duplicate(self) -> None:
        "Duplicate the current profile"
        # get the current price list id
        currentProfile = self.model.index(self.mapper.currentIndex(), CODE).data()
        dlg = DuplicateProfileDialog(self, currentProfile)
        dlg.exec()
        self.reload()
