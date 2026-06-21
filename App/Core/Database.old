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

"""Database module

This module manages database core functions and classes

"""

# standard library
from contextlib import contextmanager
import logging
from logging import Logger
from typing import Generator
from typing import Optional

import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Core.L10n import _tr


# fallback logger for database module (used if no logger is passed to the context manager)
default_logger = logging.getLogger(__name__)


# Context manager to capture psycopg errors and raise custom exceptions

@contextmanager
def db_exception_context(logger: Optional[Logger] = None) -> Generator[None, None, None]:
    # Se passi il logger del modulo, usa quello, altrimenti usa il fallback
    active_logger = logger or default_logger
    
    try:
        yield
    except psycopg.Error as er:
        sqlstate: str = er.sqlstate if er.sqlstate is not None else 'UNKNOWN'
        diag = er.diag
        
        primary_msg: str = diag.message_primary if diag and diag.message_primary else str(er).strip()
        detail_msg: str = diag.message_detail if diag and diag.message_detail else ''

        # The log will use the passed logger module!
        active_logger.error(
            "*** DATABASE ERROR ***\nSQL State: %s\nPrimary: %s\nDetail: %s", 
            sqlstate, 
            primary_msg, 
            detail_msg,
            stacklevel=3
        )
        # Raise the custom exception for the GUI layer
        raise PyAppDBError(code=sqlstate, message=primary_msg, detail=detail_msg) from er





