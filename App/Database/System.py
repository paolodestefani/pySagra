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

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def pa_setting(setting: str) -> str|None:
    "Get current value of the system setting parameter"
    # all arguments must be string
    setting = str(setting)
    try:
        with appconn.cursor() as cur:
            cur.execute(t'SELECT * FROM system.pa_setting({setting});')
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))


def pa_setting_set(setting: str, value: str|None) -> None:
    "Set the privided setting parameter to value"
    # all arguments must be string
    setting = str(setting)
    if value is not None: # must keep None (=NULL) != string
        value = str(value)
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(t'SELECT system.pa_setting_set({setting}, {value});')
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
