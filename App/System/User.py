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

"""User

This module manages application users and user access rights to each company


"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QFileInfo
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App import currentIcon
from App.Database.AbstractModels.TableModel import TableModel
from App.Database.Exceptions import PyAppDBError
from App.Database.User import change_password
from App.Database.Lookup import company_lookup
from App.Database.Lookup import profile_lookup
from App.Database.Lookup import menu_lookup
from App.Database.Lookup import toolbar_lookup
from App.Database.Models import UserModel
from App.Database.Models import UserIndexModel
from App.Database.Models import UserCompanyModelReferenceUser
from App.Database.User import encrypt_password
from App.Widget.Dialog import PrintDialog
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import ImageDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import GenericDelegate
from App.Ui.UserWidget import Ui_UserWidget
from App.Ui.ChangePasswordDialog import Ui_ChangePasswordDialog
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Core.L10n import langCountry
from App.Core.L10n import langCountryFlags


# logger
logger = logging.getLogger(__name__)


class uin(IntEnum):
    CODE         = 0
    DESCRIPTION  = 1
    IMAGE        = 2
    SYSTEM       = 3 
    IS_ADMIN     = 4
    CE_VIEWS     = 5
    CE_SORTFIL   = 6
    CE_REPORTS   = 7
    L10N         = 8
    LAST_LOGIN   = 9
    LAST_COMPANY = 10
    USER_INS     = 11
    DATE_INS     = 12
    USER_UPD     = 13
    DATE_UPD     = 14
    
class usr(IntEnum):
    CODE         = 0
    DESCRIPTION  = 1
    IMAGE        = 2
    PASSWORD     = 3
    PWD_DATE     = 4
    CHANGE_PWD   = 5
    SYSTEM       = 6
    IS_ADMIN     = 7
    CE_VIEWS     = 8
    CE_SORTFIL   = 9
    CE_REPORTS   = 10
    L10N         = 11
    LAST_COMPANY = 12
    LAST_LOGIN   = 13
    USER_INS     = 14
    DATE_INS     = 15
    USER_UPD     = 16
    DATE_UPD     = 17
    
class uc(IntEnum):
    COMPANY      = 0
    USER         = 1
    PROFILE      = 2 
    MENU         = 3
    TOOLBAR      = 4
    USER_INS     = 5
    DATE_INS     = 6
    USER_UPD     = 7
    DATE_UPD     = 8


def user(action: QAction, checked: bool = False) -> None:
    "Users management"
    logging.info('Starting users Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(
            mw,
            _tr('MessageDialog', "Warning"),
            _tr('CashDesk', 'No access right to this archive')
        )
        return
    uf = UsersForm(mw, title, auth)
    uf.applySortFilter()
    mw.addTab(title, uf)
    logging.info('Users Form added to main window')


def changePassword(action: QAction, checked: bool = False) -> None:
    "Change password dialog"
    # this dialog is used in users form too and is not called by an action
    # so can't use action properties
    logging.info('Starting change password dialog')
    mw = session['mainwin']
    pd = ChangePasswordDialog(mw, session['app_user_code'], action.icon())
    pd.exec()
    logging.info('Change password dialog shown')


class UsersForm(FormIndexManager[Ui_UserWidget]):
    "User form management"

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
        super().__init__(parent, auth)
        model = UserModel(self)
        idxModel = UserIndexModel(self)
        ucModel = UserCompanyModelReferenceUser(self)
        self.setModel(model, idxModel)
        self.addDetailRelation(ucModel, 0, 1)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, True)
        self.ui: Ui_UserWidget = Ui_UserWidget()
        self.ui.setupUi(self)
        # icons for add/remove buttons
        self.ui.pushButtonAdd.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemove.setIcon(currentIcon['edit_remove'])
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # widget settings
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('UserIndex')
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(uin.L10N, RelationDelegate(self, langCountry))
        self.ui.tableView.setItemDelegateForColumn(uin.IMAGE, ImageDelegate(self))
        # set password/password change
        self.ui.pushButtonSetTemporaryPassword.clicked.connect(self.setTemporaryPassword)
        # signal/slot mappings
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonDelete.clicked.connect(self.removeImage)
        # other widgets
        self.mapper.addMapping(self.ui.lineEditUser, usr.CODE)
        self.mapper.addMapping(self.ui.lineEditUserDescription, usr.DESCRIPTION)
        self.mapper.addMapping(self.ui.labelImage, usr.IMAGE)
        self.mapper.addMapping(self.ui.lineEditLastCompany, usr.LAST_COMPANY)
        self.mapper.addMapping(self.ui.dateTimeEditLastLogin, usr.LAST_LOGIN)
        self.ui.comboBoxL10n.setItemList(langCountryFlags())
        self.mapper.addMapping(self.ui.comboBoxL10n, usr.L10N)
        self.mapper.addMapping(self.ui.dateTimeEditPasswordDate, usr.PWD_DATE)
        self.mapper.addMapping(self.ui.checkBoxForcePasswordChange, usr.CHANGE_PWD)
        self.mapper.addMapping(self.ui.checkBoxSystem, usr.SYSTEM)
        self.mapper.addMapping(self.ui.checkBoxIsAdmin, usr.IS_ADMIN)
        self.mapper.addMapping(self.ui.checkBoxCanEditViews, usr.CE_VIEWS)
        self.mapper.addMapping(self.ui.checkBoxCanEditSortFilters, usr.CE_SORTFIL)
        self.mapper.addMapping(self.ui.checkBoxCanEditReports, usr.CE_REPORTS)
        # user/company
        self.ui.tableViewUserCompany.setModel(ucModel)
        self.ui.tableViewUserCompany.setLayoutName('UserCompany')
        self.ui.tableViewUserCompany.setItemDelegateForColumn(uc.COMPANY, RelationDelegate(self, company_lookup))
        self.ui.tableViewUserCompany.setItemDelegateForColumn(uc.PROFILE, RelationDelegate(self, profile_lookup))
        self.ui.tableViewUserCompany.setItemDelegateForColumn(uc.MENU, RelationDelegate(self, menu_lookup))
        self.ui.tableViewUserCompany.setItemDelegateForColumn(uc.TOOLBAR, RelationDelegate(self, toolbar_lookup))
        # signal - slot
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)

    def add(self) -> None:
        "Add a record"
        self.ui.tableViewUserCompany.add()

    def remove(self) -> None:
        "Remove current record"
        self.ui.tableViewUserCompany.remove()

    def new(self) -> None:
        "New user"
        super().new()
        self.ui.lineEditUser.setEnabled(True)
        self.ui.lineEditUserDescription.setEnabled(True)
        self.ui.lineEditUser.setFocus()

    def save(self) -> None:
        "Save and ask for password if null (new user)"
        if self.model.data(self.model.index(self.mapper.currentIndex(), usr.PASSWORD)) is None:
            userIndex = self.model.index(self.mapper.currentIndex(), usr.CODE)
            passwordIndex = self.model.index(self.mapper.currentIndex(), usr.PASSWORD)
            dlg = SetPasswordDialog(self, self.model, userIndex, passwordIndex)
            dlg.exec()
        super().save()
        self.ui.lineEditUser.setDisabled(True)

    def reload(self) -> None:
        "Reload data, set widgets to default state"
        super().reload()
        self.ui.lineEditUser.setDisabled(True)

    def delete(self) -> None:
        "Delete current user"
        userId = self.ui.lineEditUser.text()
        userDescription = self.ui.lineEditUserDescription.text()
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(
                self,
                _tr('MessageDialog', "Information"),
                _tr('User', "It is not possible to delete a system user")
            )
            return
        msg = _tr('User', "Are you sure you want to delete this user ?")
        if QMessageBox.question(
            self,
            _tr('MessageDialog', "Question"),
            f"{msg}\n{userId} - {userDescription}",
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
            QMessageBox.StandardButton.No  # default botton
            ) == QMessageBox.StandardButton.No:
            return
        # ok, delete
        super().delete()

    def mapperIndexChanged(self, row: int) -> None:
        "Change sittings on change record"
        super().mapperIndexChanged(row)         
        if self.ui.checkBoxSystem.isChecked():
            self.write_perm = False
            self.ui.lineEditUserDescription.setReadOnly(True)
            self.ui.comboBoxL10n.setDisabled(True)
            self.ui.pushButtonUpload.setDisabled(True)
            self.ui.pushButtonDownload.setDisabled(True)
            self.ui.pushButtonDelete.setDisabled(True)
            self.ui.checkBoxIsAdmin.setDisabled(True)  # setChackable don't work...
        else:
            self.write_perm = True
            self.ui.lineEditUserDescription.setReadOnly(False)
            self.ui.comboBoxL10n.setDisabled(False)
            self.ui.pushButtonUpload.setDisabled(False)
            self.ui.pushButtonDownload.setDisabled(False)
            self.ui.pushButtonDelete.setDisabled(False)
            self.ui.checkBoxIsAdmin.setEnabled(True)

    def setTemporaryPassword(self) -> None:
        "Ask for a temporary password for current user"
        userIndex = self.model.index(self.mapper.currentIndex(), usr.CODE)
        passwordIndex = self.model.index(self.mapper.currentIndex(), usr.PASSWORD)
        dlg = SetPasswordDialog(self, self.model, userIndex, passwordIndex)
        if dlg.exec_() == QDialog.DialogCode.Accepted:
            # if password was modified set for change required
            cprIndex = self.model.index(self.mapper.currentIndex(), usr.CHANGE_PWD)
            self.model.setData(cprIndex, True)

    def upload(self) -> None:
        "Upload user image file"
        st = QSettings()
        path = str(st.value("User/PathImages", QDir.current().path()))
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr('User', "Select the image to upload"),
                                           path,
                                           _tr('User', "Portable Network Graphics (*.png);;All files (*.*)"))

        if f == "":
            return
        pix = QPixmap(f)
        if pix.width() > 640 or pix.height() > 480:
            pix = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.ui.labelImage.setPixmap(pix)
            QMessageBox.warning(
                self,
                _tr('MessageDialog', "Warning"),
                _tr('User', "The selected image is too big, it was"
                    "automaticlly resized to the max allowed size of 640x480 pixels")
            )
        else:
            self.ui.labelImage.setPixmap(pix)
        st.setValue("User/PathImages", QFileInfo(f).path())
        if isinstance(self.model, TableModel):
            self.model.isDirty = True
            self.model.userDataChanged.emit()

    def download(self, checked: bool) -> None:
        "Download user image file"
        if not self.ui.labelImage.pixmap():
            return
        st = QSettings()
        path = str(st.value("User/PathImages", QDir.current().path()))
        f, t = QFileDialog.getSaveFileName(self,
                                           _tr('User', "Select the destination file name"),
                                           path,
                                           _tr('User', "Portable Network Graphics (*.png);;All files (*.*)"))
        if f == "":
            return
        pix = self.ui.labelImage.pixmap()
        if pix.save(f):
            QMessageBox.information(
                self,
                _tr('MessageDialog', "Information"),
                _tr('User', "Image file saved")
            )
        else:
            QMessageBox.critical(
                self,
                _tr('MessageDialog', "Critical"),
                _tr('User', "Error on saving image file")
            )

    def removeImage(self, checked: bool) -> None:
        "Remove company image"
        self.ui.labelImage.clear()
        self.ui.labelImage.setText(_tr('User', "NO IMAGE"))
        if isinstance(self.model, TableModel):
            self.model.isDirty = True
            self.model.userDataChanged.emit()

    def print(self) -> None:
        "Print users"
        dialog = PrintDialog(self, 'USER')
        dialog.show()

    def export(self) -> None:
        "Export current users list to file"
        self.ui.tableView.exportView()


class ChangePasswordDialog(QDialog):
    "Change password dialog"

    def __init__(self, parent: QWidget, user: str, icon: QIcon = QIcon()) -> None:
        super().__init__(parent)
        self.ui = Ui_ChangePasswordDialog()
        self.ui.setupUi(self)
        # this dialog is used in users too, can't use action properties
        # because is not called by an action
        self.setWindowTitle(_tr('User', 'Change password'))
        if icon:
            self.ui.labelIcon.setPixmap(icon.pixmap(100))
        else:
            self.ui.labelIcon.setPixmap(currentIcon['system_password'].pixmap(100))
        self.ui.lineEditUser.setText(user)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setDefault(True)

    def accept(self) -> None:
        "Save new password"
        # check not null and correct password
        if (self.ui.lineEditNewPassword.text() == '' or
            self.ui.lineEditConfirmPassword.text() == ''):
            QMessageBox.critical(
                self,
                _tr('MessageDialog', "Critical"),
                _tr('ChangePassword', "Insert a valid password "
                    "on both the line edit boxes")
            )
            return
        if self.ui.lineEditNewPassword.text() != self.ui.lineEditConfirmPassword.text():
            QMessageBox.critical(
                self,
                _tr('MessageDialog', "Critical"),
                _tr('ChangePassword', "The Inserted password "
                    "in the 'New password' does not match "
                    "that of the 'Confirm password'")
            )
            return
        with gui_exception_context(self, _tr('ChangePassword', 'Change password')):
            change_password(self.ui.lineEditUser.text(),
                            self.ui.lineEditNewPassword.text())
        
            QMessageBox.information(
                self,
                _tr('MessageDialog', "Information"),
                _tr('ChangePassword', "Password changed successfully")
            )
        QDialog.accept(self)


class SetPasswordDialog(ChangePasswordDialog):

    def __init__(self, 
                 parent: QWidget,
                 model: QAbstractItemModel,
                 userIndex: QModelIndex | QPersistentModelIndex,
                 passwordIndex: QModelIndex | QPersistentModelIndex) -> None:
        super().__init__(parent, model.data(userIndex))
        self.model = model
        self.userIndex = userIndex
        self.passwordIndex = passwordIndex
        self.setWindowTitle(_tr('User', 'Set temporary password dialog'))

    def accept(self) -> None:
        # check correct password
        if self.ui.lineEditConfirmPassword.text() == '':
            QMessageBox.critical(
                self,
                _tr('MessageDialog', "Critical"),
                _tr('ChangePassword', "Insert a valid password on both the line edit")
            )
            return
        if self.ui.lineEditNewPassword.text() != self.ui.lineEditConfirmPassword.text():
            QMessageBox.critical(
                self, 
                _tr('MessageDialog', "Critical"),
                _tr('ChangePassword', "New password and confirmed password does not match")
            )
            return
        # return encrypted password to model
        ep = encrypt_password(self.ui.lineEditNewPassword.text())
        self.model.setData(self.passwordIndex, ep)
        QDialog.accept(self)



