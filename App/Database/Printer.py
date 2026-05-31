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

"""Database - Printer class

This module provides classes and functions for database printer management

"""

# standard library
import logging

# application modules
from App.Database.Exceptions import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def get_printer_name(class_id: int, computer: str) -> str | None:
    "Return the printer name of class_id"
    script = t"""
SELECT printer
FROM printer_class_printer
WHERE 
        printer_class_id = {class_id} 
    AND computer = {computer};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (None,))[0]
