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

"""Database - Report

Database functions for report management

"""

# standard library
import logging

# application modules
from App.Report import REPORT_CLASSES
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn
from App.Report.ReportEngine import Report


# logger
logger = logging.getLogger(__name__)


def delete_all_reports() -> None:
    "Delete all reports, update identity"
    script = """
DELETE FROM system.report;
ALTER TABLE system.report ALTER COLUMN report_id RESTART WITH 1;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def load_report(report_code: str,
                l10n: str,
                report_class: str, 
                system: bool, 
                description: str,
                xml_data: str
                ) -> None:
    "Load a report filling system.report"
    script = t"""
INSERT INTO system.report (
    report_code,
    l10n,
    report_class,
    description,
    xml_data,
    is_system_object)
VALUES (
    {report_code}, 
    {l10n},
    {report_class},
    {description},
    {xml_data},
    {system})
ON CONFLICT ON CONSTRAINT report_unique DO
UPDATE 
SET report_class = {report_class}, 
    description = {description},
    xml_data = {xml_data},
    is_system_object = {system};
"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)


def list_all_reports() -> list:
    "List all reports from system.report for exporting purposes"
    script = f"""
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
{", \n".join([f"({i}, '{j}')" for i, j in enumerate(REPORT_CLASSES, start=1)])}
	    ) v(i, c)) v 
	ON r.report_class = v.c 
ORDER BY v.i, report_code, l10n;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()

    
def report_class_adapt_list(class_code: str, l10n: str='en_US') -> list:
    "Return id and description of all the report customizations for the input class"
    script = t"""
SELECT 
    ra.adaptation_id, 
    ra.description
FROM system.adaptation ra
JOIN system.report r ON ra.report_id = r.report_id
WHERE 
        r.report_class = {class_code}
    AND r.l10n = {l10n}
ORDER BY ra.class_sorting;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()


def get_report_list(report_class: str,
                    l10n: str, 
                    null: bool=False
                    ) -> list:
    "Return code and description of all reports of l10n localization or en_US"
    script = t"""
SELECT 
    report_id,
    report_code, 
    description
FROM system.report
WHERE 
        report_class = {report_class} 
    AND l10n = {l10n};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        records = cur.fetchall()
        return [(None, '')] + records if null else records


def report_description(report_id: int) -> str | None:
    "Return the report description of report code of l10n localization or en_US"
    script = t"""
SELECT 
    description
FROM system.report
WHERE report_id = {report_id};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (None,))[0]
 
    
def get_report_id(report_code: str, l10n: str) -> int:
    "Return the report ID of report code and l10n localization or en_US"
    script = t"""
SELECT coalesce(a.report_id, b.report_id)
FROM system.report a
JOIN system.report b ON a.report_code = b.report_code AND b.l10n = 'en_US'
WHERE a.report_code = {report_code} AND a.l10n = {l10n};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (0,))[0]


def report_xml(report_id: int) -> str | None:
    "Report XML definition of the report for required report customization"
    script = t"""
SELECT 
    xml_data
FROM system.report
WHERE report_id = {report_id};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (None,))[0]


def get_report_from_adapt(adapt_id: int) -> tuple | tuple[None]:
    script = t"""
SELECT 
    r.report_id,
    r.report_code,
    r.report_class,
    r.description,
    r.l10n
FROM system.report r
JOIN system.adaptation ra ON r.report_id = ra.report_id AND ra.type = 'R'
WHERE ra.adaptation_id = {adapt_id};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (None, None, None, None, None))


def report_query(report: Report, 
                 condition: list | None = None,
                 sorting: list | None = None
                 ) -> list | None:
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
    #print(script)
    #print(args)
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script, args)
        return cur.fetchall()
