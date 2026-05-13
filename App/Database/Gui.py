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

"""Database - Gui

Database fubctions for GUI management

"""

# standard library
import logging

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def get_actions() -> list[tuple]:
    "Returns all actions definition for current user/profile"
    script = """
SELECT 
    pa.action,
    pa.auth
FROM system.profile_action pa
JOIN system.connection cn ON pa.profile_code = cn.profile_code
JOIN system.app_user u ON cn.app_user_code = u.user_code
WHERE cn.session_id = pg_backend_pid();"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def get_menu(item: str) -> list[tuple]:
    "Returns menu definition from system.menu_toolbar_item"
    script = t"""
SELECT 
    m.child,
    m.item_type,
    m.description,
    m.action
FROM system.menu_toolbar_item m
WHERE m.parent = {item}
ORDER BY m.sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    
    
def get_toolbar(item: str) -> list[tuple]:
    "Returns toolbar definition from system.menu_item"
    script = t"""
SELECT 
    t.child,
    t.item_type,
    t.description,
    t.action
FROM system.menu_toolbar_item t
WHERE t.parent = {item}
ORDER BY t.sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        rlogger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def get_menu_tree(menu: str) -> list[tuple]:
    "Returns actions for given menu"
    script = t"""
SELECT 
    child,
    item_type,
    coalesce(description, ''),
    coalesce(action, '')
FROM system.menu_toolbar m
WHERE
    company_id = system.pa_current_company()
    AND parent = {menu}
ORDER BY sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def set_user_theme(theme: str) -> None:
    "Update last used theme for user"
    script = t"""
UPDATE system.app_user 
SET stylesheet_theme = {theme} 
WHERE id = system.pa_current_user();"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
