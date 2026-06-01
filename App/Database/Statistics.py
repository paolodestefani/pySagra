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
from App.Core.Database import db_exception_context
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
                           ) -> list[Any] | None:
    "Load a statistic data"
    script = f"""SELECT * FROM {view} WHERE "ID Evento" BETWEEN %s AND %s;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script, (from_event, to_event))
        if cur.description:
            return [(i[0] for i in cur.description)] + cur.fetchall()
        else:
            return []


# def available_statistics() -> tuple:
#     "Returns (ordered) code and description of active statistcs"
#     script = """SELECT code, description
#     FROM statistics_configuration
#     WHERE active IS true
#     ORDER BY sorting;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script)
#             return cur.fetchall()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def statistics_configuration(code: str) -> tuple:
#     "Returns the configuration of the required statistics"
#     script = """SELECT code, description, sql_query, sql_group_by, totals_row, total_label_column
#     FROM statistics_configuration
#     WHERE code = %s;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script, (code,))
#             return cur.fetchone()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def statistics_configuration_columns(code: str) -> tuple:
#     "Returns the columns definition of configuration required"
#     script = """SELECT definition,
#     description,
#     true, -- read only
#     column_type
#     FROM statistics_configuration_column
#     WHERE configuration_code = %s
#     ORDER BY sorting;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script, (code,))
#             return cur.fetchall()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def statistics_configuration_full_columns(code: str) -> tuple:
#     "Returns the columns definition of configuration required"
#     script = """SELECT definition,
#     description,
#     column_type,
#     sorting,
#     total_required
#     FROM statistics_configuration_column
#     WHERE configuration_code = %s
#     ORDER BY sorting;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script, (code,))
#             return cur.fetchall()
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def statistics_configuration_totals_columns(code: str) -> list|None:
#     "Returns the columns that require a total for given configuration"
#     script = """SELECT definition
#     FROM statistics_configuration_column
#     WHERE total_required IS true AND configuration_code = %s;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script, (code,))
#             if cur.rowcount:
#                 return [i[0] for i in cur.fetchall()]
#             else:
#                 return []
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def statistics_configuration_report(code: str) -> str|None:
#     "Returns the report code of that require configuration code"
#     script = """SELECT report_code
#     FROM statistics_configuration
#     WHERE code = %s;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script, (code,))
#             if cur.rowcount:
#                 return cur.fetchone()[0]
#             else:
#                 return None
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def load_statistic_configuration(code: str, 
#                                  description: str, 
#                                  active: bool, 
#                                  sorting: int, 
#                                  query: str, 
#                                  groupby: str, 
#                                  totals: bool, 
#                                  totcolumn: str, 
#                                  report: str
#                                  ) -> None:
#     "Load a statistic configuration"
#     script = """INSERT INTO statistics_configuration (code, description,
# active, sorting, sql_query, sql_group_by, totals_row, total_label_column, report_code)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
# ON CONFLICT ON CONSTRAINT statistics_configuration_pkey DO
# UPDATE
# SET description = %s, active = %s, sorting = %s, sql_query = %s,
# totals_row = %s, total_label_column = %s, report_code = %s;"""
#     try:
#         with appconn.cursor() as cur:
#             cur.execute(script, (code, description, active, sorting, query, groupby, totals, totcolumn, report,
#                                     description, active, sorting, query, totals, totcolumn, report))
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


# def load_statistic_configuration_column(code, definition, description, coltype, sorting, totals):
#     "Load a statistic configuration column"
#     script = """INSERT INTO statistics_configuration_column (configuration_code,
# definition, description, column_type, sorting, total_required)
# VALUES (%s, %s, %s, %s, %s, %s)
# ON CONFLICT ON CONSTRAINT statistics_configuration_column_pkey DO
# UPDATE
# SET description = %s, column_type = %s, sorting = %s, total_required = %s;"""
#     try:
#         with appconn.conn:
#             with appconn.cursor() as cur:
#                 cur.execute(script, (code, definition, description, coltype, sorting, totals,
#                                      description, coltype, sorting, totals))
#     except psycopg.Error as er:
#         raise PyAppDBError(er.pgcode, er.pgerror)


