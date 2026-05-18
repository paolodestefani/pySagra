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

"""Statistics

This module provide a print statistic launcher


"""

# standard library
import logging
import csv
import decimal

# pandas
#import pandas as pd

# PySide6
#from PySide6.QtCore import QObject
from PySide6.QtCore import QSettings
from PySide6.QtCore import QDir
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtWidgets import QDialogButtonBox

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Database.AbstractModels.TableModel import PandasModel
from App.Database.Lookup import event_lookup
from App.Database.Models import OrderHeaderPandasModel
from App.Database.Models import OrderLinePandasModel
from App.Ui.AnalysisWidget import Ui_AnalysisWidget
from App.Ui.StatisticsExportDialog import Ui_StatisticsExportDialog
from App.Widget.Dialog import PrintDialog
#from App.Widget.Delegate import PandasDelegate
from App.Core.L10n import _tr


def statisticsAnalysis(action: QAction, checked: bool = False) -> None:
    "Statistical analysis"
    logging.info('Starting Statistical Analysis')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    af = AnalysisForm(mw, title, auth)
    mw.addTab(title, af)
    logging.info('Statistical Analysis added to main window')


def statisticsPrint(action: QAction, checked: bool = False) -> None:
    "Print statistic reports"
    logging.info('Starting statistics consumption dialog')
    mw = session['mainwin']
    dialog = PrintDialog(mw, 'STATISTICS')
    dialog.show()
    logging.info('Statistics consumption dialog shown')


def statisticsExport(action: QAction, checked: bool = False) -> None:
    "Statistics export"
    logging.info('Starting statistics export dialog')
    mw = session['mainwin']
    title = action.text()
    auth = action.data()
    icon = action.icon()
    dlg = StatisticsExportDialog(mw, title, icon, auth)
    dlg.exec_()
    logging.info('Statistics  export dialog shown')


