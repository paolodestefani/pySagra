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

"""database - profiles management

This module provide all the facilities to manage application profiles

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def duplicate_profile(from_code: str, new_code: str, new_description: str) -> None:
    "Create a new profile copying parameters from another"
    # create a new profile
    sql = "INSERT INTO system.profile (profile_code, description) VALUES (%s, %s);"
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(sql, (new_code, new_description))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    # copy authorizations
    sql = """INSERT INTO system.profile_action (profile_code, action, auth)
SELECT %s, action, auth
FROM system.profile_action
WHERE profile_code = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(sql, (new_code, from_code))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
