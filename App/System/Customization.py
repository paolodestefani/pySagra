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
import json
import os
import csv
import io
import zipfile
import logging

# PySide6
from PySide6.QtCore import QDir, QFile
from PySide6.QtCore import QSettings
from PySide6.QtCore import QTimer
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
from App.Database.Adaptation import import_adaptation_settings
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
    auth = action.data()
    if not auth[2]: # no execute permission
        QMessageBox.warning(
            mw,
            _tr('MessageDialog', "Warning"),
            _tr('CashDesk', 'No access right to this function')
        )
        return
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
        "Export customizations to a psa files"
        types = []
        if self.ui.checkBoxItemView.isChecked():
            types.append(('I', 'itemview')) # itemview
        if self.ui.checkBoxSortFilter.isChecked():
            types.append(('S', 'sortfilter')) # sortfilter
        if self.ui.checkBoxReport.isChecked():
            types.append(('R', 'report')) # report
        if not types:
            QMessageBox.warning(
                self,
                _tr('MessageDialog', "Warning"),
                _tr('Customizations', 'No customization type selected')
            )
            return
        st = QSettings()
        path = st.value("Adatpations/PathExportCustomizations", QDir.current().path(), type=str)
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Customizations', "Select the directory"),
                                                     str(path))
        if directory == "":
            # ---  WORKAROUND FOR MACOS ---
            self.raise_()
            self.activateWindow()
            return
        completed = False
        with gui_exception_context(self, _tr('Customizations', 'Export customizations')):
            for adapt_type, adapt_name in types:
                fileName = f"{directory}/{adapt_name}.psa" # pySagra Adaptation
                if QFile.exists(fileName):
                    if QMessageBox.question(
                        self,
                        _tr('MessageDialog', 'Question'),
                        _tr('Customizations', 'File {0} already exists, overwrite ?').format(fileName),
                        QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
                        QMessageBox.StandardButton.No  # default botton
                        ) == QMessageBox.StandardButton.No:
                        continue
                export_data = []
                for adapt in export_adaptation(adapt_type):
                    adapt['settings'] = export_adaptation_setting(adapt['adaptation_id'])
                    del adapt['adaptation_id'] # remove id from export
                    export_data.append(adapt)
                    
                with open(fileName, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=4, ensure_ascii=False)
                
                completed = True

            st.setValue("Adatpations/PathExportCustomizations", directory)
            if completed:
                # ---  WORKAROUND FOR MACOS ---
                self.raise_() 
                self.activateWindow() 
                QMessageBox.information(
                    self,
                    _tr('MessageDialog', 'Information'),
                    _tr('Customizations', 'Export completed successfully')
                )

    def importCustomization(self) -> None:
        "Import customizations from psa files"
        st = QSettings()
        path = st.value("Adatpations/PathExportCustomizations", QDir.current().path(), type=str)
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            caption=_tr('Customizations', "Select the file name to load"),
            dir=str(path),
            filter= 'pySagra Adaptation File (*.psa);;All files (*.*)'
        )
        if fileName == "":
            return
        with gui_exception_context(self, _tr('Customizations', 'Import customizations')):
            with open(fileName, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                
            for adapt in import_data:
                adp_id = import_adaptation(adapt)
                for setting in adapt.get('settings', []):
                    setting['adaptation_id'] = adp_id
                    import_adaptation_settings(setting)
                
            st.setValue("Adatpations/PathExportCustomizations", path)
            QMessageBox.information(
                self,
                _tr('MessageDialog', 'Information'),
                _tr('Customizations', 'Import completed successfully')
            )

    def clearCustomization(self) -> None:
        "Clear current customizations"
        types = []
        if self.ui.checkBoxItemView.isChecked():
            types.append('I') # itemview
        if self.ui.checkBoxSortFilter.isChecked():
            types.append('S') # sortfilter
        if self.ui.checkBoxReport.isChecked():
            types.append('R') # report
        if not types:
            QMessageBox.warning(
                self,
                _tr('MessageDialog', "Warning"),
                _tr('Customizations', 'No customization type selected')
            )
            return
        if QMessageBox.question(
            self,
            _tr('MessageDialog', 'Question'),
            _tr('Customizations', 'Customizations will be cleared, continue ?'),
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
            QMessageBox.StandardButton.No  # default botton
            ) == QMessageBox.StandardButton.No:
            return
        
        with gui_exception_context(self, _tr('Customizations', "Clear customizations")):
            for adapt_type in types:
                clear_adaptation(adapt_type)
        
            QMessageBox.information(
                self,
                _tr('MessageDialog', 'Information'),
                _tr('Customizations', 'Customizations deleted')
            )

