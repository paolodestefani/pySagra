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

"""Gui database functions

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


def get_actions() -> list[tuple]:
    "Returns all actions definition for current user/profile"
    try:
        with appconn.cursor() as cur:
            cur.execute("SELECT * FROM system.pa_get_actions()")
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))


def get_menu(item: str) -> list[tuple]:
    "Returns menu definition from system.menu_item"
    try:
        with appconn.cursor() as cur:
            cur.execute("SELECT * FROM system.pa_get_menu(%s)", (item,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    

def get_toolbar(item: str) -> list[tuple]:
    "Returns toolbar definition from system.menu_item"
    try:
        with appconn.cursor() as cur:
            cur.execute("SELECT * FROM system.pa_get_toolbar(%s)", (item,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_menu_tree(menu: str) -> list[tuple]:
    "Returns actions for given menu"
    sql = """
SELECT 
    child,
    item_type,
    coalesce(description, ''),
    coalesce(action, '')
FROM system.menu_toolbar m
WHERE
    company_id = system.pa_current_company()
    parent = %s
ORDER BY sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(sql, (menu,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_user_theme(theme: str) -> None:
    "Update last used theme for user"
    sql = """
UPDATE system.app_user 
SET stylesheet_theme = %s 
WHERE id = system.pa_current_user();"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(sql, (theme,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
