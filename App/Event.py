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

"""Events

This module allows events management


"""

# standard library
import logging
import cryptography
#import xml.etree.ElementTree as ET

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QAction
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QFileDialog

# application modules
from App import session
from App.Core.Cryptography import string_encode
from App.Core.Cryptography import string_decode
from App.Database.Connect import get_current_event
from App.Database.Models import EventIndexModel
from App.Database.Models import EventModel
from App.Database.Event import is_used
from App.Database.Department import department_list
from App.Database.Item import item_web_list
from App.Database.Lookup import price_list_lookup
from App.Widget.Dialog import MessageBoxCritical
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import ImageDelegate
from App.Widget.Form import FormIndexManager
from App.Widget.Dialog import PrintDialog
from App.Ui.EventWidget import Ui_EventWidget
from App.Core.L10n import _tr
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod


(ID, DESCRIPTION, DATE_START, DATE_END, PRICELIST, IMAGE,
 USER_INS, DATE_INS, USER_UPD, DATE_UPD) = range(10)


def event(action: QAction, checked: bool = False) -> None:
    "Show/Edit curent connections"
    logging.info('Starting events Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    ew = EventForm(mw, title, auth)
    ew.reload()
    mw.addTab(title, ew)
    logging.info('Events Form added to main window')


class EventForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent, auth)
        model = EventModel(self)
        idxModel = EventIndexModel(self)
        self.setModel(model, idxModel)
        self.tabName = title
        self.helpLink = None
        # available status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (True, True, True, True, True, True, True, True,
                                True, True, True, True)
        self.ui = Ui_EventWidget()
        self.ui.setupUi(self)
        self.setIndexView(self.ui.tableView)
        self.ui.tableView.setLayoutName('event')
        # signal slot connections
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonDelete.clicked.connect(self.removeImage)
        #self.ui.pushButtonUpdateWebOrder.clicked.connect(self.updateWebOrderServer)
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        self.ui.tableView.setItemDelegateForColumn(PRICELIST, RelationDelegate(self, price_list_lookup))
        self.ui.tableView.setItemDelegateForColumn(IMAGE, ImageDelegate(self))
        # map view to mapper and mapper to view
        #self.ui.tableView.selectionModel().currentRowChanged.connect(self.mapper.setCurrentModelIndex)
        #self.mapper.currentIndexChanged.connect(self.ui.tableView.selectRow)
        # mapper mappings
        #self.mapper.setItemDelegate(PMapperDelegate(self))
        self.mapper.addMapping(self.ui.lineEditDescription, DESCRIPTION)
        self.mapper.addMapping(self.ui.dateTimeEditStart, DATE_START, b"modelDataDateTime")
        self.mapper.addMapping(self.ui.dateTimeEditEnd, DATE_END, b"modelDataDateTime")
        self.ui.comboBoxPriceList.setFunction(price_list_lookup)
        self.mapper.addMapping(self.ui.comboBoxPriceList, PRICELIST, b"modelDataStr")
        self.mapper.addMapping(self.ui.labelEventImage, IMAGE, b"imageBytearray")
        #self.mapper.addMapping(self.ui.plainTextEditTableList, TABLES)
         # restore settings
        #st = QSettings()       
        #self.ui.lineEditServer.setText(st.value("WebOrder/Server", ""))
        #self.ui.spinBoxPort.setValue(st.value("WebOrder/Port", 21, type=int))
        #self.ui.lineEditFileName.setText(st.value("WebOrder/FileName", ""))
        # try:
        #     self.ui.lineEditUser.setText(string_decode(st.value("WebOrder/User", "")))
        # except cryptography.fernet.InvalidToken:
        #     self.ui.lineEditUser.setText("")
        # try:
        #     self.ui.lineEditPassword.setText(string_decode(st.value("WebOrder/Password", "")))
        # except cryptography.fernet.InvalidToken:
        #     self.ui.lineEditPassword.setText("")
        # scripting init
        self.script = scriptInit(self)

    def mapperIndexChanged(self, row):
        "Check if have already movement for the event, in this case can't modifiy any date"
        super().mapperIndexChanged(row)
        model = self.mapper.model()
        event = model.index(self.mapper.currentIndex(), ID).data()
        if is_used(event):
            self.ui.dateTimeEditStart.setDisabled(True)
            self.ui.dateTimeEditEnd.setDisabled(True)
            self.ui.labelEventUsed.setVisible(True)
        else:
            self.ui.dateTimeEditStart.setEnabled(True)
            self.ui.dateTimeEditEnd.setEnabled(True)
            self.ui.labelEventUsed.setVisible(False)


    @scriptMethod
    def upload(self) -> None:
        "Upload event image file"
        # get path
        st = QSettings()
        path = st.value("PathImagesEvents", QDir.current().path())
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr("Event", "Select the image file to upload"),
                                           str(path),
                                           _tr("Event", "Portable Network Graphics (*.png);;All files (*.*)"))
        if not f:
            return
        pix = QPixmap(f)
        if pix.width() > 640 or pix.height() > 480:
            pix = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.ui.labelEventImage.setPixmap(pix)
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr('Event', "The selected image is too big, it was"
                                    "automatically resized to the max allowed size of 640x480 pixels"))
        else:
            self.ui.labelEventImage.setPixmap(pix)
        # save path
        st.setValue("PathImagesEvents", QFileInfo(f).path())
        if hasattr(self.model, 'isDirty'):
            self.model.isDirty = True
        if hasattr(self.model, 'userDataChanged'):
            self.model.userDataChanged.emit()

    @scriptMethod
    def download(self) -> None:
        "Download event image to file"
        if not self.ui.labelEventImage.pixmap():
            return
        st = QSettings()
        path = st.value("PathImagesEvents", QDir.current().path())
        f, t = QFileDialog.getSaveFileName(self,
                                           _tr("Event", "Select the destination file name"),
                                           str(path),
                                           _tr("Event", "Portable Network Graphics (*.png);;All files (*.*)"))
        if f == "":
            return
        pix = self.ui.labelEventImage.pixmap()
        if pix.save(f):
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("Event", "Image file saved"))
        else:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Critical"),
                               _tr("Event", "Error on saving image file"))

    @scriptMethod
    def removeImage(self) -> None:
        "Remove company image"
        self.ui.labelEventImage.clear()
        if hasattr(self.model, 'isDirty'):
            self.model.isDirty = True
        if hasattr(self.model, 'userDataChanged'):
            self.model.userDataChanged.emit()

    @scriptMethod
    def new(self):
        super().new()
        currentRow = self.mapper.currentIndex()
        startDate = QDateTime.currentDateTime()
        endDate = startDate.addDays(7)
        endDate.setTime(QTime(23, 59, 59))
        # enable date edits and disable used label
        self.ui.dateTimeEditStart.setEnabled(True)
        self.ui.dateTimeEditEnd.setEnabled(True)
        self.ui.labelEventUsed.setVisible(False)
        self.model.setData(self.model.index(currentRow, DATE_START), startDate)
        self.model.setData(self.model.index(currentRow, DATE_END), endDate)
        self.ui.lineEditDescription.setFocus()

    @scriptMethod
    def save(self):
        "Save and update current event"
        super().save()
        get_current_event()

    @scriptMethod
    def delete(self):
        "Delete and update current event"
        msg = _tr('Event', "Are you sure you want to delete this event ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{self.ui.lineEditDescription.text()}",
                                QMessageBox.Yes | QMessageBox.No,  # butons
                                QMessageBox.No  # default botton
                                ) == QMessageBox.No:
            return
        super().delete()
        get_current_event()

    @scriptMethod
    def reload(self):
        super().reload()

    @scriptMethod
    def print(self):
        "Event report"
        dialog = PrintDialog(self, 'EVENT')
        dialog.show()

    # def updateWebOrderServer(self):
    #     "Get and send web order server parameters"
    #     # store ftp login settinggs
    #     st = QSettings()
    #     st.setValue("WebOrder/Server", self.ui.lineEditServer.text())
    #     st.setValue("WebOrder/Port", self.ui.spinBoxPort.value())
    #     st.setValue("WebOrder/FileName", self.ui.lineEditFileName.text())
    #     st.setValue("WebOrder/User", string_encode(self.ui.lineEditUser.text()))
    #     st.setValue("WebOrder/Password", string_encode(self.ui.lineEditPassword.text()))
    #     # current selected event
    #     event = int(self.mapper.model().index(self.mapper.currentIndex(), 0).data())
    #     # file name
    #     filename = self.ui.lineEditFileName.text()
    #     # create XML file
    #     root = ET.Element("event")
    #     ET.SubElement(root, "title").text = self.ui.lineEditDescription.text()
    #     ET.SubElement(root, "date_start").text = self.ui.dateTimeEditStart.dateTime().toString(Qt.ISODate)
    #     ET.SubElement(root, "date_end").text = self.ui.dateTimeEditEnd.dateTime().toString(Qt.ISODate)

    #     items = ET.SubElement(root, "items")        
    #     for did, d in department_list():
    #             dep = ET.SubElement(items, "department")
    #             dep.set('description', d)
    #             for i, d, p, a, v in item_web_list(event, did):
    #                 item = ET.SubElement(dep, "item")
    #                 ET.SubElement(item, "id").text = str(i)
    #                 ET.SubElement(item, "description").text = d
    #                 ET.SubElement(item, "price").text = str(p)
    #                 ET.SubElement(item, "active").text = str(a)
    #                 ET.SubElement(item, "variants").text = str(v)
    #     vars = ET.SubElement(root, "itemvariants")   
    #     for did, d in department_list():     
    #         for i, d, p, a, v in item_web_list(event, did):
    #             if v:
    #                 item = ET.SubElement(vars, "item")
    #                 item.set('id', str(i))
    #                 for vd, vp in get_variants(i):
    #                     vr = ET.SubElement(item, "variant")
    #                     ET.SubElement(vr, "description").text = vd
    #                     ET.SubElement(vr, "price").text = str(vp)
    #     tree = ET.ElementTree(root)
    #     ET.indent(tree, space="    ", level=0)
    #     try:
    #         with open(filename, 'wb') as f:
    #             tree.write(f, encoding='utf-8', xml_declaration=True)
    #     except Exception as er:
    #         errors.append(str(er))
    #     else:
    #         info.append(_tr('Events', "File XML generated"))

    #     # parse XML data file
    #     #tree = ET.parse(filename)
    #     #root = tree.getroot()
    #     #event_description = root.find("title").text
    #     #department = {}
    #     #deps = root.find('departments')
    #     #for dep in deps.findall('department'):
    #     #    department[int(dep.find('id').text)] = dep.find('description').text
    #     #dep_list = []
    #     #for dep in root.find("items"):
    #     #    dep_list.append(dep.attrib['description'])
    #     #print("Reparti", dep_list)

    #     #item_list = []
    #     #for dep in root.find("items"):
    #     #    print("Reparto", dep.attrib)
    #     #    for child in dep:
    #     #        print("Art", child.find('id').text)
    #     #        print("Desc", child.find('description').text)
    #     #        print("Prz", child.find('price').text)
        
    #     # parse XML data file
    #     # session = {}
    #     # tree = ET.parse(filename)
    #     # root = tree.getroot()
    #     # session['event_description'] = root.find("title").text
    #     # session['departments'] = []
    #     # for dep in root.find("items"):
    #     #     session['departments'].append(dep.attrib['description'])
    #     # session['lines'] = {}
    #     # for dep in root.find("items"):
    #     #     session['lines'][dep.attrib['description']]=[[
    #     #         int(c.find('id').text),
    #     #         c.find('description').text,
    #     #         float(c.find('price').text),
    #     #         True if c.find('active').text == 'True' else False]
    #     #         for c in dep]

    #     # print("Session", session)
            
    #     #print(department)
    #     # send file to server

       
    #     import ftplib

    #     # Fill Required Information
    #     HOSTNAME = self.ui.lineEditServer.text()
    #     USERNAME = self.ui.lineEditUser.text()
    #     PASSWORD = self.ui.lineEditPassword.text()

    #     # Connect FTP Server
    #     ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    #     # force UTF-8 encoding
    #     ftp_server.encoding = "utf-8"

    #     # Read file in binary mode
    #     with open(filename, "rb") as file:
    #         # Command for Uploading the file "STOR filename"
    #         ftp_server.storbinary(f"STOR {filename}", file)

    #     # Get list of files
    #     #ftp_server.dir()

    #     # Close the Connection
    #     ftp_server.quit()

        


