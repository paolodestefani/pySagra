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

"""Database - utilities

This module provide a set of utility functions to interact with the archive
database

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def delete_event_order(event_id: int) -> None:
    "Delete all orders of the given event"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT company.delete_event_order(%s);', (event_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def inventory_rebuild(event_id: int) -> None:
    "Inventory rebuild for the given event"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT company.inventory_rebuild(%s);', (event_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def ordered_delivered_rebuild(event_id: int) -> None:
    "Ordered delivered rebuild for the given event"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT company.ordered_delivered_rebuild(%s);', (event_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def numbering_rebuild(event_id: int) -> None:
    "Numbering rebuild for the given event"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT company.numbering_rebuild(%s);', (event_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_order_as_processed(event_id: int) -> None:
    "Set all unprocessed orders as processed ad order date"
    # order headers are updated by the trigger
    # no need to filter by company id as event_id is unique per company
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT company.set_order_as_processed(%s);', (event_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
    
def delete_all_orders() -> None:
    "Delete ALL orders for current company"
    script = """
DELETE FROM order_header
WHERE company_id = system.pa_current_company();
DELETE FROM numbering
WHERE company_id = system.pa_current_company();
"""
    # linked tables (oreder_header_department, order_detail, etc.
    # are automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_web_orders() -> None:
    "Delete ALL web orders for current company"
    script = """
DELETE FROM web_order_header
WHERE company_id = system.pa_current_company();"""
    # linked table web_order_detail is automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_inventory() -> None:
    "Delete ALL stock inventory records for current company"
    script = """
DELETE FROM stock_inventory
WHERE company_id = system.pa_current_company();"""
    # linked table web_order_detail is automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_events() -> None:
    "Delete ALL events for current company"
    script = """
DELETE FROM event
WHERE company_id = system.pa_current_company();"""
    # linked tables (all about orders) are automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_price_lists() -> None:
    "Delete ALL price lists for current company"
    script = """
DELETE FROM price_list
WHERE company_id = system.pa_current_company();"""
    # linked table (price_list_detail) is automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_items() -> None:
    "Delete ALL items for current company"
    script = """
DELETE FROM item
WHERE company_id = system.pa_current_company();"""
    # linked table (item_part, item_variant) are automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_departments() -> None:
    "Delete ALL departments for current company"
    script = """
DELETE FROM department
WHERE company_id = system.pa_current_company();"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_tables() -> None:
    "Delete ALL tables for current company"
    script = """
DELETE FROM numbered_table
WHERE company_id = system.pa_current_company();"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_cash_desks() -> None:
    "Delete ALL cash desks for current company"
    script = """
DELETE FROM cash_desk
WHERE company_id = system.pa_current_company();"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def delete_all_printer_classes() -> None:
    "Delete ALL printer classes for current company"
    script = """
DELETE FROM printer_class
WHERE company_id = system.pa_current_company();"""
    # linked table (printer_class_printer) is automatically deleted from db cascade constraints
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    

def copy_cash_desk(from_company_id: int) -> None:
    "Copy ALL the cash desks from another company to current company"
    script = """
INSERT INTO cash_desk (
    company_id,
    computer,
    cash_desk_description,
    note)
SElECT
    system.pa_current_company(),
    computer,
    cash_desk_description,
    note
FROM cash_desk
WHERE company_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (from_company_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))


def copy_printer_class(from_company_id: int) -> None:
    "Copy ALL the printer classes from another company to current company"
    script1 = """
INSERT INTO printer_class (
    company_id,
    description,
    external_code)
SElECT
    system.pa_current_company(),
    description,
    printer_class_id
FROM printer_class
WHERE company_id = %s;"""
    script2 = """
INSERT INTO printer_class_printer (
    company_id,
    printer_class_id,
    computer,
    printer)
SELECT
    system.pa_current_company(),
    b.printer_class_id,
    a.computer,
    a.printer
FROM printer_class_printer a
JOIN (
    SELECT printer_class_id, external_code 
    FROM printer_class
    WHERE company_id = system.pa_current_company()
    ) b ON a.printer_class_id = b.external_code
WHERE a.company_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (from_company_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    

def copy_table(from_company_id: int) -> None:
    "Copy ALL the tables from another company to current company"
    script = """
INSERT INTO seat_map (
    company_id,
    table_code,
    pos_row,
    pos_column,
    text_color,
    background_color,
    is_obsolete,
    external_code)
SElECT
    system.pa_current_company(),
    table_code,
    pos_row,
    pos_column,
    text_color,
    background_color,
    is_obsolete,
    seat_map_id
FROM seat_map
WHERE company_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (from_company_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    

def copy_department(from_company_id: int) -> None:
    "Copy ALL the departments from another company to current company"
    script = """
INSERT INTO department (
    company_id,
    description,
    sorting,
    printer_class_id,
    is_obsolete,
    is_menu_container,
    is_for_takeaway,
    external_code)
SElECT
    system.pa_current_company(),
    a.description,
    a.sorting,
    b.printer_class_id,
    a.is_obsolete,
    a.is_menu_container,
    a.is_for_takeaway,
    a.department_id
FROM department a
LEFT JOIN printer_class b ON a.printer_class_id = b.external_code
WHERE a.company_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (from_company_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

    
