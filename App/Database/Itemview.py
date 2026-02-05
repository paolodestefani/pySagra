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



def create_itemview(view_class, view_description):
    "Create a new itemview customization"
    script = """
INSERT INTO system.itemview_adapt (description, itemview_class)
VALUES (%s, %s)
RETURNING itemview_adapt_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (view_description, view_class))
                return cur.fetchone()[0]
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def list_itemviews(view_class):
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

def get_view_columns(view_id):
    "Returns the view definition"
    script = """""
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

def set_view_columns(view_id, columns):
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
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                for c, p, h, w in columns:
                    cur.execute(script, (view_id,
                                         c,
                                         p,
                                         h,
                                         w,
                                         p,
                                         h,
                                         w))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def delete_view_layout(view_id):
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

def set_default_view_layout(view_class, view_id):
    "Set default layout for view class"
    script = """
UPDATE system.itemview_adapt
SET is_default_for_class = false
WHERE itemview_class = %s;
UPDATE system.itemview_adapt
SET is_default_for_class = true
WHERE itemview_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (view_class, view_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
