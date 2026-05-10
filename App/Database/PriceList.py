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

"""database - price lists management

This module provide all the facilities to manage price lists


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


def duplicate_price_list(from_id: int, new_description: str) -> None:
    "Create a new price list copying prices from another"
    # create a new price list
    script1 = t"""
INSERT INTO price_list (description) 
VALUES ({new_description}) 
RETURNING price_list_id;"""
# copy prices from another price list
    script2 = t"""
INSERT INTO price_list_item (
    price_list_id,
    item_id,
    price)
SELECT 
    {new_id},
    item_id,
    price
FROM price_list_item
WHERE price_list_id = {from_id};"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script1)
                new_id = next(cur)
                if new_id is None:
                    raise PyAppDBError("02000", "No id returned from database when creating new price list")
                else:
                    new_id = new_id[0]
                cur.execute(script2)
    except psycopg.Error as er:
        logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
        raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))
