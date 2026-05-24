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

"""Database - Order management

This module provides classes and functions for order management

"""

# standard library
from typing import Any
import logging

# psycopg
import psycopg

# PySide6
from PySide6.QtCore import QTime
from PySide6.QtCore import QDate

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Utility import Record, RecordSet
from App.Database.Connect import appconn
from App.Database.Setting import Setting
from App.Database.Item import is_menu
from App.Database.Item import get_menu_items
from App.Database.Item import get_item_dep
from App.Database.Item import has_stock_management
from App.Database.Item import get_item_stock_level
from App.Database.Item import get_item_desc
from App.Database.Department import get_department_desc
from App.Database.Department import get_department_barcode
from App.Database.Event import get_event_from_date


# logger
logger = logging.getLogger(__name__)


def get_order_number(event_id: int,
                     event_date: QDate|None = None,
                     day_part: str|None = None
                     ) -> int:
    "Returns the next available order number"
    script = t"""
SELECT
    order_number_based_on
FROM setting
WHERE company_id = system.pa_current_company();"""
    try:
        with appconn.cursor() as cur:
            result = cur.execute(script).fetchone()
            if result:
                mode = result[0]
            else:
                raise PyAppDBError(None, 'Failed to retrive order numbering mode from settings')
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    
    number = 1
    match mode:
        case 'E':
            # event based numbering, get the max value of any day/daypart
            script = t"""
SELECT max(coalesce(current_value, 0)) + 1 
FROM numbering 
WHERE   company_id  = system.pa_current_company()
    AND event_id    = {event_id};"""
            try:
                with appconn.cursor() as cur:
                    cur.execute(script)
                    number = next(cur)[0] or 1
            except psycopg.Error as er:
                logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
                raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
            
        case 'D':
            # day based numbering, get the max of L or D
            script = t"""
SELECT max(coalesce(current_value, 0)) + 1 
FROM numbering 
WHERE company_id = system.pa_current_company()
    AND event_id = {event_id}
    AND event_date = {event_date}"""
            try:
                with appconn.cursor() as cur:
                    cur.execute(script)
                    number = next(cur)[0] or 1
            except psycopg.Error as er:
                logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
                raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
        
        case 'P':
            # day part based numbering
            script = t"""
SELECT max(coalesce(current_value, 0)) + 1 
FROM numbering 
WHERE company_id = system.pa_current_company()
    AND event_id = {event_id}
    AND event_date = {event_date}
    AND day_part = {day_part};"""
            try:
                with appconn.cursor() as cur:
                    cur.execute(script)
                    number = next(cur)[0] or 1
            except psycopg.Error as er:
                logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
                raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    return number


def get_orders_issued(event_id: int, date: QDate, day_part: str) -> int:
    "Returns the issued number of orders for event, day and day part"
     # actually we don't need to filter company_id as event_id is unique across companies
    script = t"""
SELECT count(*)
FROM order_header
WHERE 
    company_id = system.pa_current_company()
    AND event_id = {event_id} 
    AND stat_order_date = {date}
    AND stat_order_day_part = {day_part};"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return next(cur)[0] or 0
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def get_order_header_department_details(barcode: str) -> tuple|None:
    "Returns params of the given order header department barcode"
    # actually we don't need to filter company_id as event_id is unique across companies
    script = t"""
SELECT 
    ohd.order_header_department_id,
    oh.order_header_id,
    oh.order_number,
    oh.order_date,
    oh.order_time,
    oh.delivery,
    oh.table_num,
    oh.customer_name,
    ohd.department_id,
    dep.description,
    ohd.fullfillment_date
