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

"""Sorting and filtering models database management


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
    # get system id
    script1 = """
SELECT coalesce(max(adaptation_id), 0) + 1
FROM system.adaptation
WHERE adaptation_id < 1000;"""
    # insert system object
    script2 = """
INSERT INTO system.adaptation (adaptation_id, type, class, report_id, description)
VALUES (%s, %s, %s, %s, %s)
RETURNING adaptation_id;"""
    # insert non-system object
    script3 = """
INSERT INTO system.adaptation (type, class, report_id, description)
VALUES (%s, %s, %s, %s)
RETURNING adaptation_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                if system:
                    cur.execute(script1)
                    result = cur.fetchone()
                    if result:
                        id = result[0]
                    else:                    
                        raise PyAppDBError('00000', 'Failed to get adaptation_id')
                    cur.execute(script2, (id, adapt_type, adapt_class, report_id, description))
                else:
                    cur.execute(script3, (adapt_type, adapt_class, report_id, description))
                result = next(cur, None)
                if result:
                    return result[0]
                else:                    
                    raise PyAppDBError('00000', 'Failed to create adaptation')
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def delete_adaptation(adapt_id: int) -> None:
    "Delete adaptation of given id"
    # also delete adaptation settings (cascade)
    script1 = """
DELETE FROM system.adaptation
WHERE adaptation_id = %s;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1001),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 100001),
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
    
def clear_adaptation(system: bool = False) -> None:
    "Delete all adaptation"
    # also delete adaptation settings (cascade)
    script1 = f"""
DELETE FROM system.adaptation WHERE adaptation_id {"<" if system else ">"} 1000;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1001),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 100001),
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
    
def export_adaptation(system: bool = False) -> list:
    "List all adaptation records for export"
    # system objects
    script = f""" 
SELECT
    adaptation_id,
    type, 
    class, 
    description, 
    class_sorting, 
    is_default_for_class,
    report_id,
    row_count_limit
FROM system.adaptation
WHERE adaptation_id {"<" if system else ">"} 1000
ORDER BY adaptation_id
"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script)
                return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def export_adaptation_setting(system: bool = False) -> list:
    "List all adaptation_setting records for export"
    script = f""" 
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
WHERE adaptation_setting_id {"<" if system else ">"} 100000
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
DELETE FROM system.adaptation;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1001),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 100001),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    script4 = """
INSERT INTO system.adaptation (
    adaptation_id,
    type,
    class,
    description,
    class_sorting,
    is_default_for_class,
    report_id,
    row_count_limit)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
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
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1)
                cur.execute(script2)
                cur.execute(script3)
                cur.executemany(script4, adaptations)
                cur.executemany(script5, adaptsettings)
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
    # get current id for system objects
    script2 = """
SELECT coalesce(max(adaptation_setting_id), 0) + 1
FROM system.adaptation_setting
WHERE adaptation_setting_id < 100000;"""
    # insert new settings for system objects
    script3 = """
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
    # insert new settings for non-system objects
    script4 = """
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
                if adapt_id < 1000: # system objects
                    cur.execute(script2)
                    result = cur.fetchone()
                    if result:
                        lid = result[0]
                    cur.executemany(script3, [(lid + i,) + tuple(t) for i, t in enumerate(columns)])
                else:
                    cur.executemany(script4, columns)
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
                    return none
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
    #params = [(adaptation_id, c, p, h, w) for c, p, h, w in columns]
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (adaptation_id,))
                cur.executemany(script2, columns)
    except psycopg.Error as er:
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))
