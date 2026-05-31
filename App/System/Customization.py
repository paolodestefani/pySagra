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

"""Customization

Import/export of report, itemview and sort-filter customizations

"""

# standard library
import os
import csv
import io
import zipfile
import logging

# PySide6
from PySide6.QtCore import QDir
from PySide6.QtCore import QSettings
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Database.Adaptation import export_adaptation
from App.Database.Adaptation import export_adaptation_setting
from App.Database.Adaptation import import_adaptation
from App.Database.Adaptation import clear_adaptation
from App.Widget.Dialog import MessageBoxCritical

from App.Ui.CustomizationsDialog import Ui_CustomizationsDialog


# logger
logger = logging.getLogger(__name__)


# export type and version
ADAPTVERSION = ['Adaptation archive for pySagra', '1.0']


def decodebool(instr: str) -> bool|None:
    "Decode boolean from string"
    outstr: bool|None = None
    match instr:
        case 'True':
            outstr = True
        case 'False':
            outstr = False
        case _:
            outstr = None
    return outstr 


def customization(action: QAction, checked: bool = False) -> None:
    "Show customization dialog"
    logger.info('Starting customization dialog')
    mw = session['mainwin']
    title = action.text()
    icon = action.icon()
    auth = action.data()
    dialog = CustomizationsDialog(mw, title, icon, auth)
    dialog.show()
    logger.info('Customization dialog shown')


class CustomizationsDialog(QDialog):
    """Customizations dialog for import/export and clear of 
    report, itemview and sort-filter customizations"""

    def __init__(self, parent: QWidget, title: str, icon: QIcon, auth: str) -> None:
        super().__init__(parent)
        self.ui = Ui_CustomizationsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(100))
        # signal/slot
        self.ui.pushButtonExport.clicked.connect(self.exportCustomization)
        self.ui.pushButtonImport.clicked.connect(self.importCustomization)
        self.ui.pushButtonClear.clicked.connect(self.clearCustomization)

    def exportCustomization(self) -> None:
        "Export customizations to a zipped CSV files - *.zip"
        st = QSettings()
        path = st.value("ExportAdaptationsFile", QDir.current().path(), type=str)
        fileName, filter = QFileDialog.getSaveFileName(self,
                                caption=_tr('Customizations', "Select the file name to create"),
                                dir=str(path),
                                filter= 'pySagra Zipped Adaptation File (*.zip *.*)',
                                options=QFileDialog.Option.DontUseNativeDialog )
        if fileName == "":
            return
        if not fileName.endswith('.zip'):
            fileName += '.zip'
        with gui_exception_context(self, _tr('Customizations', 'Export customizations')):
            # looks like zipfile accept qt file path with / so no need to use os.path.join
            with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                # version
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                writer.writerow(ADAPTVERSION)
                zf.writestr('version', string_buffer.getvalue())
                # adaptation
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                writer.writerows(export_adaptation())
                zf.writestr('adaptation', string_buffer.getvalue())
                # adaptation setting
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                writer.writerows(export_adaptation_setting())
                zf.writestr('adaptation_setting', string_buffer.getvalue())
    
                st.setValue("ExportAdaptationsFile", fileName)
                QMessageBox.information(self,
                                        _tr('MessageDialog', 'Information'),
                                        _tr('Customizations', 'Export completed successfully'))

    def importCustomization(self) -> None:
        "Import customizations from a zipped CSV files - *.zip"
        st = QSettings()
        path = st.value("ExportAdaptationsFile", QDir.current().path(), type=str)
        fileName, filter = QFileDialog.getOpenFileName(self,
                                                       caption=_tr('Customizations', "Select the file name to load"),
                                                       dir=str(path),
                                                       filter= 'pySagra Zipped Adaptation File (*.zip *.*)')
        if fileName == "":
            return
        with gui_exception_context(self, _tr('Customizations', 'Import customizations')):
            adaptations: list[tuple] = []
            adaptsettings: list[tuple] = []
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                # check version
                string_buffer = io.StringIO(zf.read('version').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    if [row[0], row[1]] != ADAPTVERSION:
                        QMessageBox.information(self,
                                                _tr('MessageDialog', 'Information'),
                                                _tr('Customizations', 'Wrong file format or version'))
                        return
                # adaptation
                clear_adaptation()
                string_buffer = io.StringIO(zf.read('adaptation').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    adaptations.append((
                        int(row[0]),                        # id
                        row[1],                             # type
                        row[2],                             # class
                        row[3],                             # description
                        int(row[4]),                        # class sorting
                        decodebool(row[5]),                 # class default
                        int(row[6]) if row[6] else None,    # report id
                        int(row[7]) if row[7] else None,    # row count limit
                        decodebool(row[8]),                 # system
                        ))
                # adaptation setting
                string_buffer = io.StringIO(zf.read('adaptation_setting').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    adaptsettings.append((
                        int(row[0]),                        # setting id
                        int(row[1]),                        # adapt id
                        int(row[2]) if row[2] else None,    # column
                        int(row[3]) if row[3] else None,    # sorting
                        decodebool(row[4]),                 # is visible
                        int(row[5]) if row[5] else None,    # size
                        row[6] or None,                     # element type
                        int(row[7]) if row[7] else None,    # layout row
                        int(row[8]) if row[8] else None,    # combo1 index
                        decodebool(row[9]),                 # negate
                        int(row[10]) if row[10] else None,  # combo2 index
                        row[11] or None                     # widget value
                                    ))
                import_adaptation(adaptations, adaptsettings)
       
            st.setValue("ExportAdaptationsFile", fileName)
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Customizations', 'Import completed successfully'))

    def clearCustomization(self) -> None:
        "Clear current customizations"
        if QMessageBox.question(self,
                                _tr('MessageDialog', 'Question'),
                                _tr('Customizations', 'Customizations will be cleared, continue ?'),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                                QMessageBox.StandardButton.No  # default botton
                                ) == QMessageBox.StandardButton.No:
            return
        with gui_exception_context(self, _tr('Customizations', "Clear customizations")):
            clear_adaptation()
        
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Customizations', 'Customizations deleted'))

