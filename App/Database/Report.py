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

"""database - sql report extraction



"""
# standard library
from typing import Callable

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn
from App.Report.ReportEngine import Report


def delete_all_reports() -> None:
    "Delete all reports, update identity"
    script = """
DELETE FROM system.report;
ALTER TABLE system.report ALTER COLUMN report_id RESTART WITH 1;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def load_report(report_code: str,
                l10n: str,
                report_class: str, 
                system: bool, 
                description: str,
                xml_data: str
                ) -> None:
    "Load a report filling system.report"
    script = """
INSERT INTO system.report (
    report_code,
    l10n,
    report_class,
    description,
    xml_data,
    is_system_object)
VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT report_unique DO
	UPDATE SET report_class = %s, description = %s, xml_data = %s, is_system_object = %s;
    """
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (report_code,
                                     l10n,
                                     report_class,
                                     description,
                                     xml_data,
                                     system,
                                     report_class,
                                     description,
                                     xml_data,
                                     system))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def list_all_reports() -> list:
    "List all reports from system.report for exporting purposes"
    script = """
SELECT
    r.report_code,
    r.l10n,
    r.report_class,
    r.is_system_object,
    r.description,
    r.xml_data
FROM system.report r
-- set a specifit sorting
LEFT JOIN (
	SELECT v.i, v.c
	FROM (VALUES 
		(1, 'COMPANY'), 
		(2, 'PROFILE'),
		(3, 'USER'), 
		(4, 'PRINTER'),
        (5, 'TABLE'),
		(6, 'EVENT'),
		(7, 'ITEM'),
		(8, 'PRICE_LIST'),
		(9, 'ORDER_CUSTOMER'),
		(10, 'ORDER_DEPARTMENT'), 
		(11, 'ORDER_COVER'),
		(12, 'ORDER_LIST'), 
		(13, 'STOCK_UNLOAD'),
		(14, 'CASH_SUMMARY'), 
		(15, 'STATISTICS'),
		(16, 'STATSVIEW')
		) v(i, c)) v 
	ON r.report_class = v.c 
ORDER BY v.i, report_code, l10n;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def clear_report_adapt(adapt_id: int) -> None:
    "Clear the report customizations setting"
    script = """
DELETE FROM system.report_adapt_setting
WHERE report_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_report_adapt_setting(adapt_id: int) -> tuple:
    "Returns the report customizations"
    script = """
SELECT 
    adapt_type,
    layout_row,
    combo1_index,
    combo2_index,
    widget_value
FROM system.report_adapt_setting
WHERE report_adapt_id = %s
ORDER BY adapt_type, layout_row;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (adapt_id,))
            if cur.rowcount == 0:
                return [], [], [] # Parameters, Filters, Sorting
            else:
                d = cur.fetchall()
                p = [i for i in d if i[0] == 'P'] # Parameters
                f = [i for i in d if i[0] == 'F'] # Filters
                s = [i for i in d if i[0] == 'S'] # Sorting
                return p, f, s
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_report_adapt(adapt_id: int, 
                     adapt_type: str, 
                     layout_row: int,
                     combo1_index: int, 
                     combo2_index: int, 
                     widget_value: str
                     ) -> None:
    "Set the report adaptation definition"
    script = """
INSERT INTO system.report_adapt_setting (
    report_adapt_id, 
    adapt_type, 
    layout_row, 
    combo1_index, 
    combo2_index, 
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT ON CONSTRAINT report_adapt_setting_pk DO 
UPDATE
SET combo1_index = %s,
    combo2_index = %s,
    widget_value = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_id,
                                     adapt_type,
                                     layout_row,
                                     combo1_index,
                                     combo2_index,
                                     widget_value,
                                     combo1_index,
                                     combo2_index,
                                     widget_value))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def delete_report_adapt(adapt_id: int) -> None:
    "Delete report adapt"
    script = """
DELETE FROM system.report_adapt
WHERE report_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (adapt_id,))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def create_new_adapt(report_id: int, adapt_desc: str) -> None:
    "Create a new customization"
    script = """
INSERT INTO system.report_adapt (report_id, description)
VALUES (%s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (report_id, adapt_desc))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def report_class_adapt_list(class_code: str, l10n: str='en_US') -> list:
    "Return id and description of all the report customizations of the input class"
    script1 = """
