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

"""Database - WebOrderServer module

This module provides classes and functions for web order server updating

"""

# standard library
import logging

# application modules
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn
from App.Core.Cryptography import string_encode
from App.Core.Cryptography import string_decode


# logger
logger = logging.getLogger(__name__)


def get_web_order_server_params() -> tuple[str | None, int | None, str | None, str | None, str | None, str | None]:
    "Get web order server connection parameters and file name"
    script = """
SELECT
    server_address,
    port_number,
    encoding_type,
    user_name,
    user_password,
    file_name
FROM web_order_server
WHERE company_id = system.pa_current_company();
"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        r = cur.fetchone()  # must be only one record
        if r:
            return (r[0],
                    r[1],
                    r[2],
                    string_decode(r[3]),
                    string_decode(r[4]),
                    string_decode(r[5]))
        else:
            return (None, 
                    None,
                    None,
                    None,
                    None,
                    None)


def set_web_order_server_params(server: str,
                                port: int,
                                encoding: str,
                                username: str,
                                password: str,
                                filename: str) -> None:
    "Set web order server connection parameters and file name"
    script = t"""
INSERT INTO web_order_server (
    company_id, 
    server_address,
    port_number,
    encoding_type,
    user_name,
    user_password,
    file_name)
VALUES (
        system.pa_current_company(),
        {server},
        {port},
        {encoding},
        {string_encode(username)},
        {string_encode(password)},
        {string_encode(filename)})
ON CONFLICT ON CONSTRAINT web_order_server_pk DO 
UPDATE 
SET server_address = EXCLUDED.server_address,
    port_number = EXCLUDED.port_number,
    user_name = EXCLUDED.user_name,
    user_password = EXCLUDED.user_password,
    file_name = EXCLUDED.file_name;
"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
    
