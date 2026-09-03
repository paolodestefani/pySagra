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

This module provides events management

"""

# standard library
from enum import IntEnum
import logging

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QAction
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog

# application modules
from App import session
from App.Core.L10n import _tr
from App.Database.Connect import get_current_event
from App.Database.Models import EventIndexModel
from App.Database.Models import EventModel
from App.Database.Event import is_used
from App.Database.Lookup import price_list_lookup
from App.Widget.Dialog import MessageBoxCritical
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import ImageDelegate
from App.Widget.Form import FormIndexManager
from App.Widget.Dialog import PrintDialog
from App.Ui.EventWidget import Ui_EventWidget
from App.Core.Scripting import scriptInit
from App.Core.Scripting import scriptMethod


# logger
logger = logging.getLogger(__name__)


class evn(IntEnum):
    ID          = 0
    DESCRIPTION = 1
    DATE_START  = 2
    DATE_END    = 3
    PRICELIST   = 4
    IMAGE       = 5
    USER_INS    = 6
    DATE_INS    = 7
    USER_UPD    = 8
    DATE_UPD    = 9


def event(action: QAction, checked: bool = False) -> None:
    "Show/Edit curent connections"
    logger.info('Starting events Form')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    if not auth[0]: # no read permission
        QMessageBox.warning(mw,
                            _tr('MessageDialog', "Warning"),
                            _tr('Event', 'No access right to this archive'))
        return
    ew = EventForm(mw, title, auth)
    ew.reload()
    mw.addTab(title, ew)
    logger.info('Events Form added to main window')


class EventForm(FormIndexManager):

    def __init__(self, parent: QWidget, title: str, auth: tuple) -> None:
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
        self.ui.tableView.setLayoutName('EventIndex')
        self.ui.labelEventUsed.setVisible(False)
        # signal slot connections
        self.ui.pushButtonUpload.clicked.connect(self.upload)
        self.ui.pushButtonDownload.clicked.connect(self.download)
        self.ui.pushButtonDelete.clicked.connect(self.removeImage)
        self.ui.tableView.horizontalHeader().setSectionsMovable(True)
        self.ui.tableView.setItemDelegateForColumn(evn.PRICELIST, RelationDelegate(self, price_list_lookup))
        self.ui.tableView.setItemDelegateForColumn(evn.IMAGE, ImageDelegate(self))
        # mapper settings
        self.mapper.addMapping(self.ui.lineEditDescription, evn.DESCRIPTION)
        self.mapper.addMapping(self.ui.dateTimeEditStart, evn.DATE_START)
        self.mapper.addMapping(self.ui.dateTimeEditEnd, evn.DATE_END)
        self.ui.comboBoxPriceList.setFunction(price_list_lookup)
        self.ui.comboBoxPriceList.setNullable(True)
        self.mapper.addMapping(self.ui.comboBoxPriceList, evn.PRICELIST)
        self.mapper.addMapping(self.ui.labelEventImage, evn.IMAGE)
        # scripting init
        self.script = scriptInit(self)

    def mapperIndexChanged(self, row) -> None:
        "Check if have already movement for the event, in this case can't modifiy any date"
        super().mapperIndexChanged(row)
        logger.info('Mapper index changed')
        model = self.mapper.model()
        event = model.index(self.mapper.currentIndex(), evn.ID).data()
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
        path = st.value("Event/PathImages", QDir.current().path())
        f, t = QFileDialog.getOpenFileName(self,
                                           _tr("Event", "Select the image file to upload"),
                                           str(path),
                                           _tr("Event", "Portable Network Graphics (*.png);;All files (*.*)"))
        if not f:
            return
        pix = QPixmap(f)
        if pix.width() > 640 or pix.height() > 480:
            pix = pix.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr('Event', "The selected image is too big, it was"
                                    "automatically resized to the max allowed size of 640x480 pixels"))
        self.ui.labelEventImage.setPixmap(pix)
        # save path
        st.setValue("Event/PathImages", QFileInfo(f).path())
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
        path = st.value("Event/PathImages", QDir.current().path())
        f, t = QFileDialog.getSaveFileName(self,
                                           _tr("Event", "Select the destination file name"),
                                           str(path),
                                           _tr("Event", "Portable Network Graphics (*.png);;All files (*.*)"))
        if f == "":
            return
        img = self.ui.labelEventImage.pixmap().toImage()
        if img.save(f, 'PNG'):
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
    def new(self) -> None:
        super().new()
        currentRow = self.mapper.currentIndex()
        startDate = QDateTime.currentDateTime()
        endDate = startDate.addDays(7)
        endDate.setTime(QTime(23, 59, 59))
        # enable date edits and disable used label
        self.ui.dateTimeEditStart.setEnabled(True)
        self.ui.dateTimeEditEnd.setEnabled(True)
        self.ui.labelEventUsed.setVisible(False)
        self.model.setData(self.model.index(currentRow, evn.DATE_START), startDate)
        self.model.setData(self.model.index(currentRow, evn.DATE_END), endDate)
        self.ui.lineEditDescription.setFocus()

    @scriptMethod
    def save(self) -> None:
        "Save and update current event"
        super().save()
        get_current_event()

    @scriptMethod
    def delete(self) -> None:
        "Delete and update current event"
        msg = _tr('Event', "Are you sure you want to delete this event ?")
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                f"{msg}\n{self.ui.lineEditDescription.text()}",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        super().delete()
        get_current_event()

    @scriptMethod
    def reload(self) -> None:
        super().reload()

    @scriptMethod
    def print(self) -> None:
        "Event report"
        dialog = PrintDialog(self, 'EVENT')
        dialog.show()
