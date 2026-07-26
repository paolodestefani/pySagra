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

"""Forms

This module contains custom form objects, used for data entry management, 
with a master/detail behavior. The main form is linked to a model and
secondary forms are linked to the main form by a relation.

"""

# standard library
from enum import IntEnum

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractItemModel
#from PySide6.QtGui import QCursor
#from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDataWidgetMapper
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QApplication

# application modules
from App import session
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import wait_cursor_context
from App.Core.ExceptionHandler import gui_exception_context
from App.Database.Connect import appconn
#from App.Database.Exceptions import PyAppDBError
from App.Database.AbstractModels.TableModel import QueryModel
from App.Database.AbstractModels.TableModel import TableModel
from App.Widget.Control import DataWidgetMapper
from App.Widget.Dialog import SortFilterDialog
from App.Widget.Dialog import EventFilterDialog
from App.Widget.Dialog import MessageBoxCritical



# edit status
class es(IntEnum):
    NEW      = 0 
    SAVE     = 1 
    DELETE   = 2
    RELOAD   = 3 
    FIRST    = 4 
    PREVIOUS = 5 
    NEXT     = 6 
    LAST     = 7
    FILTER   = 8 
    CHANGE   = 9
    REPORT   = 10 
    EXPORT   = 11

# default attributes for view/edit status
EDVIEW = True, False, True, True # new, save, delete, reload
EDEDIT = False, True, False, True # new, save, delete, reload

# edit or view
class ev(IntEnum):
    VIEW = 0
    EDIT = 1
    
# view type
class vw(IntEnum):
    FORM = 0
    GRID = 1


