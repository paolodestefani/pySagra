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

"""Database - Users management

This module provides classes and functions for users management

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


def user_list() -> list:
    script = """
SELECT id 
FROM system.app_user;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
                return [i[0] for i in cur.fetchall()]
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def user_company_set(user: str,
                     company: int,
                     profile: str,
                     menu: str,
                     toolbar: str
                     ) -> None:
    script = t'SELECT system.pa_user_company_set({user}, {company}, {profile}, {menu}, {toolbar});'
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def change_password(user: str, new_password: str) -> None:
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(t'SELECT system.pa_password_change({user}, {new_password});')
    except psycopg.Error as er:
        rlogger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    

def encrypt_password(password: str) -> str:
    script = t"SELECT system.crypt({password}, system.gen_salt('bf'));"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
                result = next(cur, None)
                if result:
                    return result[0]
                raise PyAppDBError("00000", "Password encryption failed")
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    

def force_password_change(user: str) -> None:
    script = t"""
UPDATE system.app_user
SET is_change_password_required = true
WHERE code = {user};"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
