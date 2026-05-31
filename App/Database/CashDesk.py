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

"""Database - Cash desk management

This module provides database functione required for manage cash desks

"""

# standard library
import logging


# pySide6
from PySide6.QtNetwork import QHostInfo

# application modules
from App.Database.Exceptions import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def get_cash_desk_description() -> str | None:
    "Get desk description for current computer name"
    script = t"""
SELECT
    cash_desk_description
FROM cash_desk
WHERE
    company_id = system.pa_current_company()
    AND computer = {QHostInfo.localHostName()};"""
    # Unified context managers handling error trapping, transaction lifecycle, and cursor
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return next(cur, (None,))[0]  # Safely get the first result or return None if no rows
   
