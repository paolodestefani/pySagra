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

"""SQL Models

This module provide all the sql models derived from an abstract model

"""

# standard library

# PySide6
from PySide6.QtCore import QObject
from PySide6.QtCore import Qt
from PySide6.QtCore import QModelIndex
from PySide6.QtGui import QFont

# application modules
from App.Database.AbstractModels.TableModel import QueryModel
from App.Database.AbstractModels.TableModel import QueryWithParamsModel
from App.Database.AbstractModels.TableModel import TableModel
from App.Database.AbstractModels.TreeModel import TreeQueryModel
from App.Database.AbstractModels.TreeModel import TreeModel
from App.Database.Lookup import department_lookup
from App.Database.Lookup import event_lookup
from App.Database.Lookup import item_salable_lookup
from App.Database.Lookup import item_all_lookup
from App.Core.L10n import _tr


UPDATED, INSERTED, DELETED = range(3)


class MenuItemTreeModel(TreeModel):

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.table = "system.menu_toolbar_item"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("parent", _tr('Models', 'Menu'), False, 'str'),
                        ("child", _tr('Models', 'User description'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("sorting", _tr('Models', 'Sorting'), False, 'int'),
                        ("item_type", _tr('Models', 'Item type'), False, 'str'),
                        ("action", _tr('Models', 'Action'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # primary key fields, tuple or list
        self.primaryKey = ("parent", "child")
        self.parentField = "parent"
        self.parentFieldColumn = 0
        self.childField = "child"
        self.childFieldColumn = 1
        self.repr = 'Menu item tree model'


class ToolbarItemTreeModel(TreeModel):

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.table = "system.menu_toolbar_item"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("parent", _tr('Models', 'Menu'), False, 'str'),
                        ("child", _tr('Models', 'User description'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("sorting", _tr('Models', 'Sorting'), False, 'int'),
                        ("item_type", _tr('Models', 'Item type'), False, 'str'),
                        ("action", _tr('Models', 'Action'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # primary key fields, tuple or list
        self.primaryKey = ("parent", "child")
        self.parentField = "parent"
        self.parentFieldColumn = 0
        self.childField = "child"
        self.childFieldColumn = 1
        self.repr = 'Toolbar item tree model'


class ConnectionModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    a.session_id,
    a.access_date,
    a.db_user_name,
    a.app_user_code,
    a.client_name,
    a.client_ip,
    a.client_port,
    a.company_id,
    b.description,
    a.profile_code
FROM system.connection a
LEFT JOIN system.company b ON a.company_id = b.company_id;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("a.session_id", _tr('Models', 'Session ID'), True, 'int'),
                        ("a.access_date", _tr('Models', 'Access Date'), True, 'datetime'),
                        ("a.db_user_name", _tr('Models', 'Database User'), True, 'str'),
                        ("a.app_user_code", _tr('Models', 'Application User'), True, 'str'),
                        ("a.client_name", _tr('Models', 'Client name'), True, 'str'),
                        ("a.client_ip", _tr('Models', 'Client IP'), True, 'str'),
                        ("a.client_port", _tr('Models', 'Client Port'), True, 'int'),
                        ("a.company_id", _tr('Models', 'Company'), True, 'int'),
                        ("b.description", _tr('Models', 'Company Description'), True, 'str'),
                        ("a.profile_code", _tr('Models', 'Profile'), True, 'str')) 
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Connection query model'
        self.addOrderBy('a.access_date DESC')


class ConnectionHistoryModel(QueryModel):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    history_id,
    session_id,
    login_datetime,
    logout_datetime,
    db_user_name,
    app_user_code,
    client_name,
    client_ip,
    client_port,
    company_desc,
    profile_code
FROM system.connection_history;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, float, str, date, datetime, None = no filter
        self.columns = (("history_id", _tr('Models', 'History ID'), True, 'int'),
                        ("session_id", _tr('Models', 'Session ID'), True, 'int'),
                        ("login_datetime", _tr('Models', 'Login Date'), True, 'datetime'),
                        ("logout_datetime", _tr('Models', 'Logout Date'), True, 'datetime'),
                        ("db_user_name", _tr('Models', 'Database User'), True, 'str'),
                        ("app_user_code", _tr('Models', 'Application User'), True, 'str'),
                        ("client_name", _tr('Models', 'Client name'), True, 'str'),
                        ("client_ip", _tr('Models', 'Client IP'), True, 'str'),
                        ("client_port", _tr('Models', 'Client Port'), True, 'int'),
                        ("company_desc", _tr('Models', 'Company Description'), True, 'str'),
                        ("profile_code", _tr('Models', 'Profile'), True, 'str'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Connection history query model'
        self.addOrderBy(('login_datetime DESC', 'session_id'))
        

class CompanyIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    company_id,
    description,
    is_system_object,
    company_image,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.company;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("company_id", _tr('Models', 'Company ID'), True, 'int'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("company_image", _tr('Models', 'Picture'), False, None),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Company index query model'
        self.addOrderBy('company_id ASC')
        

class CompanyModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.company"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("company_id", _tr('Models', 'Company ID'), True, 'int'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("company_image", _tr('Models', 'Picture'), False, None),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # is_system column
        self.isSystemColumn = 2
        # primary key fields, tuple or list
        self.primaryKey = ("company_id",)
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy('company_id')
        self.repr = 'Company table model'


class UserIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    user_code,
    description,
    user_image,
    is_system_object,
    is_admin,
    can_edit_views,
    can_edit_sortfilters,
    can_edit_reports,
    l10n,
    last_login,
    last_company_desc,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.app_user;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("user_code", _tr('Models', 'User'), False, 'str'),
                        ("description", _tr('Models', 'User description'), False, 'str'),
                        ("user_image", _tr('Models', 'Image'), False, None),
                        ("is_system_object", _tr('Models', 'System user'), True, 'bool'),
                        ("is_admin", _tr('Models', 'Administrator'), False, 'bool'),
                        ("can_edit_views", _tr('Models', 'Can edit views'), False, 'bool'),
                        ("can_edit_sortfilters", _tr('Models', 'Can edit sortfilters'), False, 'bool'),
                        ("can_edit_reports", _tr('Models', 'Can edit reports'), False, 'bool'),
                        ("l10n", _tr('Models', 'Language'), False, 'str'),
                        ("last_login", _tr('Models', 'Last login'), True, 'datetime'),
                        ("last_company_desc", _tr('Models', 'Last company'), True, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'User index query model'
        self.addOrderBy('user_code ASC')
        

class UserModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.app_user"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("user_code", _tr('Models', 'User'), False, 'str'),
                        ("description", _tr('Models', 'User description'), False, 'str'),
                        ("user_image", _tr('Models', 'Image'), False, None),
                        ("user_password", _tr('Models', 'Password'), False, 'str'),
                        ("password_date", _tr('Models', 'Last change'), True, 'datetime'),
                        ("new_password_required", _tr('Models', 'Force password change'), False, 'bool'),
                        ("is_system_object", _tr('Models', 'System user'), True, 'bool'),
                        ("is_admin", _tr('Models', 'Administrator'), False, 'bool'),
                        ("can_edit_views", _tr('Models', 'Can edit views'), False, 'bool'),
                        ("can_edit_sortfilters", _tr('Models', 'Can edit sortfilters'), False, 'bool'),
                        ("can_edit_reports", _tr('Models', 'Can edit reports'), False, 'bool'),
                        ("l10n", _tr('Models', 'Language'), False, 'str'),
                        ("last_company_desc", _tr('Models', 'Last company'), True, 'str'),
                        ("last_login", _tr('Models', 'Last login'), True, 'datetime'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date')) 
        # True if is a company table
        self.isCompanyTable = False
        # is_system
        self.isSystemColumn = 6
        # primary key fields, tuple or list
        self.primaryKey = ("user_code",)
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("is_system_object DESC")
        self.addOrderBy("user_code")
        self.repr = 'User table model'


class UserCompanyModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.app_user_company"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("company_id", _tr('Models', 'Company ID'), False, 'int'),
                        ("app_user_code", _tr('Models', 'User'), False, 'str'),
                        ("profile_code", _tr('Models', 'Profile'), False, 'str'),
                        ("menu_code", _tr('Models', 'Menu'), False, 'str'),
                        ("toolbar_code", _tr('Models', 'Toolbar'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # primary key fields, tuple or list
        self.primaryKey = ("app_user_code", "company_id")
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("company_id")
        self.addOrderBy("app_user_code")
        self.repr = 'User company table model'


class UserCompanyModelReferenceCompany(UserCompanyModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        # master/detail relation {table column: reference field}
        self.foreignKey = {'company_id': 'company_id'}
        self.repr = 'User company model by company'


class UserCompanyModelReferenceUser(UserCompanyModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        # master/detail relation {table column: reference field}
        self.foreignKey = {'app_user_code': 'app_user_code'}
        self.repr = 'User company model by user'


class ProfileIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    profile_code,
    description,
    is_system_object,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.profile;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("profile_code", _tr('Models', 'Profile'), True, 'int'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Profile index query model'
        self.addOrderBy('profile_code ASC')
        

class ProfileModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.profile"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("profile_code", _tr('Models', 'Profile'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # is_system
        self.isSystemColumn = 2
        # primary key fields, tuple or list
        self.primaryKey = ("profile_code",)
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("profile_code")
        self.newRecordDefault = {'profile_code': None, 
                                 'description': '',
                                 'is_system_object': False,
                                 'created_by': '',
                                 'created_at': None,
                                 'updated_by': '',
                                 'updated_at': None}
        self.repr = 'Profile table model'


class ProfileActionModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.profile_action"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("profile_code", _tr('Models', 'Profile'), False, 'str'),
                        ("action", _tr('Models', 'Action'), False, 'str'),
                        ("read", _tr('Models', 'Read'), False, 'bool'),
                        ("write", _tr('Models', 'Write'), False, 'bool'),
                        ("execute", _tr('Models', 'Execute'), False, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # primary key fields, tuple or list
        self.primaryKey = ("profile_code", "action")
        # master/detail relation {table field: reference field}
        self.foreignKey = {'profile_code': 'profile_code'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("action")
        self.repr = 'Profile action table model'


class MenuIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    code,
    description,
    is_system_object,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.menu_toolbar;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("code", _tr('Models', 'Menu'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Menu index query model'
        self.recordType = {'type': 'M'}
        self.addOrderBy('code ASC')
        

class MenuModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.menu_toolbar"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("code", _tr('Models', 'Menu'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # is_system column
        self.isSystemColumn = 2
        # primary key fields, tuple or list
        self.primaryKey = ("code",)
        self.recordType = {'type': 'M'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("code")
        self.repr = 'Menu table model'
        

class ToolbarIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    code,
    description,
    is_system_object,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.menu_toolbar;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("code", _tr('Models', 'Toolbar'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.recordType = {'type': 'T'}
        self.repr = 'Toolbar index querymodel'
        self.addOrderBy('code ASC')
        

class ToolbarModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.menu_toolbar"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("code", _tr('Models', 'Code'), False, 'str'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("is_system_object", _tr('Models', 'System'), True, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date')) 
        # True if is a company table
        self.isCompanyTable = False
        # is_system column
        self.isSystemColumn = 2
        # primary key fields, tuple or list
        self.primaryKey = ("code",)
        self.recordType = {'type': 'T'}
        # sql where clause, plain sql string without WHERE
        #self.sqlWhere = ''
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("code")
        self.repr = 'Toolbar table model'


class ReportIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT
    report_id,
    report_code,
    l10n,
    report_class,
    description,
    is_system_object,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.report;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (
            ("report_id", _tr('Models', 'ID'), True, 'int'),
            ("report_code", _tr('Models', 'Report code'), False, 'str'),
            ("l10n", _tr('Models', 'Localization'), False, 'str'),
            ("report_class", _tr('Models', 'Report class'), False, 'str'),
            ("description", _tr('Models', 'Description'), False, 'str'),
            ("is_system_object", _tr('Models', 'System'), True, 'bool'),
            ("created_by", _tr('Models', 'User Ins'), True, 'str'),
            ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
            ("updated_by", _tr('Models', 'User Update'), True, 'str'),
            ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Report index query model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("report_id, report_code, l10n")
        

class ReportModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.report"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (
            ("report_id", _tr('Models', 'ID'), True, 'int'),
            ("report_code", _tr('Models', 'Report code'), False, 'str'),
            ("l10n", _tr('Models', 'Localization'), False, 'str'),
            ("report_class", _tr('Models', 'Report class'), False, 'str'),
            ("description", _tr('Models', 'Description'), False, 'str'),
            ("xml_data", _tr('Models', 'Report XML definition'), False, None),
            ("is_system_object", _tr('Models', 'System'), True, 'bool'),
            ("created_by", _tr('Models', 'User Ins'), True, 'str'),
            ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
            ("updated_by", _tr('Models', 'User Update'), True, 'str'),
            ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # is_system column
        self.isSystemColumn = 6
        self.primaryKey = ("report_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        #self.addOrderBy(("code, l10n"))
        self.repr = 'Report table model'


class ScriptingIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    script_id,
    class_name,
    method_name,
    trigger,
    description,
    note,
    company_id,
    is_active,
    script,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM system.python_scripting;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (
            ("script_id", _tr('Models', 'ID'), True, 'int'),
            ("class_name", _tr('Models', 'Class name'), False, 'str'),
            ("method_name", _tr('Models', 'Method name'), False, 'str'),
            ("trigger", _tr('Models', 'Trigger'), False, 'str'),
            ("description", _tr('Models', 'Description'), False, 'str'),
            ("note", _tr('Models', 'Note'), False, 'str'),
            ("company_id", _tr('Models', 'Company'), False, 'int'),
            ("is_active", _tr('Models', 'Active'), False, 'bool'),
            ("script", _tr('Models', 'Python script'), False, 'str'),
            ("created_by", _tr('Models', 'User Ins'), True, 'str'),
            ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
            ("updated_by", _tr('Models', 'User Update'), True, 'str'),
            ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        self.repr = 'Scripting index query model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("class_name DESC, method_name, trigger")
        
                
class ScriptingModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "system.python_scripting"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (
            ("script_id", _tr('Models', 'ID'), True, 'int'),
            ("class_name", _tr('Models', 'Class name'), False, 'str'),
            ("method_name", _tr('Models', 'Method name'), False, 'str'),
            ("trigger", _tr('Models', 'Trigger'), False, 'str'),
            ("description", _tr('Models', 'Description'), False, 'str'),
            ("note", _tr('Models', 'Note'), False, 'str'),
            ("company_id", _tr('Models', 'Company'), False, 'int'),
            ("is_active", _tr('Models', 'Active'), False, 'bool'),
            ("is_system_object", _tr('Models', 'System'), False, 'bool'),
            ("script", _tr('Models', 'Python script'), False, 'str'),
            ("created_by", _tr('Models', 'User Ins'), True, 'str'),
            ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
            ("updated_by", _tr('Models', 'User Update'), True, 'str'),
            ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = False
        # is_system column
        self.isSystemColumn = 8
        # primary key fields, tuple or list
        self.primaryKey = ("script_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("class_name, method_name, trigger")
        self.repr = 'Scripting table model'
        

class EventIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    event_id,
    description,
    start_date,
    end_date,
    price_list_id,
    image,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM company.event;"""
        # available types: int, bool, decimal2, str, date, datetime, None"""
        # model columns: (field, description, readonly, type), tuple of tuples
        self.columns = (("event_id", _tr('Models', 'ID'), True, 'int'),
                        ("description", _tr('Models', 'Event description'), False, 'str'),
                        ("start_date", _tr('Models', 'Start date'), False, 'datetime'),
                        ("end_date", _tr('Models', 'End date'), False, 'datetime'),
                        ("price_list_id", _tr('Models', 'Price list'), False, 'int'),
                        ("image", _tr('Models', 'Event image'), False, None),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        self.repr = 'Event index query model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("event_id")


class EventModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.event"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("event_id", _tr('Models', 'ID'), True, 'int'),
                        ("description", _tr('Models', 'Event description'), False, 'str'),
                        ("start_date", _tr('Models', 'Start date'), False, 'datetime'),
                        ("end_date", _tr('Models', 'End date'), False, 'datetime'),
                        ("price_list_id", _tr('Models', 'Price list'), False, 'int'),
                        ("image", _tr('Models', 'Event image'), False, None),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("event_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("start_date DESC")
        self.repr = 'Event table model'


class CashDeskModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.cash_desk"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("cash_desk_id", _tr('Models', 'ID'), True, 'int'),
                        ("computer", _tr('Models', 'Computer name'), False, 'str'),
                        ("cash_desk_description", _tr('Models', 'Cash desk description'), False, 'str'),
                        ("note", _tr('Models', 'Note'), False, 'int'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("cash_desk_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        #self.foreignKey = {'class_id': 'id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("cash_desk_id")
        #self.newRecordDefault = {'is_obsolete': False,
        #                         'is_not_managed': False,
        #                         'is_for_takeaway': True}
        self.repr = 'Cash desk table model'
        

class PrinterIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    printer_class_id,
    description,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM company.printer_class;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        self.columns = (("printer_class_id", _tr('Models', 'ID'), True, 'int'),
                        ("description", _tr('Models', 'Class description'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        self.repr = 'Printer index query model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("printer_class_id")
        

class PrinterModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.printer_class"
        # model columns: (field, description, readonly, type), tuple of tuples
        self.columns = (("printer_class_id", _tr('Models', 'ID'), True, 'int'),
                        ("description", _tr('Models', 'Class description'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("printer_class_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("printer_class_id")
        self.repr = 'Printer table model'
        

class PrinterDetailModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.printer_class_printer"
        self.columns = (("printer_class_printer_id", _tr('Models', 'ID'), True, 'int'),
                        ("printer_class_id", _tr('Models', 'Printer class ID'), False, 'int'),
                        ("computer", _tr('Models', 'Computer'), False, 'str'),
                        ("printer", _tr('Models', 'Printer'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("printer_class_printer_id",)
        self.automaticPKey = True
        # master/detail relation {this table field: reference field}
        self.foreignKey = {'printer_class_id': 'printer_class_id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("printer_class_printer_id")
        self.repr = 'Printer detail table model'
        

class DepartmentModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.department"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("department_id", _tr('Models', 'ID'), True, 'int'),
                        ("description", _tr('Models', 'Department description'), False, 'str'),
                        ("sorting", _tr('Models', 'Sorting'), False, 'int'),
                        ("printer_class_id", _tr('Models', 'Printer class'), False, 'str'),
                        ("is_obsolete", _tr('Models', 'Obsolete'), False, 'bool'),
                        ("is_menu_container", _tr('Models', 'Menu'), False, 'bool'),
                        ("is_for_takeaway", _tr('Models', 'For takeaway'), False, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("department_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        #self.foreignKey = {'class_id': 'id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("department_id")
        self.newRecordDefault = {'is_obsolete': False,
                                 'is_menu_container': False,
                                 'is_for_takeaway': True}
        self.repr = 'Department table model'
        

class SeatMapModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.seat_map"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("seat_map_id", _tr('Models', 'ID'), True, 'int'),
                        ("table_code", _tr('Models', 'Table code'), False, 'str'),
                        ("pos_row", _tr('Models', 'Row'), False, 'int'),
                        ("pos_column", _tr('Models', 'Column'), False, 'int'),
                        ("text_color", _tr('Models', 'Text color'), False, 'str'),
                        ("background_color", _tr('Models', 'Background color'), False, 'str'),
                        ("is_unavailable", _tr('Models', 'Unavailable'), False, 'bool'),
                        ("is_obsolete", _tr('Models', 'Obsolete'), False, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("seat_map_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("seat_map_id")
        self.repr = 'Seat map table model'


class ItemIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    item_id,
    item_type,
    description,
    department_id,
    sorting,
    pos_row,
    pos_column,
    normal_text_color,
    normal_background_color,
    has_inventory_control,
    has_delivered_control,
    has_variants,
    is_kit_part,
    is_menu_part,
    is_salable,
    is_web_available,
    web_sorting,
    is_obsolete,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM company.item;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        self.columns = (("item_id", _tr('Models', 'ID'), False, 'int'),
                        ("item_type", _tr('Models', 'Item type'), False, 'str'),
                        ("description", _tr('Models', 'Item description'), False, 'str'),
                        ("department_id", _tr('Models', 'Department'), False, 'int'),
                        ("sorting", _tr('Models', 'Sorting'), False, 'int'),
                        ("pos_row", _tr('Models', 'Row'), False, 'int'),
                        ("pos_column", _tr('Models', 'Column'), False, 'int'),
                        ("normal_text_color", _tr('Models', 'Text color'), False, 'str'),
                        ("normal_background_color", _tr('Models', 'Background color'), False, 'str'),
                        ("has_inventory_control", _tr('Models', 'Inventory control'), False, 'bool'),
                        ("has_delivered_control", _tr('Models', 'Delivered control'), False, 'bool'),
                        ("has_variants", _tr('Models', 'Variants'), False, 'bool'),
                        ("is_kit_part", _tr('Models', 'Kit part'), False, 'bool'),
                        ("is_menu_part", _tr('Models', 'Menu part'), False, 'bool'),
                        ("is_salable", _tr('Models', 'Salable'), False, 'bool'),
                        ("is_web_available", _tr('Models', 'Web available'), False, 'bool'),
                        ("web_sorting", _tr('Models', 'Web sorting'), False, 'int'),
                        ("is_obsolete", _tr('Models', 'Obsolete'), False, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        self.repr = 'Item index query model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy(("item_id", "item_type", "description"))
        # reference fields dictionary
        self.reference = {'department_id': department_lookup}


class ItemModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.item"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("item_id", _tr('Models', 'ID'), False, 'int'),
                        ("item_type", _tr('Models', 'Item type'), False, 'str'),
                        ("description", _tr('Models', 'Item description'), False, 'str'),
                        ("customer_description", _tr('Models', 'Item description for customer'), False, 'str'),
                        ("department_id", _tr('Models', 'Department'), False, 'int'),
                        ("sorting", _tr('Models', 'Sorting'), False, 'int'),
                        ("pos_row", _tr('Models', 'Row'), False, 'int'),
                        ("pos_column", _tr('Models', 'Column'), False, 'int'),
                        ("normal_text_color", _tr('Models', 'Text color'), False, 'str'),
                        ("normal_background_color", _tr('Models', 'Background color'), False, 'str'),
                        ("has_inventory_control", _tr('Models', 'Inventory control'), False, 'bool'),
                        ("has_delivered_control", _tr('Models', 'Delivered control'), False, 'bool'),
                        ("has_variants", _tr('Models', 'Variants'), False, 'bool'),
                        ("is_kit_part", _tr('Models', 'Kit part'), False, 'bool'),
                        ("is_menu_part", _tr('Models', 'Menu part'), False, 'bool'),
                        ("is_salable", _tr('Models', 'Salable'), False, 'bool'),
                        ("is_web_available", _tr('Models', 'Web available'), False, 'bool'),
                        ("web_sorting", _tr('Models', 'Web sorting'), False, 'int'),
                        ("is_obsolete", _tr('Models', 'Obsolete'), False, 'bool'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("item_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("item_id")
        # reference fields dictionary
        self.reference = {'department': department_lookup}
        self.repr = 'Item table model'


class ItemVariantModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.item_variant"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("item_variant_id", _tr('Models', 'ID'), False, 'int'),
                        ("item_id", _tr('Models', 'Item'), False, None),
                        ("variant_description", _tr('Models', 'Variant description'), False, 'str'),
                        ("sorting", _tr('Models', 'Sorting'), False, 'int'),
                        ("price_delta", _tr('Models', 'Price delta'), False, 'decimal2'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("item_variant_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        self.foreignKey = {'item_id': 'item_id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("item_variant_id")
        self.addOrderBy("sorting")
        self.repr = 'Item variant table model'


class KitPartModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.item_part"
        self.recordType = {'item_type': 'K'}
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("item_part_id", _tr('Models', 'ID'), False, 'int'),
                        ("item_id", _tr('Models', 'Kit'), False, 'int'),
                        ("part_id", _tr('Models', 'Part'), False, 'int'),
                        ("quantity", _tr('Models', 'Quantity'), False, 'int'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("item_part_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        self.foreignKey = {'item_id': 'id', 'part_id': 'id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("item_part_id")
        self.repr = 'Kit part table model'


class MenuPartModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.item_part"
        self.recordType = {'item_type': 'M'}
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("item_part_id", _tr('Models', 'ID'), False, 'int'),
                        ("item_id", _tr('Models', 'Menu'), False, 'int'),
                        ("part_id", _tr('Models', 'Part'), False, 'int'),
                        ("quantity", _tr('Models', 'Quantity'), False, 'int'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("item_part_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        self.foreignKey = {'item_id': 'id', 'part_id': 'id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("item_part_id")
        self.repr = 'Menu part table model'


class PriceListIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    price_list_id,
    description,
    created_by,
    created_at,
    updated_by,
    updated_at
FROM company.price_list;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        self.columns = (("price_list_id", _tr('Models', 'ID'), False, 'int'),
                        ("description", _tr('Models', 'Price list description'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        self.repr = 'Price list index query model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("price_list_id")


class PriceListModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.price_list"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("price_list_id", _tr('Models', 'ID'), False, 'int'),
                        ("description", _tr('Models', 'Description'), False, 'str'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("price_list_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("price_list_id")
        self.repr = 'Price list table model'


class PriceListItemModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.price_list_item"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("price_list_item_id", _tr('Models', 'ID'), False, 'int'),
                        ("price_list_id", _tr('Models', 'Price list'), False, 'int'),
                        ("item_id", _tr('Models', 'Item'), False, 'int'),
                        ("price", _tr('Models', 'Price'), False, 'decimal2'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("price_list_item_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        self.foreignKey = {'price_list_id': 'price_list_item_id', 'item_id': 'id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("price_list_item_id")
        # reference fields dictionary
        self.reference = {'item': item_salable_lookup}
        # list of items for sorting by description
        self.itemDescription = {k:v for k, v in item_all_lookup()}
        self.repr = 'Price list item table model'

    def sort(self, column, order=Qt.AscendingOrder):
        "Custom inplace sorting of the model for item description"
        if column != 2: # not item column
            super().sort(column, order=Qt.AscendingOrder)
            return
        # inplace list sorting
        if order == Qt.AscendingOrder:
            self.dataSet.sort(key=lambda x: self.itemDescription[x[2]])
        else:
            self.dataSet.sort(key=lambda x: self.itemDescription[x[2]], reverse=True)
        # notify about changes
        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount(), self.columnCount()))
        
        
class OrderNumberingModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.numbering"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("numbering_id", _tr('Models', 'ID'), True, 'int'),
                        ("event_id", _tr('Models', 'Event'), False, 'int'),
                        ("event_date", _tr('Models', 'Event date'), False, 'date'),
                        ("day_part", _tr('Models', 'Day part'), False, 'str'),
                        ("current_value", _tr('Models', 'Current value'), False, 'int'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("numbering_id",)
        self.automaticPKey = True
        # master/detail relation {table field: reference field}
        #self.foreignKey = {'class_id': 'id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("numbering_id")
        #self.newRecordDefault = {'is_obsolete': False,
        #                         'is_not_managed': False,
        #                         'is_for_takeaway': True}
        self.repr = 'Order numbering table model'


class InventoryModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.inventory"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("inventory_id", _tr('Models', 'ID'), True, 'int'),
                        ("event_id", _tr('Models', 'Event'), False, 'int'),
                        ("item_id", _tr('Models', 'Item'), False, 'int'),
                        ("loaded", _tr('Models', 'Load'), False, 'decimal2'),
                        ("unloaded", _tr('Models', 'Unload'), True, 'decimal2'),
                        ("stock", _tr('Models', 'Stock'), True, 'decimal2'),
                        ("ordered", _tr('Models', 'Ordered'), True, 'decimal2'),
                        ("available", _tr('Models', 'Available'), True, 'decimal2'),
                        (None, _tr('Models', 'New stock'), False, 'decimal2'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("inventory_id",)
        self.automaticPKey = True
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("inventory_id")
        self.newRecordDefault = {'loaded': 0,
                                 'unloaded': 0,
                                 'stock': 0,
                                 'ordered': 0}
        self.repr = 'Items inventory table model'


class KitAvailabilityModel(QueryWithParamsModel):
    
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    item_id,
    item_description,
    available
FROM company.vw_item_availability
WHERE company_id = system.pa_current_company()
    AND item_type = 'K' 
    AND event_id = %(event)s
ORDER BY item_description;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, float, str, date, datetime, None = no filter
        self.columns = (("item", _tr('Models', 'Kit ID'), True, 'int'),
                        ("description", _tr('Models', 'Kit description'), True, 'str'),
                        ("available", _tr('Models', 'Available'), True, 'decimal2'))
        self.repr = 'Kit availability query with params model'
        

class MenuAvailabilityModel(QueryWithParamsModel):
    
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    item_id,
    item_description,
    available
FROM company.vw_item_availability
WHERE company_id = system.pa_current_company()
    AND item_type = 'M' 
    AND event_id = %(event)s
ORDER BY item_description;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, float, str, date, datetime, None = no filter
        self.columns = (("item", _tr('Models', 'Menu ID'), True, 'int'),
                        ("description", _tr('Models', 'Menu description'), True, 'str'),
                        ("available", _tr('Models', 'Available'), True, 'decimal2'))
        self.repr = 'Menu availability query with params model'


class ItemsOrderedDeliveredModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    s.event_id,
    s.event_date,
    s.day_part,
    s.item_id,
    i.description,
    s.ordered,
    s.delivered
FROM ordered_delivered s
JOIN item i ON s.item_id = i.item_id;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("s.event_id", _tr('Models', 'Event'), False, 'int'),
                        ("s.event_date", _tr('Models', 'Event date'), False, 'date'),
                        ("s.day_part", _tr('Models', 'L/D'), True, 'str'),
                        ("s.item_id", _tr('Models', 'Item'), False, 'int'),
                        ("i.description", _tr('Models', 'Item description'), True, 'str'),
                        ("s.ordered", _tr('Models', 'Ordered'), True, 'decimal2'),
                        ("s.delivered", _tr('Models', 'Delivered'), True, 'decimal2'))
        self.isCompanyTable = True
        self.companyField = 's.company_id'
        # reference fields dictionary
        self.reference = {'s.event_id': event_lookup}
        self.repr = 'Items ordered/delivered query model'


class OrderStatusModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT
	company_id,
	company_description,
	event_id,
	event_description,
	order_header_id,
	order_date,
    stat_order_date,
	stat_order_day_part,
	order_time,
	order_number,
	delivery,
	table_number,
	customer_name,
	covers,
	status,
	fulfillment_date,
    cash_desk,
    user_ins,
	from_web,
	department1,
	fulfillment1,
	department2,
	fulfillment2,
	department3,
	fulfillment3,
	department4,
	fulfillment4,
	department5,
	fulfillment5,
	department6,
	fulfillment6   
FROM company.vw_order_status;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        self.columns = (("company_id", _tr('Models', 'Company ID'), False, 'int'),
                        ("company_description", _tr('Models', 'Company description'), False, 'str'),
                        ("event_id", _tr('Models', 'Event ID'), False, 'int'),
                        ("event_description", _tr('Models', 'Event description'), False, 'str'),
                        ("order_header_id", _tr('Models', 'Header ID'), False, 'int'),
                        ("order_date", _tr('Models', 'Order date'), False, 'date'),
                        ("stat_order_date", _tr('Models', 'Stat order date'), False, 'date'),
                        ("stat_order_day_part", _tr('Models', 'Stat day part'), False, 'str'),
                        ("order_time", _tr('Models', 'Order time'), False, 'time'),
                        ("order_number", _tr('Models', 'Order number'), False, 'int'),
                        ("delivery", _tr('Models', 'Delivery'), False, 'str'),
                        ("table_number", _tr('Models', 'Table'), False, 'str'),
                        ("customer_name", _tr('Models', 'Customer name'), False, 'str'),
                        ("covers", _tr('Models', 'Covers'), False, 'int'),
                        ("status", _tr('Models', 'Status'), False, 'str'),
                        ("fulfillment_date", _tr('Models', 'Fulfillment date'), False, 'date'),
                        ("cash_desk", _tr('Models', 'Cash desk'), False, 'str'),
                        ("user_ins", _tr('Models', 'User ins'), False, 'str'),
                        ("from_web", _tr('Models', 'From web'), False, 'bool'),
                        ("department1", _tr('Models', 'Department 1'), False, 'str'),
                        ("fulfillment1", _tr('Models', 'Fulfillment 1'), False, 'date'),
                        ("department2", _tr('Models', 'Department 2'), False, 'str'),
                        ("fulfillment2", _tr('Models', 'Fulfillment 2'), False, 'date'),
                        ("department3", _tr('Models', 'Department 3'), False, 'str'),
                        ("fulfillment3", _tr('Models', 'Fulfillment 3'), False, 'date'),
                        ("department4", _tr('Models', 'Department 4'), False, 'str'),
                        ("fulfillment4", _tr('Models', 'Fulfillment 4'), False, 'date'),
                        ("department5", _tr('Models', 'Department 5'), False, 'str'),
                        ("fulfillment5", _tr('Models', 'Fulfillment 5'), False, 'date'),
                        ("department6", _tr('Models', 'Department 6'), False, 'str'),
                        ("fulfillment6", _tr('Models', 'Fulfillment 6'), False, 'date'))
                        
        # True if is a company table
        self.isCompanyTable = True
        self.repr = 'Order status query model'
        # reference fields dictionary
        self.reference = {'event_id': event_lookup}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy(("event_id", "order_date", "order_time"))


class SalesSummaryModel(QueryWithParamsModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
        SELECT 
            event_id,
            event_description,
            order_date,
            num_orders_lunch,
            num_orders_dinner,
            num_orders_lunch + num_orders_dinner AS num_orders,
            num_covers_lunch,
            num_covers_dinner,
            num_covers_lunch + num_covers_dinner AS num_covers,
            take_away_lunch,
            take_away_dinner,
            take_away_lunch + take_away_dinner AS tot_take_away,
            table_lunch,
            table_dinner,
            table_lunch + table_dinner AS table,
            amount_lunch,
            amount_dinner,
            amount_lunch + amount_dinner AS amount,
            discount_lunch,
            discount_dinner,
            discount_lunch + discount_dinner AS discount,
            electronic_lunch,
            electronic_dinner,
            electronic_lunch + electronic_dinner AS electronic,
            cash_lunch,
            cash_dinner,
            cash_lunch + cash_dinner AS cash,
            total_lunch AS total_lunch,
            total_dinner AS total_dinner,
            total_lunch + total_dinner AS total
        FROM vw_sales_summary
        WHERE event_id = %(event_id)s;
        """
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, float, str, date, datetime, None = no filter
        self.columns = (("event_id", _tr('Models', 'Event'), True, 'int'),
                        ("event_description", _tr('Models', 'Event description'), True, 'str'),
                        ("order_date", _tr('Models', 'Date'), True, 'date'),
                        ("num_orders_lunch", _tr('Models', 'Orders L'), True, 'int'),
                        ("num_orders_dinner", _tr('Models', 'Orders D'), True, 'int'),
                        ("num_orders", _tr('Models', 'Orders'), True, 'int'),
                        ("num_covers_lunch", _tr('Models', 'Covers L'), True, 'int'),
                        ("num_covers_dinner", _tr('Models', 'Covers D'), True, 'int'),
                        ("num_covers", _tr('Models', 'Covers'), True, 'int'),
                        ("take_away_lunch", _tr('Models', 'Take away L'), True, 'int'),
                        ("take_away_dinner", _tr('Models', 'Take away D'), True, 'int'),
                        ("take_away", _tr('Models', 'Take away'), True, 'int'),
                        ("table_lunch", _tr('Models', 'Table L'), True, 'int'),
                        ("table_dinner", _tr('Models', 'Table D'), True, 'int'),
                        ("table", _tr('Models', 'Table'), True, 'int'),
                        ("amount_lunch", _tr('Models', 'Total amount L'), True, 'decimal2'),
                        ("amount_dinner", _tr('Models', 'Total amount D'), True, 'decimal2'),
                        ("amount", _tr('Models', 'Total amount'), True, 'decimal2'),
                        ("discount_lunch", _tr('Models', 'Discount L'), True, 'decimal2'),
                        ("discount_dinner", _tr('Models', 'Discount D'), True, 'decimal2'),
                        ("discount", _tr('Models', 'Discount'), True, 'decimal2'),
                        ("electronic_lunch", _tr('Models', 'Total electronic L'), True, 'decimal2'),
                        ("electronic_dinner", _tr('Models', 'Total electronic D'), True, 'decimal2'),
                        ("electronic", _tr('Models', 'Total electronic'), True, 'decimal2'),
                        ("cash_lunch", _tr('Models', 'Total cash L'), True, 'decimal2'),
                        ("cash_dinner", _tr('Models', 'Total cash D'), True, 'decimal2'),
                        ("cash", _tr('Models', 'Total cash'), True, 'decimal2'),
                        ("total_lunch", _tr('Models', 'Total L'), True, 'decimal2'),
                        ("total_dinner", _tr('Models', 'Total D'), True, 'decimal2'),
                        ("total", _tr('Models', 'Total'), True, 'decimal2'))
        self.repr = 'Sales summary query with params model'
        
    def rowCount(self, index=QModelIndex()):
        # add 1 row for totals
        return QueryWithParamsModel.rowCount(self) + 1

    def data(self, index, role=Qt.DisplayRole):
        "Totals on last row"
        if index.row() == QueryWithParamsModel.rowCount(self): # last row
            if role == Qt.FontRole:
                font = QFont()
                font.setBold(True)
                return font
            if role == Qt.TextAlignmentRole:
                return Qt.AlignRight | Qt.AlignVCenter
            if role == Qt.DisplayRole:
                if index.column() == 1:
                    return _tr('Models', "TOTAL")
                elif 3 <= index.column() <= len(self.columns):
                    s = sum([self.dataSet[i, index.column()] for i in range(index.row())])
                    return s
        else:
            return QueryWithParamsModel.data(self, index, role)


class OrderHeaderIndexModel(QueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.selectQuery = """
SELECT 
    h.order_header_id,
    h.event_id,
	e.description AS event_description,
    h.date_time,
    h.order_number,
    h.order_date,
    h.order_time,
    h.stat_order_date,
    h.stat_order_day_part,
    h.cash_desk,
    h.delivery,
    h.is_electronic_payment,
    h.is_from_web,
    h.table_num,
    h.customer_name,
    h.covers,
    h.total_amount,
    h.discount,
    h.cash,
    h.change,
    h.status,
    h.fulfillment_date,
    h.created_by,
    h.created_at,
    h.updated_by,
    h.updated_at
FROM order_header h
JOIN event e ON h.event_id = e.event_id;"""
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal, str, date, datetime, time, None = no filter
        self.columns = (("h.order_header_id", _tr('Models', 'ID'), True, 'int'),
                        ("h.event_id", _tr('Models', 'Event'), True, 'int'),
                        ("e.event_description", _tr('Models', 'Event description'), True, 'str'),
                        ("h.date_time", _tr('Models', 'Order date/time'), True, 'datetime'),
                        ("h.order_number", _tr('Models', 'Order number'), True, 'int'),
                        ("h.order_date", _tr('Models', 'Order date'), True, 'date'),
                        ("h.order_time", _tr('Models', 'Order time'), True, 'time'),
                        ("h.stat_order_date", _tr('Models', 'Stat order date'), True, 'date'),
                        ("h.stat_order_day_part", _tr('Models', 'Stat order day part'), True, 'str'),
                        ("h.cash_desk", _tr('Models', 'Cash desk'), True, 'str'),
                        ("h.delivery", _tr('Models', 'Delivery'), True, 'str'),
                        ("h.is_electronic_payment", _tr('Models', 'EP'), True, 'bool'),
                        ("h.is_from_web", _tr('Models', 'WO'), True, 'bool'),
                        ("h.table_num", _tr('Models', 'Table'), True, 'str'),
                        ("h.customer_name", _tr('Models', 'Customer name'), True, 'str'),
                        ("h.covers", _tr('Models', 'Covers'), True, 'int'),
                        ("h.total_amount", _tr('Models', 'Total amount'), True, 'decimal'),
                        ("h.discount", _tr('Models', 'Discount'), True, 'decimal'),
                        ("h.cash", _tr('Models', 'Cash'), True, 'decimal'),
                        ("h.change", _tr('Models', 'Change'), True, 'decimal'),
                        ("h.status", _tr('Models', 'Status'), True, 'str'),
                        ("h.fulfillment_date", _tr('Models', 'Fulfillment date'), True, 'date'),
                        ("h.created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("h.created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("h.updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("h.updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        self.companyField = "h.company_id"
        # class representation
        self.repr = 'Order header index query model'
        # limit number of rows fetched
        self.addLimit(10_000)
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("h.order_header_id")
        # reference fields dictionary
        self.reference = {'h.event_id': event_lookup}


class OrderHeaderModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.order_header"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("order_header_id", _tr('Models', 'ID'), True, 'int'),
                        ("event_id", _tr('Models', 'Event'), True, 'int'),
                        ("date_time", _tr('Models', 'Order date/time'), False, 'date'),
                        ("order_number", _tr('Models', 'Order number'), False, 'int'),
                        ("order_date", _tr('Models', 'Order date'), False, 'date'),
                        ("order_time", _tr('Models', 'Order time'), False, 'time'),
                        ("stat_order_date", _tr('Models', 'Stat order date'), False, 'date'),
                        ("stat_order_day_part", _tr('Models', 'Stat order day part'), False, 'str'),
                        ("cash_desk", _tr('Models', 'Cash desk'), False, 'str'),
                        ("delivery", _tr('Models', 'Delivery'), False, 'str'),
                        ("is_electronic_payment", _tr('Models', 'EP'), False, 'bool'),
                        ("is_from_web", _tr('Models', 'FW'), False, 'bool'),
                        ("table_num", _tr('Models', 'Table'), False, 'str'),
                        ("customer_name", _tr('Models', 'Customer name'), False, 'str'),
                        ("customer_contact", _tr('Models', 'Customer contact'), False, 'str'),
                        ("covers", _tr('Models', 'Covers'), False, 'int'),
                        ("total_amount", _tr('Models', 'Total amount'), False, 'decimal2'),
                        ("discount", _tr('Models', 'Discount'), False, 'decimal2'),
                        ("cash", _tr('Models', 'Cash'), False, 'decimal2'),
                        ("change", _tr('Models', 'Change'), False, 'decimal2'),
                        ("status", _tr('Models', 'Status'), False, 'str'),
                        ("fulfillment_date", _tr('Models', 'Fulfillment date'), False, 'date'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("order_header_id",)
        self.automaticPKey = True
        # class representation
        self.repr = 'Order header table model'
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("order_header_id")
        # reference fields dictionary
        self.reference = {'event': event_lookup}


class OrderHeaderDepartmentModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.order_header_department"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("order_header_department_id", _tr('Models', 'ID'), False, 'int'),
                        ("order_header_id", _tr('Models', 'ID header'), False, 'int'),
                        ("department_id", _tr('Models', 'Department'), False, 'int'),
                        ("note", _tr('Models', 'Notes'), False, 'str'),
                        ("other_departments", _tr('Models', 'Other departments'), False, 'str'),
                        ("barcode", _tr('Models', 'Barcode'), False, 'str'),
                        ("fulfillment_date", _tr('Models', 'Fulfillment date'), False, 'date'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("order_header_department_id",)
        self.automaticPKey = True
        # class representation
        self.repr = 'Order header department table model'
        # master/detail relation {table field: reference field}
        self.foreignKey = {'order_header_id': 'order_header_id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("order_header_department_id")


class OrderLineModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.order_line"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("order_line_id", _tr('Models', 'ID'), False, 'int'),
                        ("order_header_id", _tr('Models', 'ID header'), False, 'int'),
                        ("item_id", _tr('Models', 'Item'), False, 'int'),
                        ("variants", _tr('Models', 'Variants'), False, 'str'),
                        ("quantity", _tr('Models', 'Quantity'), False, 'decimal2'),
                        ("price", _tr('Models', 'Price'), False, 'decimal2'),
                        ("amount", _tr('Models', 'Amount'), False, 'decimal2'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("order_line_id",)
        self.automaticPKey = True
        # class representation
        self.repr = 'Order line table model'
        # master/detail relation {table field: reference field}
        self.foreignKey = {'order_header_id': 'order_header_id'}
        # sql order by clause, plain sql string without ORDER BY
        self.addOrderBy("order_line_id")


class OrderLineDepartmentModel(TableModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.table = "company.order_line_department"
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("order_line_department_id", _tr('Models', 'ID'), False, 'int'),
                        ("order_header_department_id", _tr('Models', 'ID header'), False, 'int'),
                        ("event_id", _tr('Models', 'Event'), False, 'int'),
                        ("event_date", _tr('Models', 'Event date'), False, 'date'),
                        ("day_part", _tr('Models', 'Day part'), False, 'str'),
                        ("item_id", _tr('Models', 'Item'), False, 'int'),
                        ("variants", _tr('Models', 'Variants'), False, 'str'),
                        ("quantity", _tr('Models', 'Quantity'), False, 'decimal2'),
                        ("created_by", _tr('Models', 'User Ins'), True, 'str'),
                        ("created_at", _tr('Models', 'Date Ins'), True, 'date'),
                        ("updated_by", _tr('Models', 'User Update'), True, 'str'),
                        ("updated_at", _tr('Models', 'Date Update'), True, 'date'))
        # True if is a company table
        self.isCompanyTable = True
        # primary key fields, tuple or list
        self.primaryKey = ("order_line_department_id",)
        self.automaticPKey = True
        # class representation
        self.repr = 'Order line department table model'  
        # master/detail relation {table field: reference field}
        self.foreignKey = {'order_header_department_id': 'order_header_department_id'}
        # sql order by clause, plain sql string without ORDER BY
        #self.addOrderBy("department_id")
        
        
class OrderDepartmentTreeModel(TreeQueryModel):

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.script = ["""
SELECT 
    d.description                   AS department,
    Null                            AS item,
    Null                            AS variants,
    Null                            AS quantity,
    h.order_header_id               AS parent,
    h.order_header_department_id    AS child
FROM order_header_department h
JOIN department d ON h.department_id = d.department_id
WHERE h.order_header_id = %s;""",
"""
SELECT
    Null                            AS department,
    i.description                   AS item,
    l.variants                      AS variants,
    l.quantity                      AS quantity,
    l.order_header_department_id    AS parent,
    l.order_line_department_id      AS child
FROM order_line_department l
JOIN item i ON l.item_id = i.item_id
WHERE l.order_header_department_id = %s;""",
"""
SELECT Null
WHERE Null = %s;"""]
        # model columns: (field, description, readonly, type), tuple of tuples
        # available types: int, bool, decimal2, str, date, datetime, None = no filter
        self.columns = (("department", _tr('Models', 'Department'), False, 'str'),
                        ("item", _tr('Models', 'Item'), False, 'str'),
                        ("variants", _tr('Models', 'Variants'), False, 'str'),
                        ("quantity", _tr('Models', 'Quantity'), False, 'decimal'),
                        ("parent", _tr('Models', 'Header ID'), True, 'int'),
                        ("child", _tr('Models', 'Header department ID'), True, 'int'))
        self.parentField = "parent"
        self.parentFieldColumn = 4
        self.childField = "child"
        self.childFieldColumn = 5
        # class representation
        self.repr = 'Order department tree query model'  
    

# class OrderHeaderPandasModel(PandasModel):
    
#     def __init__(self, parent: QObject|None = None) -> None: 
#         super().__init__(parent)
#         self.table = "company.bi_order_header"
#         # model columns: {field: (description, pivot value, pivot axis, type, format)}, dict
#         # available types are pandas dtype: 
#         # int64, boolean, float64, string, datetime64[ns], None (=auto/generic object)
#         # available formats:
#         # int (0 decimal, right aligned), decimal2 (2 decimals, right aligned), 
#         # str (left aligned), bool (centered), 
#         # date (locale date), datetime (locale date time), time (locale time), None = no specific format
#         self.columns = {#"company_id": (_tr('Models', 'Company ID'), False, 'int64', 'int'),
#                         "event": (_tr('Models', 'Event'), False, True, 'string', 'int'),
#                         "order_number": (_tr('Models', 'Order number'), False, True, 'int64', 'int'),
#                         "order_date": (_tr('Models', 'Order date'), False, True, 'datetime64[ns]', 'date'),
#                         "order_time": (_tr('Models', 'Order time'), False, True, 'datetime64[ns]', 'time'),
#                         "order_date_time": (_tr('Models', 'Order date time'), False, True, 'datetime64[ns]', 'datetime'),
#                         "fulfillment_date": (_tr('Models', 'Fulfilment date'), False, True, 'datetime64[ns]', 'datetime'),
#                         "stat_order_date": (_tr('Models', 'Stat order date'), False, True, 'datetime64[ns]', 'date'),
#                         "stat_order_day_part": (_tr('Models', 'Stat order day part'), False, True, 'string', 'str'),
#                         "cash_desk": (_tr('Models', 'Cash desk'), False, True, 'string', 'str'),
#                         "delivery": (_tr('Models', 'Delivery'), False, True, 'string', 'str'),
#                         "payment": (_tr('Models', 'Payment'), False, True, 'string', 'str'),
#                         "web_order": (_tr('Models', 'Web order'), False, True, 'boolean', 'bool'),
#                         "table_num": (_tr('Models', 'Table number'), False, True, 'string', 'str'),
#                         "customer_name": (_tr('Models', 'Customer name'), False, True, 'string', 'str'),
#                         "customer_contact": (_tr('Models', 'Customer contact'), False, True, 'string', 'str'),
#                         "covers": (_tr('Models', 'Covers'), True, False, 'int64', 'int'),
#                         "total_amount": (_tr('Models', 'Total amount'), True, False, 'float64', 'decimal2'),
#                         "discount": (_tr('Models', 'Discount'), True, False, 'float64', 'decimal2'),
#                         "cash": (_tr('Models', 'Cash'), True, False, 'float64')}
#         # True if is a company table
#         self.isCompanyTable = True
#         self.repr = 'Order header pandas model'
        

# class OrderLinePandasModel(PandasModel):
    
#     def __init__(self, parent: QObject|None = None) -> None: 
#         super().__init__(parent)
#         self.table = "company.bi_order_line"
#         # model columns: {field: (description, pivot value, type)}, dict
#         # available types: int, bool, decimal2, str, date, datetime, None = no filter
#         self.columns = {#"company_id": (_tr('Models', 'Company ID'), False, 'int'),
#                         "event": (_tr('Models', 'Event description'), False, True, 'str'),
#                         "order_number": (_tr('Models', 'Order number'), False, True, 'int'),
#                         "order_date": (_tr('Models', 'Order date'), False, True, 'date'),
#                         "order_time": (_tr('Models', 'Order time'), False, True, 'time'),
#                         "stat_order_date": (_tr('Models', 'Stat order date'), False, True, 'date'),
#                         "stat_order_day_part": (_tr('Models', 'Stat order day part'), False, True, 'str'),
#                         "delivery": (_tr('Models', 'Delivery'), False, True, 'str'),
#                         "payment": (_tr('Models', 'Payment'), False, True, 'str'),
#                         "table_number": (_tr('Models', 'Table number'), False, True, 'str'),
#                         "customer_name": (_tr('Models', 'Customer name'), False, True, 'str'),
#                         "department": (_tr('Models', 'Department'), False, True, 'str'),
#                         "item_type": (_tr('Models', 'Item type'), False, True, 'str'),
#                         "item": (_tr('Models', 'Item'), False, True, 'str'),
#                         "variants": (_tr('Models', 'Variants'), False, True, 'str'),
#                         "item_with_variants": (_tr('Models', 'Item with variants'), False, True, 'str'),
#                         "quantity": (_tr('Models', 'Quantity'), True, False, 'int'),
#                         "price": (_tr('Models', 'Price'), True, False, 'decimal2'),
#                         "amount": (_tr('Models', 'Amount'), True, False, 'decimal2')}
#         # True if is a company table
#         self.isCompanyTable = True
#         self.repr = 'Order line pandas model'
        