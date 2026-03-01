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

"""Company

This module manages company creation/deletion/modification and user access
to each company

"""

# standard library
import logging

# PySide6
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QBuffer
from PySide6.QtCore import QIODevice
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentAction
from App import currentIcon
from App.Database import EDSAE  # Database schema already exists (create company sp)
from App.Database import ECIAE  # Company id already exists (create company sp)
from App.Database import ECIIU  # Company is in use (drop company sp)
from App.Database.Exceptions import PyAppDBError
from App.Database.Company import max_company_code
from App.Database.Company import create_company
from App.Database.Company import drop_company
from App.Database.Company import set_company_access
from App.Database.CodeDescriptionList import user_cdl
from App.Database.CodeDescriptionList import profile_cdl
from App.Database.CodeDescriptionList import menu_cdl
from App.Database.CodeDescriptionList import toolbar_cdl
from App.Database.Models import CompanyIndexModel
from App.Database.Models import CompanyModel
from App.Database.Models import UserCompanyModelReferenceCompany
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import ImageDelegate
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Dialog import PrintDialog
from App.Ui.CompanyWidget import Ui_CompanyWidget
from App.Ui.NewCompanyDialog import Ui_NewCompanyDialog
from App.Core.L10n import _tr

# logger
logger = logging.getLogger(__name__)


COMP_ID, COMP_DESC, COMP_SYSTEM, COMP_IMAGE = range(4)

(UC_COMPANY, UC_USER, UC_PROFILE, UC_MENU, UC_TOOLBAR, UC_USER_INS,
 UC_DATE_INS, UC_USER_UPD, UC_DATE_UPD) = range(9)


def company() -> None:
    "Show/Edit company table"
    logger.info('Starting company management Form')
    mw = session['mainwin']
    title = currentAction['sys_company'].text()
    auth = currentAction['sys_company'].data()
    cf = CompanyForm(mw, title, auth)
    cf.reload()
    mw.addTab(title, cf)
    logger.info('Company management Form added to main window')
    

class CompanyForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = CompanyModel()
        idxModel = CompanyIndexModel()
        model2 = UserCompanyModelReferenceCompany()
        self.setModel(model, idxModel)
        self.addDetailRelation(model2, 0, 0)
        self.tabName = title
        self.helpLink = "help/main.html#gui"
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, False)
        self.ui = Ui_CompanyWidget()
        self.ui.setupUi(self)
        # icons for add/remove buttons
        self.ui.pushButtonAdd.setIcon(currentIcon['edit_add'])
        self.ui.pushButtonRemove.setIcon(currentIcon['edit_remove'])
        # signal slot connections
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonDelete.clicked.connect(self.removeImage)
        # table view
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('company')  # after setting model
        self.ui.tableView.setItemDelegateForColumn(COMP_IMAGE, ImageDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(COMP_SYSTEM, BooleanDelegate(self))
        # mapper mappings
        self.mapper.addMapping(self.ui.spinBoxId, COMP_ID)
        self.mapper.addMapping(self.ui.lineEditDescription, COMP_DESC)
        self.mapper.addMapping(self.ui.labelCompanyImage, COMP_IMAGE) #, b"imageBytearray")
        self.mapper.addMapping(self.ui.checkBoxSystem, COMP_SYSTEM)
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # user company
        self.ui.userTableView.setModel(model2)
        self.ui.userTableView.setLayoutName('userCompany')
        self.ui.userTableView.setItemDelegateForColumn(UC_USER, RelationDelegate(self, user_cdl))
        self.ui.userTableView.setItemDelegateForColumn(UC_PROFILE, RelationDelegate(self, profile_cdl))
        self.ui.userTableView.setItemDelegateForColumn(UC_MENU, RelationDelegate(self, menu_cdl))
        self.ui.userTableView.setItemDelegateForColumn(UC_TOOLBAR, RelationDelegate(self, toolbar_cdl))
        # self.toFirst() not here because we need to set models first
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)

    def add(self) -> None:
        self.ui.userTableView.add()

    def remove(self) -> None:
        self.ui.userTableView.remove()

    def upload(self, checked: bool) -> None:
        "Upload company image file"
        st = QSettings()
        path = st.value("PathImagesCompanies", QDir.current().path())
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr('Company', "Select the image to upload"),
                                           path,
                                           _tr('Company', "Portable Network Graphics (*.png);;All files (*.*)"))

        if f == "":
            return
        pix = QPixmap(f)
        if pix.width() > 640 or pix.height() > 480:
            pix = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.ui.labelCompanyImage.setPixmap(pix)
            QMessageBox.warning(self,
                                _tr('MessageDialog', "Warning"),
                                _tr('Company', "The selected image is too big, it was"
                                    "automatically resized to the max allowed size of 640x480 pixels"))
        else:
            self.ui.labelCompanyImage.setPixmap(pix)
        st.setValue("PathImagesCompanies", QFileInfo(f).path())
        self.model.isDirty = True
        self.model.userDataChanged.emit()
        
    def download(self, checked: bool) -> None:
        "Download company image to file"
        if not self.ui.labelCompanyImage.pixmap():
            return
        st = QSettings()
        path = st.value("PathImagesCompanies", QDir.current().path())
        f, t = QFileDialog.getSaveFileName(self,
                                           _tr('Company', "Select the destination file name"),
                                           path,
                                           _tr('Company', "Portable Network Graphics (*.png);;All files (*.*)"))
        if f == "":
            return
        pix = self.ui.labelCompanyImage.pixmap()
        if pix.save(f):
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Image file saved"))
        else:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', "Critical"),
                                 _tr('Company', "Error on saving image file"))

    def removeImage(self, checked: bool) -> None:
        "Remove company image"
        self.ui.labelCompanyImage.clear()
        self.ui.labelCompanyImage.setText(_tr('Company', "NO IMAGE"))
        self.model.isDirty = True
        self.model.userDataChanged.emit()

    def new(self) -> None:
        dlg = NewCompanyDialog(self)
        if dlg.exec_() == QDialog.DialogCode.Accepted:
            self.reload()

    def delete(self) -> None:
        companyId = self.ui.spinBoxId.value()
        companyDescription = self.ui.lineEditDescription.text()
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Is not possible to delete a system company"))
            return
        msg = _tr('Company', "Delete this company ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{companyId} {companyDescription}",
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('Company', "It is possible to restore the "
                                    "company only if you have a valid copy of "
                                    "the database\nProceed anyway ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        try:
            drop_company(companyId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', "Critical"),
                                 f"Database error: {er.code}\n{er.message}")
            logger.error('Database error on drop company: %s', er.message)
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Company deleted"))
        self.reload()
        self.toFirst()

    def print(self) -> None:
        "Print company list"
        dialog = PrintDialog(self, 'COMPANY', session['l10n'])
        dialog.show()


class NewCompanyDialog(QDialog):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_NewCompanyDialog()
        self.ui.setupUi(self)
        self.ui.spinBoxCode.setValue(max_company_code() + 10)
        self.ui.comboBoxProfile.setFunction(profile_cdl)
        self.ui.comboBoxMenu.setFunction(menu_cdl)
        self.ui.comboBoxToolbar.setFunction(toolbar_cdl)
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonClear.clicked.connect(self.removeImage)

    def upload(self) -> None:
        st = QSettings()
        path = st.value("PathImages", QDir.current().path())
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr('Company', "Select the image file to upload"),
                                           path,
                                           _tr('Company', "Portable Network "
                                               "Graphics (*.png);;All files (*.*)"))
        if f == "":
            return
        pix = QPixmap(f)
        if pix.width() > 640 or pix.height() > 480:
            pix = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.ui.labelImage.setPixmap(pix)
            QMessageBox.warning(self,
                                _tr('MessageDialog', "Warning"),
                                _tr('Company', "The selected image is too big, "
                                    "it was automaticlly resized to the max "
                                    "allowed size of 640x480 pixels"))
        else:
            self.ui.labelImage.setPixmap(pix)
        st.setValue("PathImages", QFileInfo(f).path())

    def removeImage(self) -> None:
        self.ui.labelImage.clear()
        self.ui.labelImage.setText(_tr('Company', "NO IMAGE"))

    def accept(self) -> None:
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('Company', "Create the new company ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        companyCode = self.ui.spinBoxCode.value()
        companyDescription = self.ui.lineEditDescription.text()
        pixmap = self.ui.labelImage.pixmap()
        if pixmap:
            companyImage = QByteArray()
            buffer = QBuffer(companyImage)
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            pixmap.save(buffer, "PNG")
        else:
            companyImage = None
        userProfile = self.ui.comboBoxProfile.currentData()
        userMenu = self.ui.comboBoxMenu.currentData()
        userToolbar = self.ui.comboBoxToolbar.currentData()
        # create a new company from template
        try:
            create_company(companyCode,
                           companyDescription,
                           companyImage)
            set_company_access(companyCode,
                               session['app_user_code'],
                               userProfile,
                               userMenu,
                               userToolbar)
        except PyAppDBError as er:
            if er.code == EDSAE:
                msg = _tr("Company", "Database schema already exists. "
                                 "Try to set a different name for the new "
                                 "database schema")
            elif er.code == ECIAE:
                msg = _tr("Company", "Company ID already exists. "
                                 "Try to set a different company ID for the new "
                                 "company")
            else:
                msg = f"Error: {er.code}\n{er.message}"
            mbox = QMessageBox(self)
            mbox.setIcon(QMessageBox.Icon.Critical)
            mbox.setWindowTitle(_tr("MessageDialog", "Critical"))
            mbox.setText(msg)
            mbox.setDetailedText(er.message)
            mbox.exec_()
            logger.error('Database error on create new company: %s', er.message)
            logger.error('Error code: %s', er.code)
            logger.error('Error message: %s', er.message)
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Company created succesfully"))
            logger.info('New company %s/%s created', companyCode, companyDescription)
            super().accept()
