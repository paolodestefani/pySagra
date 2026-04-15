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

"""Itemview database management

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def create_itemview(view_class: str, view_description: str) -> int:
    "Create a new itemview customization"
    script = """
INSERT INTO system.adaptation (type, class, description)
VALUES ('I', %s, %s)
RETURNING adaptation_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (view_class, view_description))
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    raise PyAppDBError("02000", "No adaptation_id returned from database")
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def list_itemviews(view_class: str) -> list[tuple]:
    "Get available view customizations for class"
    script = """
SELECT 
    adaptation_id, 
    description, 
    is_default_for_class
FROM system.adaptation
WHERE type = 'I' AND class = %s
ORDER BY class_sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (view_class,))
            return cur.fetchall()
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

def delete_view_layout(adaptation_id: int) -> None:
    "Delete a view adaptation"
    script = """
DELETE FROM system.adaptation 
WHERE adaptation_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adaptation_id,))
    except psycopg.Error as er:
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))

def set_default_view_layout(view_class: str, view_id: int) -> None:
    "Set default layout for view class"
    script1 = """
UPDATE system.adaptation
SET is_default_for_class = false
WHERE class = %s;"""
    script2 = """
UPDATE system.adaptation
SET is_default_for_class = true
WHERE adaptation_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (view_class,))
                cur.execute(script2, (view_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
