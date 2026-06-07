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
such as the enhanced table view with layout customizations

"""

# standard library
import os
import sys
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
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QTimer
from PySide6.QtCore import QPoint
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QTableView
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
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
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


from typing import Any
from PySide6.QtWidgets import QDialog, QTableWidgetItem
from PySide6.QtCore import Qt

# Note: Assumes _tr, Ui_ViewSettingsDialog, TableWidgetItem, BooleanDelegate, 
# IntegerDelegate, GenericReadOnlyDelegate, and EnhancedTableView are available.

class TableViewSettingsDialog(QDialog):
    """Dialog to manage advanced table view layouts such as column sorting orders, visibility, and size rules."""

    def __init__(self, parent: "EnhancedTableView") -> None:
        super().__init__(parent)
        self._parent = parent
        self.ui = Ui_ViewSettingsDialog()
        self.ui.setupUi(self)
        
        # Configure target layout structure constraints
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
        
        header = parent.horizontalHeader()
        
        # Build layout customization dataset rows
        for i in range(column_count):
            # Extract real core configuration elements from current parent state
            item_idx = TableWidgetItem(i)
            item_name = TableWidgetItem(model.headerData(i, Qt.Orientation.Horizontal))
            item_sort = TableWidgetItem(header.visualIndex(i))
            item_visible = TableWidgetItem(not parent.isColumnHidden(i))
            item_width = TableWidgetItem(parent.columnWidth(i))
            
            # FIX: Apply interaction flags immediately upon instantiation to prevent sorting race-conditions
            readonly_flags = (
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsSelectable | 
                Qt.ItemFlag.ItemIsDragEnabled | 
                Qt.ItemFlag.ItemIsDropEnabled
            )
            item_idx.setFlags(readonly_flags)
            item_name.setFlags(readonly_flags)
            item_sort.setFlags(readonly_flags)
            
            # Load populated entity cards into destination spaces
            table_widget.setItem(i, 0, item_idx)
            table_widget.setItem(i, 1, item_name)
            table_widget.setItem(i, 2, item_sort)
            table_widget.setItem(i, 3, item_visible)
            table_widget.setItem(i, 4, item_width)
            
        # Re-index visual layout positions based on historical sorting sequences
        table_widget.sortItems(2, Qt.SortOrder.AscendingOrder)
        
        # Hide raw structural configuration metadata fields from the user view
        table_widget.horizontalHeader().hideSection(0)
        table_widget.horizontalHeader().hideSection(2)
        table_widget.resizeColumnToContents(1)

    def accept(self) -> None:
        """Applies user layout parameters downstream to the parent table view grid canvas."""
        # Cache primary initial clean interface layout geometry mapping
        if self._parent.horizontal_header_state:
            self._parent.horizontalHeader().restoreState(self._parent.horizontal_header_state)
        else:
            self._parent.horizontal_header_state = self._parent.horizontalHeader().saveState()

        header = self._parent.horizontalHeader()
        
        # Deactivate signal pipelines temporarily to block visual layout stuttering
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
                
                # Fetch visual orientation context records
                current_visual = header.visualIndex(logical_idx)
                
                # Shift columns onto designated spatial array points
                header.moveSection(current_visual, r)
                self._parent.setColumnHidden(logical_idx, not visible)
                
                if visible:
                    self._parent.setColumnWidth(logical_idx, width)
        finally:
            # Safely release blocking flags and trigger a master canvas reprint
            header.blockSignals(False)
            header.viewport().update()
            self._parent.update()
            
        super().accept()


class EnhancedTableView(QTableView):
    """Generic but enhanced QTableView custom implementation for modern PySide6 workflows."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        
        self.layout_name: str | None = None
        self.horizontal_header_state: QByteArray | None = None
        
        # Apply secure, production-ready UX view defaults
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | 
            QAbstractItemView.EditTrigger.SelectedClicked
        )
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        
        # Optimize header configurations
        vertical_hdr = self.verticalHeader()
        horizontal_hdr = self.horizontalHeader()
        
        vertical_hdr.hide()
        vertical_hdr.setDefaultAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        horizontal_hdr.setSortIndicatorShown(True)
        horizontal_hdr.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        horizontal_hdr.setSectionsMovable(False)
        
        # Assign localized dynamic read-only default item delegates
        # NOTE: Ensure GenericReadOnlyDelegate is imported in your module
        self.setItemDelegate(GenericReadOnlyDelegate(self))
        
        # Initialize context menu engine
        self._create_context_menu()
        
        # Configure standard modern context menu signals
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def _create_context_menu(self) -> None:
        """Helper function to isolate setup logic for clean action mapping pipelines."""
        # Visual tuning toggles
        self.cm_sorting = QAction(_tr("View", "Column sorting"), self)
        self.cm_sorting.setCheckable(True)
        self.cm_sorting.setChecked(False)
        self.cm_sorting.triggered.connect(self.activateSorting)
        
        self.cm_movable = QAction(_tr("View", "Column movable"), self)
        self.cm_movable.setCheckable(True)
        self.cm_movable.triggered.connect(self.activateMovableColumns)
        
        self.cm_vheader = QAction(_tr("View", "Show vertical header"), self)
        self.cm_vheader.setCheckable(True)
        self.cm_vheader.setChecked(False)
        self.cm_vheader.triggered.connect(self.showVerticalHeader)
        
        # Content resize triggers
        self.cm_resize_cols = QAction(_tr("View", "Resize columns to contents"), self)
        self.cm_resize_cols.triggered.connect(self.resizeColumnsToContents)
        
        self.cm_resize_rows = QAction(_tr("View", "Resize rows to contents"), self)
        self.cm_resize_rows.triggered.connect(self.resizeRowsToContents)
        
        # Reporting / Output actions
        self.cm_export = QAction(_tr("View", "Export to CSV file"), self)
        self.cm_export.triggered.connect(self.exportView)
        
        # Layout management containers
        self.cm_user_default = QAction(_tr("View", "Set current layout as user default"), self)
        self.cm_user_default.triggered.connect(self.setUserDefaultLayout)
        
        self.cm_customizations = QMenu(_tr("View", "Set layout"), self)
        self.action_group = QActionGroup(self)
        self.action_group.triggered.connect(self.setStoredLayout)
        
        # Instantiate contextual admin-level commands conditionally using global session
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
            
        # Build the final physical menu tree structure
        self.context_menu = QMenu(self)
        self.context_menu.addActions([self.cm_sorting, self.cm_movable, self.cm_vheader])
        self.context_menu.addSeparator()
        self.context_menu.addActions([self.cm_resize_cols, self.cm_resize_rows])
        self.context_menu.addSeparator()
        self.context_menu.addActions([self.cm_export])
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
        """Sincronizza lo stato delle voci del menu con lo stato reale del widget"""
        self.cm_sorting.setChecked(self.isSortingEnabled())
        self.cm_movable.setChecked(self.horizontalHeader().sectionsMovable())
        self.cm_vheader.setChecked(self.verticalHeader().isVisible())


    def fillCustomizationMenu(self) -> None:
        """Populate the customizations context menu with database layouts."""
        if not self.layout_name:
            return
            
        # FIX: Explicitly delete old actions to prevent memory leaks in PySide6
        old_actions = list(self.action_group.actions())
        for action in old_actions:
            self.action_group.removeAction(action)
            action.deleteLater() # Safely destroys the C++ object
            
        self.cm_customizations.clear()
        
        title: str = _tr("Menu", "Error loading menu customizations")
        with gui_exception_context(self, title):
            # 1. Fetch available adaptations from the database
            result = list_adaptation('I', self.layout_name)
            
            # Populate the menu with the retrieved database records
            for adapt_id, description, is_class_default in result:
                action = QAction(description, self)
                action.setCheckable(True)
                action.setData(str(adapt_id))
                if is_class_default:
                    action.setChecked(True)
                self.action_group.addAction(action)
                self.cm_customizations.addAction(action)
                
            # 2. Fetch and apply the initial default layout for the current user
            default_layout_id = get_adapt_default('I', self.layout_name, session['user'])
            for action in self.action_group.actions():
                if action.data() == str(default_layout_id):
                    action.setChecked(True)

    def setModel(self, model: QAbstractItemModel | None) -> None:
        """Override setModel to reset core configuration flags cleanly."""
        super().setModel(model)
        self.setSortingEnabled(False)  # Better not to sort when editing/resetting
        self.horizontalHeader().setSectionsMovable(False)  # Better not to move when editing

    def setLayoutName(self, name: str) -> None:
        """Set the layout identifier name after instantiation to trigger database sync."""
        self.layout_name = name
        self.fillCustomizationMenu()
        if self.cm_movable:
            self.cm_movable.setChecked(True)
            self.cm_movable.trigger()      
        
        # FIX: Safer async trigger loop that resolves the action at execution time
        QTimer.singleShot(0, lambda: self.setStoredLayout(self.action_group.checkedAction()))

    def setStoredLayout(self, action: QAction | None) -> None:
        """Apply a layout definition stored in the database to the table view."""
        if action is None:  # Safe boundary protection against PySide6 checkedAction() race-conditions
            return
            
        view_id = int(action.data())
        header = self.horizontalHeader()
        
        # Reset layout first (or store the initial state on the first run)
        if self.horizontal_header_state:
            header.restoreState(self.horizontal_header_state)
        else:
            self.horizontal_header_state = header.saveState()
            
        title: str = _tr("Menu", "Error applying stored layout")
        with gui_exception_context(self, title):
            # Fetch columns implementation: column_number, sorting, is_visible, size
            result = get_view_columns(view_id)
            
            # Disable sorting temporarily to prevent heavy UI updates during layout shifts
            self.setSortingEnabled(False)
            
            for col_num, sorting_idx, is_visible, size in result:
                # Boundary check: ensure the stored column index exists in the current view
                if col_num >= header.count():
                    continue   
                    
                # Toggle column visibility
                self.setColumnHidden(col_num, not is_visible)
                
                # Apply column width if visible and has a valid size
                if is_visible and size > 0:
                    self.setColumnWidth(col_num, size)  
                    
                # Reorder columns dynamically by moving sections if index mismatches
                visual_idx = header.visualIndex(col_num)
                if visual_idx != sorting_idx:
                    header.moveSection(visual_idx, sorting_idx)
        
    # Note: Assumes _tr is available in your module context.

    def showContextMenu(self, pos: QPoint) -> None:
        """Executes the custom layout options context menu at the requested position."""
        # FIX: Explicit type hinting with QPoint ensures modern PySide6 binding safety
        self.context_menu.exec(self.mapToGlobal(pos))

    def activateSorting(self) -> None:
        """Activate/deactivate sorting by column and sync action check state."""
        # Sync the core widget property based on the action's current check state
        is_enabled = self.cm_sorting.isChecked()
        self.setSortingEnabled(is_enabled)

    def activateMovableColumns(self) -> None:
        """Activate/deactivate movable columns and sync action check state."""
        header = self.horizontalHeader()
        is_movable = self.cm_movable.isChecked()
        header.setSectionsMovable(is_movable)
        self.syncContextMenuStates()

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
            
        if QMessageBox.question(
            self,
            _tr("MessageDialog", "Question"),
            _tr("View", "delete the selected row?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.No:
            return
            
        index = self.currentIndex()
        if not index.isValid():
            return
            
        # FIX: Replaced parent=QModelIndex() keyword syntax with standard empty index signature
        if not model.removeRows(index.row(), 1, QModelIndex()):
            QMessageBox.critical(
                self,
                _tr("MessageDialog", "Critical"),
                _tr("View", "Error deleting row")
            )

    def exportView(self) -> None:
        """Export visible table data to a CSV file with localized formatting."""
        settings = QSettings()
        path = str(settings.value("ExportPath", os.getcwd()))
        
        model = self.model()
        if model is None:
            return
            
        rows = model.rowCount()
        columns = model.columnCount()
        
        # Select destination file path
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            _tr("View", "Select file name and path"),
            path,
            _tr("View", "Comma separated values (*.csv);;All files (*.*)")
        )
        if not file_name:  # User cancelled the dialog
            return
            
        # Optimization: Pre-cache column visibility and column delegates outside the row loop
        visible_columns = []
        column_delegates = {}
        
        for col_idx in range(columns):
            if not self.isColumnHidden(col_idx):
                visible_columns.append(col_idx)
                column_delegates[col_idx] = self.itemDelegateForColumn(col_idx)
                
        # Open and write directly to the CSV file safely
        try:
            with open(file_name, 'w', encoding="utf-8", newline='') as f:
                writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                # 1. Write Header Row
                header_row = [model.headerData(col_idx, Qt.Orientation.Horizontal) for col_idx in visible_columns]
                writer.writerow(header_row)
                
                # 2. Write Data Rows
                for row_idx in range(rows):
                    csv_row = []
                    for col_idx in visible_columns:
                        index = model.index(row_idx, col_idx)
                        delegate = column_delegates[col_idx]
                        
                        # Extract data checking custom delegate logic blocks
                        if isinstance(delegate, RelationDelegate):
                            data = delegate.getRelationData(index)
                        elif isinstance(delegate, HideTextDelegate):
                            data = _tr('View', 'HIDDEN TEXT')
                        else:
                            data = model.data(index, Qt.ItemDataRole.DisplayRole)
                            
                        # Format and normalize data types cleanly for Excel compatibility
                        if isinstance(data, QByteArray):
                            data = _tr('View', 'BINARY DATA')
                        elif isinstance(data, QDate):
                            data = session['qlocale'].toString(data, QLocale.FormatType.ShortFormat)
                        elif isinstance(data, QDateTime):
                            data = session['qlocale'].toString(data, QLocale.FormatType.ShortFormat)
                        elif isinstance(data, bool):
                            data = "I" if data else "O"  # Best localization pattern for raw spreadsheet inputs
                        elif isinstance(data, float):
                            data = f"{data}".replace(".", ",")
                        elif data is None:
                            data = ""
                            
                        csv_row.append(data)
                    writer.writerow(csv_row)
                    
        except Exception as err:
            QMessageBox.critical(
                self,
                _tr('MessageDialog', "Critical"),
                _tr('View', f"Unable to write to filename: {file_name}\nError: {str(err)}")
            )
            return

        # Save the successfully validated export path location
        settings.setValue("ExportPath", os.path.dirname(file_name))
        
        # Ask user to open the generated document
        if QMessageBox.question(
            self,
            _tr('MessageDialog', "Question"),
            _tr('View', "Export data completed.\nOpen the generated file?"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            # FIX: QUrl.fromLocalFile builds safe cross-platform file paths automatically
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))

    def hideCurrentColumn(self) -> None:
        """Hide the currently selected column layout index."""
        current_idx = self.currentIndex()
        if current_idx.isValid():
            self.hideColumn(current_idx.column())

    def showAllColumns(self) -> None:
        """Unhide all dataset columns and restore default layout grid widths."""
        header = self.horizontalHeader()
        for i in range(header.count()):
            if self.isColumnHidden(i):
                self.showColumn(i)
                self.setColumnWidth(i, 120)

    def resetViewState(self) -> None:
        """Reset the horizontal header orientation to its initial cached layout state."""
        if self.horizontal_header_state:
            self.horizontalHeader().restoreState(self.horizontal_header_state)
            
            # Uncheck any active layout configuration in the menu group context
            active_action = self.action_group.checkedAction()
            if active_action:
                active_action.setChecked(False)


    def manageSettings(self) -> None:
        """Open the administrative dialog layout box to manage advanced table view parameters."""
        dialog = TableViewSettingsDialog(self)
        title = _tr('view', 'View settings')
        title = f'{title} (layout: {self.layout_name})'
        dialog.ui.groupBoxViewSettings.setTitle(title)
        dialog.exec_()

    def updateViewLayout(self) -> None:
        """Save the exact active column widths, visibility, and sorting indexes to the database."""
        if not self.layout_name:
            return
            
        checked_action = self.action_group.checkedAction()
        if not checked_action:  # Out of boundary safety check
            return
            
        view_id = int(checked_action.data())
        if not view_id:
            return 
            
        header = self.horizontalHeader()
        
        # Build layout positioning schema structure natively
        columns = [
            (
                view_id,
                col_idx,
                header.visualIndex(col_idx),
                not self.isColumnHidden(col_idx),
                self.columnWidth(col_idx),
                None, None, None, None, None, None  # Database structural padding definitions
            )
            for col_idx in range(header.count())
        ]
        
        title: str = _tr("Menu", "Error saving view layout")
        with gui_exception_context(self, title):
            set_adapt_setting(view_id, columns)
            
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
        
        # Sanitize and validate target context input strings securely
        if not ok or not view_desc.strip():
            return
            
        title: str = _tr("Menu", "Error creating new layout")
        with gui_exception_context(self, title):
            # Write entity and extract generated master view table ID reference
            view_id = create_adaptation('I', self.layout_name, view_desc.strip())
            
            # Rebuild structural elements on context menus safely
            self.fillCustomizationMenu()
            
            # Map state adjustments dynamically across newly instantiated actions
            for action in self.action_group.actions():
                if action.data() == str(view_id):
                    action.setChecked(True)
                    break      
                    
            # Perform instant schema sync to serialize configurations downstream
            self.updateViewLayout()

    def deleteViewLayout(self, action: QAction | None = None) -> None:
        """Remove the active layout mapping definition safely after validation gates clear."""
        checked_action = self.action_group.checkedAction()
        if not checked_action:
            return
            
        view_id = int(checked_action.data())
        title: str = _tr("Menu", "Error deleting layout")
        
        with gui_exception_context(self, title):
            # Restrict core system-level objects against destructive user operations
            if is_system_object(view_id):
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
                
            # Fire structural drop commands at database layers
            delete_adaptation(view_id)
            
            # Re-render system structures to clear lingering pointers cleanly
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
        if not checked_action:  # Safe fallback warning check
            QMessageBox.warning(
                self,
                _tr("MessageDialog", "Warning"),
                _tr("View", "No configuration has been set")
            )
            return
            
        view_id = int(checked_action.data())
        title: str = _tr("Menu", "Error setting user default layout")
        
        # Safe transaction pipeline wrapped in the exception handler boundary
        with gui_exception_context(self, title):
            set_adapt_user_default('I', self.layout_name, session['user'], view_id)
            
            # Rebuild structural elements on context menus safely
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
        if not checked_action:  # Safe fallback warning check
            QMessageBox.warning(
                self,
                _tr("MessageDialog", "Warning"),
                _tr("View", "No configuration has been set")
            )
            return
            
        view_id = int(checked_action.data())
        title: str = _tr("Menu", "Error setting class default layout")
        
        with gui_exception_context(self, title):
            set_adapt_class_default(view_id)
            
            # Rebuild structural elements on context menus safely
            self.fillCustomizationMenu()
            
            QMessageBox.information(
                self,
                _tr("MessageDialog", "Information"),
                _tr("View", "Current layout set as class default")
            )
