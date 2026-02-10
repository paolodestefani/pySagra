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
from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App import currentAction
from App.Core.L10n import _tr
from App.Database.Customization import get_itemview_customization
from App.Database.Customization import set_itemview_customize
from App.Database.Customization import set_itemview_customize_setting
from App.Database.Customization import get_sortfilter_customization
from App.Database.Customization import set_sortfilter_customize
from App.Database.Customization import set_sortfilter_customize_setting
from App.Database.Customization import get_report_customization
from App.Database.Customization import set_report_customize
from App.Database.Customization import set_report_customize_setting
from App.Database.Customization import clear_customization
from App.Database.Customization import update_identity

from App.Ui.CustomizationsDialog import Ui_CustomizationsDialog

# logger
logger = logging.getLogger(__name__)


# file name (including extension)
ITEMVIEW = 'itemview.csv'
ITEMVIEWSETTING = 'itemviewssetting.csv'
SORTFILTER = 'sortfilter.csv'
SORTFILTERSETTING = 'sortfiltersetting.csv'
REPORT = 'report.csv'
REPORTSETTING = 'reportsetting.csv'


def customization() -> None:
    logger.info('Starting customization dialog')
    mw = session['mainwin']
    auth = currentAction['sys_customization'].data()
    title = currentAction['sys_customization'].text()
    icon = currentAction['sys_customization'].icon()
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
        "Export customizations to CSV file"
        st = QSettings()
        path = st.value("PathExportCustomizations", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Customizations', "Select the directory"),
                                                     str(path))
        if directory == "":
            return
        try:
            if self.ui.checkBoxItemView.isChecked():
                # looks like zipfile accept qt file path with / so no need to use os.path.join
                fileName = f"{directory}/itemview.ctm.zip"
                with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                    string_buffer = io.StringIO()
                    writer = csv.writer(string_buffer)
                    writer.writerows(get_itemview_customization())
                    zf.writestr('itemview', string_buffer.getvalue())
                    string_buffer = io.StringIO()
                    writer = csv.writer(string_buffer)
                    writer.writerows(get_itemview_customization(True))
                    zf.writestr('itemviewsetting', string_buffer.getvalue())
            if self.ui.checkBoxSortFilter.isChecked():
                # looks like zipfile accept qt file path with / so no need to use os.path.join
                fileName = f"{directory}/sortfilter.ctm.zip"
                with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                    string_buffer = io.StringIO()
                    writer = csv.writer(string_buffer)
                    writer.writerows(get_sortfilter_customization())
                    zf.writestr('sortfilter', string_buffer.getvalue())
                    string_buffer = io.StringIO()
                    writer = csv.writer(string_buffer)
                    writer.writerows(get_sortfilter_customization(True))
                    zf.writestr('sortfiltersetting', string_buffer.getvalue())
            if self.ui.checkBoxReport.isChecked():
                # looks like zipfile accept qt file path with / so no need to use os.path.join
                fileName = f"{directory}/report.ctm.zip"
                with zipfile.ZipFile(fileName, 'w', zipfile.ZIP_DEFLATED) as zf:
                    string_buffer = io.StringIO()
                    writer = csv.writer(string_buffer)
                    writer.writerows(get_report_customization())
                    zf.writestr('report', string_buffer.getvalue())
                    string_buffer = io.StringIO()
                    writer = csv.writer(string_buffer)
                    writer.writerows(get_report_customization(True))
                    zf.writestr('reportsetting', string_buffer.getvalue())
        except Exception as er:
            msg = _tr('Customizations', "Error on saving customizations to file")
            QMessageBox.critical(self,
                                 _tr('Customizations', "Export customizations"),
                                 f"{msg}\n{er}")
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Customizations', 'Export completed successfully'))

    def importCustomization(self) -> None:
        "Import customizations from CSV file"
        st = QSettings()
        path = st.value("PathExportCustomizations", QDir.current().path())
        directory = QFileDialog.getExistingDirectory(self,
                                                     _tr('Customizations', "Select the directory"),
                                                     str(path))
        if directory == "":
            return

        if self.ui.checkBoxItemView.isChecked():
            fileName = f"{directory}/itemview.ctm.zip"
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                string_buffer = io.StringIO(zf.read('itemview').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    set_itemview_customize(row[0], row[1], row[2], row[3])
                string_buffer = io.StringIO(zf.read('itemviewsetting').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    set_itemview_customize_setting(row[0], row[1], row[2], row[3], row[4])
        if self.ui.checkBoxSortFilter.isChecked():
            fileName = f"{directory}/sortfilter.ctm.zip"
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                string_buffer = io.StringIO(zf.read('sortfilter').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    set_sortfilter_customize(row[0], row[1], row[2], row[3])
                string_buffer = io.StringIO(zf.read('sortfiltersetting').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    set_sortfilter_customize_setting(row[0], row[1], row[2], row[3], row[4], row[5])
        if self.ui.checkBoxReport.isChecked():
            fileName = f"{directory}/report.ctm.zip"
            with zipfile.ZipFile(fileName, 'r', zipfile.ZIP_DEFLATED) as zf:
                string_buffer = io.StringIO(zf.read('report').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    rid = int(row[0])
                    report_code = row[1]
                    description = row[2]
                    class_sorting = int(row[3])
                    set_report_customize(rid, report_code, description, class_sorting)
                string_buffer = io.StringIO(zf.read('reportsetting').decode('utf-8'))
                reader = csv.reader(string_buffer)
                for row in reader:
                    customize_id = int(row[0])
                    customize_type = row[1]
                    layout_row = int(row[2])
                    if row[3]:
                        combo1_index = int(row[3])
                    else:
                        combo1_index = None
                    if row[4]:
                        combo2_index = int(row[4])
                    else:
                        combo2_index = None
                    widget_value = row[5]
                    set_report_customize_setting(customize_id,
                                                 customize_type,
                                                 layout_row,
                                                 combo1_index,
                                                 combo2_index,
                                                 widget_value)
        # update identity on all tables
        update_identity()
        # everything is ok
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
        if self.ui.checkBoxItemView.isChecked():
            clear_customization('I')
        if self.ui.checkBoxSortFilter.isChecked():
            clear_customization('S')
        if self.ui.checkBoxReport.isChecked():
            clear_customization('R')
        # completed
        QMessageBox.information(self,
                                _tr('MessageDialog', 'Information'),
                                _tr('Customizations', 'Customizations deleted'))

    def accept(self) -> None:
        QDialog.accept(self)
