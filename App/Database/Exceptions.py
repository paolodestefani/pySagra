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

"""Database - Exceptions

Definition of database exceptions

"""

# standard library
from contextlib import contextmanager
import logging
from typing import Generator
from typing import Optional

import psycopg

logger = logging.getLogger(__name__)


# Exceptions hierarchy
#
# PyAppDatabaseException
#   -> PyAppDBWarning
#   -> PyAppDBInfo
#   -> PyAppDBError
#      -> PyAppDBConnectionError
#      -> PyAppDBFunctionError
#      -> PyAppDBConcurrencyError


class PyAppDatabaseException(Exception):
    "Base exception class for all database interactions"
    
    def __init__(self, 
                 code: Optional[str] = None,
                 message: Optional[str] = None,
                 detail: Optional[str] = None) -> None:
        # Passiamo il messaggio a Exception. str(error) eviterà cicli infiniti.
        super().__init__(message) 
        self.code: str = code or 'UNKNOWN'
        self.message: str = message or ''
        self.detail: str = detail or ''

    def __str__(self) -> str:
        "Format the message if printed"
        if self.detail:
            return f"[{self.code}] {self.message} - {self.detail}"
        return f"[{self.code}] {self.message}"


# --- Level 1: main exceptions ---

class PyAppDBWarning(PyAppDatabaseException):
    "Warnings from database server"


class PyAppDBInfo(PyAppDatabaseException):
    "Informational messages from database server"


class PyAppDBError(PyAppDatabaseException):
    "Generic error on interacting with database server"


# --- Level 2: specific errors (inherit from PyAppDBError) ---

class PyAppDBConnectionError(PyAppDBError):
    "Errors on connecting to database server"


class PyAppDBFunctionError(PyAppDBError):
    "Errors execution database functions or procedures"


class PyAppDBConcurrencyError(PyAppDBError):
    "Error on row modified before update/delete"

    def __init__(self, 
                 code: str = 'CCER', 
                 message: str = 'Row modified before update/delete', 
                 detail: Optional[str] = None) -> None:
        # Manteniamo la firma compatibile con la classe base usando i parametri di default
        super().__init__(code=code, message=message, detail=detail)


# Context manager to capture psycopg errors and raise custom exceptions

@contextmanager
def db_exception_context() -> Generator[None, None, None]:
    """
    Context manager to catch native psycopg 3 errors, 
    log them centrally, and raise a custom PyAppDBError exception.
    """
    try:
        yield
    except psycopg.Error as er:
        # Extract SQLSTATE (e.g., '23505'). Fallback to 'UNKNOWN' if missing.
        sqlstate: str = er.sqlstate or 'UNKNOWN'
        
        # In psycopg 3, the attribute is 'diag', which returns a Diagnostic object
        diag = er.diag
        
        # Safely extract messages ensuring Mypy knows they can be strings
        primary_msg: str = diag.message_primary if diag and diag.message_primary else str(er)
        detail_msg: str = diag.message_detail if diag and diag.message_detail else ''

        # Structural logging for developers
        logger.error(
            "*** DATABASE ERROR ***\nSQL State: %s\nPrimary: %s\nDetail: %s", 
            sqlstate, 
            primary_msg, 
            detail_msg
        )
        
        # Raise the custom exception for the GUI layer
        raise PyAppDBError(code=sqlstate, message=primary_msg, detail=detail_msg) from er
