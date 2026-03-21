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

This module contains custom form objects, used for data entry management


"""

# standard library
#from typing import TypeVar, Generic

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtGui import QCursor
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QDataWidgetMapper
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QTableView

# application modules
from App import session
from App.Core.L10n import _tr
from App.Database.Connect import appconn
from App.Database.Exceptions import PyAppDBError
from App.Database.AbstractModels.TableModel import TableModel, QueryModel
#from App.Widget.Delegate import mapperItemDelegate
from App.Widget.Control import DataWidgetMapper
from App.Widget.Dialog import SortFilterDialog
from App.Widget.Dialog import MessageBoxCritical

# edit status settings
(NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST,
 FILTER, CHANGE, REPORT, EXPORT) = range(12)

# default attributes for view/edit status
EDVIEW = True, False, True, True # new, save, delete, reload
EDEDIT = False, True, False, True # new, save, delete, reload

VIEW, EDIT = range(2)
FORM, GRID = range(2)


class FormManager[T](QWidget):
    """Generic form manager container
    
    This container class manage the main form and secondary form in a
    master/detail behavior. The role of this class is:
    - drive user actions derived from edit actions
    - consider user authorizations (r/w or r/o form)
    - drive linked forms/grids
    """

    def __init__(self, parent: QWidget, auth: str) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        # subclass must define available status, default: nothing is available
        # 12 boolean values:
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False,) * 12 # False, False, False, False, False, False, False,
                                #False, False, False, False)
        self.model: TableModel # main form model
        self.detailRelations: list = []  # detail relation list
        self.state = VIEW # initial state
        self.repr = 'Generic form manager'
        self.reloadConfirmation = True  # ask confirmation on reload
        # track form's state
        self._state = VIEW # initial state
        # mapper
        self.mapper = DataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        self.ui: T # The type will be decided by the subclass
        #self.mapper.setItemDelegate(mapperItemDelegate(self))
        self.linkedMappers: list = [] # linked mapper list
        self.auth = auth
        # mapper cursor changed update detail
        self.mapper.currentIndexChanged.connect(self.mapperIndexChanged)
        
    def __repr__(self) -> str:
        "Model representation"
        return self.repr
    
    def setModel(self, model: TableModel|QueryModel) -> None:
        "Set the main form model"
        self.model = model
        self.mapper.setModel(self.model) # main form model
        # only for editable models
        if self.model.isEditable:
            self.model.userDataChanged.connect(self.modelChanged)
        self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.model, self)
    
    def addDetailRelation(self, 
                          relation: QueryModel|TableModel,
                          masterColumn: int,
                          detailColumn: int
                          ) -> None:
        "Add linked models to detailRelations list"
        self.detailRelations.append((relation, masterColumn, detailColumn))
        if relation.isEditable:
            if hasattr(relation, 'userDataChanged'):
                relation.userDataChanged.connect(self.modelChanged)

    def addLinkedMapper(self, mapper: QDataWidgetMapper) -> None:
        "Add linked mapper"
        self.linkedMappers.append(mapper)

    def modelChanged(self) -> None:
        "Update status and navigation on (main) model changed"
        self.state = EDIT
        self.updateEditStatus()

    def mapperIndexChanged(self, row: int) -> None:
        "Reload detail relations on main model index change"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        # connecting form and tableview causes 2 time execution of this method
        if self.detailRelations:  # query model don't have primary key
            for relation, masterColumn, detailColumn in self.detailRelations:
                value = self.model.data(self.model.createIndex(row, masterColumn))
                relation.filter(detailColumn, value)
        self.updateEditStatus()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()

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

        if self.state == EDIT:
            # don't allow navigation while editing
            nav = False, False, False, False
            currentStatus = EDEDIT + nav + (False, True, True, True)
        else:
            currentStatus = EDVIEW + nav + (True, True, True, True)
        # filter available status
        status = [i and j for i, j in zip(currentStatus, self.availableStatus)]
        # disable Delete if no record
        if self.state != EDIT and self.availableStatus[DELETE]:
            if total == 0:
                status[DELETE] = False
            else:
                status[DELETE] = True
        # disable unavailable actions for R auth
        if self.auth == 'R':
            for i in (NEW, SAVE, DELETE):
                status[i] = False
        session['mainwin'].updateEditStatus(status, current, total)

    def toFirst(self) -> None:
        "To first"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.mapper.toFirst()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()

    def toPrevious(self) -> None:
        "To previous"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.mapper.toPrevious()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()

    def toNext(self) -> None:
        "To next"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.mapper.toNext()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()

    def toLast(self) -> None:
        "To last"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        self.mapper.toLast()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()

    def new(self) -> None:
        "Create a new record on model"
        # enable widget, in case it's disabled)
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setEnabled(True)
            # move in the form view
            self.ui.stackedWidget.setCurrentIndex(FORM)
        row = self.model.rowCount()
        if not self.model.insertRow(row):
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 _tr("Form", "Error inserting a new row"))
        self.state = EDIT
        self.mapper.setCurrentIndex(row) # setCurrentIndex() imply updateEditStatus()

    def save(self) -> None:
        "Save data to db and commit"
        row = self.mapper.currentIndex()
        # this is required on new record otherwise need lost focus on all controls.
        # on update apdate all record not only modified fields
        if not self.mapper.submit():
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 _tr("Form", "Error on mapper submit"))
            self.mapper.setCurrentIndex(row)
            return
        try:
            self.model.submitAll()
        except PyAppDBError as er:
            if er.code == '23000':
                msg = _tr("Form", "Integrity constraint violation: "
                          "unable to commit the transaction because "
                          "a generic integrity violation occured")
            if er.code == '23502':
                msg = _tr("Form", "Integrity constraint violation: "
                          "unable to commit the transaction because "
                          "a not null error occured")
            if er.code == '23503':
                msg = _tr("Form", "Foreign key violation: "
                          "unable to delete the current record because "
                          "is still referenced from another database object")
            if er.code == '23505':
                msg = _tr("Form", "Duplicate key value violates unique constraint: "
                          "Can not insert the current record because a key value "
                          "is already present in the database table")
            else:
                msg = (f"Unrecognized database error code: {er.code}\n"
                       f"For more information click on 'Show Details...'")
            MessageBoxCritical(self, 
                               _tr("Form", "Error on model submit all"),
                               msg,
                               er.message)
            appconn.rollback()
            self.mapper.setCurrentIndex(row)
            return
        # details data and mapper
        for mapper in self.linkedMappers:
            mapper.submit()
        for relation, masterColumn, detailField in self.detailRelations:
            try:
                value = self.model.data(self.model.index(row, masterColumn))
                relation.submitAll(detailField, value)
            except PyAppDBError as er:
                if er.code == '23503':
                    msg = _tr("Form", "Referential integrity violation: "
                              "unable to delete the current record because "
                              "is still referenced from another database object")
                if er.code == '23505':
                    msg = _tr("Form", "Duplicate key value violates unique constraint: "
                              "Can not insert the current record because a key value "
                              "is already present in the database table")
                else:
                    msg = (f"Unrecognized database error code: {er.code}\n"
                           f"For more information click on 'Show Details...'")
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model detail submit all"),
                                   msg,
                                   er.message)
                appconn.rollback()
                return
        # commit transactions
        appconn.commit()
        # mapper repositioning
        self.state = VIEW
        self.mapper.setCurrentIndex(row)

    def delete(self) -> None:
        "Delete current record and commit"
        row = self.mapper.currentIndex()
        # details data
        for relation, masterColumn, detailColumn in self.detailRelations:
            try:
                relation.removeRows(0, relation.rowCount())
                relation.submitAll()
            except PyAppDBError as er:
                if er.code == '23503':
                    msg = _tr("Form", "Referential integrity violation: "
                              "unable to delete the current record because "
                              "is still referenced from another database object")
                if er.code == '23505':
                    msg = _tr("Form", "Duplicate key value violates unique constraint: "
                              "Can not insert the current record because a key value "
                              "is already present in the database table")
                else:
                    msg = (f"Unrecognized database error code: {er.code}\n"
                           f"For more information click on 'Show Details...'")
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model detail submit all"),
                                   msg,
                                   er.message)
                appconn.rollback()
                return
        # master table
        try:
            self.model.removeRow(row)
            row -= 1
        except PyAppDBError as er:
            msg = "Error: {}\n{}".format(er.code, er.message)
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 msg)
            appconn.rollback()
            return
        try:
            self.model.submitAll()
        except PyAppDBError as er:
            if er.code == '23503':
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model submit all"),
                                   _tr("Form", "Referential integrity violation: "
                                    "unable to delete the current record because "
                                    "is still referenced from another database object"),
                                   er.message)
            else:
                MessageBoxCritical(self,
                                   _tr("MessageDialog", "Critical"),
                                   er.code,
                                   er.message)
            appconn.rollback()
            self.reload()
            return
        else:
            appconn.commit()

        self.mapper.revert() # mandatory when table is empty
        self.state = VIEW
        # riposition the mapper, index could be invalid if < 0 or > model.rowCount()
        # invalid indexes don't emit currentIndexChanged so we must do a
        # manual updateEditStatus()
        if row < 0: # invalid index/empty table
            self.updateEditStatus()
            return
        if row + 1 > self.model.rowCount(): # index grater then records
            row = self.model.rowCount() - 1
        self.mapper.setCurrentIndex(row) # setCurrentIndex() implies updateEditStatus()
        # NO effect on detail relations, sql relational integrity MUST do that

    def reload(self) -> None:
        "Undo pending changes and Reload data from db"
        row = self.mapper.currentIndex()
        try:
            # cursor wait
            QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
            self.model.revertAll()  # also do a select()
        except PyAppDBError as er:
            msg = "Error: {}\n{}".format(er.code, er.message)
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 msg)
        finally:
            # cursor restore
            QGuiApplication.restoreOverrideCursor()
        self.state = VIEW
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

    def setFilters(self) -> None:
        "Create/open filter dialog and update main model"
        self.sortFilterDialog.show()

    def changeView(self) -> None:
        "Move from and to form/grid view"
        if hasattr(self.ui, 'stackedWidget'):
            if self.ui.stackedWidget.currentIndex() == FORM:
                self.ui.stackedWidget.setCurrentIndex(GRID)
                # this works but don't enable navigation on tableview
                # self.widget.tableView.selectRow(self.mapper.currentIndex())
            else:
                self.ui.stackedWidget.setCurrentIndex(FORM)
                # this works but don't enable navigation on tableview
                #self.mapper.setCurrentModelIndex(self.widget.tableView.selectionModel().currentIndex())
                
    def close(self) -> bool:
        "Close the form, ask confirmation if dirty"
        if self.state == EDIT:
            result = QMessageBox.question(self,
                                          _tr("MessageDialog", "Question"),
                                          _tr("Form", "The data has been modified, save ?"),
                                          QMessageBox.StandardButton.Yes|
                                          QMessageBox.StandardButton.No|
                                          QMessageBox.StandardButton.Cancel)
            if result == QMessageBox.StandardButton.Cancel:
                return False
            elif result == QMessageBox.StandardButton.Yes:
                self.save()
            else:
                self.model.revert()
                self.state = VIEW
                self.updateEditStatus()
        super().close()
        return True


class FormViewManager[T](QWidget):
    """A simplified form manager container for only one tableview to manage, no mapper
    """

    def __init__(self, parent: QWidget, auth: str) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ui: T # The type will be decided by the subclass
        # subclass must define available status, default: nothing is available
        # 12 boolean values:
        # NEW, SAVE, DELETE, RELOAD, FIRST, PREVIOUS, NEXT, LAST
        # FILTER, CHANGE, REPORT, EXPORT
        self.availableStatus = (False,) * 12
        self.model: QueryModel|TableModel|None
        self.state = VIEW # initial state
        self.reloadConfirmation = True  # ask confirmation on reload
        # model is mapped direct to tableview
        self.auth: str = auth
        self.view: QTableView|None = None # subclass must set this
        
    def setModel(self, model: QueryModel|TableModel) -> None:
        "Set the main form model"
        self.model = model
        # used for isDirty method, only for editable models
        if self.model.isEditable:
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
        if self.state != EDIT:
            self.state = EDIT
            self.updateEditStatus()

    def updateEditStatus(self) -> None:
        "Update main window edit status based on current model and mapper index"
        if not self.model:
            return
        if not self.view:
            return
        total = self.model.rowCount()
        index = self.view.selectionModel().currentIndex()
        if index:
            current = index.row() + 1 or - 1  # if index.row() == -1
        else:
            current = -1

        if self.state == EDIT:
            currentStatus = EDEDIT + (False,) * 8
        else:
            currentStatus = EDVIEW + (True,) * 8

        # filter available status
        status = [i and j for i, j in zip(currentStatus, self.availableStatus)]
        # disable Delete and form if no record
        if self.state != EDIT and self.availableStatus[DELETE]:
            if total == 0:
                status[DELETE] = False
            else:
                status[DELETE] = True
        # disable unavailable actions for R auth
        if self.auth == 'R':
            for i in (NEW, SAVE, DELETE):
                status[i] = False
        session['mainwin'].updateEditStatus(status, current, total)

    # def currentPrimaryKey(self) -> list|None:
    #     if not self.model or isinstance(self.model, QueryModel):
    #         return None
    #     if not self.view:
    #         return None
    #     if self.view.selectionModel().currentIndex():
    #         if self.model.getPrimaryKey(self.view.selectionModel().currentIndex().row()):
    #             return list(self.model.getPrimaryKey(self.view.selectionModel().currentIndex().row()).values())[0]
    #     return None

    def new(self) -> None:
        "Create a new record on model"
        if not self.view:
            return None
        if hasattr(self.view, 'add'):
            self.view.add()
        self.state = EDIT

    def save(self) -> None:
        "Save data to db and commit"
        # save only if not editing anything
        #if self.tableViewCompetitors.state() != QAbstractItemView.NoState:
        #    return
        if not self.model:
            return None
        try:
            if hasattr(self.model, 'submitAll'):
                self.model.submitAll()
        except PyAppDBError as er:
            if er.code == '23503':
                msg = _tr("Form", "Referential integrity violation: "
                          "unable to delete the current record because "
                          "is still referenced from another database object")
            if er.code == '23505':
                msg = _tr("Form", "Duplicate key value violates unique constraint: "
                          "Can not insert the current record because a key value "
                          "is already present in the database table")
            else:
                msg = (f"Unrecognized database error code: {er.code}\n"
                       f"For more information click on 'Show Details...'")

            MessageBoxCritical(self,
                               _tr("Form", "Error on model submit all"),
                               msg,
                               er.message)

            appconn.rollback()
        else:
            # commit transactions
            appconn.commit()

        # mapper repositioning
        self.state = VIEW
        self.updateEditStatus()

    def delete(self) -> None:
        "Delete current record and commit"
        # confirm deletion request BETTER TO IN SUBCLASS
        #if QMessageBox.question(self,
                                #_tr("MessageDialog", "Question"),
                                #_tr("Form", "Are you sure you want to delete the current record ?"),
                                #QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
            #return
        if not self.model:
            return None
        if not self.view:
            return None
        if hasattr(self.view, 'remove'):
            self.view.remove()
        try:
            if hasattr(self. model, 'submitAll'):
                self.model.submitAll()
        except PyAppDBError as er:
            if er.code == '23503':
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model submit all"),
                                   _tr("Form", "Referential integrity violation: "
                                    "unable to delete the current record because "
                                    "is still referenced from another database object"),
                                   er.message)
            else:
                MessageBoxCritical(self,
                                   _tr("Form", "Error on submitAll"),
                                   er.code,
                                   er.message)
            appconn.rollback()
        else:
            # commit transactions
            appconn.commit()

        self.state = VIEW
        self.updateEditStatus()

    def reload(self) -> None:
        "Undo pending changes and Reload data from db"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        if self.model and self.model.isEditable:
            if hasattr(self.model, 'submitAll'):
                self.model.revertAll() # also do a select()
        # cursor restore
        QGuiApplication.restoreOverrideCursor()
        self.state = VIEW
        self.updateEditStatus()

    def setFilters(self) -> None:
        if not self.model:
            return None
        # create filter dialog if not exists
        if not hasattr(self, 'sortFilterDialog'):
            self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.model, self)
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
            
    def close(self) -> bool:
        "Close the form, ask confirmation if dirty"
        if self.state == EDIT:
            result = QMessageBox.question(self,
                                          _tr("MessageDialog", "Question"),
                                          _tr("Form", "The data has been modified, save ?"),
                                          QMessageBox.StandardButton.Yes|
                                          QMessageBox.StandardButton.No|
                                          QMessageBox.StandardButton.Cancel)
            if result == QMessageBox.StandardButton.Cancel:
                return False
            elif result == QMessageBox.StandardButton.Yes:
                self.save()
            else:
                if self.model and self.model.isEditable:
                    self.model.revert()
                self.state = VIEW
                self.updateEditStatus()
        super().close()
        return True


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
                 auth: str
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
        self.state = VIEW # initial state
        self.auth = auth
        self.detailRelations: list = []  # detail relation list
        self.model: QueryModel|TableModel = TableModel()
        self.indexModel = QueryModel()
        self.ui: T # The type will be decided by the subclass
        # index mapper
        self.indexMapper = QDataWidgetMapper(self)
        self.indexMapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        self.indexMapper.currentIndexChanged.connect(self.mapperIndexChanged)
        # form mapper
        self.mapper = DataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.AutoSubmit)
        #self.mapper.setItemDelegate(mapperItemDelegate(self))

    def setModel(self, model: QueryModel|TableModel, indexModel: QueryModel) -> None:
        "Set the main form model and index model, index model can change from filter dialog"
        self.model = model
        self.indexModel = indexModel
        self.mapper.setModel(self.model) # main form model
        self.indexMapper.setModel(self.indexModel) # index model
        # used for isDirty method, only for editable models
        if hasattr(self.model, 'userDataChanged'):
            self.model.userDataChanged.connect(self.modelChanged)
        self.sortFilterDialog = SortFilterDialog(self.__class__.__name__, self.indexModel, self)
        #self.indexMapper.setModel(self.sortFilterDialog.model)

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
                          relation: QueryModel|TableModel,
                          masterColumn: int,
                          detailColumn: int
                          ) -> None:
        "Add linked models to detailRelations list"
        self.detailRelations.append((relation, masterColumn, detailColumn))
        #print("add relation", relation, masterColumn, detailColumn)
        if hasattr(relation, 'userDataChanged'):  # a modification of the relation cause an update of the status of the main form
            relation.userDataChanged.connect(self.modelChanged)

    def modelChanged(self) -> None:
        "Update status and navigation on model changed"
        self.state = EDIT
        self.updateEditStatus()

    def mapperIndexChanged(self, index: int) -> None:
        "Reload form model and detail relations on mapper index change"
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        #QGuiApplication.processEvents() # non funziona...
        self.model.filter(0, self.indexModel.index(index, 0).data())
        self.mapper.toFirst()
        for relation, masterColumn, detailColumn in self.detailRelations:
            value = self.model.index(self.mapper.currentIndex(), masterColumn).data()
            relation.filter(detailColumn, value)
        self.updateEditStatus()
        #print("Mapper model rows:", self.mapper.model().rowCount())
        # cursor restore
        QGuiApplication.restoreOverrideCursor()

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

        if self.state == EDIT:
            # don't allow navigation while editing
            nav = False, False, False, False
            currentStatus = EDEDIT + nav + (False, True, True, True)
        else:
            currentStatus = EDVIEW + nav + (True, True, True, True)
        # filter available status
        status = [i and j for i, j in zip(currentStatus, self.availableStatus)]
        # disable Delete and form if no record
        if self.state != EDIT and self.availableStatus[DELETE]:
            if total == 0:
                status[DELETE] = False
                if hasattr(self.ui, 'stackedWidget'):
                    self.ui.stackedWidget.setDisabled(True)
            else:
                status[DELETE] = True
                if hasattr(self.ui, 'stackedWidget'):
                    self.ui.stackedWidget.setEnabled(True)
        # disable unavailable actions for R auth
        if self.auth == 'R':
            for i in (NEW, SAVE, DELETE):
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
        # enable widget, in case it's disabled)
        if hasattr(self.ui, 'stackedWidget'):
            if self.ui.stackedWidget:
                self.ui.stackedWidget.setEnabled(True)
                # move in the form view
                self.ui.stackedWidget.setCurrentIndex(FORM)
        if hasattr(self.model, 'clearData'):
            self.model.clearData() # delete current data if any
        if not self.model.insertRow(0):
            MessageBoxCritical(self,
                                _tr("MessageDialog", "Critical"),
                                _tr("Form", "Error inserting a new row"))
        self.state = EDIT
        self.mapper.toFirst() # setCurrentIndex() imply updateEditStatus()
        for relation, masterColumn, detailColumn in self.detailRelations:
            value = None
            relation.filter(detailColumn, value)
        self._new = True
        self.updateEditStatus()

    def save(self) -> None:
        "Save data to db and commit"
        if isinstance(self.model, QueryModel):
            return
        # get current index
        #current_index = self.indexMapper.currentIndex()
        #self.model.filter(0, self.indexModel.index(index, 0).data())
        # mapper master data
        if not self.mapper.submit():
            QMessageBox.critical(self,
                                 _tr("MessageDialog", "Critical"),
                                 _tr("Form", "Error on mapper submit"))
            return
        # master data
        try:
            self.model.submitAll()
        except PyAppDBError as er:
            match er.code:
                case 'CCER':
                    msg = _tr("Form", "Row modified before update/delete: "
                            "unable to commit the transaction because "
                            "the row was modified before update or delete "
                            "from unother client")
                case '23000':
                    msg = _tr("Form", "Integrity constraint violation: "
                            "unable to commit the transaction because "
                            "a generic integrity violation occured")
                case '23502':
                    msg = _tr("Form", "Integrity constraint violation: "
                            "unable to commit the transaction because "
                            "a not null error occured")
                case '23503':
                    msg = _tr("Form", "Foreign key violation: "
                            "unable to delete the current record because "
                            "is still referenced from another database object")
                case '23505':
                    msg = _tr("Form", "Duplicate key value violates unique constraint: "
                            "Can not insert the current record because a key value "
                            "is already present in the database table")
                case _:
                    msg = (f"Unrecognized database error code: {er.code}\n"
                        f"For more information click on 'Show Details...'")
            MessageBoxCritical(self,
                               _tr("Form", "Error on model submit all"),
                               msg,
                               er.message)
            appconn.rollback()
            return
        # details data
        for relation, masterColumn, detailColumn in self.detailRelations:
            value = self.model.index(0, masterColumn).data()
            try:
                relation.submitAll(detailColumn, value)
            except PyAppDBError as er:
                if er.code == '23503':
                    msg = _tr("Form", "Referential integrity violation: "
                              "unable to delete the current record because "
                              "is still referenced from another database object")
                if er.code == '23505':
                    msg = _tr("Form", "Duplicate key value violates unique constraint: "
                              "Can not insert the current record because a key value "
                              "is already present in the database table")
                else:
                    msg = (f"Unrecognized database error code: {er.code}\n"
                           f"For more information click on 'Show Details...'")
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model detail submit all"),
                                   msg,
                                   er.message)
                appconn.rollback()
                return
        # commit transactions
        appconn.commit()
        self.reload()
        self._new = False
        self.state = VIEW

    def delete(self) -> None:
        "Delete current record and commit. Resets the index mapper to the previous value -1"
        if isinstance(self.model, QueryModel):
            return
        # confirm deletion request BETTER DO THIS IN SUBCLASS
        current_index = self.indexMapper.currentIndex()
        # details data
        for relation, masterColumn, detailColumn in self.detailRelations:
            try:
                relation.removeRows(0, relation.rowCount())
                relation.submitAll()
            except PyAppDBError as er:
                if er.code == '23503':
                    msg = _tr("Form", "Referential integrity violation: "
                              "unable to delete the current record because "
                              "is still referenced from another database object")
                if er.code == '23505':
                    msg = _tr("Form", "Duplicate key value violates unique constraint: "
                              "Can not insert the current record because a key value "
                              "is already present in the database table")
                else:
                    msg = (f"Unrecognized database error code: {er.code}\n"
                           f"For more information click on 'Show Details...'")
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model detail submit all"),
                                   msg,
                                   er.message)
                appconn.rollback()
                return
        # master data
        try:
            self.model.removeRow(0)
        except PyAppDBError as er:
            MessageBoxCritical(self,
                                _tr("MessageDialog", "Critical"),
                                msg,
                                er.message)
            appconn.rollback()
            return
        try:
            self.model.submitAll()
        except PyAppDBError as er:
            if er.code == '23503':
                MessageBoxCritical(self,
                                   _tr("Form", "Error on model submit all"),
                                   _tr("Form", "Referential integrity violation: "
                                 "unable to delete the current record because "
                                 "is still referenced from another database object"),
                                   er.message)
            else:
                MessageBoxCritical(self,
                                   _tr("MessageDialog", "Critical"),
                                   msg,
                                   er.message)
            appconn.rollback()
            self.reload()
            return
        else:
            appconn.commit()
        self.reload()
        self.indexMapper.setCurrentIndex(current_index - 1)
        self.state = VIEW

    def reload(self) -> None:
        "Undo pending changes and Reload data from db. Index mapper is set to the previous value"
        if not self.indexModel: # no index model currently setted
            return
        # cursor wait
        QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        currentIndex = self.indexMapper.currentIndex() # before first select = -1
        brc = self.indexModel.rowCount() # before first select = 0
        # 
        self.indexModel.revertAll()  # also do a select()
        #
        # reposition mapper
        crc = self.indexModel.rowCount()
        if currentIndex == -1:
            self.indexMapper.toFirst()
        elif crc == 0: # no rows
            self.mapperIndexChanged(-1)
            self.mapper.revert()
        #elif indexRowCount == rc: # same rows of before -> update
        #    self.indexMapper.setCurrentIndex(currentIndex)
        #elif indexRowCount < rc: # less rows then before -> delete
        #    self.indexMapper.setCurrentIndex(currentIndex -1)
        elif brc < crc: # more rows then before -> insert
            self.indexMapper.toLast()
        #    key = self.model.index(0, 0).data() # None on first select and after delete-
        #    # look for index number of the current id
        #    for i in range(self.indexModel.rowCount(), -1, -1):
        #        if self.indexModel.index(i, 0).data() == key:
        #            break
        #    self.indexMapper.setCurrentIndex(i)
        else:
            self.indexMapper.setCurrentIndex(currentIndex)    
        # cursor restore
        QGuiApplication.restoreOverrideCursor()
        self.state = VIEW
        self.updateEditStatus()

    def setIndexModel(self, model: QueryModel) -> None:
        self.indexModel = model

    def setFilters(self) -> None:
        "Create/open filter dialog and update main model"
        self.sortFilterDialog.show()

    def changeView(self) -> None:
        "Move from and to form/grid view"
        if not hasattr(self.ui, 'stackedWidget'):
            return
        if self.ui.stackedWidget.currentIndex() == FORM:
            self.ui.stackedWidget.setCurrentIndex(GRID)
        else:
            self.ui.stackedWidget.setCurrentIndex(FORM)
            
    def close(self) -> bool:
        "Close the form, ask confirmation if dirty"
        if self.state == EDIT:
            result = QMessageBox.question(self,
                                          _tr("MessageDialog", "Question"),
                                          _tr("Form", "The data has been modified, save ?"),
                                          QMessageBox.StandardButton.Yes|
                                          QMessageBox.StandardButton.No|
                                          QMessageBox.StandardButton.Cancel)
            if result == QMessageBox.StandardButton.Cancel:
                return False
            elif result == QMessageBox.StandardButton.Yes:
                self.save()
            else:
                if self.model and self.model.isEditable:
                    self.model.revert()
                self.state = VIEW
                self.updateEditStatus()
        super().close()
        return True