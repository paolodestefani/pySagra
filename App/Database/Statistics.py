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

"""Database - Statistics management

This module provides classes and functions for statistics management

"""

# standard library
from typing import Any

# pandas
#import pandas as pd

# application modules
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn


# def load_pandas_dataframe():
#     script = """
# SELECT * 
# FROM company.bi_order_header
# WHERE company = system.pa_current_company();"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script)
#             df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
#             #print(df.head())
#             return df
#     except psycopg.Error as er:
#         raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))   


def load_statistic_bi_data(view: str,
                           from_event: int,
                           to_event: int
                           ) -> list[tuple[Any, ...]]:
    "Load a statistic data"
    script = f"""SELECT * FROM {view} WHERE event_id BETWEEN %s AND %s AND company_id = system.pa_current_company();"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script, (from_event, to_event))
        if cur.rowcount:
            return cur.fetchall()
        else:
            return []