class StatisticsExportDialog(QDialog):

    def __init__(self, parent, title, icon, auth):
        super().__init__(parent)
        self.ui = Ui_StatisticsExportDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelIcon.setPixmap(icon.pixmap(128))
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setDefault(True)

        for i, d in event_lookup():
            self.ui.comboBoxFromEvent.addItem(d, i)
            self.ui.comboBoxToEvent.addItem(d, i)
        # restore settings
        st = QSettings(self)
        if st.value("StatisticsExport/Geometry"):
            self.restoreGeometry(st.value("StatisticsExport/Geometry"))
        self.ui.lineEditHeadersFileName.setText(st.value("StatisticsExport/HeadersFileName", ""))
        self.ui.lineEditDetailsFileName.setText(st.value("StatisticsExport/DetailsFileName", ""))
        self.ui.checkBoxIncludeAll.setChecked(st.value("StatisticsExport/IncludeAll", 'false') == 'true')
        self.ui.comboBoxFromEvent.setCurrentIndex(int(st.value("StatisticsExport/FromEvent", '1')))
        self.ui.comboBoxToEvent.setCurrentIndex(int(st.value("StatisticsExport/ToEvent", '1')))
        # signal slot connections
        self.ui.checkBoxIncludeAll.toggled.connect(self.includeAllEvents)
        self.ui.pushButtonSelectHeaders.clicked.connect(self.selectHeadersClicked)
        self.ui.pushButtonSelectDetails.clicked.connect(self.selectDetailsClicked)

    def includeAllEvents(self, checked):
        if checked:
            self.ui.comboBoxFromEvent.setCurrentIndex(-1)
            self.ui.groupBoxFromEvent.setDisabled(True)
            self.ui.comboBoxToEvent.setCurrentIndex(-1)
            self.ui.groupBoxToEvent.setDisabled(True)
        else:
            self.ui.groupBoxFromEvent.setEnabled(True)
            self.ui.groupBoxToEvent.setEnabled(True)

    def selectHeadersClicked(self):
        if self.ui.lineEditHeadersFileName.text():
            path = self.ui.lineEditHeadersFileName.text()
        else:
            path = QDir.currentPath()
        fname, t = QFileDialog.getSaveFileName(self,
                                               _tr("View", "Select file name and path"),
                                               path,
                                               _tr("View", "Comma separated values (*.csv);;All files (*.*)"))
        if not fname: # clicked cancel
            return
        self.ui.lineEditHeadersFileName.setText(fname)
        # save export path
        st = QSettings()
        st.setValue("StatisticsExport/HeadersFileName", fname)

    def selectDetailsClicked(self):
        if self.ui.lineEditDetailsFileName.text():
            path = self.ui.lineEditDetailsFileName.text()
        else:
            path = QDir.currentPath()
        fname, t = QFileDialog.getSaveFileName(self,
                                               _tr("View", "Select file name and path"),
                                               path,
                                               _tr("View", "Comma separated values (*.csv);;All files (*.*)"))
        if not fname: # clicked cancel
            return
        self.ui.lineEditDetailsFileName.setText(fname)
        # save export path
        st = QSettings()
        st.setValue("StatisticsExport/DetailsFileName", fname)

    def accept(self):
        "Proceed on export data"
        if self.ui.checkBoxIncludeAll.isChecked():
            fromEvent = 1
            toEvent = 999999
        else:
            fromEvent = int(self.ui.comboBoxFromEvent.currentData())
            toEvent = int(self.ui.comboBoxToEvent.currentData())
        fnameh = self.ui.lineEditHeadersFileName.text()
        fnamed = self.ui.lineEditDetailsFileName.text()
        try:
            for view, fn in (('bi_order_header', fnameh), ('bi_order_detail', fnamed)):
                # write to csv file
                with open(fn, 'w', encoding="utf-8", newline='') as f:
                    writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    for r in load_statistic_bi_data(view, fromEvent, toEvent):
                        row = []
                        for c in r:
                            if isinstance(c, QByteArray):
                                data = 'BINARY DATA'
                            elif isinstance(c, QDate):
                                data = c.toString(Qt.DefaultLocaleShortDate)
                            elif isinstance(c, QDateTime):
                                data = c.toString(Qt.DefaultLocaleShortDate)
                            elif isinstance(c, QTime):
                                data = c.toString(Qt.DefaultLocaleShortDate)
                            elif isinstance(c, bool):
                                #data = "\u2611" if data else "\u2610" # tick
                                data = "I" if c else "O" # less problem with excel
                            elif isinstance(c, (float, decimal.Decimal)):
                                data = str(c).replace(".", ",")
                            elif c is None:
                                data = ''
                            else:
                                data = str(c)
                            row.append(data)
                        writer.writerow(row)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', 'Critical'),
                                 f"Database error: {er.code}\n{er.message}")
        else:
            QMessageBox.information(self,
                                    _tr('MessageDialog', 'Information'),
                                    _tr('Utility', 'Operation completed successfully'))
        # save settings
        st = QSettings()
        st.setValue("StatisticsExport/IncludeAll", self.checkBoxIncludeAll.isChecked())
        st.setValue("StatisticsExport/FromEvent", self.comboBoxFromEvent.currentIndex())
        st.setValue("StatisticsExport/ToEvent", self.comboBoxToEvent.currentIndex())
        super().accept()

# def format_number(x):
#     """
#     Formats a number with . as thousand separators.
#     """
#     return f"{x:,.2f}".replace(",", "*").replace(".", ",").replace("*", ".")

