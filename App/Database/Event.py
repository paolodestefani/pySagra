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

"""Database - Event management

This module provides classes and functions for database management of events

"""

# standard library
from typing import Any
import logging

# psycopg
import psycopg

# pySide6
from PySide6.QtCore import QDate

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def get_event_data(event: int) -> Any:
    "Get event data"
    script = t"""
SELECT
    description,
    start_date,
    end_date,
    price_list_id
FROM event
WHERE event_id = {event};"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return next(cur, None)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))  


def is_used(event: int) -> bool:
    "Returns True if have orders for the given event"
    script = t"""
SELECT EXISTS(
    SELECT event_id 
    FROM order_header 
    WHERE event_id = {event} 
    LIMIT 1);"""
    try:
        with appconn.cursor() as cur:
            result = cur.execute(script).fetchone()
            if result:
                return result[0]
            else:
                return False
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    
    
def get_event_from_date(date: QDate) -> tuple[int, str] | None:
    "Get event id from QDate or QDateTime"
    script = t"""
SELECT 
    event_id,
    description
FROM event
WHERE
        company_id = system.pa_current_company()
    AND start_date <= {date} AND end_date >= {date};"""
    try:
        with appconn.cursor() as cur:
            result = cur.execute(script).fetchone()
            if result:
                return result
            else:
                return None
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))

