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

"""Cash desk management

This module provide all the facilities to manage cash desks

"""

# psycopg
import psycopg

# pySide6
#from PySide6.QtCore import QDate
from PySide6.QtNetwork import QHostInfo

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


def get_cash_desk_description() -> str|None:
    "Get desk description for current computer name"
    sql = """
SELECT
    cash_desk_description
FROM cash_desk
WHERE
    company_id = system.pa_current_company()
    AND computer = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(sql, (QHostInfo.localHostName(),))
            if cur.rowcount:
                return cur.fetchone()[0]
            else:
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))   

