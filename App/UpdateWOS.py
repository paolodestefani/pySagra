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
import ftplib
import io
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
from App.Database.SeatMap import table_list
from App.Database.WebOrderServer import get_web_order_server_params
from App.Database.WebOrderServer import set_web_order_server_params 
from App.Common.L10n import _tr
from App.Widget.ExceptionHandler import gui_exception_context
from App.Ui.UpdateWebOrderServerDialog import Ui_UpdateWebOrderServerDialog


# logger
logger = logging.getLogger(__name__)

# seconds to wait for the ftp server before giving up
FTP_TIMEOUT = 30


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

    def __init__(self, parent: QWidget, title: str, icon: QIcon, auth: tuple) -> None:
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
        "Create the event XML file and send it to the web order server"
        logger.info('Updating web order server')
        # current selected event
        if self.ui.comboBoxEvent.currentData() is None:
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("UpdateWOS", "Select an event first"))
            return
        event = int(self.ui.comboBoxEvent.currentData())
        # path of the file on the server, as the ftp user sees it: relative to its
        # home folder or absolute, whatever the server allows
        filename = self.ui.lineEditFileName.text().strip()
        if not filename:
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("UpdateWOS", "The file name is required"))
            return
        # create XML file: any error stops here, an incomplete file is never sent
        with gui_exception_context(self, _tr("UpdateWOS", "Generate the XML file")) as outcome:
            root = self.eventXml(event)
        if not outcome.ok:
            return
        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ", level=0)
        # the file is made in memory: no local file, its path is the one on the server only
        xml = io.BytesIO()
        tree.write(xml, encoding='utf-8', xml_declaration=True)
        xml.seek(0)
        logger.info('XML file for %s created successfully', filename)
        # UPLOAD FILE TO FTP SERVER
        logger.info('Uploading web order file to FTP server')
        server = self.ui.lineEditServer.text().strip()
        port = self.ui.spinBoxPort.value()
        encoding = self.ui.lineEditEncoding.text().strip() or 'utf-8'
        user = self.ui.lineEditUser.text()
        password = self.ui.lineEditPassword.text()
        with gui_exception_context(self, _tr("UpdateWOS", "Update ftp server")) as outcome:
            # the port of the dialog, a timeout instead of a frozen window,
            # the connection closed also on errors
            with ftplib.FTP(encoding=encoding, timeout=FTP_TIMEOUT) as ftp_server:
                ftp_server.connect(server, port)
                ftp_server.login(user, password)
                # Command for Uploading the file "STOR filename"
                ftp_server.storbinary(f"STOR {filename}", xml)
            # store ftp settinggs to db
            set_web_order_server_params(server,
                                        port,
                                        encoding,
                                        user,
                                        password,
                                        filename)
        if outcome.ok:
            logger.info('Web order server updated successfully') 
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("UpdateWOS", "Web order server updated successfully."),
                                    QMessageBox.StandardButton.Ok)

    def eventXml(self, event: int) -> ET.Element:
        "The XML of the event: dates, tables, items by department and item variants"
        root = ET.Element("event")
        if not (data := get_event_data(event)):
            raise ValueError(_tr("UpdateWOS", "Event not found"))
        ed, ds, de, pli = data
        ET.SubElement(root, "title").text = ed
        ET.SubElement(root, "start_date").text = ds.toString(Qt.DateFormat.ISODate)
        ET.SubElement(root, "end_date").text = de.toString(Qt.DateFormat.ISODate)
        # tables
        tl = []
        for table_code, row_pos, col_pos, text_color, bg_color, unavailable in table_list():
            if row_pos is None or col_pos is None:
                continue
            if not unavailable and not ',' in table_code:
                tl.append(table_code)
        ET.SubElement(root, "tables").text = ",".join(tl)
        # items by department, then the variants of the items that have them
        items = ET.SubElement(root, "items")
        variants = ET.SubElement(root, "itemvariants")
        for did, desc, ta in department_web_list():
            dep = ET.SubElement(items, "department")
            dep.set('description', desc)
            dep.set('is_for_takeaway', str(ta))
            for i, d, p, a, v in item_web_list(event, did):
                item = ET.SubElement(dep, "item")
                ET.SubElement(item, "id").text = str(i)
                ET.SubElement(item, "description").text = d
                ET.SubElement(item, "price").text = str(p)
                ET.SubElement(item, "active").text = str(a)
                ET.SubElement(item, "variants").text = str(v)
                if v:
                    vitem = ET.SubElement(variants, "item")
                    vitem.set('id', str(i))
                    for vd, vp in get_variants(i):
                        vr = ET.SubElement(vitem, "variant")
                        ET.SubElement(vr, "description").text = vd
                        ET.SubElement(vr, "price").text = str(vp)
        return root
