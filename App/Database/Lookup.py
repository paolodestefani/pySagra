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

"""Database - Lookup

This module provide  functions that return a code - description list of values
used by delegates and combo boxes

"""

# standard library
#from typing import Any
import logging

# application modules
from App import session
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn
from App.Database.Report import get_report_list


# logger
logger = logging.getLogger(__name__)


def get_list(query: str) -> list[tuple | list]:
    """
    A select query that returns code + description list of values
    """
    if query.startswith('LIST:'):
        data = query.split(':')[1]
        return [(i.split('=')) for i in data.split(',')]
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def abstract_lookup(code: str,
                    description: str, 
                    table: str, 
                    condition=[], 
                    order_by=[], 
                    null=False) -> list[tuple]:
    """
    Get a list of code, description values from a table. 
    Condition and order by are optional.
    Null=True add a null value item at the beginning of the list
    """
    # t-strings in this context looks unusable
    script = f"SELECT {code}, {description} FROM {table}"
    if condition:
        script += f" WHERE {' AND '.join(condition)}"
    if order_by:
        script += f" ORDER BY {', '.join(order_by)};"
    else:
        script += f" ORDER BY {code};"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        records = cur.fetchall()
        return [(None, '')] + records if null else records


def abstract_with_code_lookup(code: str,
                              description: str,
                              table: str,
                              condition=[],
                              order_by=[],
                              null=False) -> list[tuple]:
    """
    Get a list of code, code + description values from table.
    Condition and order by are optional.
    Null=True add a null value item at the beginning of the list
    """
    # t-strings in this context looks unusable
    script = f"SELECT {code}, format('%5s %s', {code}, {description}) FROM {table}"
    if condition:
        script += f" WHERE {' AND '.join(condition)}"
    if order_by:
        script += f" ORDER BY {', '.join(order_by)};"
    else:
        script += f" ORDER BY {code};"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        records = cur.fetchall()
        return [(None, '')] + records if null else records


def profile_lookup(null: bool = False) -> list[tuple]:
    "Get profile list"
    return abstract_lookup('profile_code',
                           'description',
                           'system.profile',
                           null=null)


def menu_lookup(null: bool = False) -> list[tuple]:
    "Get menu list"
    return abstract_lookup('code',
                           'description',
                           'system.menu_toolbar',
                           condition=["type = 'M'"],
                           null=null)


def toolbar_lookup(null: bool = False) -> list[tuple]:
    "Get toolbars list"
    return abstract_lookup('code',
                           'description',
                           'system.menu_toolbar',
                           condition=["type = 'T'"],
                           null=null)


def user_lookup(null: bool = False) -> list[tuple]:
    "Get users list"
    return abstract_lookup('user_code',
                           'description',
                           'system.app_user',
                           null=null)


def company_lookup(null: bool = False) -> list[tuple]:
    "Get companies list"
    return abstract_with_code_lookup('company_id',
                                     'description',
                                     'system.company',
                                     null=null)


# def printer_class_lookup() -> list[tuple]:
#     "Get printer classes list with null"
#     return abstract_lookup('printer_class_id',
#                            'description',
#                            'printer_class',
#                            condition=['company_id = system.pa_current_company()'], 
#                            null=True)

    
def customer_order_driver_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all report (code, description) of customer order class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list(f'D', 'ORDER_CUSTOMER', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list(f'D', 'ORDER_CUSTOMER', session['l10n'])]

def customer_order_escpos_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all report (code, description) of customer order class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list('E', 'ORDER_CUSTOMER', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list('E', 'ORDER_CUSTOMER', session['l10n'])]

def department_order_driver_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all reports of department order class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list('D', 'ORDER_DEPARTMENT', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list('D', 'ORDER_DEPARTMENT', session['l10n'])]

def department_order_escpos_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all reports of department order class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list('E', 'ORDER_DEPARTMENT', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list('E', 'ORDER_DEPARTMENT', session['l10n'])]

def cover_order_driver_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all reports of cover order class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list('D', 'ORDER_COVER', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list('D', 'ORDER_COVER', session['l10n'])]

def cover_order_escpos_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all reports of cover order class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list('E', 'ORDER_COVER', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list('E', 'ORDER_COVER', session['l10n'])]