class FormManager[T](QWidget):
    """Generic form manager container
    
    This container class manage the main form and secondary form in a
    master/detail behavior. The role of this class is:
    - drive user actions derived from edit actions
    - consider user authorizations (r/w or r/o form)
    - drive linked forms/grids
    """
    # T = The type will be decided by the subclass

    def __init__(self, parent: QWidget, auth: tuple) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # subclass must define available status, default: nothing is available
        # 12 boolean values:
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False,) * 12 # False, False, False, False, False, False, False,
                                #False, False, False, False)
        self.model: QueryModel|TableModel # main form model
        self.detailRelations: list = []  # detail relation list
        self.state = ev.VIEW # initial state
        self.repr = 'Generic form manager'
        self.reloadConfirmation = True  # ask confirmation on reload
        # mapper
        self.mapper = DataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        self.ui: T # The type will be decided by the subclass
        self.linkedMappers: list = [] # linked mapper list
        self.read_perm, self.write_perm, self.execute_perm = auth
        # mapper cursor changed update detail
        self.mapper.currentIndexChanged.connect(self.mapperIndexChanged)
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr
    
    def setModel(self, model: QueryModel|TableModel) -> None:
        "Set the main form model"
        self.model = model
        self.mapper.setModel(self.model) # main form model
        # only for editable models
        if hasattr(self.model, 'isEditable') and self.model.isEditable:
            if hasattr(self.model, 'userDataChanged'):
                self.model.userDataChanged.connect(self.modelChanged)
        self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.model, self)
    
    def addDetailRelation(self, 
                          relation: QAbstractItemModel,
                          masterColumn: int,
                          detailColumn: int
                          ) -> None:
        "Add linked models to detailRelations list"
        self.detailRelations.append((relation, masterColumn, detailColumn))
        if hasattr(relation, 'isEditable') and relation.isEditable:
            if hasattr(relation, 'userDataChanged'):
                relation.userDataChanged.connect(self.modelChanged)

    def addLinkedMapper(self, mapper: QDataWidgetMapper) -> None:
        "Add linked mapper"
        self.linkedMappers.append(mapper)

    def modelChanged(self) -> None:
        "Update status and navigation on (main) model changed"
        self.state = ev.EDIT
        self.updateEditStatus()

    def mapperIndexChanged(self, row: int) -> None:
        "Reload detail relations on main model index change"
        if row < 0 or not self.model:
            return
        # connecting form and tableview causes 2 time execution of this method
        with wait_cursor_context():
            if self.detailRelations:  # query model don't have primary key
                for relation, masterColumn, detailColumn in self.detailRelations:
                    value = self.model.data(self.model.index(row, masterColumn))
                    relation.filter(detailColumn, value)
            self.updateEditStatus()
        
    def updateEditStatus(self) -> None:
        "Update main window edit status based on current model and mapper index"
        # get current values
        current = self.mapper.currentIndex() + 1 # mapper index is zero based
        total = self.model.rowCount()
        # define current navigation settings
        if current > total: # this can happen on reload
            current = total
        # no navigation needed
        if current < 0 and total < 0:
            nav = False, False, False, False
        # no record at all, disable counter and navigation
        elif current == 0 and total == 0:
            nav = False, False, False, False
        # one record, no need of navigation
        elif total == 1:
            nav = False, False, False, False
        # first record, not need of first/previous arrows
        elif current == 1:
            nav = False, False, True, True
        # last record, no need of next/last arrows
        elif current == total:
            nav = True, True, False, False
        # otherwise
        else:
            nav = True, True, True, True

        if self.state == ev.EDIT:
            # don't allow navigation while editing
            nav = False, False, False, False
            currentStatus = EDEDIT + nav + (False, True, True, True)
        else:
            currentStatus = EDVIEW + nav + (True, True, True, True)
        # filter available status
        status = [i and j for i, j in zip(currentStatus, self.availableStatus)]
        # disable Delete if no record
        if self.state != ev.EDIT and self.availableStatus[es.DELETE]:
            if total == 0:
                status[es.DELETE] = False
            else:
                status[es.DELETE] = True
        # disable unavailable actions for Read only auth
        if not self.write_perm:
            for i in (es.NEW, es.SAVE, es.DELETE):
                status[i] = False
        session['mainwin'].updateEditStatus(status, current, total)

    def toFirst(self) -> None:
        "To first"
        with wait_cursor_context():
            self.mapper.toFirst()
        
    def toPrevious(self) -> None:
        "To previous"
        with wait_cursor_context():
            self.mapper.toPrevious()
        
    def toNext(self) -> None:
        "To next"
        with wait_cursor_context():
            self.mapper.toNext()
        
    def toLast(self) -> None:
        "To last"
        with wait_cursor_context():
            self.mapper.toLast()
        
    def new(self) -> None:
        "Create a new record on model"
        if not self.write_perm:
            return
        # enable widget, in case it's disabled)
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setEnabled(True)
            # move in the form view
            self.ui.stackedWidget.setCurrentIndex(vw.FORM)
        row = self.model.rowCount()
        if not self.model.insertRow(row):
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 _tr("Form", "Error inserting a new row"))
        self.state = ev.EDIT
        self.mapper.setCurrentIndex(row) # setCurrentIndex() imply updateEditStatus()
            
    def save(self) -> None:
        "Save data to db and commit"
        if not self.write_perm:
            return
        active_widget = QApplication.focusWidget()
        if active_widget:
            active_widget.clearFocus()
            
        row = self.mapper.currentIndex()
        if not self.mapper.submit():
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"), 
                                 _tr("Form", "Error on mapper submit"))
            self.mapper.setCurrentIndex(row)
            return
            
        with gui_exception_context(self, _tr("Form", "Error on model submit all")):
            if hasattr(self.model, 'submitAll'):
                self.model.submitAll()
                
            self.mapper.setCurrentIndex(row)
            
            for mapper in self.linkedMappers:
                mapper.submit()
                
            for relation, masterColumn, detailField in self.detailRelations:
                with gui_exception_context(self, _tr("Form", "Error on model detail submit all")):
                    idx = self.model.index(row, masterColumn)
                    value = self.model.data(idx) if idx.isValid() else None
                    if hasattr(relation, 'submitAll'):
                        relation.submitAll(detailField, value)
                        
            appconn.commit()
            self.state = ev.VIEW
            self.mapper.setCurrentIndex(row)
        
    def delete(self) -> None:
        "Delete current record and commit"
        if not self.write_perm:
            return
        
        row = self.mapper.currentIndex()
        # *** not sure about this removeRows on detail
        if self.detailRelations:
            for relation, masterColumn, detailColumn in self.detailRelations:
                with gui_exception_context(self, _tr("Form", "Relation delete")):
                    if relation.rowCount() > 0:
                        relation.removeRows(masterColumn, detailColumn)
                        relation.submitAll()
            
        success = False
        with gui_exception_context(self, _tr("Form", "model delete")):
            self.model.removeRow(row)
            row -= 1
            success = True
        if not success:
            return
            
        with gui_exception_context(self, _tr("Form", "model delete")):
            if hasattr(self.model, 'submitAll'):
                self.model.submitAll()

        # call revert only if there are still records in the model
        if self.model.rowCount() > 0:
            self.mapper.revert()
        else:
            # visual cleaming on empty model
            self.mapper.clearMapping() 
            
        self.state = ev.VIEW
        
        if row < 0: 
            self.updateEditStatus()
            return
        if row + 1 > self.model.rowCount(): 
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)

    def reload(self) -> None:
        "Undo pending changes and Reload data from db"
        row = self.mapper.currentIndex()
        with gui_exception_context(self, _tr('FormManager', 'Reload')):
            if hasattr(self.model, 'revertAll'):
                self.model.revertAll()  # also do a select()
        self.state = ev.VIEW
        # riposition the mapper, index could be invalid if < 0 or > model.rowCount()
        # invalid indexes don't emit currentIndexChanged so we must do a
        # manual updateEditStatus()
        if self.mapper.currentIndex() < 0 or self.model.rowCount() == 0: # invalid index/empty table
            self.mapper.toFirst()
            self.updateEditStatus()
            return
        if row + 1 > self.model.rowCount():  # index grater then records
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row)  # setCurrentIndex() implies updateEditStatus()

    def applySortFilter(self)-> None:
        self.sortFilterDialog.applySortFilter()

    def setFilters(self) -> None:
        "Create/open filter dialog and update main model"
        self.sortFilterDialog.show()

    def changeView(self) -> None:
        "Move from and to form/grid view"
        if hasattr(self.ui, 'stackedWidget'):
            if self.ui.stackedWidget.currentIndex() == vw.FORM:
                self.ui.stackedWidget.setCurrentIndex(vw.GRID)
                # this works but don't enable navigation on tableview
                # self.widget.tableView.selectRow(self.mapper.currentIndex())
            else:
                self.ui.stackedWidget.setCurrentIndex(vw.FORM)
                # this works but don't enable navigation on tableview
                #self.mapper.setCurrentModelIndex(self.widget.tableView.selectionModel().currentIndex())
                
    def closeEvent(self, event: QCloseEvent) -> None:
        "Close the form, ask confirmation if dirty"
        if self.state == ev.EDIT:
            result = QMessageBox.question(
                self,
                _tr("MessageDialog", "Question"),
                _tr("Form", "The data has been modified, save ?"),
                QMessageBox.StandardButton.Yes|
                QMessageBox.StandardButton.No|
                QMessageBox.StandardButton.Cancel
            )
            match result:
                case QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                case QMessageBox.StandardButton.Yes:
                    if self.write_perm:
                        self.save()
                case QMessageBox.StandardButton.No:
                    self.model.revert()
                    self.state = ev.VIEW
                    self.updateEditStatus()
                    
        event.accept()


