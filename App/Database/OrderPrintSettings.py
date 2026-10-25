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

"""Database - Order print setting

This module provides classes and functions for database order print settings

"""

# standard library
import logging
from typing import Any

# application modules
from App import session
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def order_print_settings(print_type: str,
                         department_id: int | None ) -> Any | None:
    "Order print settings for customer/Department/Cover copy, include settings parameter"
    if department_id is None:
        script = t"""
    SELECT 
        (o.print_copy AND 
            s.print_customer_copy) AS print_customer_copy,
        o.print_method,
        o.number_of_copies,
        o.driver_report,
        o.driver_printer,
        o.escpos_report,
        o.escpos_printer
    FROM order_print_settings o
    JOIN settings s ON o.company_id = s.company_id
    WHERE 
            s.company_id = system.pa_current_company()
        AND o.hostname = {session['hostname']}
        AND o.print_type = {print_type};
    """
    else:
        script = t"""
            SELECT 
                (o.print_copy AND 
                    s.print_customer_copy) AS print_customer_copy,
                o.print_method,
                o.number_of_copies,
                o.driver_report,
                o.driver_printer,
                o.escpos_report,
                o.escpos_printer
            FROM order_print_settings o
            JOIN settings s ON o.company_id = s.company_id
            WHERE 
                    s.company_id = system.pa_current_company()
                AND o.hostname = {session['hostname']}
                AND o.print_type = {print_type}
                AND o.department_id = {department_id};
            """
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchone()


def copy_order_print_settings(from_host: str, to_host: str) -> None:
    "Copy all settings from / to the provided host names"
    script = t"""
INSERT INTO order_print_settings(
	company_id,
	hostname,
	print_type,
	department_id,
	print_copy,
	print_method,
	number_of_copies,
	driver_report,
	driver_printer,
	escpos_report,
	escpos_printer
)
SELECT
	company_id,
	{to_host},
	print_type,
	department_id,
	print_copy,
	print_method,
	number_of_copies,
	driver_report,
	driver_printer,
	escpos_report,
	escpos_printer
FROM order_print_settings
WHERE company_id = system.pa_current_company()
	AND hostname = {from_host}
ORDER BY order_print_settings_id;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        