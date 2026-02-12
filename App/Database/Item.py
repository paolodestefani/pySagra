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

"""Item database functions


"""

# psycopg
import psycopg

# application modules
from App.Database.Connect import appconn
from App.Database.Exceptions import PyAppDBError



def get_variants(item_id: int) -> list[tuple]:
    "Get a list of variants from item_id"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT 
    variant_description,
    price_delta
FROM item_variant
WHERE   company_id  = system.pa_current_company() 
    AND item_id     = %s
ORDER BY sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def item_list(event_id: int, department_id: int) -> list[tuple]:
    "Get item list for supplied event and department"
    # actually we don't need to filter company_id as event_id and department_id are unique across companies
    script = """
SELECT 
    item_id,
    item_description,
    price,
    pos_row,
    pos_column,
    has_inventory_control,
    has_delivered_control,
    normal_text_color,
    normal_background_color,
    has_variants,
    available
FROM vw_item_availability
WHERE 
        company_id      = system.pa_current_company() 
    AND is_salable      IS true 
    AND event_id        = %(event_id)s 
    AND department_id   = %(department_id)s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, {'event_id': event_id, 'department_id': department_id})
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def item_web_list(event_id: int, department_id: int) -> list[tuple]:
    # actually we don't need to filter company_id as event_id and department_id are unique across companies
    "Get item list for supplied event for web order"
    script = """
SELECT 
    item_id,
    item_description,
    price,
    is_available,
    has_variants
FROM vw_item_availability
WHERE 
        company_id      = system.pa_current_company() 
    AND is_salable      IS true 
    AND is_web_available IS true 
    AND event_id        = %(event_id)s 
    AND department_id   = %(department_id)s
ORDER BY web_sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, {'event_id': event_id, 'department_id': department_id})
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def is_menu(item_id: int) -> bool:
    "Return True if item is a menu type item"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT item_id 
FROM item 
WHERE 
        company_id  = system.pa_current_company() 
    AND item_id     = %s 
    AND item_type   = 'M';"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            return bool(cur.rowcount)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def is_kit(item_id: int) -> bool:
    "Return True if item is a kit type item"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT item_id 
FROM item 
WHERE
        company_id  = system.pa_current_company()
    AND item_id     = %s 
    AND item_type   = 'K';"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            return bool(cur.rowcount)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def is_for_takeaway(item_id: int) -> bool:
    "Return True if item is available for takeaway, based on department's flag"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT i.item_id
FROM item i
JOIN department d on i.department_id = d.department_id
WHERE 
        i.company_id    = system.pa_current_company()
    AND i.item_id       = %s 
    AND d.is_for_takeaway IS True;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            return bool(cur.rowcount)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def has_stock_management(item_id: int) -> bool:
    "Return True if item's require stock management"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT 
    has_inventory_control 
FROM item 
WHERE
        company_id  = system.pa_current_company()
    AND item_id     = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            return bool(cur.rowcount)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_menu_items(item_id: int) -> list[tuple]:
    "Return menu components"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT 
    part_id,
    quantity
FROM item_part
WHERE
        company_id  = system.pa_current_company()
    AND item_id     = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_item_dep(item_id: int) -> int|None:
    "Return department id for item"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT 
    department_id
FROM item
WHERE 
        company_id  = system.pa_current_company()
    AND item_id     = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_item_desc(item_id: int) -> str|None:
    "Return description of item item"
    # actually we don't need to filter company_id as item_id is unique across companies
    script = """
SELECT 
    description 
FROM item 
WHERE 
        company_id  = system.pa_current_company()
    AND item_id     = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (item_id,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:                
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_item_stock_level(event_id: int, item_id: int) -> int:
    "Return item stock level for given event of type 'A'"
    # actually we don't need to filter company_id as event_id and item_id are unique across companies
    script = """
SELECT 
    available 
FROM vw_item_availability 
WHERE
        company_id  = system.pa_current_company()
    AND event_id    = %s 
    AND item_id     = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (event_id, item_id))
            result = cur.fetchone()
            if result:
                return result[0] or 0 # if stock not set balance is null
            else:
                return 0
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def kit_availability(event_id: int) -> list[tuple]:
    # actually we don't need to filter company_id as event_id is unique across companies
    script = """
SELECT 
    item_id,
    item_description,
    available
FROM vw_item_availability
WHERE
        company_id  = system.pa_current_company()
    AND item_type   = 'K' 
    AND event_id    = %(event_id)s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, {'event_id': event_id})
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def menu_availability(event_id: int) -> list[tuple]:
    script = """
SELECT 
    item_id,
    available
FROM vw_item_availability
WHERE
        company_id  = system.pa_current_company()
    AND item_type   = 'M' 
    AND event_id    = %(event_id)s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, {'event_id': event_id})
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
