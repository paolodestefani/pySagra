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
INSERT INTO system.itemview_adapt (description, itemview_class)
VALUES (%s, %s)
RETURNING itemview_adapt_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (view_description, view_class))
                result = cur.fetchone()
                if result:
                    return result[0]
                else:
                    raise PyAppDBError("02000", "No itemview_adapt_id returned from database")
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def list_itemviews(view_class: str) -> list[tuple]:
    "Get available view customizations for class"
    script = """
SELECT 
    itemview_adapt_id, 
    description, 
    is_default_for_class
FROM system.itemview_adapt
WHERE itemview_class = %s
ORDER BY itemview_adapt_id;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (view_class,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_view_columns(view_id: int) -> list[tuple]:
    "Returns the view definition"
    script = """
SELECT 	
    column_number,
    sorting,
    is_visible,
    size
FROM system.itemview_adapt_setting
WHERE itemview_adapt_id = %s
ORDER BY sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (view_id,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_view_columns(view_id: int, columns: list[tuple]) -> None:
    "Set the view definition"
    script = """
INSERT INTO system.itemview_adapt_setting (
    itemview_adapt_id,
    column_number,
    sorting,
    is_visible,
    size)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT itemview_adapt_setting_pk DO
UPDATE SET sorting = %s, is_visible = %s, size = %s;"""
    params = [(view_id, c, p, h, w, p, h, w) for c, p, h, w in columns]
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                # Esecuzione batch: molto più veloce del loop for
                cur.executemany(script, params)
    except psycopg.Error as er:
        # Recuperiamo lo stato SQL se disponibile
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))

def delete_view_layout(view_id: int) -> None:
    "Delete a view customization"
    script = """
DELETE FROM system.itemview_adapt 
WHERE itemview_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (view_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_default_view_layout(view_class: str, view_id: int) -> None:
    "Set default layout for view class"
    script1 = """
UPDATE system.itemview_adapt
SET is_default_for_class = false
WHERE itemview_class = %s;"""
    script2 = """
UPDATE system.itemview_adapt
SET is_default_for_class = true
WHERE itemview_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (view_class,))
                cur.execute(script2, (view_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
