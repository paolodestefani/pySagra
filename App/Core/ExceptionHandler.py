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

"""Exception handlers

This module managesprovides exception handling functionsfor the application

"""

# standard library
import logging
from contextlib import contextmanager
from typing import Generator
from typing import Any
from typing import Optional

# psycopg
import psycopg

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QMessageBox

# application modules
from App.Database.Exceptions import PyAppDBConnectionError
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn
from App.Core.L10n import _tr


# main application and postgres error codes and messages mapping
error_code_messages = {
    # custom application error codes
    'PA001': _tr("PGError", "Wrong database server version (connect sp)"),
    'PA002': _tr("PGError", "Wrong application database (connect sp)"),
    'PA003': _tr("PGError", "Wrong application database version (connect sp)"),
    'PA004': _tr("PGError", "Authentication failed, user does not exist (connect sp)"),
    'PA005': _tr("PGError", "A password is required (connect sp)"),
    'PA006': _tr("PGError", "Authentication failed, wrong password (connect sp)"),
    'PA007': _tr("PGError", "Unknown company (change company)"),
    'PA008': _tr("PGError", "No access rights to required company (change company)"),
    'PA009': _tr("PGError", "Can not kill current connection (kill client)"),
    'PA011': _tr("PGError", "Database schema already exists (create company sp)"),
    'PA012': _tr("PGError", "Company id already exists (create company sp)"),
    'PA013': _tr("PGError", "Company is in use (drop company sp)"),

    'CCER': _tr("PGError", "Row modified before update/delete, roaload records"),
    
    # data exceptions
    '22000': _tr("PGError", "Generic data exception"),
    '22021': _tr("PGError", "Character not in repertoire"),
    '22008': _tr("PGError", "DateTime field overflow"),
    '22012': _tr("PGError", "Division by zero"),
    '22004': _tr("PGError", "Null value not allowed"),
    '22003': _tr("PGError", "Numeric value out of range"),
    '22P01': _tr("PGError", "Floating point exception"),
    # integrity constraint violations
    '23000': _tr("PGError", "Integrity constraint violation"),
    '23502': _tr("PGError", "Not null violation"),
    '23503': _tr("PGError", "Foreign key violation"),
    '23505': _tr("PGError", "Unique constraint violation"),
    '23514': _tr("PGError", "Check constraint violation"),
    # syntax error or access rule violation
    '42601': _tr("PGError", "Syntax error"),
    '42501': _tr("PGError", "Insufficient privilege"),
    '42703': _tr("PGError", "Column does not exist"),
    '42P09': _tr("PGError", "Ambiguous column name or alias")
}

# fallback logger for database module (used if no logger is passed to the context manager)
default_logger = logging.getLogger(__name__)


# Context manager to capture psycopg errors and raise custom exceptions

@contextmanager
def db_exception_context(logger: Optional[logging.Logger] = None) -> Generator[None, None, None]:
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


# Context manager to capture exceptions in GUI operations and show critical dialogs

@contextmanager
def gui_exception_context(parent_widget: Any, operation_title: str) -> Generator[None, None, None]:
    """
    Catches PyAppDBError exceptions, translates PostgreSQL SQLSTATE codes 
    into user-friendly localized messages, and displays a critical dialog.
    """
    # local import to avoid circular import and exception
    from App.Widget.Dialog import MessageBoxCritical
    QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
    try:
        try:
            yield
            
            # If the execution is successful, restore the cursor here
            if QGuiApplication.overrideCursor() is not None:
                if QGuiApplication.overrideCursor().shape() == Qt.CursorShape.WaitCursor:
                    QGuiApplication.restoreOverrideCursor()
                    
        except Exception:
            # reset the cursor in case of any exception and raise it for subsequent management
            if QGuiApplication.overrideCursor() is not None:
                if QGuiApplication.overrideCursor().shape() == Qt.CursorShape.WaitCursor:
                    QGuiApplication.restoreOverrideCursor()
            raise
        
    except PyAppDBConnectionError as er:
        msg = error_code_messages.get(er.code, _tr("PGError", "Connection error"))
        MessageBoxCritical(parent_widget,
                           _tr("MessageDialog", "Database connection"),
                           er.code,
                           msg,
                           er.detail)
        
    except PyAppDBError as er:
        # Map standard PostgreSQL SQLSTATE error codes to clear messages
        msg = error_code_messages.get(er.code, _tr("PGError", "Undefined database error"))
        if er.code in ('PA004', 'PA005', 'PA006', 'PA007', 'PA008', 'CCER'):
            QMessageBox.warning(parent_widget,
                                 _tr('MessageDialog', 'Warning'),
                                 msg)   
        elif "item_grid_position" in str(er):
            QMessageBox.warning(parent_widget,
                                 _tr('MessageDialog', 'Warning'),
                                 _tr('MessageError', "Is not possible to set the same row and column of a salable item"))  
        else:
            # Display the custom PySide6 critical dialog box
            MessageBoxCritical(parent_widget, operation_title, er.code, msg, er.message)
        # Safe fallback: rollback the shared connection to reset the transaction state
        appconn.rollback()
        
    except Exception as ex:
        # Handle any other unexpected exceptions gracefully
        MessageBoxCritical(parent_widget, operation_title, _tr("Error", "Unexpected error"), str(ex))


@contextmanager
def wait_cursor_context():
    """
    Simple context manager for wait cursor only, usefull for 
    heavy operation that does not involve the database
    """
    QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
    try:
        yield
    finally:
        QGuiApplication.restoreOverrideCursor()


