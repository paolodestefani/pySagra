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
from App.Common.L10n import _tr
from App.Common.ExceptionHandler import gui_exception_context
from App.Database.Adaptation import export_adaptation
from App.Database.Adaptation import export_adaptation_setting
from App.Database.Adaptation import import_adaptation
from App.Database.Adaptation import import_adaptation_settings
from App.Database.Adaptation import clear_adaptation
from App.Widget.Dialog import MessageBoxCritical

from App.Ui.AdaptationsDialog import Ui_AdaptationsDialog


# logger
logger = logging.getLogger(__name__)


# def decodebool(instr: str) -> bool|None:
#     "Decode boolean from string"
#     outstr: bool|None = None
#     match instr:
#         case 'True':
#             outstr = True
#         case 'False':
#             outstr = False
#         case _:
#             outstr = None
#     return outstr 


def adaptation(action: QAction, checked: bool = False) -> None:
    "Show adaptation dialog"
    logger.info('Starting adaptation dialog')
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
    dialog = AdaptationsDialog(mw, title, icon, auth)
    dialog.show()
    logger.info('Adaptation dialog shown')


class AdaptationsDialog(QDialog):
    """Adaptations dialog for import/export and clear of 
    report, itemview and sort-filter adaptations"""

    def __init__(self, parent: QWidget, title: str, icon: QIcon, auth: str) -> None:
        super().__init__(parent)
        self.ui = Ui_AdaptationsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(100))
        # signal/slot
        self.ui.pushButtonExport.clicked.connect(self.exportAdaptations)
        self.ui.pushButtonImport.clicked.connect(self.importAdaptations)
        self.ui.pushButtonClear.clicked.connect(self.clearAdaptations)

    def exportAdaptations(self) -> None:
        "Export adaptations to a psa files"
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
                _tr('Adaptations', 'No adaptation type selected')
            )
            return
        st = QSettings()
        path = st.value("Adaptations/PathExportAdaptations", QDir.current().path(), type=str)
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Adaptations', "Select the directory"),
                                                     str(path))
        if directory == "":
            # ---  WORKAROUND FOR MACOS ---
            self.raise_()
            self.activateWindow()
            return
        completed = False
        with gui_exception_context(self, _tr('Adaptations', 'Export adaptations')):
            for adapt_type, adapt_name in types:
                fileName = f"{directory}/{adapt_name}.psa" # pySagra Adaptation
                if QFile.exists(fileName):
                    if QMessageBox.question(
                        self,
                        _tr('MessageDialog', 'Question'),
                        _tr('Adaptations', 'File {0} already exists, overwrite ?').format(fileName),
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

            st.setValue("Adaptations/PathExportAdaptations", directory)
            if completed:
                # ---  WORKAROUND FOR MACOS ---
                self.raise_() 
                self.activateWindow() 
                QMessageBox.information(
                    self,
                    _tr('MessageDialog', 'Information'),
                    _tr('Adaptations', 'Export completed successfully')
                )

    def importAdaptations(self) -> None:
        "Import adaptations from psa files"
        st = QSettings()
        path = st.value("Adaptations/PathExportAdaptations", QDir.current().path(), type=str)
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            caption=_tr('Adaptations', "Select the file name to load"),
            dir=str(path),
            filter= 'pySagra Adaptation File (*.psa);;All files (*.*)'
        )
        if fileName == "":
            return
        with gui_exception_context(self, _tr('Adaptations', 'Import adaptations')):
            with open(fileName, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
                
            for adapt in import_data:
                adp_id = import_adaptation(adapt)
                for setting in adapt.get('settings', []):
                    setting['adaptation_id'] = adp_id
                    import_adaptation_settings(setting)
                
            st.setValue("Adaptations/PathExportAdaptations", path)
            QMessageBox.information(
                self,
                _tr('MessageDialog', 'Information'),
                _tr('Adaptations', 'Import completed successfully')
            )

    def clearAdaptations(self) -> None:
        "Clear current adaptations"
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
                _tr('Adaptations', 'No adaptation type selected')
            )
            return
        if QMessageBox.question(
            self,
            _tr('MessageDialog', 'Question'),
            _tr('Adaptations', 'Adaptations will be cleared, continue ?'),
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No,  # butons
            QMessageBox.StandardButton.No  # default botton
            ) == QMessageBox.StandardButton.No:
            return
        
        with gui_exception_context(self, _tr('Adaptations', "Clear adaptations")):
            for adapt_type in types:
                clear_adaptation(adapt_type)
        
            QMessageBox.information(
                self,
                _tr('MessageDialog', 'Information'),
                _tr('Adaptations', 'Adaptations deleted')
            )

