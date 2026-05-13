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

"""Database - Profiles management

This module provides classes and functions for application profiles database management

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


def duplicate_profile(from_code: str, new_code: str, new_description: str) -> None:
    "Create a new profile copying parameters from another"
    # create a new profile
    script = t"""
INSERT INTO system.profile (
    profile_code,
    description) 
VALUES (
    {new_code},
    {new_description});"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
    # copy authorizations
    script = t"""
INSERT INTO system.profile_action (
    profile_code,
    action,
    auth)
SELECT 
    {new_code},
    action,
    auth
FROM system.profile_action
WHERE profile_code = {from_code};"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
