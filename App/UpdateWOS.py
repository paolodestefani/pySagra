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


"""Update web order server

This module export event data di a web order server

"""

# standard library
import logging
import ftplib
import logging
import xml.etree.ElementTree as ET

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialogButtonBox

# application modules
from App import session
from App.Database.Event import get_event_data
from App.Database.Lookup import event_lookup
from App.Database.Department import department_web_list
from App.Database.Item import item_web_list
from App.Database.Item import get_variants
from App.Database.WebOrderServer import get_web_order_server_params
from App.Database.WebOrderServer import set_web_order_server_params 
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Ui.UpdateWebOrderServerDialog import Ui_UpdateWebOrderServerDialog


# logger
logger = logging.getLogger(__name__)


def updateWOS(action: QAction, checked: bool = False) -> None:
    logger.info('Starting update web order server dialog')
    mw = session['mainwin']
    title = _tr("UpdateWOS", "Update Web Order Server")
    auth = action.data()
    icon = action.icon()
    if not auth[2]: # no execute permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('UpdateWOS', 'No access right to this function'))
        return
    dialog = UpdateWebOrderServerDialog(mw, title, icon, auth)
    dialog.show()
    logger.info('Web order server dialog shown')


class UpdateWebOrderServerDialog(QDialog):
    "Customizations dialog"

    def __init__(self, parent: QWidget, title: str, icon: QIcon, auth: str) -> None:
        super().__init__(parent)
        self.ui = Ui_UpdateWebOrderServerDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(100))
        self.ui.comboBoxEvent.setItemList(event_lookup())
        # set web order server parameters from database
        server, port, encoding, username, password, filename = get_web_order_server_params()
        self.ui.lineEditServer.setText(server)
        self.ui.spinBoxPort.setValue(port or 21)
        self.ui.lineEditEncoding.setText(encoding or 'utf-8')
        self.ui.lineEditUser.setText(username)
        self.ui.lineEditPassword.setText(password)
        self.ui.lineEditFileName.setText(filename)
        # connect signals
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Close).setDefault(True)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.updateWebOrderServer)
        
    def updateWebOrderServer(self):
        "Get and send web order server parameters"
        logger.info('Updating web order server')
        # current selected event
        event = int(self.ui.comboBoxEvent.currentData())
        # file name
        filename = self.ui.lineEditFileName.text()
        # create XML file
        root = ET.Element("event")
        ed, ds, de, pli = get_event_data(event)
        ET.SubElement(root, "title").text = ed
        ET.SubElement(root, "start_date").text = ds.toString(Qt.ISODate)
        ET.SubElement(root, "end_date").text = de.toString(Qt.ISODate)

        items = ET.SubElement(root, "items")        
        with gui_exception_context(self, _tr("UpdateWOS", "Generate items")):
            for did, d in department_web_list():
                    dep = ET.SubElement(items, "department")
                    dep.set('description', d)
                    for i, d, p, a, v in item_web_list(event, did):
                        item = ET.SubElement(dep, "item")
                        ET.SubElement(item, "id").text = str(i)
                        ET.SubElement(item, "description").text = d
                        ET.SubElement(item, "price").text = str(p)
                        ET.SubElement(item, "active").text = str(a)
                        ET.SubElement(item, "variants").text = str(v)
        vars = ET.SubElement(root, "itemvariants")   
        with gui_exception_context(self, _tr("UpdateWOS", "Generate item variants")):
            for did, d in department_web_list():     
                for i, d, p, a, v in item_web_list(event, did):
                    if v:
                        item = ET.SubElement(vars, "item")
                        item.set('id', str(i))
                        for vd, vp in get_variants(i):
                            vr = ET.SubElement(item, "variant")
                            ET.SubElement(vr, "description").text = vd
                            ET.SubElement(vr, "price").text = str(vp)
        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ", level=0)
        success = False
        with gui_exception_context(self, _tr("UpdateWOS", "Save XML file")):
            with open(filename, 'wb') as f:
                tree.write(f, encoding='utf-8', xml_declaration=True)
            success = True
        if success:
            logger.info('XML file %s created successfully', filename)
        else:
            return
        # UPLOAD FILE TO FTP SERVER
        logger.info('Uploading web order file to FTP server')
        # Fill Required Information
        server = self.ui.lineEditServer.text()
        port = self.ui.spinBoxPort.value()
        encoding = self.ui.lineEditEncoding.text()
        user = self.ui.lineEditUser.text()
        password = self.ui.lineEditPassword.text()
        filename = self.ui.lineEditFileName.text()
        # Connect FTP Server
        success = False
        with gui_exception_context(self, _tr("UpdateWOS", "Update ftp server")):
            # connect
            ftp_server = ftplib.FTP(server, user, password)
            # force encoding
            ftp_server.encoding = encoding
            # Read file in binary mode
            with open(filename, "rb") as file:
                # Command for Uploading the file "STOR filename"
                ftp_server.storbinary(f"STOR {filename}", file)
            # Close the Connection
            ftp_server.quit()
            # store ftp settinggs to db
            set_web_order_server_params(server,
                                        port,
                                        encoding,
                                        user,
                                        password,
                                        filename)
            success = True
        if success:
            logger.info('Web order server updated successfully') 
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("UpdateWOS", "Web order server updated successfully."),
                                    QMessageBox.StandardButton.Ok)
                