class FormViewManager[T](QWidget):
    """A simplified form manager container for only one tableview to manage, no mapper
    """

    def __init__(self, parent: QWidget, auth: tuple) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ui: T # The type will be decided by the subclass
        # subclass must define available status, default: nothing is available
        # 12 boolean values:
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False,) * 12
        self.model: QueryModel|TableModel # main form model
        self.state = ev.VIEW # initial state
        self.reloadConfirmation = True  # ask confirmation on reload
        self.repr = 'Generic form view manager'
        # model is mapped direct to tableview
        self.read_perm, self.write_perm, self.execute_perm = auth
        self.view: QTableView|None = None # subclass must set this
        self.sortFilterDialog: SortFilterDialog | EventFilterDialog | None # subclass must set this
        
    def setModel(self, model: QueryModel|TableModel) -> None:
        "Set the main form model"
        self.model = model
        # used for isDirty method, only for editable models
        if hasattr(self.model, 'isEditable') and self.model.isEditable:
            if hasattr(self.model, 'userDataChanged'):
                self.model.userDataChanged.connect(self.modelChanged)
        self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.model, self)
        
    def setView(self, view: QTableView) -> None:
        "Set the form view to manage and link the model to the view"
        self.view = view
        self.view.setModel(self.model)
        self.view.activateWindow()
        self.view.horizontalHeader().setSectionsMovable(True)
        self.view.setSortingEnabled(True)
        self.view.selectionModel().selectionChanged.connect(self.updateEditStatus)
        
    def modelChanged(self) -> None:
        "Update status and navigation on model changed"
        if self.state != ev.EDIT:
            self.state = ev.EDIT
            self.updateEditStatus()

    def updateEditStatus(self) -> None:
        "Update main window edit status based on current model and mapper index"
        if not self.model:
            return
        if not self.view:
            return
        total = self.model.rowCount()
        index = self.view.selectionModel().currentIndex()
        current = (index.row() + 1) if (index and index.isValid()) else -1

        if self.state == ev.EDIT:
            currentStatus = EDEDIT + (False,) * 8
        else:
            currentStatus = EDVIEW + (True,) * 8

        # filter available status
        status = [i and j for i, j in zip(currentStatus, self.availableStatus)]
        # disable Delete and form if no record
        if self.state != ev.EDIT and self.availableStatus[es.DELETE]:
            if total == 0:
                status[es.DELETE] = False
            else:
                status[es.DELETE] = True
        # disable unavailable actions for RO auth
        if not self.write_perm:
            for i in (es.NEW, es.SAVE, es.DELETE):
                status[i] = False
        session['mainwin'].updateEditStatus(status, current, total)

    def new(self) -> None:
        "Create a new record on model"
        if not self.write_perm:
            return
        if not self.view:
            return None
        if hasattr(self.view, 'add'):
            self.view.add()
        self.state = ev.EDIT

    def save(self) -> None:
        "Save data to db and commit"
        if not self.write_perm:
            return
        if not self.model:
            return None
        with gui_exception_context(self, _tr("Form", "Error on model submit all")):
            if hasattr(self.model, 'submitAll'):
                self.model.submitAll()
            # mapper repositioning
            self.state = ev.VIEW
            self.updateEditStatus()

    def delete(self) -> None:
        "Delete current record and commit"
        if not self.write_perm:
            return
        if not self.model:
            return
        if not self.view:
            return
        rows = self.view.selectionModel().selectedRows()
        if rows:
            row = rows[0].row()
        success = False
        with gui_exception_context(self, _tr("Form", "Mmodel submit all")):
            if hasattr(self.view, 'remove'):
                self.view.remove()
            if hasattr(self. model, 'submitAll'):
                self.model.submitAll()
            success = True
        if not success:
            self.reload()
            self.view.selectRow(row)
        self.state = ev.VIEW
        self.updateEditStatus()

    def reload(self) -> None:
        "Undo pending changes and Reload data from db"
        with gui_exception_context(self, _tr('FormViewManager', 'Reload')):
            if self.model and hasattr(self.model, 'revertAll'):
                self.model.revertAll() # also do a select()
        self.state = ev.VIEW
        self.updateEditStatus()

    def applySortFilter(self)-> None:
        if self.sortFilterDialog and hasattr(self.sortFilterDialog, 'applySortFilter'):
            self.sortFilterDialog.applySortFilter()

    def setFilters(self) -> None:
        if not self.model:
            return None
        # create filter dialog if not exists
        if not hasattr(self, 'sortFilterDialog'):
            self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.model, self)
        if self.sortFilterDialog:
            self.sortFilterDialog.show()

    def toFirst(self) -> None:
        "To first"
        if self.view:
            self.view.selectRow(0)

    def toPrevious(self) -> None:
        "To previous"
        if not self.view:
            return None
        index = self.view.selectionModel().currentIndex()
        if index:
            self.view.selectRow(index.row() - 1)

    def toNext(self) -> None:
        "To next"
        if not self.view:
            return None
        index = self.view.selectionModel().currentIndex()
        if index:
            self.view.selectRow(index.row() + 1)

    def toLast(self) -> None:
        "To last"
        if not self.view:
            return None
        if self.model:
            self.view.selectRow(self.model.rowCount() - 1)
            
    def closeEvent(self, event: QCloseEvent) -> None:
        "Close the form, ask confirmation if dirty"
        if self.state == ev.EDIT:
            result = QMessageBox.question(
                self,
                _tr("MessageDialog", "Question"),
                _tr("Form", "The data has been modified, save ?"),
                QMessageBox.StandardButton.Yes|
                QMessageBox.StandardButton.No|
                QMessageBox.StandardButton.Cancel
            )
            match result:
                case QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                case QMessageBox.StandardButton.Yes:
                    if self.write_perm:
                        self.save()
                case QMessageBox.StandardButton.No:
                    self.model.revert()
                    self.state = ev.VIEW
                    self.updateEditStatus()
        
        event.accept()


