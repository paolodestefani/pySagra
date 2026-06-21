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

"""Database - Connections management

This module provides all the facilities to manage connections

"""

# standard library
import logging

# apllication modules
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def current_logins() -> int:
    "Returns the number of logged users"
    sql = """
SELECT count(*) 
FROM system.connection;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(sql)
        return next(cur, (0,))[0]  # Safely get the first result or return 0 if no rows


def delete_connection_history(days: int) -> None:
    "Delete connection log table - all records or older then provided days"
    script = t"""
DELETE FROM system.connection_history
WHERE cast(logout_datetime as date) <= (current_date - {days});"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def kill_client(cid: int) -> None:
    "Kills the client of cid process id"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT system.pa_kill_client({cid});')
    