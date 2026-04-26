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

"""database - connections management

This module provide all the facilities to manage connections

"""

# psycopg
import psycopg

# apllication modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


def current_logins() -> int:
    "Returns the number of logged users"
    sql = """
SELECT count(*) 
FROM system.connection;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(sql)
            return next(cur)[0]
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def delete_connection_history(days: int) -> None:
    "Delete connection log table - all records or older then provided days"
    script = """
DELETE FROM system.connection_history
WHERE cast(logout_datetime as date) <= (current_date - %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (days,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def kill_client(cid: int) -> None:
    "Kills the client of cid process id"
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute('SELECT system.pa_kill_client(%s);', (cid,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