SELECT 
    ra.report_adapt_id, 
    ra.description
FROM system.report_adapt ra
JOIN system.report r ON ra.report_id = r.report_id
WHERE r.report_class = %s AND r.l10n = %s 
ORDER BY ra.class_sorting;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script1, (class_code, l10n))
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def report_adapt_sorting(adapt_id: int) -> int:
    "Returns the report customization sorting index"
    script = """
SELECT 
    class_sorting
FROM system.report_adapt
WHERE report_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (adapt_id,))
            result = next(cur, None)
            if result:
                return result[0]
            else:
                return 0
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_report_adapt_sorting(adapt_id: int, sorting: int) -> None:
    "Set customization sorting index"
    script = """
UPDATE system.report_adapt
SET class_sorting = %s
WHERE report_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sorting, adapt_id))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))


def get_report_list(report_class: str,
                    l10n: str, 
                    null: bool=False
                    ) -> list:
    "Return code and description of all reports of l10n localization or en_US"
    script = """
SELECT 
    report_id,
    report_code, 
    description
FROM system.report
WHERE 
    report_class = %s AND
    l10n = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (report_class, l10n))
            records = cur.fetchall()
            return [(None, '')] + records if null else records
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def report_description(report_id: int) -> str|None:
    "Return the report description of report code of l10n localization or en_US"
    script = """
SELECT 
    description
FROM system.report
WHERE report_id = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (report_id,))
            result = next(cur, None)
            if result:
                return result[0]
            else:
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
    
def get_report_id(report_code: str, l10n: str) -> int:
    "Return the report ID of report code and l10n localization or en_US"
    script = """
SELECT coalesce(a.report_id, b.report_id)
FROM system.report a
JOIN system.report b ON a.report_code = b.report_code AND b.l10n = 'en_US'
WHERE a.report_code = %s AND a.l10n = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (report_code, l10n))
            result = next(cur, None)
            if result:                
                return result[0]
            else:                
                return 0
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def report_xml(report_id: int) -> str|None:
    "Report XML definition of the report for required report customization"
    script = """
SELECT 
    xml_data
FROM system.report
WHERE report_id = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (report_id,))
            result = next(cur, None)
            if result:
                return result[0]
            else:
                return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_report_from_adapt(adapt_id: int) -> tuple|None:
    script = """
SELECT 
    r.report_id,
    r.report_code,
    r.report_class,
    r.description,
    r.l10n
FROM system.report r
JOIN system.report_adapt ra ON r.report_id = ra.report_id
WHERE ra.report_adapt_id = %s;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script, (adapt_id,))
            return next(cur, None)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def report_query(report: Report, condition: list|None = None, sorting: list|None = None) -> list|None:
    "Returns dataset from report query/where/order by and dynamic where/orderby clauses"
    # remove trailing ; if any
    if not report.query:
        return None
    query = report.query.strip()
    script = query if query[-1] != ';' else query[:-1]
    # parameters
    if report.parameter:
        for i in report.parameter:
            if isinstance(report.parameter[i], tuple):
                script = script.replace(f"{{{{{i}}}}}", str(report.parameter[i][0]))
            else:
                script = script.replace(f"{{{{{i}}}}}", str(report.parameter[i]))
    # fixed where clause
    if report.query_where:
        script += f"\nWHERE {report.query_where}"
    # construct dynamic where clause
    # args must be a list, conditions can have the same field
    args = []
    if condition:
        if not report.query_where:
            script += "\nWHERE "
        else:
            script += ' AND '
        script += f"{' AND '.join([i[0] for i in condition])}"
        args += [i[1] for i in condition if i[1] is not None] # for unary operant es. IS NULL, IS NOT NULL
    # fixed group by
    if report.query_group_by:
        script += f"\nGROUP BY {report.query_group_by}"
    # fixed order by
    if report.query_order_by:
        script += f"\nORDER BY {report.query_order_by}"
    # construct dynamic order by clause
    if sorting:
        if not report.query_order_by:
            script += "\nORDER BY "
            script += f"{', '.join(sorting)}"
        else:
            script += f", {', '.join(sorting)}"
    # terminate script
    script += ";"
    # execute query and returns result set
    print(script)
    print(args)
    try:
        with appconn.cursor() as cur:
            #print(cur.mogrify(script, args))
            cur.execute(script, args)
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
