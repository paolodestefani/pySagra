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

"""database - users management

This module provide all the facilities to manage application users

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def user_list() -> list:
    sql = """
SELECT id 
FROM system.app_user;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(sql)
                return [i[0] for i in cur.fetchall()]
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def user_company_set(user: str,
                     company: int,
                     profile: str,
                     menu: str,
                     toolbar: str
                     ) -> None:
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT system.pa_user_company_set(%s, %s, %s, %s, %s);',
                            (user, company, profile, menu, toolbar))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def change_password(user: str, new_password: str) -> None:
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute('SELECT system.pa_password_change(%s, %s);',
                            (user, new_password,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def encrypt_password(password: str) -> str:
    sql = "SELECT system.crypt(%s, system.gen_salt('bf'));"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(sql, (password,))
                result = next(cur, None)
                if result:
                    return result[0]
                raise PyAppDBError("00000", "Password encryption failed")
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def force_password_change(user: str) -> None:
    sql = """
UPDATE system.app_user
SET is_change_password_required = true
WHERE code = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(sql, (user,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

# def user_email_list(user):
#     "Returns a list of the email accounts for user"
#     sql = """SELECT id, description || ' - ' || sender
#     FROM system.app_user_email
#     WHERE app_user = %s
#     ORDER BY sorting;"""
#     try:
#         with appconn.transaction():
#             with appconn.cursor() as cur:
#                 cur.execute(sql, (user,))
#                 return cur.fetchall()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.diag.sqlstate, str(er))

# def user_email_details(account):
#     "Returns all the parameter for the account id"
#     sql = """SELECT sender,
#     reply_to,
#     server,
#     port,
#     account_user,
#     account_password,
#     require_auth,
#     require_ssl,
#     require_tls,
#     sender_copy
#     FROM system.app_user_email
#     WHERE id = %s;"""
#     try:
#         with appconn.transaction():
#             with appconn.cursor() as cur:
#                 cur.execute(sql, (account,))
#                 return cur.fetchone()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.diag.sqlstate, str(er))

# def user_email_signature(account):
#     "Returns signature for the account id"
#     sql = """SELECT signature, sender_copy
#     FROM system.app_user_email
#     WHERE id = %s;"""
#     try:
#         with appconn.transaction():
#             with appconn.cursor() as cur:
#                 cur.execute(sql, (account,))
#                 return cur.fetchone() or (None, False)
#     except psycopg.Error as er:
#         raise PyAppDBError(er.diag.sqlstate, str(er))

    # if cur.rowcount:
        # return cur.fetchone()[0] or 0 # if stock not set balance is null
    # return 0