def order_driver_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all report (code, description) of customer/cover/department reports"
    return (customer_order_driver_report_lookup(null) + 
            department_order_driver_report_lookup(null) +
            cover_order_driver_report_lookup(null))
    
def order_escpos_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all report (code, description) of customer/cover/department reports"
    return (customer_order_escpos_report_lookup(null) + 
            department_order_escpos_report_lookup(null) +
            cover_order_escpos_report_lookup(null))

def stock_unload_report_lookup(null: bool = False) -> list[tuple]:
    "Get a list of all reports of stock unload class"
    if null:
        return [(None, None)] + [(c, d) for i, c, d in get_report_list('STOCK_UNLOAD', session['l10n'])]
    else:
        return [(c, d) for i, c, d in get_report_list('STOCK_UNLOAD', session['l10n'])]
    

def escpos_printer_lookup(null: bool = False) -> list[tuple]:
    "Get departments list"
    return abstract_lookup('escpos_printer_id',
                           'name',
                           'escpos_printer',
                           ['company_id = system.pa_current_company()',
                            f"hostname IS NULL OR hostname = '{session['hostname']}'"],
                           null=True)


def event_lookup(null: bool = False) -> list[tuple]:
    "Get event list"
    return abstract_lookup('event_id', 
                           'description',
                           'event', 
                           ['company_id = system.pa_current_company()'], 
                           ['end_date DESC'],
                           null=null)


def department_lookup(null=False) -> list[tuple]:
    "Get departments list"
    return abstract_lookup('department_id',
                           'description',
                           'department',
                           ['company_id = system.pa_current_company()'],
                           null=null)
    
# def department_lookup_n() -> list[tuple]:
#     "Get departments list"
#     return abstract_lookup('department_id',
#                            'description',
#                            'department',
#                            ['company_id = system.pa_current_company()'],
#                            null=True)

def current_item_lookup(null: bool = False) -> list[tuple]:
    "Items"
    return abstract_lookup('item_id',
                           'description',
                           'item',  
                           ["is_obsolete IS false",
                            "company_id = system.pa_current_company()"],
                           null=null)


def item_all_lookup(null: bool = False) -> list[tuple]:
    "Items"
    return abstract_lookup('item_id', 
                           'description', 'item', 
                           ['company_id = system.pa_current_company()'],
                           null=null)


def item_lookup(null: bool = False) -> list[tuple]:
    "Items"
    return abstract_lookup('item_id',
                           'description',
                           'item', 
                           ["item_type = 'I'",
                            "company_id = system.pa_current_company()"],
                           null=null)


def item_salable_lookup(null: bool = False) -> list[tuple]:
    "Items salable"
    return abstract_lookup('item_id',
                           'description',
                           'item',
                           ["is_obsolete IS false",
                            "is_salable IS true",
                            "company_id = system.pa_current_company()"],
                           null=null)


def item_with_stock_control_lookup(null: bool = False) -> list[tuple]:
    "Items with stock control"
    return abstract_lookup('item_id', 
                           'description',
                           'item', 
                           ["item_type = 'I'", 
                            "has_inventory_control IS true", 
                            "is_obsolete is false",
                            "company_id = system.pa_current_company()"],
                           null=null)


def item_with_variant_lookup(null: bool = False) -> list[tuple]:
    "Items with variants"
    return abstract_lookup('item_id', 
                           'description',
                           'item', 
                           ["has_variants IS true",
                            "company_id = system.pa_current_company()"],
                           null=null)


def kit_part_lookup(null: bool = False) -> list[tuple]:
    "Kit Parts"
    return abstract_lookup('item_id',
                           'description',
                           'item', 
                           ["item_type = 'I'",
                            "is_kit_part IS true",
                            "company_id = system.pa_current_company()"],
                           null=null)


def menu_part_lookup(null: bool = False) -> list[tuple]:
    "Menu Parts"
    return abstract_lookup('item_id', 
                           'description',
                           'item', 
                           ["item_type IN ('I', 'K')",
                            "is_menu_part IS true",
                            "company_id = system.pa_current_company()"],
                           null=null)


def price_list_lookup(null: bool = False) -> list[tuple]:
    "Get price list list"
    return abstract_lookup('price_list_id',
                           'description',
                           'price_list',
                           ['company_id = system.pa_current_company()'],
                           null=null)

# def statisticsList():
#     "Get statistics list"
#     return abstract_lookup('id', 'description', 'statistics_configuration')

