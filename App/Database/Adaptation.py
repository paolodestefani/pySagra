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

"""pySagra - Database adaptation management

This module provides functions to manage adaptations in the database, including
creating, deleting, listing, exporting, importing adaptations and their settings.   

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def create_adaptation(adapt_type: str,
                      adapt_class: str, 
                      description: str, 
                      report_id: int|None = None,
                      system: bool = False) -> int:
    "Create a new adaptation returning the id"
    script = """
INSERT INTO system.adaptation (type, class, description, report_id, is_system_object)
VALUES (%s, %s, %s, %s, %s)
RETURNING adaptation_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_type, adapt_class, description, report_id, system))
                result = next(cur, None)
                if result:
                    return result[0]
                else:                    
                    raise PyAppDBError('00000', 'Failed to create adaptation')
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def is_system_object(adapt_id: int) -> int|None:
    "Check if the adaptation id is a system object"
    script = """
SELECT adaptation_id
FROM system.adaptation
WHERE adaptation_id = %s
    AND is_system_object IS true;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (adapt_id,))
                if cur.rowcount > 0:
                    return True
                else:
                    return False
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def delete_adaptation(adapt_id: int) -> None:
    "Delete adaptation of given id"
    # also delete adaptation settings (cascade)
    script1 = """
DELETE FROM system.adaptation
WHERE adaptation_id = %s
    AND is_system_object = false;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 1),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (adapt_id,))
                cur.execute(script2)
                cur.execute(script3)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def clear_adaptation() -> None:
    "Delete all adaptation"
    # also delete adaptation settings (cascade)
    script1 = """
DELETE FROM system.adaptation;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 1),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    script4 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_user_default', 'adaptation_user_default_id'),
    COALESCE((SELECT max(adaptation_user_default_id) FROM system.adaptation_user_default), 1),
    (SELECT max(adaptation_user_default_id) IS NOT NULL FROM system.adaptation_user_default)
);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                for i in (script1, script2, script3, script4):
                    cur.execute(i)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def list_adaptation(adapt_type: str, adapt_class: str) -> list:
    "Get available adaptations for the given type and class"
    script = """ 
SELECT
    adaptation_id,
    description,
    is_default_for_class
FROM system.adaptation
WHERE type = %s AND class = %s
ORDER BY class_sorting;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_type, adapt_class))
                return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def export_adaptation() -> list:
    "List all adaptation records for export"
    # system objects
    script = """ 
SELECT
    adaptation_id,
    type, 
    class, 
    description, 
    class_sorting, 
    is_default_for_class,
    report_id,
    row_count_limit,
    is_system_object
FROM system.adaptation
ORDER BY adaptation_id
"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script)
                return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def export_adaptation_setting() -> list:
    "List all adaptation_setting records for export"
    script = """ 
SELECT
    adaptation_setting_id,
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value
FROM system.adaptation_setting
ORDER BY adaptation_setting_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script)
                return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def import_adaptation(adaptations: list, adaptsettings: list) -> None:
    "Import all records in adaptation and adaptation_setting tables"
    script1 = """
DELETE FROM system.adaptation;""" # also delete adaptation settings (cascade)
    script2 = """
ALTER TABLE system.adaptation ALTER COLUMN adaptation_id RESTART WITH 1;"""
    script3 = """
ALTER TABLE system.adaptation_setting ALTER COLUMN adaptation_setting_id RESTART WITH 1;"""
    script4 = """
INSERT INTO system.adaptation (
    adaptation_id,
    type,
    class,
    description,
    class_sorting,
    is_default_for_class,
    report_id,
    row_count_limit,
    is_system_object)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    script5 = """
INSERT INTO system.adaptation_setting (
    adaptation_setting_id, 
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    script6 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script7 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 1),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1)
                cur.execute(script2)
                cur.execute(script3)
                cur.executemany(script4, adaptations)
                cur.executemany(script5, adaptsettings)
                cur.execute(script6)
                cur.execute(script7)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_adapt_limit(adapt_id: int) -> int|None:
    "Get row count limit for adaptation_id"
    script = """
SELECT 
    row_count_limit
FROM system.adaptation
WHERE adaptation_id = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (adapt_id,))
            result = next(cur, None)
            if result:
                return result[0]
            else:
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_adapt_limit(adapt_id: int, limit: int|None) -> None:
    "Set row count limit for adaptation_id"
    script = """
