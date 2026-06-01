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

"""Database - System settings

This module provides classes and functions for system settings management

"""

# standard library
import logging

# application modules
from App.Core.Database import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def pa_setting(setting: str) -> str | None:
    "Get current value of the system setting parameter"
    # all arguments must be string
    setting = str(setting)
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT * FROM system.pa_setting({setting});')
        return next(cur, (None,))[0]


def pa_setting_set(setting: str, 
                   value: str | None
                   ) -> None:
    "Set the privided setting parameter to value"
    # all arguments must be string
    setting = str(setting)
    if value is not None: # must keep None (=NULL) != string
        value = str(value)
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(t'SELECT system.pa_setting_set({setting}, {value});')