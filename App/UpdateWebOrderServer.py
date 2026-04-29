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
import os
import csv
import locale
import zipfile
import logging
import ftplib
import logging
import cryptography
import xml.etree.ElementTree as ET

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialogButtonBox

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Database.Event import get_event_data
from App.Database.Lookup import event_lookup
from App.Database.Department import department_list
from App.Database.Item import item_web_list
from App.Database.Item import get_variants
from App.Database.WebOrderServer import get_web_order_server_params
from App.Database.WebOrderServer import set_web_order_server_params 
from App.Core.L10n import _tr

from App.Ui.UpdateWebOrderServerDialog import Ui_UpdateWebOrderServerDialog



def updateWebOrderServer(action: QAction, checked: bool = False) -> None:
    logging.info('Starting update web order server dialog')
    mw = session['mainwin']
    auth = action.data()
    title = action.text()
    icon = action.icon()
    dialog = UpdateWebOrderServerDialog(mw, title, icon, auth)
    dialog.show()
    logging.info('Web order server dialog shown')


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
        logging.info('Updating web order server')
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
        for did, d in department_list():
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
        for did, d in department_list():     
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
        try:
            with open(filename, 'wb') as f:
                tree.write(f, encoding='utf-8', xml_declaration=True)
        except Exception as er:
            logging.error('Error on writing XML file: %s', str(er))
            QMessageBox.critical(self,
                                 _tr("Weborder server", "Error on writing XML file"),
                                str(er),
                                QMessageBox.StandardButton.Ok)
            return
        else:
            logging.info('XML file %s created successfully', filename)

        # UPLOAD FILE TO FTP SERVER
        logging.info('Uploading web order file to FTP server')
        # Fill Required Information
        server = self.ui.lineEditServer.text()
        port = self.ui.spinBoxPort.value()
        encoding = self.ui.lineEditEncoding.text()
        user = self.ui.lineEditUser.text()
        password = self.ui.lineEditPassword.text()
        filename = self.ui.lineEditFileName.text()
        # Connect FTP Server
        try:
            ftp_server = ftplib.FTP(server, user, password)
            # force encoding
            ftp_server.encoding = encoding
        except Exception as er:
            logging.error('Error connecting to ftp server: %s', str(er))
            QMessageBox.critical(self,
                                 _tr("Weborder server", "Ftp connection error"),
                                str(er),
                                QMessageBox.StandardButton.Ok)
            return

        # Read file in binary mode
        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {filename}", file)

        # Close the Connection
        ftp_server.quit()
        
        # store ftp settinggs to db
        try:
            set_web_order_server_params(server,
                                        port,
                                        encoding,
                                        user,
                                        password,
                                        filename)
        except PyAppDBError as er:
            logging.error('Error storing web order server parameters: %s', str(er))
            QMessageBox.critical(self,
                                 _tr("Weborder server", "Error updating web order server"),
                                str(er),
                                QMessageBox.StandardButton.Ok)
        else:
            logging.info('Web order server parameters stored to database')
            QMessageBox.information(self,
                                    _tr("Weborder server", "Update Web Order Server"),
                                    _tr("Weborder server", "Web order server updated successfully."),
                                    QMessageBox.StandardButton.Ok)
            logging.info('Web order server updated successfully')   
            
            
        # # parse XML to check for errors
        # # parse XML data file
        # session = {}
        # tree = ET.parse(filename)
        # root = tree.getroot()
        # session['event_description']    = root.find("title").text
        # session['departments']          = []
        # session['dep_index']            = 0
        # for dep in root.find("items"):
        #     session['departments'].append(dep.attrib['description'])
        # session['lines'] = {}
        # for dep in root.find("items"):
        #     session['lines'][dep.attrib['description']]=[[
        #         c.find('id').text,                                      # 0 item id as string (session dict are stored as string anyway)
        #         c.find('description').text,                             # 1 item description
        #         0,                                                      # 2 quantity
        #         float(c.find('price').text),                            # 3 price number (for totals)
        #         locale.currency(float(c.find('price').text)),           # 4 price as currency string
        #         True if c.find('active').text == 'True' else False,     # 5 is active
        #         True if c.find('variants').text == 'True' else False,   # 6 has variants
        #         '',                                                     # 7 variants description 
        #         0.0]                                                    # 8 variant price delta
        #         for c in dep]
        # session['variants'] = {}
        # for i in root.find("itemvariants"):
        #     itemid = i.attrib['id'] # session dict keys are stored as string anyway
        #     session['variants'][itemid] = []
        #     for v in i.findall('variant'):
        #         description = v.find('description').text
        #         pricedelta  = float(v.find('price').text)
        #         pricedescr  = '(+' + locale.currency(pricedelta) + ')' if pricedelta != 0.0 else ''
        #         session['variants'][itemid].append([
        #             description,
        #             pricedelta,
        #             pricedescr])
                
        # print("SESSION", session)
        # for i, l in enumerate(session['lines'][session['departments'][0]]):
        #     print(f"LINE {i}: ", l)
  
        
        