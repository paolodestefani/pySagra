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

"""Database - Menu management

This module provide class and functions for application menu management


"""

# standard library
import logging

# application modules
from App.Core.Database import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def duplicate_menu(from_code: str, new_code: str, new_description: str) -> None:
    "Create a new menu copying parameters from another"
    # create a new menu
    script1 = t"""
INSERT INTO system.menu_toolbar (
    type,
    code,
    description) 
VALUES (
    'M',
    {new_code},
    {new_description});"""

    # copy first level menu items
    script2 = t"""
INSERT INTO system.menu_toolbar_item (
    parent,
    child,
    description,
    sorting,
    item_type,
    action)
SELECT 
    {new_code},
    child,
    description,
    sorting,
    item_type,
    action
FROM system.menu_toolbar_item
WHERE parent = {from_code};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.execute(script2)






