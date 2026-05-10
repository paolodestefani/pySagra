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

"""Views

This module contains general custom views


"""

# standard library
import os
import csv
from typing import Any

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QUrl
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QLocale
from PySide6.QtCore import QPoint
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QTimer

from PySide6.QtGui import QDropEvent
from PySide6.QtGui import QDesktopServices
from PySide6.QtGui import QCursor
from PySide6.QtGui import QContextMenuEvent

from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtGui import QAction
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App import currentIcon
from App.Core.L10n import _tr
from App.Database.Exceptions import PyAppDBError
from App.Database.Adaptation import list_adaptation
from App.Database.Adaptation import create_adaptation
from App.Database.Adaptation import get_view_columns
from App.Database.Adaptation import set_adapt_setting
from App.Database.Adaptation import delete_adaptation
from App.Database.Adaptation import set_adapt_class_default
from App.Database.Adaptation import set_adapt_user_default
from App.Database.Adaptation import get_adapt_default
from App.Database.Adaptation import is_system_object
from App.Widget.Delegate import GenericReadOnlyDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import HideTextDelegate
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Delegate import IntegerDelegate
from App.Widget.TableWidget import TableWidgetItem
from App.Widget.Dialog import MessageBoxCritical

from App.Ui.ViewSettingsDialog import Ui_ViewSettingsDialog



class TableViewSettingsDialog(QDialog):

    def __init__(self, parent: EnhancedTableView) -> None:
        super().__init__(parent)
        self._parent = parent
        self.ui = Ui_ViewSettingsDialog()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setItemDelegateForColumn(3, BooleanDelegate(self))
        self.ui.tableWidget.setItemDelegateForColumn(4, IntegerDelegate(self))
        self.ui.tableWidget.setHorizontalHeaderLabels([_tr('View', 'Field index'),
                                                       _tr('View', 'Field'),
                                                       _tr('View', 'Sorting'),
                                                       _tr('View', 'Visible'),
                                                       _tr('View', 'Width')])
        self.ui.tableWidget.verticalHeader().setVisible(True)
        self.ui.tableWidget.setRowCount(parent.model().columnCount())
        for i in range(parent.horizontalHeader().count()):
            self.ui.tableWidget.setItem(i, 0, TableWidgetItem(i))
            self.ui.tableWidget.setItem(i, 1, TableWidgetItem(parent.model().headerData(i, Qt.Orientation.Horizontal)))  # header
            self.ui.tableWidget.setItem(i, 2, TableWidgetItem(parent.horizontalHeader().visualIndex(i)))
            self.ui.tableWidget.setItem(i, 3, TableWidgetItem(not parent.isColumnHidden(i)))
            self.ui.tableWidget.setItem(i, 4, TableWidgetItem(parent.columnWidth(i)))
        self.ui.tableWidget.sortItems(2, Qt.SortOrder.AscendingOrder)
        self.ui.tableWidget.horizontalHeader().hideSection(0)
        self.ui.tableWidget.horizontalHeader().hideSection(2)
        self.ui.tableWidget.resizeColumnToContents(1)
        # set flags for drag and drop and item selection
        for r in range(parent.horizontalHeader().count()):
            for c in range(5):
                if c in (0, 1, 2):
                    self.ui.tableWidget.item(r, c).setFlags(Qt.ItemFlag.ItemIsEnabled|
                                                            Qt.ItemFlag.ItemIsSelectable|
                                                            Qt.ItemFlag.ItemIsDragEnabled|
                                                            Qt.ItemFlag.ItemIsDropEnabled)
        # set readonly for field name
        self.ui.tableWidget.setItemDelegateForColumn(1, GenericReadOnlyDelegate(self))

    def accept(self) -> None:
        # reset layout first (first time store the state)
        if self._parent.horizontalHeaderState:
            self._parent.horizontalHeader().restoreState(self._parent.horizontalHeaderState)
        else:
            self._parent.horizontalHeaderState = self._parent.horizontalHeader().saveState()

        header = self._parent.horizontalHeader()
        # avoid table redraw while updating layout
        header.blockSignals(True)
        
        def get_val(row: int, col: int) -> Any:
            item = self.ui.tableWidget.item(row, col)
            # Prendi l'EditRole (dato fresco dal delegate) 
            # o il DisplayRole (dato iniziale) se l'EditRole è None
            v = item.data(Qt.ItemDataRole.EditRole)
            return v if v is not None else item.data(Qt.ItemDataRole.DisplayRole)

        try:
            for r in range(self.ui.tableWidget.rowCount()):
                # Ora il codice è di nuovo pulitissimo!
                logical_idx = int(get_val(r, 0))
                visible = bool(get_val(r, 3))
                width = int(get_val(r, 4))

                # Applicazione layout (con visualIndex per evitare l'effetto domino)
                current_visual = header.visualIndex(logical_idx)
                header.moveSection(current_visual, r)
                
                self._parent.setColumnHidden(logical_idx, not visible)
                if visible:
                    self._parent.setColumnWidth(logical_idx, width)
        finally:
            # 2. Sblocca e forza un aggiornamento finale pulito
            header.blockSignals(False)
            header.viewport().update()
            
        super().accept()
        

