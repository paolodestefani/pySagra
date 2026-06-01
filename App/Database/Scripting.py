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

"""Database - Scripting

This module provides classes and functions for database scripting management

"""

# standard library
import logging
from typing import Any, List

# application modules
from App.Core.Database import db_exception_context
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
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        if cur.rowcount:
            return {(m, j): s for m, j, s in cur.fetchall()}
        else:
            return {}


def load_script(cls: str,
                mth: str, 
                trg: str, 
                act: bool,
                cmp: int,
                script: str) -> None:
    "Load a python script to database overwriting if necessary"
    sql = t"""
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
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(sql)


def get_all_scripts() -> List[Any]:
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
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()
