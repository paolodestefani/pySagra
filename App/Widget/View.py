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
from App.Database.Itemview import list_itemviews
from App.Database.Itemview import create_itemview
from App.Database.Itemview import get_view_columns
from App.Database.Itemview import set_view_columns
from App.Database.Itemview import delete_view_layout
from App.Database.Itemview import set_default_view_layout
from App.Widget.Delegate import GenericReadOnlyDelegate
from App.Widget.Delegate import RelationDelegate
from App.Widget.Delegate import HideTextDelegate
from App.Widget.Delegate import BooleanDelegate
from App.Widget.Delegate import IntegerDelegate
from App.Widget.TableWidget import TableWidgetItem

from App.Ui.ViewSettingsDialog import Ui_ViewSettingsDialog


# navigation status settings

(NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST, FILTER, ADD,
 REMOVE, CHANGE, PRINT, EXPORT) = range(14)

VIEW, EDIT = range(2)
FORM, GRID = range(2)


class TableViewSettingsDialog(QDialog, Ui_ViewSettingsDialog):

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setItemDelegateForColumn(3, BooleanDelegate(self))
        self.tableWidget.setItemDelegateForColumn(4, IntegerDelegate(self))
        self.tableWidget.setHorizontalHeaderLabels([_tr('View', 'Field index'),
                                                    _tr('View', 'Field'),
                                                    _tr('View', 'Sorting'),
                                                    _tr('View', 'Visible'),
                                                    _tr('View', 'Width')])
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.setRowCount(parent.model().columnCount())
        for i in range(parent.horizontalHeader().count()):
            self.tableWidget.setItem(i, 0, TableWidgetItem(i))
            self.tableWidget.setItem(i, 1, TableWidgetItem(parent.model().headerData(i, Qt.Orientation.Horizontal)))  # header
            self.tableWidget.setItem(i, 2, TableWidgetItem(parent.horizontalHeader().visualIndex(i)))
            self.tableWidget.setItem(i, 3, TableWidgetItem(not parent.isColumnHidden(i)))
            self.tableWidget.setItem(i, 4, TableWidgetItem(parent.columnWidth(i)))
        self.tableWidget.sortItems(2, Qt.SortOrder.AscendingOrder)
        self.tableWidget.horizontalHeader().hideSection(0)
        self.tableWidget.horizontalHeader().hideSection(2)
        self.tableWidget.resizeColumnToContents(1)

        for r in range(parent.horizontalHeader().count()):
            for c in range(5):
                if c in (0, 1, 2):
                    self.tableWidget.item(r, c).setFlags(Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsSelectable|Qt.ItemFlag.ItemIsDragEnabled|Qt.ItemFlag.ItemIsDropEnabled)

    def accept(self) -> None:
        # reset layout first (first time store the state)
        if self.parent().horizontalHeaderState:
            self.parent().horizontalHeader().restoreState(self.parent().horizontalHeaderState)
        else:
            self.parent().horizontalHeaderState = self.parent().horizontalHeader().saveState()

        for r in range(self.tableWidget.rowCount()):
            c = int(self.tableWidget.item(r, 0).data())
            # ci = self.tableWidget.item(r, 2).data()
            v = bool(self.tableWidget.item(r, 3).data())
            s = int(self.tableWidget.item(r, 4).data())
            # set position
            ci = self.parent().horizontalHeader().visualIndex(c)
            self.parent().horizontalHeader().moveSection(ci, r)
            # show/hide
            if not v:
                self.parent().setColumnHidden(c, True)
            # width
            self.parent().setColumnWidth(c, s)
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
        # self.horizontalHeader().setStretchLastSection(True)
        # state of the hoerizontal header, used for reset
        self.horizontalHeaderState = None
        # context menu actions
        # activate/deactivate column sorting
        self.cmSorting = QAction(_tr("View", "Column sorting"), self)
        # self.cmSorting.setIcon(currentIcon['view_sort'])
        self.cmSorting.setCheckable(True)
        self.cmSorting.setChecked(False)
        self.cmSorting.triggered.connect(self.activateSorting)
        # activate/deactivate column movable
        self.cmMovable = QAction(_tr("View", "Column movable"), self)
        #self.cmMovable.setIcon(currentIcon['view_movablecolumns'])
        self.cmMovable.setCheckable(True)
        self.cmMovable.setChecked(False)
        self.cmMovable.triggered.connect(self.activateMovableColumns)
        # show vertical header
        self.cmVHeader = QAction(_tr("View", "Show vertical header"), self)
        self.cmVHeader.setCheckable(True)
        self.cmVHeader.setChecked(False)
        self.cmVHeader.triggered.connect(self.showVerticalHeader)
        # resize to content
        self.cmResizeColsToContent = QAction(_tr("View", "Resize columns to contents"), self)
        self.cmResizeColsToContent.setCheckable(False)
        self.cmResizeColsToContent.setIcon(currentIcon['view_resize_columns'])
        self.cmResizeColsToContent.triggered.connect(self.resizeColumnsToContents)
        self.cmResizeRowsToContent = QAction(_tr("View", "Resize rows to contents"), self)
        self.cmResizeRowsToContent.setCheckable(False)
        self.cmResizeRowsToContent.setIcon(currentIcon['view_resize_rows'])
        self.cmResizeRowsToContent.triggered.connect(self.resizeRowsToContents)
        # export to CSV file
        self.cmExport = QAction(_tr("View", "Export to CSV file"), self)
        self.cmExport.setIcon(currentIcon['edit_export'])
        self.cmExport.triggered.connect(self.exportView)
        # layout customizations
        self.cmCustomizations = QMenu(_tr("View", "Set layout"), self)
        self.cmCustomizations.setIcon(currentIcon['view_layout'])
        self.ag = QActionGroup(self)
        # customizations are inserted in a separate method after name assignement
        self.ag.triggered.connect(self.setStoredLayout)
        if session['can_edit_views']:
            # save customization
            self.cmUpdateLayout = QAction(_tr("View", "Update current layout"), self)
            self.cmUpdateLayout.setIcon(currentIcon['edit_save'])
            self.cmUpdateLayout.triggered.connect(self.updateViewLayout)
            # delete view layout
            self.cmDelete = QAction(_tr("View", "Delete current layout"), self)
            self.cmDelete.setIcon(currentIcon['view_delete'])
            self.cmDelete.triggered.connect(self.deleteViewLayout)
            # set as default current view layout
            self.cmDefault = QAction(_tr("View", "Set current layout as default"), self)
            self.cmDefault.setIcon(currentIcon['view_default'])
            self.cmDefault.triggered.connect(self.defaultViewLayout)
            # save customization as
            self.cmSaveLayout = QAction(_tr("View", "Save current layout as ..."), self)
            self.cmSaveLayout.setIcon(currentIcon['edit_save_as'])
            self.cmSaveLayout.triggered.connect(self.saveViewLayoutAs)
            # hide current column
            self.cmHide = QAction(_tr("View", "Hide current column"), self)
            self.cmHide.setIcon(currentIcon['view_hide_column'])
            self.cmHide.triggered.connect(self.hideCurrentColumn)
            # show all view columns
            self.cmShow = QAction(_tr("View", "Show all columns"), self)
            self.cmShow.setIcon(currentIcon['view_show_columns'])
            self.cmShow.triggered.connect(self.showAllColumns)
            # reset view state
            self.cmReset = QAction(_tr("View", "Reset view state"), self)
            self.cmReset.setIcon(currentIcon['edit_reload'])
            self.cmReset.triggered.connect(self.resetViewState)
            # manage view settings
            self.cmManage = QAction(_tr("View", "Manage settings"), self)
            self.cmManage.setIcon(currentIcon['view_configure'])
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
        self.cm.addSeparator()
        if session['can_edit_views']:
            self.cm.addActions([self.cmUpdateLayout,
                                self.cmDelete,
                                self.cmDefault,
                                self.cmSaveLayout])
            self.cm.addSeparator()
            self.cm.addActions([self.cmHide, self.cmShow, self.cmReset, self.cmManage])
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

    def fillCustomizationMenu(self) -> None:
        # clear everything
        for i in self.ag.actions():
            self.ag.removeAction(i)
        self.cmCustomizations.clear()
        # create actions and menu
        try:
            result = list_itemviews(self.layoutName)
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

    def setModel(self, model: QAbstractItemModel|None) -> None:
        super().setModel(model)
        self.setSortingEnabled(False) # better not to sort when editing

    def setLayoutName(self, name: str|None) -> None:
        "As EnhancedTableView is declared in QtDesigner we must set the name of the layout after instantiation"
        self.layoutName = name
        self.fillCustomizationMenu()
        self.setStoredLayout(self.ag.checkedAction())

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
        for c, i, v, s in result:
            # set position
            ci = self.horizontalHeader().visualIndex(c)
            self.horizontalHeader().moveSection(ci, i)
            # show/hide
            if not v:
                self.setColumnHidden(c, True)
            # width
            self.setColumnWidth(c, s)

    def contextMenuEvent(self, position: QContextMenuEvent) -> None:
        # self.cm.exec_(self.viewport().mapToGlobal(position))
        self.cm.exec_(QCursor.pos())

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
        #session['mainwin'].updateEditStatus(ESINS)
        #self.setSortingEnabled(False)
        row = self.model().rowCount()
        success = self.model().insertRow(row)
        #print("success", success)
        index = self.model().createIndex(row, 0)
        self.scrollTo(index)
        self.setCurrentIndex(index)
        self.edit(index)
        #print('Rows', self.model().rowCount())
        return row

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
                                 self.model().lastError().text())

    #def printView(self):
        #"Print table content"
        #notes = _tr("View", "Print")
        #dialog = QPrintPreviewDialog()
        #dialog.setGeometry(QStyle.alignedRect(Qt.LeftToRight,
                                              #Qt.AlignCenter,
                                              #QSize(800, 600),
                                              #qApp.desktop().availableGeometry()))
        #dialog.setWindowFlags(Qt.Dialog|Qt.WindowMinMaxButtonsHint|Qt.WindowCloseButtonHint)
        #dialog.setWindowTitle(_tr("View", "Print preview"))
        #st = PrintView(self)
        #dialog.paintRequested.connect(st.print_)
        #dialog.exec_()

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
                row.append(model.headerData(i, Qt.Horizontal))
            writer.writerow(row)
            # details
            for i in range(rows):
                row = []
                for j in range(columns):
                    if self.isColumnHidden(j):
                        continue
                    index = model.index(i, j)
                    # custom delegates
                    if isinstance(self.itemDelegateForColumn(j), RelationDelegate):
                        data = self.itemDelegateForColumn(j).getRelationData(index)
                    elif isinstance(self.itemDelegateForColumn(j), HideTextDelegate):
                        data = _tr('View', 'HIDDEN TEXT')
                    else:
                        data = model.data(index)
                    # standard delegates
                    if isinstance(data, QByteArray):
                        data = _tr('View', 'BINARY DATA')
                    if isinstance(data, QDate):
                        data = session['qlocale'].toString(data, QLocale.ShortFormat)
                    elif isinstance(data, QDateTime):
                        data = session['qlocale'].toString(data, QLocale.ShortFormat)
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
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
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
        dialog.groupBoxViewSettings.setTitle(title)
        dialog.exec_()

    def updateViewLayout(self, viewId: int = None) -> None:
        "Save current view layout to database"
        if not viewId:
            viewId = int(self.ag.checkedAction().data())
        columns = [(i,
                    self.horizontalHeader().visualIndex(i),
                    not self.isColumnHidden(i),
                    self.columnWidth(i))
                   for i in range(self.horizontalHeader().count())]
        try:
            set_view_columns(viewId, columns)
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
        viewDesc, ok = QInputDialog.getText(self,
                                            _tr("View", "New layout customization"),
                                            _tr("View", "Insert new customizazion description"))
        if not ok or viewDesc == '':
            return
        # create new customization
        try:
            viewId = create_itemview(self.layoutName, viewDesc)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
        else:
            # update layput settings
            self.updateViewLayout(viewId)
            # recreate customization list
            self.fillCustomizationMenu()

    def deleteViewLayout(self, action: QAction = None) -> None:
        "Delete current view layout from database"
        viewId = int(self.ag.checkedAction().data())
        try:
            delete_view_layout(viewId)
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

    def defaultViewLayout(self) -> None:
        "Set curent layout as default for view class"
        if not self.ag.checkedAction():  # no layout setted
            QMessageBox.warning(self,
                                _tr("MessageDialog", "Warning"),
                                _tr("View", "No configuration has been set"))
            return
        viewId = int(self.ag.checkedAction().data())
        try:
            set_default_view_layout(self.layoutName, viewId)
        except PyAppDBError as er:
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 "{}\n{}".format(er.code, er.message))
        else:
            # recreate customization list
            self.fillCustomizationMenu()
            QMessageBox.information(self,
                                    _tr("MessageDialog", "Information"),
                                    _tr("View", "Current layout setted as default"))
