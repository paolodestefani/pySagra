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

"""Database - Company

This module provides database functions used for company management

"""

# standard library
import logging

# application modules
from App.Database.Exceptions import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def max_company_code() -> int:
    "Return current used max company code"
    script = """
SELECT 
    max(company_id) 
FROM system.company;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (0,))[0] or 10 # Safely get the first result or return 0 if no rows
   

def company_is_in_use(company: int) -> bool:
    "Return True if the company is currently in use"
    script = t"""
SELECT company_id 
FROM system.connection 
WHERE company_id = {company};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        # Using fetchone() is safer than rowcount for SELECT queries in psycopg 3
        return cur.fetchone() is not None


def create_company(company_id: int,
                   company_desc: str,
                   company_image: bytes | bytearray | memoryview[int] | None
                   ) -> None:
    "Create a new company with the given parameters"
    script = t"""
SELECT system.pa_company_create({company_id}, {company_desc}, {False}, {company_image});
"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def drop_company(company_id: int) -> None:
    "Drop company"
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t"SELECT system.pa_company_drop({company_id});")
        

def set_company_access(company_id: int,
                       user_code: str,
                       profile_code: str,
                       menu_code: str,
                       toolbar_code: str
                       ) -> None:
    "Set access company for one user to the given company"
    script = t"""
INSERT INTO system.app_user_company (
    company_id,
    app_user_code,
    profile_code,
    menu_code,
    toolbar_code)
VALUES (
    {company_id},
    {user_code}, 
    {profile_code}, 
    {menu_code}, 
    {toolbar_code});"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
    

def company_list() -> list[tuple]:
    "Return available companies in current database"
    script = """
SELECT 
    company_id, 
    description 
FROM system.company;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()
        