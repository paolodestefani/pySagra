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

"""Login

This module provide a login dialog that ask for connection parameters and start
up the database connection. Also a change company dialog let the user choose
the working company

"""

# standard library
import sys
import logging
from cryptography.fernet import InvalidToken

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QLocale
from PySide6.QtCore import QTranslator
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QMovie
from PySide6.QtGui import QCursor
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QMessageBox
from PySide6.QtNetwork import QHostInfo

# application definitions
from App import APPNAME
from App import APPVERSIONMAJOR
from App import APPVERSIONMINOR
from App import APPVERSIONPATCH
from App import APPVERSIONTAG
from App import session
from App import currentIcon
from App.Database import EWDBS # wrong database server version
from App.Database import EWADB # wrong application database
from App.Database import EWAPV # wrong application version
from App.Database import EUKNU  # unknown user id
from App.Database import EPWDR # a password is required
from App.Database import EWPWD # password authentication failed
from App.Database import EUKNC # Unknown company
from App.Database import ENACR # No access rights to required company

# application modules
from App.Core.Cryptography import string_encode
from App.Core.Cryptography import string_decode
from App.Core.L10n import _tr
from App.Core.gui import setTheme
from App.Core.gui import setColorScheme
from App.Core.gui import setFont
from App.Core.gui import setIconTheme
from App.Database.Connect import appconn
from App.Database.Exceptions import PyAppDBError
from App.Database.Exceptions import PyAppDBConnectionError
from App.Database.Connect import has_companies_available
from App.Database.Connect import get_companies_list
from App.Database.Connect import get_company_desc
from App.Database.Connect import get_current_event
from App.Database.Connect import can_use_company
from App.Database.Connect import get_current_event
from App.Widget.Dialog import MessageBoxCritical
from App.System.User import ChangePasswordDialog
from App.Ui.LoginDialog import Ui_LoginDialog
from App.Ui.ChangeCompanyDialog import Ui_ChangeCompanyDialog


# logger
logger = logging.getLogger(__name__)