UPDATE system.adaptation
SET row_count_limit = %s
WHERE adaptation_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (limit, adapt_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def get_adapt_setting(adapt_id: int) -> tuple[list, list, list]:
    "Get available adaptation settings for the given id"
    script = """
SELECT 
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value
FROM system.adaptation_setting
WHERE adaptation_id = %s
ORDER BY layout_row;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_id,))
                if cur.rowcount == 0:
                    return [], [], []  # no customization
                else:
                    d = cur.fetchall()
                    p = [i for i in d if i[0] == 'P'] # Parameters
                    f = [i for i in d if i[0] == 'F'] # Filters
                    s = [i for i in d if i[0] == 'S'] # Sorting
                    return p, f, s
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_adapt_setting(adapt_id: int, columns: list[tuple]) -> None:
    "Set available adaptation settings for the given id"
    # delete all settings for adapt_id
    script1 = """
DELETE FROM system.adaptation_setting
WHERE adaptation_id = %s;"""
    # insert new settings
    script2 = """
INSERT INTO system.adaptation_setting (
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script1, (adapt_id,))
                cur.executemany(script2, columns)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_adapt_sorting(adapt_id: int) -> int:
    "Returns adaptation sorting index"
    script = """
SELECT class_sorting
FROM system.adaptation
WHERE adaptation_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_id,))
                result = next(cur, None)
                if result:
                    return result[0]
                else:
                    return 0
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_adapt_sorting(adapt_id: int, sorting: int) -> None:
    "Set adaptation sorting index"
    script = """
UPDATE system.adaptation
SET class_sorting = %s
WHERE adaptation_id = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (sorting, adapt_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def get_adapt_class_default(adapt_type: str, adapt_class: str) -> int|None:
    "Get the default adaptation_id for type and class"
    script = """
SELECT adaptation_id
FROM system.adaptation
WHERE type = %s AND class = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (adapt_type, adapt_class))
                result = next(cur, None)
                if result:
                    return result[0]
                else:
                    return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def set_adapt_class_default(adapt_id: int) -> None:
    "Set the adaptation class default for type/class"
    script1 = """
SELECT type, class FROM system.adaptation
WHERE adaptation_id = %s;"""
    script2 = """
UPDATE system.adaptation
SET is_default_for_class = false
WHERE type = %s AND class = %s;"""
    script3 = """
UPDATE system.adaptation
SET is_default_for_class = true
WHERE adaptation_id = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script1, (adapt_id,))
                result = next(cur, None)
                if not result:
                    return None
                adapt_type = result[0]
                adapt_class = result[1]
                cur.execute(script2, (adapt_type, adapt_class))
                cur.execute(script3, (adapt_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def get_adapt_user_default(adapt_type: str, adapt_class: str, user: str) -> int|None:
    "Get the default adaptation if any for type/class/user"
    script = """
SELECT adaptation_id
FROM system.adaptation_user_default
WHERE type = %s AND class = %s AND app_user_code = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (adapt_type, adapt_class, user))
                result = next(cur, None)
                if result:
                    return result[0]
                else:
                    return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def get_adapt_default(adapt_type: str, adapt_class: str, user: str) -> int|None:
    "Get the default adaptation if any for type/class/user or type/class"
    script1 = """
SELECT adaptation_id
FROM system.adaptation_user_default
WHERE type = %s AND class = %s AND app_user_code = %s;"""
    script2 = """
SELECT adaptation_id
FROM system.adaptation
WHERE type = %s AND class = %s AND is_default_for_class IS true;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script1, (adapt_type, adapt_class, user))
                result = next(cur, None)
                if result:
                    return result[0]
                cur.execute(script2, (adapt_type, adapt_class))
                result = next(cur, None)
                if result:
                    return result[0]
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def set_adapt_user_default(adapt_type: str, adapt_class: str, user: str, adapt_id: int) -> None:
    "Set given adaptation the default for user"
    script1 = """
DELETE FROM system.adaptation_user_default 
WHERE type = %s AND class = %s AND app_user_code = %s;"""
    script2 = """
INSERT INTO system.adaptation_user_default (type, class, app_user_code, adaptation_id)
VALUES (%s, %s, %s, %s);"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script1, (adapt_type, adapt_class, user))
                cur.execute(script2, (adapt_type, adapt_class, user, adapt_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_view_columns(adaptation_id: int) -> list[tuple]:
    "Returns the view definition"
    script = """
SELECT 	
    column_number,
    sorting,
    is_visible,
    size
FROM system.adaptation_setting
WHERE adaptation_id = %s
ORDER BY sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (adaptation_id,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_view_columns(adaptation_id: int, columns: list[tuple]) -> None:
    "Set the view definition"
    script1 = """
DELETE FROM system.adaptation_setting
WHERE adaptation_id = %s;"""
    script2 = """
INSERT INTO system.adaptation_setting (
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size)
VALUES (%s, %s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (adaptation_id,))
                cur.executemany(script2, columns)
    except psycopg.Error as er:
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))
