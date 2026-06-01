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
from contextlib import contextmanager
from typing import Generator
from typing import Any

# PySide6
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMessageBox

# application modules
from App.Database.Exceptions import PyAppDBConnectionError
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn
from App.Core.L10n import _tr
from App.Widget.Dialog import MessageBoxCritical


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

    'CCER': _tr("PGError", "Row modified before update/delete"),
    
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

# Context manager to capture exceptions in GUI operations and show critical dialogs

@contextmanager
def gui_exception_context(parent_widget: Any, operation_title: str) -> Generator[None, None, None]:
    """
    Catches PyAppDBError exceptions, translates PostgreSQL SQLSTATE codes 
    into user-friendly localized messages, and displays a critical dialog.
    """
    try:
        yield
    except PyAppDBConnectionError as er:
        QGuiApplication.restoreOverrideCursor()
        msg = error_code_messages.get(er.code, _tr("PGError", "Undefined database error"))
        MessageBoxCritical(parent_widget,
                           _tr("MessageDialog", "Database connection"),
                           er.code,
                           msg,
                           er.detail)
        
    except PyAppDBError as er:
        QGuiApplication.restoreOverrideCursor()
        # Map standard PostgreSQL SQLSTATE error codes to clear messages
        msg = error_code_messages.get(er.code, _tr("PGError", "Undefined database error"))
        
        if er.code in ('PA004', 'PA005', 'PA006', 'PA007', 'PA008'):
            msg = _tr("Login", "Authentication failed\nwrong user or password")
            QMessageBox.warning(parent_widget,
                                 _tr('MessageDialog', 'Warning'),
                                 msg)
        else:
            # Display the custom PySide6 critical dialog box
            MessageBoxCritical(parent_widget, operation_title, er.code, msg, er.message)
        
        # Safe fallback: rollback the shared connection to reset the transaction state
        appconn.rollback()
        
    except Exception as ex:
        QGuiApplication.restoreOverrideCursor()
        # Handle any other unexpected exceptions gracefully
        MessageBoxCritical(parent_widget, operation_title, _tr("Error", "Unexpected error"), str(ex))
        
    finally:
        QGuiApplication.restoreOverrideCursor()