FROM order_header_department ohd
JOIN order_header oh ON ohd.order_header_id = oh.order_header_id
JOIN department dep ON ohd.department_id = dep.department_id
WHERE 
    ohd.company_id = system.pa_current_company()
    AND ohd.barcode = {barcode};"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchone()
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def update_order_header_department_status(order_id: int, mark: bool=True) -> None:
    "Set to processed the given order header department id"
    # actually we don't need to filter company_id as order_id is unique across companies
    if mark:  # set datetime or null to unmark
        script = t"""
UPDATE order_header_department
SET fullfillment_date = CURRENT_TIMESTAMP
WHERE
    company_id = system.pa_current_company()
    AND order_header_department_id = {order_id};"""
    else:
        script = t"""
UPDATE order_header_department
SET fullfillment_date = Null
WHERE
    company_id = system.pa_current_company()
    AND order_header_department_id = {order_id};"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


class Order():
    "A order header and lines"

    def __init__(self) -> None:
        self.header = Record('order_header', ('order_header_id',))
        self.lines = RecordSet('order_line', ('order_line_id',))
        self.depnote: dict = {} # dict(dep: note)
        
    def out_of_stock(self) -> list[str|None]:
        "Returns a list of out of stock items"
        result = get_event_from_date(self.header['date_time'])
        if not result:
            raise PyAppDBError("02000", "No event found for order date")
        event_id = result[0]
        out_of_stock = []
        for i in self.lines:
            if has_stock_management(i['item_id']):
                if get_item_stock_level(event_id, i['item_id']) - i['quantity'] < 0:
                    out_of_stock.append(get_item_desc(i['item_id']))
        return out_of_stock

    def insert(self) -> tuple[Any, set[int | None]]:
        "Insert everything after completed the order"
        headersdep = RecordSet('order_header_department', ('order_header_department_id',))
        linesdep = RecordSet('order_line_department', ('order_line_department_id',))
        # set event
        result = get_event_from_date(self.header['date_time'])
        if not result:
            raise PyAppDBError("02000", "No event found for order date")
        self.header['event_id'] = result[0]
        # order date and time set in insert for management of event date changes
        self.header['order_date'] = self.header['date_time'].date()
        self.header['order_time'] = self.header['date_time'].time()
        # set date, statistical date and date part
        setting = Setting()
        # if time between 0.0.0 and lunch start time stat date is the day before date part is dinner
        if QTime(0, 0) <= self.header['order_time'] < QTime(setting['lunch_start_time'], 0):
            # dinner of the day before
            self.header['stat_order_date'] = self.header['order_date'].addDays(-1)
            self.header['stat_order_day_part'] = 'D'
        elif QTime(setting['lunch_start_time'], 0) <= self.header['order_time'] < QTime(setting['dinner_start_time'], 0):
            # lunch
            self.header['stat_order_date'] = self.header['order_date']
            self.header['stat_order_day_part'] = 'L'
        else:
            # dinner of the current date
            self.header['stat_order_date'] = self.header['order_date']
            self.header['stat_order_day_part'] = 'D'
        # obtain order number
        self.header['order_number'] = get_order_number(self.header['event_id'], 
                                                       self.header['stat_order_date'],
                                                       self.header['stat_order_day_part'])
        # from lines create an intermediate detail list resolving menu items
        # resolve menu
        intermediate = []
        for i in self.lines: # also have to remove price and amount
            if is_menu(i['item_id']):
                for p, q in get_menu_items(i['item_id']):
                    r = dict()
                    r['item_id'] = p
                    if setting['menu_description_on_menu_items']:
                        r['variants'] = f"({get_item_desc(i['item_id'])})" 
                    else:
                        r['variants'] = None # menu part can not have variants
                    r['quantity'] = i['quantity'] * q
                    intermediate.append(r)
            else:
                r = dict()
                r['item_id'] = i['item_id']
                r['variants'] = i['variants']
                r['quantity'] = i['quantity']
                intermediate.append(r)
        # sum qty of same item that can come out from previous elaboration
        detail: list = []
        for i in intermediate:
            if (i['item_id'], i['variants']) in [(r['item_id'], r['variants']) for r in detail]:
                for n, j in enumerate([(r['item_id'], r['variants']) for r in detail]):
                    if (i['item_id'], i['variants']) == j:
                        detail[n]['quantity'] += i['quantity']
            else:
                detail.append(i.copy())
        # generate headersdep and linesdep
        # compute used departments set and create headersdep
        used_dep = {get_item_dep(i['item_id']) for i in detail}
        used_dep_desc = [get_department_desc(i) for i in used_dep if i is not None]
        for i in used_dep:
            # dep header
            r = dict()
            r['department_id'] = i
            r['note'] = self.depnote.get(i)
            others = list(used_dep_desc)
            others.remove(get_department_desc(i))
            if others:
                r['other_departments'] = ", ".join([d for d in others if d])
            else:
                r['other_departments'] = None
            headersdep.append(r)
        
        # set status and fullfillment date if required
        if not setting['manage_order_progress']:
            self.header['status'] = 'P'  # set as already processed
            self.header['fullfillment_date'] = self.header['date_time']
            for i in headersdep:
                i['fullfillment_date'] = self.header['fullfillment_date']
        # insert
        try:
            self.header.insert_record()
            t = self.header['order_header_id']
            ev = self.header['event_id']
            for r in headersdep:
                r['order_header_id'] = t
                # set barcode on header department if required
                if setting['manage_order_progress']:
                    # as we don't know header_department_id yet, we will create a unique barcode
                    # based on department barcode + order_header_id padded to 9 digits
                    r['barcode'] = f"{get_department_barcode(r['department_id'])}{t:09}"
            for r in self.lines:
                r['order_header_id'] = t
            self.lines.insert_records()
            headersdep.insert_records()
            for h in headersdep:
                for i in detail:
                    if get_item_dep(i['item_id']) == h['department_id']:
                        r = dict()
                        r['order_header_department_id'] = h['order_header_department_id']
                        r['event_id'] = self.header['event_id']
                        r['event_date'] = self.header['stat_order_date']
                        r['day_part'] = self.header['stat_order_day_part']
                        r['item_id'] = i['item_id']
                         #[j['order_header_department_id'] for j in headersdep 
                                                        #if j['department_id'] == get_item_dep(r['item_id'])][0]
                        r['variants'] = i['variants']
                        r['quantity'] = i['quantity']
                        if setting['manage_order_progress']:
                            r['ordered_quantity'] = i['quantity']
                        else:
                            r['delivered_quantity'] = i['quantity']
                        linesdep.append(r)
            linesdep.insert_records()
        except PyAppDBError as er:
            appconn.rollback()
            raise PyAppDBError(str(er))
        else:
            appconn.commit()
            return t, used_dep
