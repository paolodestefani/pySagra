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

# application modules
from App.Core.Database import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def duplicate_profile(from_code: str, new_code: str, new_description: str) -> None:
    "Create a new profile copying parameters from another"
    # create a new profile
    script1 = t"""
INSERT INTO system.profile (
    profile_code,
    description) 
VALUES (
    {new_code},
    {new_description});"""

    # copy authorizations
    script2 = t"""
INSERT INTO system.profile_action (
    profile_code,
    action,
    read,
    write,
    execute)
SELECT 
    {new_code},
    action,
    read,
    write,
    execute
FROM system.profile_action
WHERE profile_code = {from_code};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.execute(script2)
