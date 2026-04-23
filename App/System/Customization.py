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

This module allow import/export of report, itemview and sort-filter customizations


"""

# standard library
import os
import csv
import io
import zipfile
import logging

# PySide6
from PySide6.QtCore import QDir
from PySide6.QtCore import QFileInfo
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDialogButtonBox

# application modules
from App import session
from App import currentAction
from App.Core.L10n import _tr
# from App.Database.Customization import get_itemview_adapt
# from App.Database.Customization import set_itemview_adapt
# from App.Database.Customization import set_itemview_adapt_setting
# from App.Database.Customization import get_sortfilter_adapt
# from App.Database.Customization import set_sortfilter_adapt
# from App.Database.Customization import set_sortfilter_adapt_setting
# from App.Database.Customization import get_report_adapt
#from App.Database.Customization import set_report_adapt
#from App.Database.Customization import set_report_adapt_setting
#from App.Database.Customization import clear_adapt
#from App.Database.Customization import update_identity
from App.Database.Adaptation import set_adapt_setting
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


def customization() -> None:
    logger.info('Starting customization dialog')
    mw = session['mainwin']
    title = currentAction['sys_customization'].text()
    icon = currentAction['sys_customization'].icon()
    auth = currentAction['sys_customization'].data()
    dialog = CustomizationsDialog(mw, title, icon, auth)
    dialog.show()
    logger.info('Customization dialog shown')


class CustomizationsDialog(QDialog):
    "Customizations dialog"

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
        "Export customizations to a zipped CSV files - *.psa"
        st = QSettings()
        path = st.value("ExportAdaptationsFile", QDir.current().path(), type=str)
        fileName, filter = QFileDialog.getSaveFileName(self,
                                                       caption=_tr('Customizations', "Select the file name to create"),
                                                       dir=str(path),
                                                       filter= 'pySagra Adapt File (*.psa)',
                                                       options=QFileDialog.Option.DontUseNativeDialog )
        if fileName == "":
            return
        try:
            # looks like zipfile accept qt file path with / so no need to use os.path.join
            with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                # version
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                writer.writerow(ADAPTVERSION)
                zf.writestr('version', string_buffer.getvalue())
                # adaptation system
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                if self.ui.checkBoxSystem.isChecked():
                    writer.writerows(export_adaptation(system=True ))
                zf.writestr('adaptation_system', string_buffer.getvalue())
                # adaptation non-system
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                if self.ui.checkBoxNonSystem.isChecked():
                    writer.writerows(export_adaptation(system=False))
                zf.writestr('adaptation_non_system', string_buffer.getvalue())
                # adaptation setting system
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                if self.ui.checkBoxSystem.isChecked():
                    writer.writerows(export_adaptation_setting(system=True))
                zf.writestr('adaptationsetting_system', string_buffer.getvalue())
                # adaptation setting non-system
                string_buffer = io.StringIO()
                writer = csv.writer(string_buffer)
                if self.ui.checkBoxNonSystem.isChecked():
                    writer.writerows(export_adaptation_setting(system=False))
                zf.writestr('adaptationsetting_non_system', string_buffer.getvalue())
        except Exception as er:
            msg = _tr('Customizations', "Error on saving customizations to file")
            MessageBoxCritical(self,
                               _tr('Customizations', "Export customizations"),
                               f"{msg}\n{er}")
        else:
            st.setValue("ExportAdaptationsFile", fileName)
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Customizations', 'Export completed successfully'))

    def importCustomization(self) -> None:
        "Import customizations from a zipped CSV files - *.psa"
        st = QSettings()
        path = st.value("ExportAdaptationsFile", QDir.current().path(), type=str)
        fileName, filter = QFileDialog.getOpenFileName(self,
                                                       caption=_tr('Customizations', "Select the file name to load"),
                                                       dir=str(path),
                                                       filter= 'pySagra Adapt File (*.psa *.*)')
        if fileName == "":
            return
        try:
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
                filea, files = [], []
                if self.ui.checkBoxSystem.isChecked():
                    clear_adaptation(system=True)
                    filea.append('adaptation_system')
                    files.append('adaptationsetting_system')
                if self.ui.checkBoxNonSystem.isChecked():
                    clear_adaptation(system=False)
                    filea.append('adaptation_non_system')
                    files.append('adaptationsetting_non_system')
                for f in filea:
                    # adaptation
                    string_buffer = io.StringIO(zf.read(f).decode('utf-8'))
                    reader = csv.reader(string_buffer)
                    for row in reader:
                        adaptations.append((
                                        int(row[0]),                # id
                                        row[1],                     # type
                                        row[2],                     # class
                                        row[3],                     # description
                                        int(row[4]),                # class sorting
                                        decodebool(row[5]),         # class default
                                        int(row[6]) if row[6] else None, # report id
                                        int(row[7]) if row[7] else None, # row count limit
                                        ))
                for f in files:
                    # adaptation setting
                    string_buffer = io.StringIO(zf.read(f).decode('utf-8'))
                    reader = csv.reader(string_buffer)
                    for row in reader:
                        adaptsettings.append((
                                        int(row[0]),                # setting id
                                        int(row[1]),                # adapt id
                                        int(row[2]) if row[2] else None, # column
                                        int(row[3]) if row[3] else None, # sorting
                                        decodebool(row[4]),         # is visible
                                        int(row[5]) if row[5] else None, # size
                                        row[6] or None,             # element type
                                        int(row[7]) if row[7] else None, # layout row
                                        int(row[8]) if row[8] else None, # combo1 index
                                        decodebool(row[9]),         # negate
                                        int(row[10]) if row[10] else None, # combo2 index
                                        row[11] or None             # widget value
                                        ))
            import_adaptation(adaptations, adaptsettings)
        except Exception as er:
            msg = _tr('Customizations', "Error on reading customizations from file")
            #print(er, er.__cause__, er.__context__, er.__traceback__)
            MessageBoxCritical(self,
                               _tr('Customizations', "Import customizations"),
                               f"{msg}\n{er}")
        else:
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
        if self.ui.checkBoxSystem.isChecked():
            clear_adaptation(system=True)
        if self.ui.checkBoxNonSystem.isChecked():
            clear_adaptation(system=False)
        # completed
        QMessageBox.information(self,
                                _tr('MessageDialog', 'Information'),
                                _tr('Customizations', 'Customizations deleted'))

