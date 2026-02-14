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

"""database - scripting


"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


def get_script(class_id: str) -> dict:
    "Return script bind to provided class"
    script = """SELECT method_name, trigger, script
FROM system.python_scripting
WHERE class_name = %s AND is_active IS true;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (class_id,))
            if cur.rowcount:
                return {(m, j): s for m, j, s in cur.fetchall()}
            else:
                return {}
    except psycopg.Error as er:
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))


def load_script(cls: str,
                mth: str, 
                trg: str, 
                script: str, 
                act: bool
                ) -> None:
    "Load a python script to database overwriting if necessary"
    sql = """INSERT INTO system.python_scripting (class_name, method_name, trigger, script, is_active)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT python_scripting_pkey DO
    UPDATE SET script = %s, is_active = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(sql, (cls, mth, trg, script, act, script, act))
    except psycopg.Error as er:
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))
