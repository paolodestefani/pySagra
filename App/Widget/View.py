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

This module contains general custom views and related dialogs, 
such as the enhanced table and tree views with layout customizations

"""

# standard library
import os
import csv
from decimal import Decimal
from typing import Any

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QSettings
from PySide6.QtCore import QUrl
from PySide6.QtCore import QDate
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QTime
from PySide6.QtCore import QByteArray
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QLocale
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QTimer
from PySide6.QtCore import QPoint
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QTreeView
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtGui import QAction
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QInputDialog
from PySide6.QtWidgets import QDialog

# application modules
from App import session
from App.Common.L10n import _tr
from App.Common.ExceptionHandler import gui_exception_context
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

from App.Ui.ViewSettingsDialog import Ui_ViewSettingsDialog



class ViewSettingsDialog(QDialog):
    """Dialog to manage the column layout of an enhanced table or tree view: order, visibility and width."""

    def __init__(self, parent: "LayoutViewMixin") -> None:
        super().__init__(parent)
        self._parent = parent
        self.ui = Ui_ViewSettingsDialog()
        self.ui.setupUi(self)
        # configure target layout structure constraints
        table_widget = self.ui.tableWidget
        table_widget.setColumnCount(5)
        table_widget.setItemDelegateForColumn(1, GenericReadOnlyDelegate(self))
        table_widget.setItemDelegateForColumn(3, BooleanDelegate(self))
        table_widget.setItemDelegateForColumn(4, IntegerDelegate(self))
        table_widget.setHorizontalHeaderLabels([
            _tr('View', 'Field index'),
            _tr('View', 'Field'),
            _tr('View', 'Sorting'),
            _tr('View', 'Visible'),
            _tr('View', 'Width')
        ])
        table_widget.verticalHeader().setVisible(True)
        model = parent.model()
        if model is None:
            return
        column_count = model.columnCount()
        table_widget.setRowCount(column_count)
        header = parent.header()
        # build layout customization dataset rows
        for i in range(column_count):
            # extract real core configuration elements from current parent state
            item_idx = TableWidgetItem(i)
            item_name = TableWidgetItem(model.headerData(i, Qt.Orientation.Horizontal))
            item_sort = TableWidgetItem(header.visualIndex(i))
            item_visible = TableWidgetItem(not parent.isColumnHidden(i))
            # a hidden column has width 0: propose the default one to show it again
            item_width = TableWidgetItem(parent.columnWidth(i) or header.defaultSectionSize())
            # apply interaction flags immediately upon instantiation to prevent sorting race-conditions
            readonly_flags = (
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsSelectable | 
                Qt.ItemFlag.ItemIsDragEnabled | 
                Qt.ItemFlag.ItemIsDropEnabled
            )
            item_idx.setFlags(readonly_flags)
            item_name.setFlags(readonly_flags)
            item_sort.setFlags(readonly_flags)
            # load populated entity cards into destination spaces
            table_widget.setItem(i, 0, item_idx)
            table_widget.setItem(i, 1, item_name)
            table_widget.setItem(i, 2, item_sort)
            table_widget.setItem(i, 3, item_visible)
            table_widget.setItem(i, 4, item_width)
        # re-index visual layout positions based on historical sorting sequences
        table_widget.sortItems(2, Qt.SortOrder.AscendingOrder)
        # hide raw structural configuration metadata fields from the user view
        table_widget.horizontalHeader().hideSection(0)
        table_widget.horizontalHeader().hideSection(2)
        table_widget.resizeColumnToContents(1)

    def accept(self) -> None:
        """Applies user layout parameters downstream to the parent table view grid canvas."""
        # cache primary initial clean interface layout geometry mapping
        if self._parent.header_state:
            self._parent.header().restoreState(self._parent.header_state)
        else:
            self._parent.header_state = self._parent.header().saveState()
        header = self._parent.header()
        # deactivate signal pipelines temporarily to block visual layout stuttering
        header.blockSignals(True)
        def get_val(row_idx: int, col_idx: int) -> Any:
            item = self.ui.tableWidget.item(row_idx, col_idx)
            if item is None:
                return None
            v = item.data(Qt.ItemDataRole.EditRole)
            return v if v is not None else item.data(Qt.ItemDataRole.DisplayRole)
        try:
            for r in range(self.ui.tableWidget.rowCount()):
                logical_val = get_val(r, 0)
                if logical_val is None:
                    continue
                logical_idx = int(logical_val)
                visible = bool(get_val(r, 3))
                width = int(get_val(r, 4))
                # fetch visual orientation context records
                current_visual = header.visualIndex(logical_idx)
                # shift columns onto designated spatial array points
                header.moveSection(current_visual, r)
                self._parent.setColumnHidden(logical_idx, not visible)
                if visible:
                    self._parent.setColumnWidth(logical_idx, width)
        finally:
            # safely release blocking flags and trigger a master canvas reprint
            header.blockSignals(False)
            header.viewport().update()
            self._parent.update()
        super().accept()


class LayoutViewMixin:
    """Column layouts of a view stored in the database: visibility, width and position
    of every column, set from the context menu. Shared by the enhanced table and tree
    views, it works on the header of the view returned by header()"""

    def _initLayout(self, view_actions: list, resize_actions: list, output_actions: list) -> None:
        "Set up the layout state and the context menu, called by the view constructor"
        self.layout_name: str | None = None
        self.header_state: QByteArray | None = None
        self._create_context_menu(view_actions, resize_actions, output_actions)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def _create_context_menu(self, view_actions: list, resize_actions: list, output_actions: list) -> None:
        """Build the context menu: sorting, movable columns and layouts are common,
        the actions of each kind of view are added to their group"""
        # visual tuning toggles
        self.cm_sorting = QAction(_tr("View", "Column sorting"), self)
        self.cm_sorting.setCheckable(True)
        self.cm_sorting.setChecked(False)
        self.cm_sorting.triggered.connect(self.activateSorting)
        self.cm_movable = QAction(_tr("View", "Column movable"), self)
        self.cm_movable.setCheckable(True)
        self.cm_movable.triggered.connect(self.activateMovableColumns)
        # content resize triggers
        self.cm_resize_cols = QAction(_tr("View", "Resize columns to contents"), self)
        # resizeColumnToContents exists in tables and trees, resizeColumnsToContents in tables only
        self.cm_resize_cols.triggered.connect(
            lambda: [self.resizeColumnToContents(c) for c in range(self.header().count())])
        # layout management containers
        self.cm_user_default = QAction(_tr("View", "Set current layout as user default"), self)
        self.cm_user_default.triggered.connect(self.setUserDefaultLayout)
        self.cm_customizations = QMenu(_tr("View", "Set layout"), self)
        self.action_group = QActionGroup(self)
        self.action_group.triggered.connect(self.setStoredLayout)
        # instantiate contextual admin-level commands conditionally using global session
        if session['can_edit_views']:
            self.cm_update_layout = QAction(_tr("View", "Update current layout"), self)
            self.cm_update_layout.triggered.connect(self.updateViewLayout)
            self.cm_delete = QAction(_tr("View", "Delete current layout"), self)
            self.cm_delete.triggered.connect(self.deleteViewLayout)
            self.cm_class_default = QAction(_tr("View", "Set current layout as class default"), self)
            self.cm_class_default.triggered.connect(self.setClassDefaultLayout)
            self.cm_save_layout = QAction(_tr("View", "Save current layout as ..."), self)
            self.cm_save_layout.triggered.connect(self.saveViewLayoutAs)
            self.cm_hide = QAction(_tr("View", "Hide current column"), self)
            self.cm_hide.triggered.connect(self.hideCurrentColumn)
            self.cm_show = QAction(_tr("View", "Show all columns"), self)
            self.cm_show.triggered.connect(self.showAllColumns)
            self.cm_reset = QAction(_tr("View", "Reset view state"), self)
            self.cm_reset.triggered.connect(self.resetViewState)
            self.cm_manage = QAction(_tr("View", "Manage settings"), self)
            self.cm_manage.triggered.connect(self.manageSettings)
        # build the final physical menu tree structure
        self.context_menu = QMenu(self)
        self.context_menu.addActions([self.cm_sorting, self.cm_movable] + view_actions)
        self.context_menu.addSeparator()
        self.context_menu.addActions([self.cm_resize_cols] + resize_actions)
        self.context_menu.addSeparator()
        if output_actions:
            self.context_menu.addActions(output_actions)
            self.context_menu.addSeparator()
        self.context_menu.addMenu(self.cm_customizations)
        self.context_menu.addAction(self.cm_user_default)
        self.context_menu.addSeparator()
        if session['can_edit_views']:
            self.context_menu.addActions([
                self.cm_update_layout, self.cm_delete, 
                self.cm_class_default, self.cm_save_layout
            ])
            self.context_menu.addSeparator()
            self.context_menu.addActions([
                self.cm_hide, self.cm_show, self.cm_reset, self.cm_manage
            ])

    def syncContextMenuStates(self) -> None:
        """Synchronize the state of menu items with the actual state of the widget"""
        self.cm_sorting.setChecked(self.isSortingEnabled())
        self.cm_movable.setChecked(self.header().sectionsMovable())

    def fillCustomizationMenu(self) -> None:
        """Populate the customizations context menu with database layouts."""
        if not self.layout_name:
            return
        # explicitly delete old actions to prevent memory leaks in PySide6
        old_actions = list(self.action_group.actions())
        for action in old_actions:
            self.action_group.removeAction(action)
            action.deleteLater() # safely destroys the C++ object
        self.cm_customizations.clear()
        title: str = _tr("Menu", "Error loading menu customizations")
        with gui_exception_context(self, title):
            # fetch available adaptations from the database
            result = list_adaptation('I', self.layout_name)
            # populate the menu with the retrieved database records
            for adapt_id, description, is_class_default in result:
                action = QAction(description, self)
                action.setCheckable(True)
                action.setData(str(adapt_id))
                if is_class_default:
                    action.setChecked(True)
                self.action_group.addAction(action)
                self.cm_customizations.addAction(action)
            # fetch and apply the initial default layout for the current user
            default_layout_id = get_adapt_default('I', self.layout_name, session['user'])
            for action in self.action_group.actions():
                if action.data() == str(default_layout_id):
                    action.setChecked(True)

    def setModel(self, model: QAbstractItemModel | None) -> None:
        """Set the model, no sorting and no moving while editing."""
        super().setModel(model)
        self.setSortingEnabled(False)  # better not to sort when editing/resetting
        self.header().setSectionsMovable(False)  # better not to move when editing

    def setLayoutName(self, name: str) -> None:
        """Set the layout identifier name after instantiation to trigger database sync."""
        self.layout_name = name
        self.fillCustomizationMenu()
        # trigger() would invert a checkable action: set the state and apply it
        self.cm_movable.setChecked(True)
        self.activateMovableColumns()
        # applied when the view is ready, the timer is dropped if the view is deleted first
        QTimer.singleShot(0, self, lambda: self.setStoredLayout(self.action_group.checkedAction()))

    def setStoredLayout(self, action: QAction | None) -> None:
        """Apply a layout definition stored in the database to the table view."""
        if action is None:  # safe boundary protection against PySide6 checkedAction() race-conditions
            return
        view_id = int(action.data())
        header = self.header()
        # reset layout first (or store the initial state on the first run)
        if self.header_state:
            header.restoreState(self.header_state)
        else:
            self.header_state = header.saveState()
        title: str = _tr("Menu", "Error applying stored layout")
        sorting = self.isSortingEnabled()
        with gui_exception_context(self, title):
            # fetch columns implementation: column_number, sorting, is_visible, size
            result = get_view_columns(view_id)
            # disable sorting temporarily to prevent heavy UI updates during layout shifts
            self.setSortingEnabled(False)
            for col_num, sorting_idx, is_visible, size in result:
                # boundary check: ensure the stored column index exists in the current view
                if col_num >= header.count():
                    continue    
                # toggle column visibility
                self.setColumnHidden(col_num, not is_visible)
                # apply column width if visible and has a valid size
                if is_visible and size > 0:
                    self.setColumnWidth(col_num, size)  
                # reorder columns dynamically by moving sections if index mismatches
                visual_idx = header.visualIndex(col_num)
                if visual_idx != sorting_idx:
                    header.moveSection(visual_idx, sorting_idx)
        self.setSortingEnabled(sorting)

    def showContextMenu(self, pos: QPoint) -> None:
        """Executes the custom layout options context menu at the requested position."""
        self.context_menu.exec(self.mapToGlobal(pos))

    def activateSorting(self) -> None:
        """Activate/deactivate sorting by column and sync action check state."""
        # sync the core widget property based on the action's current check state
        is_enabled = self.cm_sorting.isChecked()
        self.setSortingEnabled(is_enabled)

    def activateMovableColumns(self) -> None:
        """Activate/deactivate movable columns and sync action check state."""
        header = self.header()
        is_movable = self.cm_movable.isChecked()
        header.setSectionsMovable(is_movable)
        self.syncContextMenuStates()

    def hideCurrentColumn(self) -> None:
        """Hide the currently selected column layout index."""
        current_idx = self.currentIndex()
        if current_idx.isValid():
            self.hideColumn(current_idx.column())

    def showAllColumns(self) -> None:
        """Unhide all dataset columns and restore default layout grid widths."""
        header = self.header()
        for i in range(header.count()):
            if self.isColumnHidden(i):
                self.showColumn(i)
                self.setColumnWidth(i, 120)

    def resetViewState(self) -> None:
        """Reset the horizontal header orientation to its initial cached layout state."""
        if self.header_state:
            self.header().restoreState(self.header_state)
            # uncheck any active layout configuration in the menu group context
            active_action = self.action_group.checkedAction()
            if active_action:
                active_action.setChecked(False)

    def manageSettings(self) -> None:
        """Open the administrative dialog layout box to manage advanced table view parameters."""
        dialog = ViewSettingsDialog(self)
        title = _tr('view', 'View settings')
        title = f'{title} (layout: {self.layout_name})'
        dialog.ui.groupBoxViewSettings.setTitle(title)
        dialog.exec()

    def updateViewLayout(self) -> None:
        """Save the exact active column widths, visibility, and sorting indexes to the database."""
        if not self.layout_name:
            return
        checked_action = self.action_group.checkedAction()
        if not checked_action:  # out of boundary safety check
            return
        view_id = int(checked_action.data())
        if not view_id:
            return 
        header = self.header()
        # build layout positioning schema structure natively
        columns = [
            (
                view_id,
                col_idx,
                header.visualIndex(col_idx),
                not self.isColumnHidden(col_idx),
                self.columnWidth(col_idx),
                None, None, None, None, None, None  # database structural padding definitions
            )
            for col_idx in range(header.count())
        ]
        title: str = _tr("Menu", "Error saving view layout")
        with gui_exception_context(self, title) as outcome:
            set_adapt_setting(view_id, columns)
        if outcome.ok:  # messages outside of the context, it shows the wait cursor
            QMessageBox.information(
                self,
                _tr("MessageDialog", "Information"),
                _tr("View", "Layout customization saved")
            )

    def saveViewLayoutAs(self) -> None:
        """Create a new distinct database layout customization record from current workspace shapes."""
        if not self.layout_name:
            return
        view_desc, ok = QInputDialog.getText(
            self,
            _tr("View", "New layout customization"),
            _tr("View", "Insert new customization description")
        )
        # sanitize and validate target context input strings securely
        if not ok or not view_desc.strip():
            return
        title: str = _tr("Menu", "Error creating new layout")
        with gui_exception_context(self, title) as outcome:
            # write entity and extract generated master view table ID reference
            view_id = create_adaptation('I', self.layout_name, view_desc.strip())
        if not outcome.ok:
            return
        # rebuild structural elements on context menus safely
        self.fillCustomizationMenu()
        # map state adjustments dynamically across newly instantiated actions
        for action in self.action_group.actions():
            if action.data() == str(view_id):
                action.setChecked(True)
                break
        # perform instant schema sync to serialize configurations downstream
        self.updateViewLayout()

    def deleteViewLayout(self, action: QAction | None = None) -> None:
        """Remove the active layout mapping definition safely after validation gates clear."""
        checked_action = self.action_group.checkedAction()
        if not checked_action:
            return
        view_id = int(checked_action.data())
        title: str = _tr("Menu", "Error deleting layout")
        system = None
        with gui_exception_context(self, title):
            system = is_system_object(view_id)
        if system is None:
            return
        # restrict core system-level objects against destructive user operations
        if system:
            QMessageBox.warning(
                self,
                _tr("MessageDialog", "Warning"),
                _tr("View", "System layout cannot be deleted")
            )
            return
        confirm = QMessageBox.question(
            self,
            _tr("MessageDialog", "Question"),
            _tr("View", "Are you sure you want to delete the current layout?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.No:
            return
        with gui_exception_context(self, title) as outcome:
            # fire structural drop commands at database layers
            delete_adaptation(view_id)
        if outcome.ok:
            # re-render system structures to clear lingering pointers cleanly
            self.fillCustomizationMenu()
            QMessageBox.information(
                self,
                _tr("MessageDialog", "Information"),
                _tr("View", "Current layout deleted")
            )

    def setUserDefaultLayout(self) -> None:
        """Set the current layout customization as the default for the logged-in user."""
        if not self.layout_name:
            return
        checked_action = self.action_group.checkedAction()
        if not checked_action:  # safe fallback warning check
            QMessageBox.warning(
                self,
                _tr("MessageDialog", "Warning"),
                _tr("View", "No configuration has been set")
            )
            return
        view_id = int(checked_action.data())
        title: str = _tr("Menu", "Error setting user default layout")
        # safe transaction pipeline wrapped in the exception handler boundary
        with gui_exception_context(self, title) as outcome:
            set_adapt_user_default('I', self.layout_name, session['user'], view_id)
        if outcome.ok:
            # rebuild structural elements on context menus safely
            self.fillCustomizationMenu()
            QMessageBox.information(
                self,
                _tr("MessageDialog", "Information"),
                _tr("View", "Current layout set as user default")
            )

    def setClassDefaultLayout(self) -> None:
        """Set the current layout customization as the global default for this view class."""
        if not self.layout_name:
            return
        checked_action = self.action_group.checkedAction()
        if not checked_action:  # safe fallback warning check
            QMessageBox.warning(
                self,
                _tr("MessageDialog", "Warning"),
                _tr("View", "No configuration has been set")
            )
            return
        view_id = int(checked_action.data())
        title: str = _tr("Menu", "Error setting class default layout")
        with gui_exception_context(self, title) as outcome:
            set_adapt_class_default(view_id)
        if outcome.ok:
            # rebuild structural elements on context menus safely
            self.fillCustomizationMenu()
            QMessageBox.information(
                self,
                _tr("MessageDialog", "Information"),
                _tr("View", "Current layout set as class default")
            )


class EnhancedTableView(LayoutViewMixin, QTableView):
    """Generic but enhanced QTableView: stored column layouts, CSV export, row add/remove."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        # apply secure, production-ready UX view defaults
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | 
            QAbstractItemView.EditTrigger.SelectedClicked
        )
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        vertical_hdr = self.verticalHeader()
        horizontal_hdr = self.horizontalHeader()
        vertical_hdr.hide()
        vertical_hdr.setDefaultAlignment(Qt.AlignmentFlag.AlignVCenter)
        horizontal_hdr.setSortIndicatorShown(True)
        horizontal_hdr.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        horizontal_hdr.setSectionsMovable(False)
        # assign localized dynamic read-only default item delegates
        self.setItemDelegate(GenericReadOnlyDelegate(self))
        # table only actions, then the layout context menu
        self.cm_vheader = QAction(_tr("View", "Show vertical header"), self)
        self.cm_vheader.setCheckable(True)
        self.cm_vheader.setChecked(False)
        self.cm_vheader.triggered.connect(self.showVerticalHeader)
        self.cm_resize_rows = QAction(_tr("View", "Resize rows to contents"), self)
        self.cm_resize_rows.triggered.connect(self.resizeRowsToContents)
        self.cm_export = QAction(_tr("View", "Export to CSV file"), self)
        self.cm_export.triggered.connect(self.exportView)
        self._initLayout([self.cm_vheader], [self.cm_resize_rows], [self.cm_export])

    def header(self) -> QHeaderView:
        "The header of the column layouts, as QTreeView.header()"
        return self.horizontalHeader()

    def syncContextMenuStates(self) -> None:
        """Synchronize the state of menu items with the actual state of the widget"""
        super().syncContextMenuStates()
        self.cm_vheader.setChecked(self.verticalHeader().isVisible())

    def showVerticalHeader(self) -> None:
        """Toggle the visibility layout of the table vertical line numbers."""
        header = self.verticalHeader()
        if header.isVisible():
            header.hide()
            self.cm_vheader.setChecked(False)
        else:
            header.show()
            self.cm_vheader.setChecked(True)

    def add(self) -> int | None:
        """Insert a new blank row at the bottom of the current grid model."""
        model = self.model()
        if model is None:
            return None
        row = model.rowCount()
        success = model.insertRow(row)
        if not success:
            QMessageBox.critical(
                self,
                _tr("MessageDialog", "Critical"),
                _tr("View", "Error inserting row")
            )
            return None
        index = model.index(row, 0)
        self.scrollTo(index)
        self.setCurrentIndex(index)
        return row

    def remove(self) -> None:
        """Delete the currently selected row from the grid layout safely."""
        model = self.model()
        if model is None:
            return
        index = self.currentIndex()
        if not index.isValid():
            return
        if QMessageBox.question(
            self,
            _tr("MessageDialog", "Question"),
            _tr("View", "delete the selected row?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.No:
            return
        if not model.removeRows(index.row(), 1, QModelIndex()):
            QMessageBox.critical(
                self,
                _tr("MessageDialog", "Critical"),
                _tr("View", "Error deleting row")
            )

    def exportView(self) -> None:
        """Export visible table data to a CSV file with localized formatting."""
        settings = QSettings()
        path = str(settings.value("EnhancedTableView/ExportPath", os.getcwd()))
        model = self.model()
        if model is None:
            return
        rows = model.rowCount()
        columns = model.columnCount()
        # select destination file path
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            _tr("View", "Select file name and path"),
            path,
            _tr("View", "Comma separated values (*.csv);;All files (*.*)")
        )
        if not file_name:  # user cancelled the dialog
            return
        visible_columns = []
        column_delegates = {}
        for col_idx in range(columns):
            if not self.isColumnHidden(col_idx):
                visible_columns.append(col_idx)
                column_delegates[col_idx] = self.itemDelegateForColumn(col_idx)
        # open and write directly to the CSV file safely
        try:
            with open(file_name, 'w', encoding="utf-8", newline='') as f:
                writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # write Header Row
                header_row = [model.headerData(col_idx, Qt.Orientation.Horizontal) for col_idx in visible_columns]
                writer.writerow(header_row)
                # write Data Rows
                for row_idx in range(rows):
                    csv_row = []
                    for col_idx in visible_columns:
                        index = model.index(row_idx, col_idx)
                        delegate = column_delegates[col_idx]
                        # extract data checking custom delegate logic blocks
                        if isinstance(delegate, RelationDelegate):
                            data = delegate.getRelationData(index)
                        elif isinstance(delegate, HideTextDelegate):
                            data = _tr('View', 'HIDDEN TEXT')
                        else:
                            data = model.data(index, Qt.ItemDataRole.DisplayRole)
                            if data is None:  # booleans are shown by the check state only
                                check = model.data(index, Qt.ItemDataRole.CheckStateRole)
                                if check is not None:
                                    data = Qt.CheckState(check) == Qt.CheckState.Checked
                        csv_row.append(self._csvValue(data))
                    writer.writerow(csv_row)
        except Exception as err:
            QMessageBox.critical(
                self,
                _tr('MessageDialog', "Critical"),
                _tr('View', "Unable to write to filename: {}\nError: {}").format(file_name, err)
            )
            return
        # save the successfully validated export path location
        settings.setValue("EnhancedTableView/ExportPath", os.path.dirname(file_name))
        # ask user to open the generated document
        if QMessageBox.question(
            self,
            _tr('MessageDialog', "Question"),
            _tr('View', "Export data completed.\nOpen the generated file?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))

    @staticmethod
    def _csvValue(data: Any) -> Any:
        """Return a value as text for the CSV file, formatted with the locale of the
        current user; numbers have no group separator so that any program can read them"""
        locale: QLocale = session['qlocale']
        match data:
            case QByteArray():
                return _tr('View', 'BINARY DATA')
            case QDate() | QTime() | QDateTime():
                return locale.toString(data, QLocale.FormatType.ShortFormat)
            case bool():
                return "I" if data else "O"
            case Decimal():
                return f"{data:f}".replace(".", locale.decimalPoint())
            case float():
                text = repr(data) if 'e' not in repr(data) else f"{data:f}"
                return text.replace(".", locale.decimalPoint())
            case None:
                return ""
            case _:
                return data


class EnhancedTreeView(LayoutViewMixin, QTreeView):
    """QTreeView with the stored column layouts of the enhanced table view"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        header = self.header()
        header.setSortIndicatorShown(True)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setSectionsMovable(False)
        # as in a table: the last column keeps its width, a tree stretches it by default
        header.setStretchLastSection(False)
        self._initLayout([], [], [])
