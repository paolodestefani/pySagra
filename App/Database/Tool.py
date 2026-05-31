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

"""Database - Utilities

This module provides a set of utility functions to interact with the archive
database

"""

# standard library
import logging

# application modules
from App.Database.Exceptions import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def delete_event_order(event_id: int) -> None:
    "Delete all orders of the given event"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT company.delete_event_order({event_id});')


def inventory_rebuild(event_id: int) -> None:
    "Inventory rebuild for the given event"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT company.inventory_rebuild({event_id});')

    
def ordered_delivered_rebuild(event_id: int) -> None:
    "Ordered delivered rebuild for the given event"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT company.ordered_delivered_rebuild({event_id});')


def numbering_rebuild(event_id: int) -> None:
    "Numbering rebuild for the given event"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT company.numbering_rebuild({event_id});')


def set_order_as_processed(event_id: int) -> None:
    "Set all unprocessed orders as processed ad order date"
    # order headers are updated by the trigger
    # no need to filter by company id as event_id is unique per company
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT company.set_order_as_processed({event_id});')
 
    
def delete_all_orders() -> None:
    "Delete ALL orders for current company, update identity sequences"
    script1 = """
DELETE FROM order_header
WHERE company_id = system.pa_current_company();
"""
    script2 = """
DELETE FROM numbering
WHERE company_id = system.pa_current_company();
"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('company.order_header', 'order_header_id'),
    COALESCE((SELECT max(order_header_id) FROM company.order_header), 1),
    (SELECT max(order_header_id) IS NOT NULL FROM company.order_header)
);"""
    script4 = """
SELECT setval(
    pg_get_serial_sequence('company.order_header_department', 'order_header_department_id'),
    COALESCE((SELECT max(order_header_department_id) FROM company.order_header_department), 1),
    (SELECT max(order_header_department_id) IS NOT NULL FROM company.order_header_department)
);"""
    script5 = """
SELECT setval(
    pg_get_serial_sequence('company.order_line', 'order_line_id'),
    COALESCE((SELECT max(order_line_id) FROM company.order_line), 1),
    (SELECT max(order_line_id) IS NOT NULL FROM company.order_line)
);"""
    script6 = """
SELECT setval(
    pg_get_serial_sequence('company.order_line_department', 'order_line_department_id'),
    COALESCE((SELECT max(order_line_department_id) FROM company.order_line_department), 1),
    (SELECT max(order_line_department_id) IS NOT NULL FROM company.order_line_department)
);"""
    # linked tables (oreder_header_department, order_detail, etc.
    # are automatically deleted from db cascade constraints
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        for statement in (script1, script2, script3, script4, script5, script6):
            cur.execute(statement)

    
def delete_all_inventory() -> None:
    "Delete ALL stock inventory records for current company"
    script = """
DELETE FROM inventory
WHERE company_id = system.pa_current_company();"""
    # linked table web_order_detail is automatically deleted from db cascade constraints
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def delete_all_events() -> None:
    "Delete ALL events for current company"
    script = """
DELETE FROM event
WHERE company_id = system.pa_current_company();"""
    # linked tables (all about orders) are automatically deleted from db cascade constraints
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def delete_all_price_lists() -> None:
    "Delete ALL price lists for current company"
    script = """
DELETE FROM price_list
WHERE company_id = system.pa_current_company();"""
    # linked table (price_list_detail) is automatically deleted from db cascade constraints
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
 
    
def delete_all_items() -> None:
    "Delete ALL items for current company"
    script = """
DELETE FROM item
WHERE company_id = system.pa_current_company();"""
    # linked table (item_part, item_variant) are automatically deleted from db cascade constraints
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def delete_all_departments() -> None:
    "Delete ALL departments for current company"
    script = """
DELETE FROM department
WHERE company_id = system.pa_current_company();"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def delete_all_tables() -> None:
    "Delete ALL tables for current company"
    script = """
DELETE FROM seat_map
WHERE company_id = system.pa_current_company();"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def delete_all_cash_desks() -> None:
    "Delete ALL cash desks for current company"
    script = """
DELETE FROM cash_desk
WHERE company_id = system.pa_current_company();"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def delete_all_printer_classes() -> None:
    "Delete ALL printer classes for current company"
    script = """
DELETE FROM printer_class
WHERE company_id = system.pa_current_company();"""
    # linked table (printer_class_printer) is automatically deleted from db cascade constraints
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def copy_cash_desk(from_company_id: int) -> None:
    "Copy ALL the cash desks from another company to current company"
    script = t"""
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
WHERE company_id = {from_company_id};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def copy_printer_class(from_company_id: int) -> None:
    "Copy ALL the printer classes from another company to current company"
    script = t"""
INSERT INTO printer_class (
    company_id,
    description,
    external_code)
SElECT
    system.pa_current_company(),
    description,
    printer_class_id
FROM printer_class
WHERE company_id = {from_company_id};
"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
 

def copy_table(from_company_id: int) -> None:
    "Copy ALL the tables from another company to current company"
    script = t"""
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
WHERE company_id = {from_company_id};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def copy_department(from_company_id: int) -> None:
    "Copy ALL the departments from another company to current company"
    script = t"""
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
LEFT JOIN printer_class b ON a.printer_class_id = b.external_code AND b.company_id = {from_company_id}
WHERE a.company_id = {from_company_id};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)

    
def copy_item(from_company_id: int) -> None:
    "Copy all items from selected company to current company"
    script = t"""
INSERT INTO company.item (
	item_type,
	description,
	customer_description,
	department_id,
	sorting,
	pos_row,
	pos_column,
	normal_background_color,
	normal_text_color,
	has_variants,
	has_inventory_control,
	has_delivered_control,
	is_kit_part,
	is_menu_part,
	is_salable,
	is_web_available,
	web_sorting,
	is_obsolete
)
SELECT
	i.item_type,
	i.description,
	i.customer_description,
	d.department_id,
	i.sorting,
	i.pos_row,
	i.pos_column,
	i.normal_background_color,
	i.normal_text_color,
	i.has_variants,
	i.has_inventory_control,
	i.has_delivered_control,
	i.is_kit_part,
	i.is_menu_part,
	i.is_salable,
	i.is_web_available,
	i.web_sorting,
	i.is_obsolete
FROM company.item i
JOIN company.department d ON i.department_id = d.external_code 
WHERE i.company_id = {from_company_id}
"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