class LoginDialog(QDialog):
    "Login dialog, ask for parameters and launch th connection to server"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(_tr("Login", f"{APPNAME} - Login"))
        # hide connection details
        self.ui.frameMore.hide()
        # restore settings
        st = QSettings()
        if not st.value("LogInDatabase"): # first time usage
            self.ui.checkBoxMore.setChecked(True)
            self.ui.frameMore.show()
        #if st.value("LogIn_Animation", False) is True: # on demand animated gif
        self.logo = QMovie(":/login_gif")
        if self.logo.isValid():
            self.ui.labelMain.setMovie(self.logo)
            self.logo.start()
        self.ui.lineEditServer.setText(st.value("LogInServer", ""))
        self.ui.spinBoxPort.setValue(st.value("LogInPort", 5432, type=int))
        self.ui.lineEditDatabase.setText(st.value("LogInDatabase", ""))
        try:
            self.ui.lineEditDBUser.setText(string_decode(st.value("LogInDbUser", "")))
        except InvalidToken:
            self.ui.lineEditDBUser.setText("")
        try:
            self.ui.lineEditDBPassword.setText(string_decode(st.value("LogInDbPassword", "")))
        except InvalidToken:
            self.ui.lineEditDBPassword.setText("")
        self.ui.lineEditUser.setFocus()
        self.ui.checkBoxMore.clicked.connect(self.expand) # error if i set this in QtDesigner
        self.ui.labelVersion.setText(f"Application Version: {APPVERSIONMAJOR}.{APPVERSIONMINOR}.{APPVERSIONPATCH} {APPVERSIONTAG}")
        
    def expand(self, state: bool) -> None:
        self.ui.frameMore.setVisible(state)

    def accept(self) -> None:
        "Connect to database/application"
        # create a parameters dictionary
        par = dict()
        par['user'] = self.ui.lineEditUser.text()
        par['password'] = self.ui.lineEditPassword.text() or None
        par['server'] = self.ui.lineEditServer.text()
        par['port'] = self.ui.spinBoxPort.value()
        par['database'] = self.ui.lineEditDatabase.text()
        par['db_user'] = self.ui.lineEditDBUser.text()
        par['db_password'] = self.ui.lineEditDBPassword.text()
        par['hostname'] = QHostInfo.localHostName()
        # connect
        try:
            # on network error is better to have a wait cursor
            QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
            appconn.connect(par)
        except PyAppDBConnectionError as er:
            # for normal cursor on error message box
            QGuiApplication.restoreOverrideCursor()
            msg = _tr("Login", "Error on connecting to database server")
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Database connection"),
                               msg,
                               str(er))
            self.ui.lineEditPassword.clear()
            logger.error("Database connection error %s", er)
            return
        except PyAppDBError as er:
            # for normal cursor on error message box
            QGuiApplication.restoreOverrideCursor()
            if er.code == EWDBS: # wrong database server version
                msg = _tr("Login", "Wrong database server version")
            elif er.code == EWADB: # wrong application database
                msg = _tr("Login", "Wrong application database")
            elif er.code == EWAPV: # wrong application version
                msg = _tr("Login", "Wrong application version")
            elif er.code == EPWDR: # a password is required
                msg = _tr("Login", "A password is required")
            elif er.code in (EUKNU, EWPWD): # authentication failed (wrong user or password)
                msg = _tr("Login", "Authentication failed (wrong user or password)")
            else:
                msg = f"Error:{er.code or 'undefined'}"

            MessageBoxCritical(self,
                               _tr('MessageDialog', 'Critical'),
                               msg,
                               str(er.message))
            self.ui.lineEditPassword.clear()
            logger.critical("Connection error %s\n%s", er.code, er.message)
            
            return
        finally:
            QGuiApplication.restoreOverrideCursor()
        logger.info("Database connection established")

        # store login settinggs
        st = QSettings()
        st.setValue("LogInServer", par['server'])
        st.setValue("LogInPort", par['port'])
        st.setValue("LogInDatabase", par['database'])
        st.setValue("LogInDbUser", string_encode(par['db_user']))
        st.setValue("LogInDbPassword", string_encode(par['db_password']))

        # user style theme
        logger.info("Setting user style to %s", session['style_theme'])
        setTheme(session['style_theme'])
        # user style colore scheme
        logger.info("Setting user color palette to %s", session['color_scheme'] or "Unknown")
        setColorScheme(session['color_scheme'])
        # user icon theme
        logger.info("Setting user icon theme to %s", session['icon_theme'])
        setIconTheme(session['icon_theme'])
        # set default font and font size
        logger.info("Setting user font to %s size %s", session['font_family'], session['font_size'])
        setFont(session['font_family'], session['font_size'])
        # user l10n
        # set locale
        if session['l10n']:
            logger.info("Setting user l10n to %s", session['l10n'])
            session['qlocale'] = QLocale(session['l10n'])
            #print(session['qlocale'])    
            QLocale.setDefault(session['qlocale'])
        else:
            logger.info("Localization set to system default %s", QLocale.system().name())
        # remove login translator if any
        logger.info("Removing login translations")
        for i in ('qt', APPNAME):
            QCoreApplication.removeTranslator(session.get(i + '_translator')) # type: ignore
        # install user's translators if lang != 'en'
        if session['l10n']:
            lang = session['l10n'][:2]
            if lang != 'en':
                logger.info("Setting user translations to %s", lang)
                for i in ('qt', APPNAME):
                    t = QTranslator()
                    if t.load(f"{i}_{lang}", ":/"):
                        if QCoreApplication.installTranslator(t):
                            session[i + '_translator'] = t
                        else:
                            logger.error("Error installing application translator for %s", i)
                    else:
                        logger.error("Error loading application translator for %s", i)
        else:
            logger.info("No translation required for user %s", session['app_user_code'])
        
        # set working company
        if session['current_company'] and can_use_company(session['app_user_code'], session['current_company']):
            logger.info("Setting working company to %s", session['current_company'])
            try:
                appconn.change_company(session['current_company'])
            except PyAppDBError as er:
                QMessageBox.critical(None,
                                     _tr("MessageDialog", "Critical"),
                                     f"Database error: {er.code}\n{er.message}")
                logger.error("Database error %s", er.message)
                return
        else:
            if has_companies_available(session['app_user_code']):
                dlg = ChangeCompanyDialog(self)
                if dlg.exec() == QDialog.DialogCode.Rejected:
                    sys.exit(0)
                dlg.close()
            else:
                MessageBoxCritical(self,
                                   _tr('MessageDialog', "Critical"),
                                   _tr('Login', "There is no company "
                                       "you can log on"))
                return
            
        # get current event
        logger.info("Setting current event if any")
        try:
            get_current_event()
        except PyAppDBError as er:
            MessageBoxCritical(None,
                               _tr("MessageDialog", "Database error"),
                               er.code,
                               er.message)
            logger.error("Database error %s %s", er.code, er.message)
            return
        logger.info("Current event setted to %s %s",
                     session['event_id'],
                     session['event_description'])

        # change password required
        if session['new_password_required']:
            QMessageBox.information(self,
                                    _tr('MessageDialog', "Information"),
                                    _tr('Login', "Password change is required"))
            pd = ChangePasswordDialog(self, session['user'])
            if pd.exec_() == QDialog.DialogCode.Rejected:
                sys.exit(0)
        super().accept()