class EnhancedTableView(QTableView):
    "Generic (but enhanced :-) ) table View"

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.layoutName: str|None = None
        #fw = QApplication.fontMetrics().averageCharWidth()
        # good defaults
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.SelectedClicked)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.verticalHeader().hide()
        self.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalHeader().setSectionsMovable(False)
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignVCenter)
        # default item delegate for all column
        self.setItemDelegate(GenericReadOnlyDelegate(self))
        # state of the horizontal header, used for reset
        self.horizontalHeaderState: QByteArray|None = None
        # CONTEXT MENU ACTIONS
        # activate/deactivate column sorting
        self.cmSorting = QAction(_tr("View", "Column sorting"), self)
        self.cmSorting.setCheckable(True)
        self.cmSorting.setChecked(False)
        self.cmSorting.triggered.connect(self.activateSorting)
        # activate/deactivate column movable
        self.cmMovable = QAction(_tr("View", "Column movable"), self)
        self.cmMovable.setCheckable(True)
        self.cmMovable.setChecked(False)
        self.cmMovable.triggered.connect(self.activateMovableColumns)
        # show vertical header
        self.cmVHeader = QAction(_tr("View", "Show vertical header"), self)
        self.cmVHeader.setCheckable(True)
        self.cmVHeader.setChecked(False)
        self.cmVHeader.triggered.connect(self.showVerticalHeader)
        # resize columns to content
        self.cmResizeColsToContent = QAction(_tr("View", "Resize columns to contents"), self)
        self.cmResizeColsToContent.setCheckable(False)
        self.cmResizeColsToContent.triggered.connect(self.resizeColumnsToContents)
        # resize rows to content
        self.cmResizeRowsToContent = QAction(_tr("View", "Resize rows to contents"), self)
        self.cmResizeRowsToContent.setCheckable(False)
        self.cmResizeRowsToContent.triggered.connect(self.resizeRowsToContents)
        # export to CSV file
        self.cmExport = QAction(_tr("View", "Export to CSV file"), self)
        self.cmExport.triggered.connect(self.exportView)
        # set as user default current view layout
        self.cmUserDefault = QAction(_tr("View", "Set current layout as user default"), self)
        self.cmUserDefault.triggered.connect(self.setUserDefaultLayout)
        # layout customizations
        self.cmCustomizations = QMenu(_tr("View", "Set layout"), self)
        self.ag = QActionGroup(self)
        # customizations are inserted in a separate method after name assignement
        self.ag.triggered.connect(self.setStoredLayout)
        if session['can_edit_views']:
            # update customization
            self.cmUpdateLayout = QAction(_tr("View", "Update current layout"), self)
            self.cmUpdateLayout.triggered.connect(self.updateViewLayout)
            # delete view layout
            self.cmDelete = QAction(_tr("View", "Delete current layout"), self)
            self.cmDelete.triggered.connect(self.deleteViewLayout)
            # set as class default current view layout
            self.cmClassDefault = QAction(_tr("View", "Set current layout as class default"), self)
            self.cmClassDefault.triggered.connect(self.setClassDefaultLayout)
            # save customization as
            self.cmSaveLayout = QAction(_tr("View", "Save current layout as ..."), self)
            self.cmSaveLayout.triggered.connect(self.saveViewLayoutAs)
            # hide current column
            self.cmHide = QAction(_tr("View", "Hide current column"), self)
            self.cmHide.triggered.connect(self.hideCurrentColumn)
            # show all view columns
            self.cmShow = QAction(_tr("View", "Show all columns"), self)
            self.cmShow.triggered.connect(self.showAllColumns)
            # reset view state
            self.cmReset = QAction(_tr("View", "Reset view state"), self)
            self.cmReset.triggered.connect(self.resetViewState)
            # manage view settings
            self.cmManage = QAction(_tr("View", "Manage settings"), self)
            self.cmManage.triggered.connect(self.manageSettings)
        # add actions to context menu
        self.cm = QMenu(self)
        self.cm.addActions([self.cmSorting,
                            self.cmMovable,
                            self.cmVHeader])
        self.cm.addSeparator()
        self.cm.addActions([self.cmResizeColsToContent,
                            self.cmResizeRowsToContent])
        self.cm.addSeparator()
        self.cm.addActions([self.cmExport]) #, self.cmPrint])
        self.cm.addSeparator()
        self.cm.addMenu(self.cmCustomizations)
        self.cm.addAction(self.cmUserDefault)
        self.cm.addSeparator()
        if session['can_edit_views']:
            self.cm.addActions([self.cmUpdateLayout,
                                self.cmDelete,
                                self.cmClassDefault,
                                self.cmSaveLayout])
            self.cm.addSeparator()
            self.cm.addActions([self.cmHide, self.cmShow, self.cmReset, self.cmManage])
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def fillCustomizationMenu(self) -> None:
        if not self.layoutName:
            return
        # clear everything
        for i in self.ag.actions():
            self.ag.removeAction(i)
        self.cmCustomizations.clear()
        # create actions and menu
        try:
            result = list_adaptation('I', self.layoutName)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
            return
        for i, d, c in result:
            a = QAction(d, self)
            a.setCheckable(True)
            a.setData(str(i))
            if c:
                a.setChecked(True)
            self.ag.addAction(a)
            self.cmCustomizations.addAction(a)
        # initial default layout
        dl = get_adapt_default('I', self.layoutName, session['user'])
        for a in self.ag.actions():
            if a.data() == str(dl):
                a.setChecked(True)

    def setModel(self, model: QAbstractItemModel|None) -> None:
        super().setModel(model)
        self.setSortingEnabled(False) # better not to sort when editing
        self.horizontalHeader().setSectionsMovable(False) # better not to move when editing

    def setLayoutName(self, name: str) -> None:
        # As EnhancedTableView is declared in QtDesigner we must set the name of the layout after instantiation
        # in the widget definition in order to load the correct customizations
        self.layoutName = name
        self.fillCustomizationMenu()
        target_action = self.ag.checkedAction() # pyside6 requirement... 
        QTimer.singleShot(0, lambda: self.setStoredLayout(target_action))

    def setStoredLayout(self, action: QAction) -> None:
        if not action: # no customization available
            return
        viewId = int(action.data())
        # reset layout first (first time store the state)
        if self.horizontalHeaderState:
            self.horizontalHeader().restoreState(self.horizontalHeaderState)
        else:
            self.horizontalHeaderState = self.horizontalHeader().saveState()
        # set columns implementation: column, sorting index, visible, size
        try:
            result = get_view_columns(viewId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
            return
        
        self.setSortingEnabled(False)
        header = self.horizontalHeader()
        for c, i, v, s in result:
            # check if column exists
            if c >= header.count():
                continue
            # show/hide
            self.setColumnHidden(c, not v)
            # width
            if v and s > 0:
                self.setColumnWidth(c, s)
            # set position
            ci = header.visualIndex(c)
            if ci != i:
                header.moveSection(ci, i)
        
    def showContextMenu(self, pos) -> None:
        self.cm.exec(self.mapToGlobal(pos))

    def activateSorting(self) -> None:
        "Activate/deactivate sorting by column"
        if self.isSortingEnabled():
            self.setSortingEnabled(False)
            self.cmSorting.setChecked(False)
        else:
            self.setSortingEnabled(True)
            self.cmSorting.setChecked(True)

    def activateMovableColumns(self) -> None:
        "Activate/deactivate movable columns"
        if self.horizontalHeader().sectionsMovable():
            self.horizontalHeader().setSectionsMovable(False)
            self.cmMovable.setChecked(False)
        else:
            self.horizontalHeader().setSectionsMovable(True)
            self.cmMovable.setChecked(True)

    def showVerticalHeader(self) -> None:
        if self.verticalHeader().isVisible():
            self.verticalHeader().hide()
        else:
            self.verticalHeader().show()

    def add(self) -> int:
        "Insert a row in grid at the end"
        row = self.model().rowCount()
        success = self.model().insertRow(row)
        #index = self.model().createIndex(row, 0)
        index = self.model().index(row, 0)
        self.scrollTo(index)
        self.setCurrentIndex(index)
        #self.edit(index)
        return row
    # def add(self) -> int:
    #     "Insert a row in grid at the end"
    #     model = self.model()
    #     row = model.rowCount()
        
    #     if model.insertRow(row):
    #         # Recuperiamo l'indice corretto dal modello
    #         index = model.index(row, 0)
            
    #         self.scrollTo(index)
    #         self.setCurrentIndex(index)
            
    #         # Aspettiamo il prossimo ciclo di eventi per avviare l'editing
    #         QTimer.singleShot(0, lambda: self.edit(index))
            
    #     return row

    def remove(self) -> None:
        "Delete the current row"
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                _tr("View", "Are you sure to delete the selected row ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return
        index = self.currentIndex()
        if not index.isValid():
            return
        if not self.model().removeRows(index.row(), 1, parent=QModelIndex()):
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 _tr("View", "Error deleting row"))

    def exportView(self) -> None:
        "Export to CSV file"
        # read previously used path
        st = QSettings()
        if st.value("ExportPath") is not None:
            path = st.value("ExportPath")
        else:
            path = os.getcwd()
        # parameters
        model = self.model()
        rows = model.rowCount()
        columns = model.columnCount()
        # select file to save
        fname, t = QFileDialog.getSaveFileName(self,
                                               _tr("View", "Select file name and path"),
                                               path,
                                               _tr("View", "Comma separated values (*.csv);;All files (*.*)"))
        if not fname: # clicked cancel
            return
        # check access rights
        try:
            open(fname, 'w')
        except Exception as er:
            QMessageBox.critical(self,
                                 _tr('MessageDialog', "Critical"),
                                 _tr('View', "Unable to write to filename: {}".format(fname)))
            return
        # write to csv file
        with open(fname, 'w', encoding="utf-8", newline='') as f:
            writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # headers
            row = []
            for i in range(columns):
                if self.isColumnHidden(i):
                    continue
                row.append(model.headerData(i, Qt.Orientation.Horizontal))
            writer.writerow(row)
            # details
            for i in range(rows):
                row = []
                for j in range(columns):
                    if self.isColumnHidden(j):
                        continue
                    index = model.index(i, j)
                    # custom delegates
                    delegate = self.itemDelegateForColumn(j)
                    if isinstance(delegate, RelationDelegate):
                        data = delegate.getRelationData(index)
                    elif isinstance(delegate, HideTextDelegate):
                        data = _tr('View', 'HIDDEN TEXT')
                    else:
                        data = model.data(index)
                    # standard delegates
                    if isinstance(data, QByteArray):
                        data = _tr('View', 'BINARY DATA')
                    if isinstance(data, QDate):
                        data = session['qlocale'].toString(data, QLocale.FormatType.ShortFormat)
                    elif isinstance(data, QDateTime):
                        data = session['qlocale'].toString(data, QLocale.FormatType.ShortFormat)
                    elif isinstance(data, bool):
                        #data = "\u2611" if data else "\u2610" # tick
                        data = "I" if data else "O" # less problem with excel
                    elif isinstance(data, float):
                        data = str(data).replace(".", ",")
                    row.append(data)
                writer.writerow(row)
        # save export path
        st = QSettings()
        st.setValue("ExportPath", os.path.dirname(fname))
        # request for open csv file
        if QMessageBox.question(self,
                                _tr('MessageDialog', "Question"),
                                _tr('View', "Export data completed.\n"
                                    "Open the generated file?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
                                ) == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(QUrl("file:///{}".format(fname)))

    def hideCurrentColumn(self) -> None:
        "Hide current column"
        self.hideColumn(self.currentIndex().column())

    def showAllColumns(self) -> None:
        "Show all columns"
        for i in range(self.horizontalHeader().count()):
            if self.isColumnHidden(i):
                self.showColumn(i)
                self.setColumnWidth(i, 120)

    def resetViewState(self) -> None:
        "Reset the view state to initial state previously stored"
        # restore view state
        if self.horizontalHeaderState:
            self.horizontalHeader().restoreState(self.horizontalHeaderState)
            # current layout, if any, is no more setted
            if self.ag.checkedAction():
                self.ag.checkedAction().setChecked(False)

    def manageSettings(self) -> None:
        "Manage view settings on a dialog box"
        dialog = TableViewSettingsDialog(self)
        title = _tr('view', 'View settings')
        title = f'{title} (layout: {self.layoutName})'
        dialog.ui.groupBoxViewSettings.setTitle(title)
        dialog.exec_()

    def updateViewLayout(self) -> None:
        "Save current view layout to database"
        if not self.layoutName:
            return
        if not self.ag.checkedAction():  # no layout setted
            return
        viewId = int(self.ag.checkedAction().data())
        if not viewId:
            return
        columns = [(viewId,
                    i,
                    self.horizontalHeader().visualIndex(i),
                    not self.isColumnHidden(i),
                    self.columnWidth(i),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None)
                   for i in range(self.horizontalHeader().count())]
        try:
            set_adapt_setting(viewId, columns)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
        else:
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("View", "Layout customization saved"))

    def saveViewLayoutAs(self) -> None:
        "Create a new layout customization"
        if not self.layoutName:
            return
        viewDesc, ok = QInputDialog.getText(self,
                                            _tr("View", "New layout customization"),
                                            _tr("View", "Insert new customizazion description"))
        if not ok or viewDesc == '':
            return
        # create new customization
        try:
            viewId = create_adaptation('I', self.layoutName, viewDesc, None)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                               _tr("MessageDialog", "Database error"),
                               er.code,
                               er.message,
                               er.detail)
        else:
            # recreate customization list
            self.fillCustomizationMenu()
            # set new customization as current
            for a in self.ag.actions():
                if a.data() == str(viewId):
                    a.setChecked(True)
                    break
            # update layout settings
            self.updateViewLayout()

    def deleteViewLayout(self, action: QAction|None = None) -> None:
        "Delete current view layout from database"
        viewId = int(self.ag.checkedAction().data())
        if is_system_object(viewId):
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("View", "System layout cannot be deleted"))
            return
        if QMessageBox.question(self,
                                _tr("MessageDialog", "Question"),
                                _tr("View", "Are you sure to delete the current layout ?"),
                                QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No) == QMessageBox.StandardButton.No:
            return
        try:
            delete_adaptation(viewId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
        else:
            # recreate customization list
            self.fillCustomizationMenu()
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("View", "Current layout deleted"))

    def setUserDefaultLayout(self) -> None:
        "Set curent layout as default for user"
        if not self.layoutName:
            return
        if not self.ag.checkedAction():  # no layout setted
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("View", "No configuration has been set"))
            return
        viewId = int(self.ag.checkedAction().data())
        try:
            set_adapt_user_default('I', self.layoutName, session['user'], viewId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
        else:
            # recreate customization list
            self.fillCustomizationMenu()
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("View", "Current layout setted as user default"))

    def setClassDefaultLayout(self) -> None:
        "Set curent layout as default for view class"
        if not self.layoutName:
            return
        if not self.ag.checkedAction():  # no layout setted
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("View", "No configuration has been set"))
            return
        viewId = int(self.ag.checkedAction().data())
        try:
            set_adapt_class_default(viewId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
        else:
            # recreate customization list
            self.fillCustomizationMenu()
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("View", "Current layout setted as class default"))
