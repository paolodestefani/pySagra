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

"""Database - ESC/POS

Database classes and functions related to ESC/POS printers.

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


def get_escpos_printer_params(printer_id: int) -> tuple[Any] | None:
    "Returns all the parameters for printer_id"
    script = t"""
SELECT
    hostname,
    name,
    type,
    -- network printer
    host,
    port,
    connection_timeout,
    -- USB printer
    id_vendor,
    id_product,
    usb_timeout,
    in_endpoint,
    out_endpoint
FROM escpos_printer
WHERE escpos_printer_id = {printer_id};"""
    # Unified context managers ensuring proper evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchone()
    
    
def get_escpos_printers() -> list[Any] | None:
    "Returns the ESC/POS printer list optionally filtered by host name"
    script = t"""
SELECT
    escpos_printer_id,
    name
FROM escpos_printer
WHERE company_id = system.pa_current_company()
    AND hostname = {session['hostname']};
"""
    # Unified context managers ensuring proper evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()
    
