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

Management of company: creation, deletion, modification and
user access to each company

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QBuffer
from PySide6.QtCore import QIODevice
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QAction
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentIcon
from App.Database.Company import max_company_code
from App.Database.Company import create_company
from App.Database.Company import drop_company
from App.Database.Company import set_company_access
from App.Database.Company import company_is_in_use
from App.Database.Lookup import user_lookup
from App.Database.Lookup import profile_lookup
from App.Database.Lookup import menu_lookup
from App.Database.Lookup import toolbar_lookup
from App.Database.Models import CompanyIndexModel
from App.Database.Models import CompanyModel
from App.Database.Models import UserCompanyModelReferenceCompany
from App.Widget.Form import FormIndexManager
from App.Widget.Delegate import ImageDelegate
from App.Widget.Delegate import GenericDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Dialog import PrintDialog
from App.Ui.CompanyWidget import Ui_CompanyWidget
from App.Ui.NewCompanyDialog import Ui_NewCompanyDialog
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context


# logger
logger = logging.getLogger(__name__)

class cmp(IntEnum):
    COMP_ID     = 0
    COMP_DESC   = 1
    COMP_SYSTEM = 2
    COMP_IMAGE  = 3
    
class uc(IntEnum):
    COMPANY  = 0
    USER     = 1 
    PROFILE  = 2
    MENU     = 3
    TOOLBAR  = 4
    USER_INS = 5
    DATE_INS = 6
    USER_UPD = 7
    DATE_UPD = 8


def company(action: QAction, checked: bool = False) -> None:
    "Show/Edit company table"
    logger.info('Starting company management Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('CashDesk', 'No access right to this archive'))
        return
    cf = CompanyForm(mw, title, auth)
    cf.applySortFilter()
    mw.addTab(title, cf)
    logger.info('Company management Form added to main window')
    

class CompanyForm(FormIndexManager):
    """Form for management of companies: creation, deletion, modification
     and user access to each company"""

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
        # table view
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('CompanyIndex')  # after setting model
        self.ui.tableView.setItemDelegate(GenericDelegate(self))
        self.ui.tableView.setItemDelegateForColumn(cmp.COMP_IMAGE, ImageDelegate(self))
        # mapper mappings
        self.mapper.addMapping(self.ui.spinBoxId, cmp.COMP_ID)
        self.mapper.addMapping(self.ui.lineEditDescription, cmp.COMP_DESC)
        self.mapper.addMapping(self.ui.labelCompanyImage, cmp.COMP_IMAGE)
        self.mapper.addMapping(self.ui.checkBoxSystem, cmp.COMP_SYSTEM)
        # make system checkbox not user editable
        self.ui.checkBoxSystem.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ui.checkBoxSystem.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        # user company
        self.ui.userTableView.setModel(model2)
        self.ui.userTableView.setLayoutName('CompanyUser')
        self.ui.userTableView.setItemDelegateForColumn(uc.USER, RelationDelegate(self, user_lookup))
        self.ui.userTableView.setItemDelegateForColumn(uc.PROFILE, RelationDelegate(self, profile_lookup))
        self.ui.userTableView.setItemDelegateForColumn(uc.MENU, RelationDelegate(self, menu_lookup))
        self.ui.userTableView.setItemDelegateForColumn(uc.TOOLBAR, RelationDelegate(self, toolbar_lookup))
        # signal slot connections
        self.ui.pushButtonAdd.clicked.connect(self.add)
        self.ui.pushButtonRemove.clicked.connect(self.remove)
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonDelete.clicked.connect(self.removeImage)

    def add(self) -> None:
        "Add a new user company relation"
        self.ui.userTableView.add()

    def remove(self) -> None:
        "Remove the selected user company relation"
        self.ui.userTableView.remove()

    def upload(self, checked: bool) -> None:
        "Upload company image file"
        st = QSettings()
        path = st.value("PathImagesCompanies", QDir.current().path())
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr('Company', "Select the image to upload"),
                                           str(path),
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
        if hasattr(self.model, 'isDirty'):
            self.model.isDirty = True
        if hasattr(self.model, 'userDataChanged'):
            self.model.userDataChanged.emit()

    def download(self, checked: bool) -> None:
        "Download company image to file"
        if not self.ui.labelCompanyImage.pixmap():
            return
        st = QSettings()
        path = st.value("PathImagesCompanies", QDir.current().path())
        f, t = QFileDialog.getSaveFileName(self,
                                           _tr('Company', "Select the destination file name"),
                                           str(path),
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
        if hasattr(self.model, 'isDirty'):
            self.model.isDirty = True
        if hasattr(self.model, 'userDataChanged'):
            self.model.userDataChanged.emit()

    def new(self) -> None:
        "Create a new company"
        dlg = NewCompanyDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.reload()

    def delete(self) -> None:
        "Delete the current selected company"
        companyId = self.ui.spinBoxId.value()
        companyDescription = self.ui.lineEditDescription.text()
        if self.ui.checkBoxSystem.isChecked():
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Is not possible to delete a system company"))
            return
        if company_is_in_use(companyId):
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Is not possible to delete this company because it is currently in use"))
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
        with gui_exception_context(self, _tr('Company', "Deleting company")):
            drop_company(companyId)
            
            logger.info('Company %s/%s deleted', companyId, companyDescription)
            
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
    """Dialog for creation of a new company with the specified data and image"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_NewCompanyDialog()
        self.ui.setupUi(self)
        self.ui.spinBoxCode.setValue(max_company_code() + 10)
        self.ui.comboBoxProfile.setFunction(profile_lookup)
        self.ui.comboBoxMenu.setFunction(menu_lookup)
        self.ui.comboBoxToolbar.setFunction(toolbar_lookup)
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonClear.clicked.connect(self.removeImage)

    def upload(self) -> None:
        "Upload company image file"
        st = QSettings()
        path = st.value("PathImages", QDir.current().path())
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr('Company', "Select the image file to upload"),
                                           str(path),
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
        "Remove company image file"
        self.ui.labelImage.clear()
        self.ui.labelImage.setText(_tr('Company', "NO IMAGE"))

    def accept(self) -> None:
        "Create the new company with the specified data"
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
            image = companyImage.data()
        else:
            image = None
        userProfile = self.ui.comboBoxProfile.currentData()
        userMenu = self.ui.comboBoxMenu.currentData()
        userToolbar = self.ui.comboBoxToolbar.currentData()
        # create a new company
        with gui_exception_context(self, _tr('Company', "Creating new company")):
            create_company(companyCode,
                           companyDescription,
                           image)
            set_company_access(companyCode,
                               session['app_user_code'],
                               userProfile,
                               userMenu,
                               userToolbar)
        
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Company', "Company created succesfully"))
            logger.info('New company %s/%s created', companyCode, companyDescription)
            super().accept()
