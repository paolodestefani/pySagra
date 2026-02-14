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



def create_sortfilter(sortfilter_class: str, sortfilter_description: str) -> int:
    "Create a new sortfilter customization"
    script = """
INSERT INTO system.sortfilter_adapt (description, sortfilter_class)
VALUES (%s, %s)
RETURNING sortfilter_adapt_id;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sortfilter_description, sortfilter_class))
                result = next(cur, None)
                if result:
                    return result[0]
                else:                    
                    raise PyAppDBError('00000', 'Failed to create sortfilter customization')
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def delete_sortfilter(sortfilter_id: int) -> None:
    "Delete sortfilter customization of sortfilter_id"
    script = """
DELETE FROM system.sortfilter_adapt
WHERE sortfilter_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sortfilter_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def list_sortfilter(sortfilter_class: str) -> list:
    "Get available sortfilter customizations for class"
    script = """ 
SELECT
    sortfilter_adapt_id,
    description
FROM system.sortfilter_adapt
WHERE sortfilter_class = %s
ORDER BY class_sorting;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sortfilter_class,))
                return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

# def list_sortfilter_model(sortfilter_class):
#     "Get available sortfilter models for class"
#     script = """
# SELECT 
#     id,
#     description
# FROM system.item_model
# WHERE model_class = %s
# ORDER BY id;"""
#     try:
#         with appconn.transaction():
#             with appconn.cursor() as cur:
#                 cur.execute(script, (sortfilter_class,))
#                 return cur.fetchall()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.diag.sqlstate, str(er))

# def get_sortfilter_model(sortfilter_id):
#     "Get sortfilter model"
#     script = """
# SELECT item_model_id
# FROM system.sortfilter_customize
# WHERE id = %s;"""
#     try:
#         with appconn.transaction():
#             with appconn.cursor() as cur:
#                 cur.execute(script, (sortfilter_id,))
#                 return cur.fetchone()[0]
#     except psycopg.Error as er:
#         raise PyAppDBError(er.diag.sqlstate, str(er))

def get_sortfilter_limit(sf_id: int) -> int|None:
    "Get row count limit for sortfilter_adapt_id"
    script = """
SELECT 
    row_count_limit
FROM system.sortfilter_adapt
WHERE sortfilter_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (sf_id,))
            result = next(cur, None)
            if result:
                return result[0]
            else:
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_sortfilter_limit(sf_id: int, limit: int|None) -> None:
    "Set row count limit for sortfilter_adapt_id"
    script = """
UPDATE system.sortfilter_adapt
SET row_count_limit = %s
WHERE sortfilter_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (limit, sf_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def clear_sortfilter_setting(sf_id: int) -> None:
    "Claer sortfilter customizations, required before updating"
    script = """
DELETE FROM system.sortfilter_adapt_setting
WHERE sortfilter_adapt_id = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (sf_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_sortfilter_setting(sf_id: int) -> tuple[list, list]:
    "Get available sortfilter customizations settings for id and element"
    script = """
SELECT 
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value
FROM system.sortfilter_adapt_setting
WHERE sortfilter_adapt_id = %s
ORDER BY layout_row;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sf_id,))
                if cur.rowcount == 0:
                    return [], []  # no customization
                else:
                    d = cur.fetchall()
                    f = [i for i in d if i[0] == 'F'] # Filters
                    s = [i for i in d if i[0] == 'S'] # Sorting
                    return f, s
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_sortfilter_setting(sf_id: int, 
                           sf_element: str, 
                           row: int, 
                           cmb1: int,
                           neg: bool, 
                           cmb2: int, 
                           widget: str
                           ) -> None:
    "Set available sortfilter customizations settings for id and element"
    script = """
-- insert/update setting
INSERT INTO system.sortfilter_adapt_setting (
    sortfilter_adapt_id,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT sortfilter_adapt_setting_pk DO
UPDATE SET 
    combo1_index = %s,
    negate_state = %s,
    combo2_index = %s,
    widget_value = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (sf_id,
                                     sf_element,
                                     row,
                                     cmb1,
                                     neg,
                                     cmb2,
                                     widget,
                                     cmb1,
                                     neg,
                                     cmb2,
                                     widget))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def sortfilter_adapt_sorting(sortfilter_id: int) -> int:
    "Returns sortfilter sorting index"
    script = """
SELECT class_sorting
FROM system.sortfilter_adapt
WHERE sortfilter_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sortfilter_id,))
                result = next(cur, None)
                if result:
                    return result[0]
                else:
                    return 0
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_sortfilter_adapt_sorting(sortfilter_id: int, sorting: int) -> None:
    "Set sortfilter sorting index"
    script = """
UPDATE system.sortfilter_adapt
SET class_sorting = %s
WHERE sortfilter_adapt_id = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (sorting, sortfilter_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