class ChangeCompanyDialog(QDialog):
    "Choose/change company dialog"

    def __init__(self, parent: QWidget|None) -> None:  # first access after installation
        super().__init__(parent)
        # this dialog is used in first access too and is not always called by
        # an action so can't use action properties for set title , icon, etc.
        self.ui = Ui_ChangeCompanyDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(_tr('ChangeCompany', 'Change company'))
        self.ui.labelIcon.setPixmap(currentIcon['system_change_company'].pixmap(100))
        # get available companies
        try:
            companies = get_companies_list(session['user'])
        except PyAppDBError as er:
            MessageBoxCritical(parent,
                               _tr('MessageDialog', "Database error"),
                               er.code,
                               er.message)
            logger.error("Database error %s %s", er.code, er.message)
            return
        if not companies:
            self.ui.labelMessage.setText(_tr('MessageDialog', "There aro no other companies you can login"))
            self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setDisabled(True)
        else:
            self.ui.labelMessage.setText(_tr('MessageDialog', "Choose a company to login"))
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        self.ui.lineEditUser.setText(session['user'])
        self.ui.lineEditCompany.setText(session.get('company_description') or '')
        self.ui.comboBoxCompanies.setItemList(companies)

    def accept(self) -> None:
        "Change company"
        # get the new company code and description
        value = self.ui.comboBoxCompanies.currentData(Qt.ItemDataRole.UserRole)
        if not value:  # no other companies available for user
            super().reject()
            return
        newco = int(value)
        newde = get_company_desc(newco)
        logger.info("On change company starting of setting working company")
        try:
            appconn.change_company(newco)
        except PyAppDBError as er:
            if er.code == EUKNC: # unknown company id
                msg = _tr('ChangeCompany', "Unknown company id")
            elif er.code == ENACR: # no access rights to required company
                msg = _tr('ChangeCompany', "No access rights to required company")
            else:
                msg = f"Database error: {er.code}"

            MessageBoxCritical(self,
                               _tr('MessageDialog', 'Critical'),
                               msg,
                               er.message)
            logger.error("Database error %s %s", er.code, er.message)
            return
        session['company'] = newco
        session['company_description'] = newde
        logger.info("On change company setting working company to %s", session['company'])
        # setting current event
        logger.info("On change company setting current event if any")
        try:
            get_current_event()
        except PyAppDBError as er:
            MessageBoxCritical(self,
                               _tr('MessageDialog', "Database error"),
                               er.code,
                               er.message)
            logger.error("On change company database error %s %s", er.code, er.message)
        else:
            logger.info("On change company current event setted to %s %s",
                         session['event_id'],
                         session['event_description'])
        super().accept()