class AnalysisForm(QWidget):

    def __init__(self, parent: QWidget, title: str, auth: str) -> None:
        super().__init__(parent)
        self.model: PandasModel|None = None
        self.tabName = title
        self.helpLink = None
        # available edit status
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False, False, False, False, False, False, False, False,
                                False, False, False, False)
        self.ui = Ui_AnalysisWidget()
        self.ui.setupUi(self)
        self.ui.tableView.setItemDelegate(QStyledItemDelegate(self))
        # select Analysis
        self.ui.comboBoxAnalysis.addItems(['',
                                           _tr("Statistics", "Order header analysis"),
                                           _tr("Statistics", "Order lines analysis")])
        # signal slot connections
        self.ui.comboBoxAnalysis.currentIndexChanged.connect(self.changeAnalysis)
        self.ui.pushButtonShowApply.clicked.connect(self.showApplyOptions)
        # fill comboboxes for functions and sorting, not depending on dataframe
        for f in (self.ui.comboBoxFunction1,
                  self.ui.comboBoxFunction2):
            for i, j in [('', ''),
                         (_tr('Statistics', 'Sum'), 'sum'),
                         (_tr('Statistics', 'Count'), 'count'),
                         (_tr('Statistics', 'Average'), 'mean'),
                         (_tr('Statistics', 'Median'), 'median'),
                         (_tr('Statistics', 'Min'), 'min'),
                         (_tr('Statistics', 'Max'), 'max'),
                         (_tr('Statistics', 'Standard Deviation'), 'std'),
                         (_tr('Statistics', 'Variance'), 'var')]:
                f.addItem(i, j)
        for c in (self.ui.comboBoxSort1, self.ui.comboBoxSort2):
            for i, j in [('', ''), # type: ignore
                         (_tr('Statistics', 'Ascending'), True),
                         (_tr('Statistics', 'Descending'), False)]:
                c.addItem(i, j)
                
    def changeAnalysis(self, index: int) -> None:
        "Change analysis type"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        match index:
            case 1:
                self.model = OrderHeaderPandasModel()
                self.model.select()
            case 2:
                self.model = OrderLinePandasModel()
                self.model.select()
            case _:
                self.model = None
                logging.info("No analysis selected")
        # cursor restore
        QGuiApplication.restoreOverrideCursor()
        # events filter
        self.ui.comboBoxEvent.clear()
        if self.model and hasattr(self.model, 'getEvents'):
            self.ui.comboBoxEvent.addItems([''] + self.model.getEvents())
        # assign columns to comboboxes
        for c in (self.ui.comboBoxColumn1,
                  self.ui.comboBoxColumn2,
                  self.ui.comboBoxColumn3,
                  self.ui.comboBoxRow1,
                  self.ui.comboBoxRow2,
                  self.ui.comboBoxRow3,
                  self.ui.comboBoxRow4,
                  self.ui.comboBoxRow5,
                  self.ui.comboBoxRow6,
                  self.ui.comboBoxRow7):
            c.clear()
            if self.model and hasattr(self.model, 'columns'):
                c.addItems([''] + [i[0] for i in self.model.columns.values() if i[2]])
        # values comboboxes
        for v in (self.ui.comboBoxValue1,
                  self.ui.comboBoxValue2):
            v.clear()
            if self.model and hasattr(self.model, 'columns'):
                v.addItems([''] + [i[0] for i in self.model.columns.values() if i[1]])
        
    def showApplyOptions(self):
        if self.ui.groupBoxValues.isVisible():
            self.ui.groupBoxValues.setVisible(False)
            self.ui.groupBoxRow.setVisible(False)
            self.ui.groupBoxColumn.setVisible(False)
            self.ui.pushButtonShowApply.setText(_tr("Statistics", "Show options"))
            # filter by event first
            if self.ui.comboBoxEvent.currentText() != '':
                self.model.filterEvent(self.ui.comboBoxEvent.currentText())
            # filter by index
            for c, l in ((self.ui.comboBoxRow1, self.ui.lineEditRow1),
                         (self.ui.comboBoxRow2, self.ui.lineEditRow2),
                         (self.ui.comboBoxRow3, self.ui.lineEditRow3),
                         (self.ui.comboBoxRow4, self.ui.lineEditRow4),
                         (self.ui.comboBoxRow5, self.ui.lineEditRow5),
                         (self.ui.comboBoxRow6, self.ui.lineEditRow6),
                         (self.ui.comboBoxRow7, self.ui.lineEditRow7)):
                if c.currentText() != '':
                    self.model.filterLike(c.currentText(), l.text())
            # filter by columns
            for c, l in ((self.ui.comboBoxColumn1, self.ui.lineEditColumn1),
                         (self.ui.comboBoxColumn2, self.ui.lineEditColumn2),
                         (self.ui.comboBoxColumn3, self.ui.lineEditColumn3)):
                if c.currentText() != '':
                    self.model.filterLike(c.currentText(), l.text())
            # get selected values and aggregations
            values = []
            aggfunc = {}
            if self.ui.comboBoxValue1.currentText() != '':
                values.append(self.ui.comboBoxValue1.currentText())
                if self.ui.comboBoxFunction1.currentData() != '':
                    aggfunc[self.ui.comboBoxValue1.currentText()] = self.ui.comboBoxFunction1.currentData()
            if self.ui.comboBoxValue2.currentText() != '':
                values.append(self.ui.comboBoxValue2.currentText())
                if self.ui.comboBoxFunction2.currentData() != '':
                    aggfunc[self.ui.comboBoxValue2.currentText()] = self.ui.comboBoxFunction2.currentData()

            if not values or not aggfunc or len(values) != len(aggfunc):
                QMessageBox.warning(self,
                                    _tr("Statistics", "Warning"),
                                    _tr("Statistics", "At least one value must be selected"))
                return
            # get selected rows
            rows = []
            for r in (self.ui.comboBoxRow1,
                      self.ui.comboBoxRow2,
                      self.ui.comboBoxRow3,
                      self.ui.comboBoxRow4,
                      self.ui.comboBoxRow5,
                      self.ui.comboBoxRow6,
                      self.ui.comboBoxRow7):
                if r.currentText() != '':
                    rows.append(r.currentText())
            if not rows:
                QMessageBox.warning(self,
                                    _tr("Statistics", "Warning"),
                                    _tr("Statistics", "At least one row must be selected"))
                return
            # get selected columns
            columns = []
            for c in (self.ui.comboBoxColumn1,
                      self.ui.comboBoxColumn2,
                      self.ui.comboBoxColumn3):
                if c.currentText() != '':
                    columns.append(c.currentText())
            # totals
            t = self.ui.checkBoxTotal.isChecked()
            # create pivot table
            self.model.createPivot(rows, columns, values, aggfunc, t)
            # pivot = pd.pivot_table(df,
            #                         index=rows,
            #                         columns=columns,
            #                         values=values,
            #                         aggfunc=aggfunc,
            #                         fill_value=0.0,
            #                         margins=False,
            #                         margins_name='Totale Generale')
            #logging.info(f"Pivot table created with {len(pivot)} rows and {len(pivot.columns)} columns")
            # sorting
            # if self.ui.comboBoxValue1.currentText() != '':
            #     if self.ui.comboBoxSort1.currentData() != '':
            #         pivot = pivot.sort_values(by=[self.ui.comboBoxValue1.currentText()], ascending=self.ui.comboBoxSort1.currentData())
            # if self.ui.comboBoxValue2.currentText() != '':
            #     if self.ui.comboBoxSort2.currentData() != '':
            #         pivot = pivot.sort_values(by=[self.ui.comboBoxValue2.currentText()], ascending=self.ui.comboBoxSort2.currentData())
            # display pivot table
            #print('Index:', pivot.index.names, 'Columns:', pivot.columns)
            #model = PandasModel(pivot)
            self.ui.tableView.setModel(self.model)   
            # set span for aggregated rows
            agg = len(rows)
            rc = self.model.rowCount()
            # set span
            #self.ui.tableView.clearSpans()
            # for c in range(agg): # for each aggregated column
            #     rowStart, rowCount = 0, 1
            #     for i in range(rc):
            #         if self.model.index(i, c).data() == self.model.index(i + 1, c).data():
            #             rowCount += 1
            #         else:
            #             if rowCount > 1: # set span only if more than one row
            #                 self.ui.tableView.setSpan(rowStart, c, rowCount, 1)
            #             rowStart = i + 1
            #             rowCount = 1
            
            logging.info("Pivot table displayed in analysis widget")
        else:
            self.ui.groupBoxValues.setVisible(True)
            self.ui.groupBoxRow.setVisible(True)
            self.ui.groupBoxColumn.setVisible(True)
            self.ui.pushButtonShowApply.setText(_tr("Statistics", "Apply/Refresh"))