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

# standard library
import logging

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def get_script(class_id: str) -> dict:
    "Return script bind to provided class for current company"
    script = t"""
SELECT 
    method_name,
    trigger,
    script
FROM system.python_scripting
WHERE 
        company_id = system.pa_current_company()
    AND class_name = {class_id} 
    AND is_active IS true;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            if cur.rowcount:
                return {(m, j): s for m, j, s in cur.fetchall()}
            else:
                return {}
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def load_script(cls: str,
                mth: str, 
                trg: str, 
                act: bool,
                cmp: int,
                script: str) -> None:
    "Load a python script to database overwriting if necessary"
    script = t"""
INSERT INTO system.python_scripting (
    class_name,
    method_name,
    trigger,
    is_active,
    company_id,
    script)
VALUES (
    {cls},
    {mth},
    {trg},
    {act},
    {cmp},
    {script})
ON CONFLICT ON CONSTRAINT python_scripting_unique DO
UPDATE 
SET script = {script},
    is_active = {act};
"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def get_all_scripts() -> None:
    "Get all python scripts available"
    script = """
SELECT 
    class_name,
    method_name,
    trigger,
    is_active,
    company_id,
    script
FROM system.python_scripting;
"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