class FormIndexManager[T](QWidget):
    """Generic form manager container with index model
    This container class manage the main form and linked form in a
    master/detail behavior. The role of this class is:
    - drive user actions derived from edit actions
    - consider user authorizations (r/w or r/o form)
    - drive linked forms/grids
    Index model and main model are implicitly linked by the first column of both"""
    #ui: T # The type will be decided by the subclass

    def __init__(self, 
                 parent: QWidget,
                 auth: tuple
                 ) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # subclass must define available status, default: nothing is available
        # 12 boolean values:
        # new, save, delete, reload, first, previous, next,
        # last, filter, change, report, export
        self.availableStatus = (False,) * 12
        self.reloadConfirmation = True  # ask confirmation on reload
        # track form's state
        self.state = ev.VIEW # initial state
        self.read_perm, self.write_perm, self.execute_perm = auth
        self.detailRelations: list = []  # detail relation list
        self.model: QAbstractItemModel = TableModel()
        self.indexModel = QueryModel()
        self.repr = 'Generic form index manager'
        self.ui: T # The type will be decided by the subclass
        # index mapper
        self.indexMapper = QDataWidgetMapper(self)
        self.indexMapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        self.indexMapper.currentIndexChanged.connect(self.mapperIndexChanged)
        # form mapper
        self.mapper = DataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        # vavigation flag
        self._is_navigating = False 

    def setModel(self, model: QAbstractItemModel, indexModel: QueryModel) -> None:
        "Set the main form model and index model, index model can change from filter dialog"
        self.model = model
        self.indexModel = indexModel
        self.mapper.setModel(self.model) # main form model
        self.indexMapper.setModel(self.indexModel) # index model
        # used for isDirty method, only for editable models
        if hasattr(self.model, 'userDataChanged'):
            self.model.userDataChanged.connect(self.modelChanged)
        self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.indexModel, self)

    def setIndexView(self, view: QTableView) -> None:
        "Set index view"
        self.indexView = view
        self.indexView.setModel(self.indexModel) # set index model
        # map view to mapper and mapper to view
        self.indexView.selectionModel().currentRowChanged.connect(self.indexMapper.setCurrentModelIndex)
        self.indexMapper.currentIndexChanged.connect(self.indexView.selectRow)
        # read only view
        self.indexView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.indexView.activateWindow()
        self.indexView.horizontalHeader().setSectionsMovable(True)

    def addDetailRelation(self, 
                          relation: QAbstractItemModel,
                          masterColumn: int,
                          detailColumn: int
                          ) -> None:
        "Add linked models to detailRelations list"
        self.detailRelations.append((relation, masterColumn, detailColumn))
        if hasattr(relation, 'userDataChanged'):  # a modification of the relation cause an update of the status of the main form
            relation.userDataChanged.connect(self.modelChanged)

    def modelChanged(self) -> None:
        "Update status and navigation on model changed"
        if self._is_navigating:
            return
        self.state = ev.EDIT
        self.updateEditStatus()
    
    def mapperIndexChanged(self, index: int) -> None:
        "Reload form model and detail relations on mapper index change"
        # sanity checks
        if index < 0 or not self.indexModel or self.indexModel.rowCount() == 0:
            return
        
        # enable blocking to avoid false positives of changes to widgets
        self._is_navigating = True
        try:
            with gui_exception_context(self, _tr('FormIndexManager', 'Reloading data')):
                if not hasattr(self.model, 'filter'):
                    return
                # safe index recovery
                model_index = self.indexModel.index(index, 0)
                if not model_index.isValid():
                    return
                # filter the main model that have always only one row
                self.model.filter(0, model_index.data())    
                # synchronize the second mapper on the single record uploaded
                self.mapper.toFirst()
                # load detail relations
                if self.detailRelations:
                    current_row = self.mapper.currentIndex()
                    if current_row >= 0:
                        for relation, masterColumn, detailColumn in self.detailRelations:
                            idx_master = self.model.index(current_row, masterColumn)
                            if idx_master.isValid():
                                value = idx_master.data()
                                relation.filter(detailColumn, value)
                # update the main window status
                self.updateEditStatus()
        finally:
            # release the block in any case
            self._is_navigating = False

    def updateEditStatus(self) -> None:
        "Update main window edit status based on current model and mapper index"
        # get current values
        current = self.indexMapper.currentIndex() + 1
        total = self.indexModel.rowCount()
        # define current navigation settings
        if current > total:  # this can happen on reload
            current = total
        # no navigation needed
        if current < 0 and total < 0:
            nav = False, False, False, False
        # no record at all, disable counter and navigation
        elif current == 0 and total == 0:
            nav = False, False, False, False
        # one record, no need of navigation
        elif total == 1:
            nav = False, False, False, False
        # first record, not need of first/previous arrows
        elif current == 1:
            nav = False, False, True, True
        # last record, no need of next/last arrows
        elif current == total:
            nav = True, True, False, False
        # otherwise
        else:
            nav = True, True, True, True
        if self.state == ev.EDIT:
            # don't allow navigation while editing
            nav = False, False, False, False
            currentStatus = EDEDIT + nav + (False, True, True, True)
        else:
            currentStatus = EDVIEW + nav + (True, True, True, True)
        # filter available status
        status = [i and j for i, j in zip(currentStatus, self.availableStatus)]
        # disable Delete and form if no record
        if self.state != ev.EDIT and self.availableStatus[es.DELETE]:
            if total == 0:
                status[es.DELETE] = False
                if hasattr(self.ui, 'stackedWidget'):
                    self.ui.stackedWidget.setDisabled(True)
            else:
                status[es.DELETE] = True
                if hasattr(self.ui, 'stackedWidget'):
                    self.ui.stackedWidget.setEnabled(True)
        # disable unavailable actions for RO auth
        if not self.write_perm:
            for i in (es.SAVE, es.DELETE):
                status[i] = False
        # disable write option if is_system is set on the main model
        if hasattr(self.model, 'isSystemColumn'):
            system_index = self.model.index(0, self.model.isSystemColumn)
            if system_index.isValid() and bool(system_index.data(Qt.ItemDataRole.EditRole)):
                for i in (es.SAVE, es.DELETE):
                    status[i] = False
        session['mainwin'].updateEditStatus(status, current, total, self.indexModel.limitCondition)

    def toFirst(self) -> None:
        "To first"
        self.indexMapper.toFirst()

    def toPrevious(self) -> None:
        "To previous"
        self.indexMapper.toPrevious()

    def toNext(self) -> None:
        "To next"
        self.indexMapper.toNext()

    def toLast(self) -> None:
        "To last"
        self.indexMapper.toLast()

    def new(self) -> None:
        "Create a new record on model deleting the current one"
        if isinstance(self.model, QueryModel):
            return
        self._new = True
        self._is_navigating = True
        try:
            if hasattr(self.ui, 'stackedWidget') and self.ui.stackedWidget:
                self.ui.stackedWidget.setEnabled(True)
                self.ui.stackedWidget.setCurrentIndex(vw.FORM)
            if hasattr(self.model, 'clearData'):
                self.model.clearData() 
            if not self.model.insertRow(0):
                MessageBoxCritical(self,
                                    _tr("MessageDialog", "Critical"),
                                    _tr("Form", "Error inserting a new row"))
                self._new = False
                return
            self.state = ev.EDIT
            self.mapper.toFirst() 
            for relation, masterColumn, detailColumn in self.detailRelations:
                relation.filter(detailColumn, None)
        finally:
            self._is_navigating = False
            self._new = False
            self.updateEditStatus()

    def save(self) -> None:
        "Save data to db and commit"
        if not self.write_perm:
            return
        active_widget = QApplication.focusWidget()
        if active_widget:
            active_widget.clearFocus()
        if isinstance(self.model, QueryModel):
            return 
        if not self.mapper.submit():
            QMessageBox.critical(
                self,
                _tr("MessageDialog", "Critical"),
                _tr("Form", "Error on mapper submit")
            )
            return
        with gui_exception_context(self, _tr("Form", "Master and detail model submit all")):
            # save the main model record
            if hasattr(self.model, 'submitAll'):
                self.model.submitAll()
            # save the detail records
            for relation, masterColumn, detailColumn in self.detailRelations:
                idx = self.model.index(0, masterColumn)
                value = idx.data() if idx.isValid() else None
                if hasattr(relation, 'submitAll'):
                    relation.submitAll(detailColumn, value)   
            self.reload()
            self._new = False
            self.state = ev.VIEW
            
    def delete(self) -> None:
        "Delete current record and commit. Resets the index mapper to the previous value -1"
        if not self.write_perm:
            return
        if isinstance(self.model, QueryModel):
            return
        current_index = self.indexMapper.currentIndex()
        with gui_exception_context(self, _tr("Form", "Master and detail model delete")):
            for relation, masterColumn, detailColumn in self.detailRelations:
                if relation.rowCount() > 0:
                    relation.removeRows(0, relation.rowCount())
                    if hasattr(relation, 'submitAll'): # sometimes relation i read only
                        relation.submitAll()
            self.model.removeRow(0)
            if hasattr(self.model, 'submitAll'):
                self.model.submitAll()   
        self.state = ev.VIEW
        self.reload()
        new_indice = current_index - 1
        if new_indice < 0:
            new_indice = 0
        if self.indexModel and self.indexModel.rowCount() > 0:
            if new_indice >= self.indexModel.rowCount():
                new_indice = self.indexModel.rowCount() - 1
            self.indexMapper.setCurrentIndex(new_indice)
        else:
            self.indexMapper.toFirst()
            self.updateEditStatus()
    
    def reload(self) -> None:
        "Undo pending changes and Reload data from db. Automatically stays on the same or new record"
        if not self.indexModel: 
            return
        with wait_cursor_context():
            # DYNAMIC IDENTIFICATION OF THE PRIMARY KEY COLUMN
            # If it is not defined, we assume column 0 as the fallback.
            pk_col = getattr(self.model, 'pkColumn', 0)
            # PRIMARY KEY RECOVERY BEFORE REFRESH
            last_saved_key = None
            was_new_record = getattr(self, '_new', False)
            if was_new_record and self.model and self.model.rowCount() > 0:
                # in the new record (row 0 of the main model), we search in the correct key column
                last_saved_key = self.model.index(0, pk_col).data()
            elif self.indexMapper.currentIndex() >= 0:
                # in the index, we look for the key in the correct column
                last_saved_key = self.indexModel.index(self.indexMapper.currentIndex(), pk_col).data()
            currentIndex = self.indexMapper.currentIndex() 
            self.state = ev.VIEW
            with gui_exception_context(self, _tr("Form", "Form reload")):
                self.indexModel.revertAll()  # reruns the SQL select with filters and sorts
            crc = self.indexModel.rowCount()
            # SEQUENTIAL SEARCH ON THE REAL KEY COLUMN
            row_found = -1
            if last_saved_key is not None and crc > 0:
                for i in range(crc):
                    # compare the data on the correct pk_col column
                    valore_indice = self.indexModel.index(i, pk_col).data()
                    # we use str() for comparison so we are immune to type differences (e.g. integer vs. string)
                    if str(valore_indice) == str(last_saved_key):
                        row_found = i
                        break
            # REPOSITIONING THE MAPPER
            if crc == 0:  
                if hasattr(self.model, 'clearData'):
                    self.model.clearData()
                self.mapper.revert()
                self.updateEditStatus()
            elif row_found >= 0:
                self.indexMapper.setCurrentIndex(row_found)
            else:
                if currentIndex >= crc:
                    currentIndex = crc - 1
                if currentIndex < 0:
                    currentIndex = 0
                self.indexMapper.setCurrentIndex(currentIndex)    
            self.updateEditStatus()

    def setIndexModel(self, model: QueryModel) -> None:
        self.indexModel = model
        
    def applySortFilter(self)-> None:
        self.sortFilterDialog.applySortFilter()

    def setFilters(self) -> None:
        "Create/open filter dialog and update main model"
        self.sortFilterDialog.show()

    def changeView(self) -> None:
        "Move from and to form/grid view"
        if not hasattr(self.ui, 'stackedWidget'):
            return
        if self.ui.stackedWidget.currentIndex() ==vw.FORM:
            self.ui.stackedWidget.setCurrentIndex(vw.GRID)
        else:
            self.ui.stackedWidget.setCurrentIndex(vw.FORM)
            
    def closeEvent(self, event: QCloseEvent) -> None:
        "Close the form, ask confirmation if dirty"
        if self.state == ev.EDIT and self.write_perm:
            result = QMessageBox.question(
                self,
                _tr("MessageDialog", "Question"),
                _tr("Form", "The data has been modified, save ?"),
                QMessageBox.StandardButton.Yes|
                QMessageBox.StandardButton.No|
                QMessageBox.StandardButton.Cancel
            )
            match result:
                case QMessageBox.StandardButton.Cancel:
                    event.ignore()
                    return
                case QMessageBox.StandardButton.Yes:
                    if self.write_perm:
                        self.save()
                case QMessageBox.StandardButton.No:
                    self.model.revert()
                    self.state = ev.VIEW
                    self.updateEditStatus()
        event.accept()
