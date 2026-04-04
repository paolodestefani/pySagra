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

"""Code - description list

This module provide  functions that return a code - description list of values
used by delegates and combo boxes


"""

# psycopg
import psycopg

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn
#from App.Core.L10n import _tr
from App.Database.Report import get_report_list


def get_list(query):
    "A select query that returns code + description list of values"
    if query.startswith('LIST:'):
        data = query.split(':')[1]
        return [(i.split('=')) for i in data.split(',')]
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(query)
                records = cur.fetchall()
                return records
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))


def generic_cdl(code: str, description: str, table: str, condition=[], order_by=[], null=False) -> list[tuple]:
    "Get a list of code, description values from a table"
    script = f"SELECT {code}, {description} FROM {table}"
    if condition:
        script += ' WHERE ' + ' AND '.join(condition)
    if order_by:
        script += f' ORDER BY {", ".join(order_by)};'
    else:
        script += f' ORDER BY {code};'
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            records = cur.fetchall()
            if null:
                return [(None, '')] + records
            else:
                return records
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def generic_with_code_cdl(code: str, description: str, table: str, condition=[], order_by=[], null=False) -> list[tuple]:
    "Get a list of code, code + description values from table"
    script = f"SELECT {code}, format('%5s %s', {code}, {description}) FROM {table}"
    if condition:
        script += ' WHERE ' + ' AND '.join(condition)
    if order_by:
        script += f' ORDER BY {", ".join(order_by)};'
    else:
        script += f' ORDER BY {code};'
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            records = cur.fetchall()
            return [(None, '')] + records if null else records
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))


def profile_cdl() -> list[tuple]:
    "Get profile list"
    return generic_cdl('profile_code', 'description', 'system.profile')

def menu_cdl() -> list[tuple]:
    "Get menu list"
    return generic_cdl('menu_code', 'description', 'system.menu')

def toolbar_cdl() -> list[tuple]:
    "Get toolbars list"
    return generic_cdl('toolbar_code', 'description', 'system.toolbar')

def user_cdl() -> list[tuple]:
    "Get users list"
    return generic_cdl('user_code', 'description', 'system.app_user')

def company_cdl() -> list[tuple]:
    "Get companies list"
    return generic_with_code_cdl('company_id', 'description', 'system.company')

def printer_class_cdl() -> list[tuple]:
    "Get printer classes list with null"
    return generic_cdl('printer_class_id', 'description', 'printer_class',
                        condition=['company_id = system.pa_current_company()'], 
                        null=True)
    
def customer_order_report_cdl() -> list[tuple]:
    "Get a list of all report (code, description) of customer order class"
    return [(c, d) for i, c, d in get_report_list('ORDER_CUSTOMER', session['l10n'])]

def department_order_report_cdl() -> list[tuple]:
    "Get a list of all reports of department order class"
    return [(c, d) for i, c, d in get_report_list('ORDER_DEPARTMENT', session['l10n'])]

def cover_order_report_cdl() -> list[tuple]:
    "Get a list of all reports of cover order class"
    return [(c, d) for i, c, d in get_report_list('ORDER_COVER', session['l10n'])]

def stock_unload_report_cdl() -> list[tuple]:
    "Get a list of all reports of stock unload class"
    return [(c, d) for i, c, d in get_report_list('STOCK_UNLOAD', session['l10n'])]

# def statisticsViewerReportList():
#     "Get a list of all reports available for statistics viewer"
#     return get_report_list('STATSVIEW', session['l10n'], null=True)

def event_cdl() -> list[tuple]:
    "Get event list"
    return generic_cdl('event_id', 'description', 'event', 
                        ['company_id = system.pa_current_company()'], 
                        ['end_date DESC'])

def department_cdl() -> list[tuple]:
    "Get departments list"
    return generic_cdl('department_id', 'description', 'department',
                        ['company_id = system.pa_current_company()'])

def current_item_cdl() -> list[tuple]:
    "Items"
    return generic_cdl('item_id', 'description', 'item',  
                        ["is_obsolete IS false",
                         'company_id = system.pa_current_company()'])

def item_all_cdl() -> list[tuple]:
    "Items"
    return generic_cdl('item_id', 'description', 'item', 
                        ['company_id = system.pa_current_company()'])

def item_cdl() -> list[tuple]:
    "Items"
    return generic_cdl('item_id', 'description', 'item', 
                        ["item_type = 'I'",
                         'company_id = system.pa_current_company()'])

def item_salable_cdl() -> list[tuple]:
    "Items salable"
    return generic_cdl('item_id', 'description', 'item',
                        ["is_obsolete IS false",
                         "is_salable IS true",
                         'company_id = system.pa_current_company()'])

def item_with_stock_control_cdl() -> list[tuple]:
    "Items with stock control"
    return generic_cdl('item_id', 'description', 'item', 
                        ["item_type = 'I'", 
                         "has_inventory_control IS true", 
                         "is_obsolete is false",
                         'company_id = system.pa_current_company()'])

def item_with_variant_cdl() -> list[tuple]:
    "Items with variants"
    return generic_cdl('item_id', 'description', 'item', 
                        ["has_variants IS true",
                         'company_id = system.pa_current_company()'])

def kit_part_cdl() -> list[tuple]:
    "Kit Parts"
    return generic_cdl('item_id', 'description', 'item', 
                        ["item_type = 'I'",
                         "is_kit_part IS true",
                         'company_id = system.pa_current_company()'])

def menu_part_cdl() -> list[tuple]:
    "Menu Parts"
    return generic_cdl('item_id', 'description', 'item', 
                        ["item_type IN ('I', 'K')",
                         "is_menu_part IS true",
                         'company_id = system.pa_current_company()'])

def price_list_cdl() -> list[tuple]:
    "Get price list list"
    return generic_cdl('price_list_id', 'description', 'price_list',
                        ['company_id = system.pa_current_company()'])

# def statisticsList():
#     "Get statistics list"
#     return generic_cdl('id', 'description', 'statistics_configuration')

