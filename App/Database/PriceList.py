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

"""Database - Price list management

This module provides classes and functions for price list database management

"""

# standard library
import logging

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Core.Database import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def duplicate_price_list(from_id: int, new_description: str) -> None:
    "Create a new price list copying prices from another"
    # t-string parameter are evaluated just when the scriptt-string is created
    # we nee to move the definition of script2 after the execution of script1 
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        # create a new price list
        new_id = None
        script1 = t"""
INSERT INTO price_list (company_id, description) 
VALUES (system.pa_current_company(), {new_description}) 
RETURNING price_list_id;"""
        cur.execute(script1)
        new_id = next(cur, (None,))[0]
        if new_id is None:
            raise PyAppDBError("02000", "No id returned from database when creating new price list")
        # copy prices from another price list
        script2 = t"""
INSERT INTO price_list_item (
    company_id,
    price_list_id,
    item_id,
    price)
SELECT
    system.pa_current_company(),
    {new_id},
    item_id,
    price
FROM price_list_item
WHERE price_list_id = {from_id};"""
        cur.execute(script2)
