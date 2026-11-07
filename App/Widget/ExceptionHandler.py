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

This module shows database and report exceptions to the user

"""

# standard library
import logging
from contextlib import contextmanager
from typing import Generator
from typing import Any

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Database.Exceptions import PyAppDBConnectionError
from App.Database.Exceptions import PyAppDBError
from App.Report import ReportException, ReportNoDataError
from App.Report import NoOrderReportParameters, NotEnoughtReportParameters

from App.Database.Connect import appconn
from App.Common.Gui import no_wait_cursor_context
from App.Common.Gui import remove_wait_cursor
from App.Common.L10n import _tr
from App.Widget.MessageBox import MessageBoxCritical


# logger
logger = logging.getLogger(__name__)

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

# Context manager to capture exceptions in GUI operations and show critical dialogs

class ContextOutcome:
    """What an exception context reports to its block:
    ok is True only when the block ended without exceptions"""

    def __init__(self) -> None:
        self.ok = False


def _rollback() -> None:
    "Reset the transaction state of the shared connection, it can already be closed"
    try:
        appconn.rollback()
    except Exception:
        logger.exception("Rollback failed after a database error")


def _showError(parent_widget: Any,
               operation_title: str,
               messages: dict[str, str] | None,
               error: Exception) -> None:
    "Show an error caught by gui_exception_context"
    match error:
        case PyAppDBConnectionError():
            msg = error_code_messages.get(error.code, _tr("PGError", "Connection error"))
            MessageBoxCritical(parent_widget,
                               _tr("MessageDialog", "Database connection"),
                               error.code,
                               msg,
                               error.detail)
        case PyAppDBError():
            # message of the form for this constraint or code
            messages = messages or {}
            user_msg = messages.get(error.constraint) if error.constraint else None
            user_msg = user_msg or messages.get(error.code)
            # Map standard PostgreSQL SQLSTATE error codes to clear messages
            msg = error_code_messages.get(error.code, _tr("PGError", "Undefined database error"))
            if user_msg:
                QMessageBox.warning(parent_widget, _tr('MessageDialog', 'Warning'), user_msg)
            elif error.code in ('PA004', 'PA005', 'PA006', 'PA007', 'PA008', 'CCER'):
                # non critical errors are translated here, critical ones stay in English
                QMessageBox.warning(parent_widget,
                                    _tr('MessageDialog', 'Warning'),
                                    _tr("PGError", msg))
            elif "item_grid_position" in str(error):
                QMessageBox.warning(parent_widget,
                                    _tr('MessageDialog', 'Warning'),
                                    _tr('MessageError', "Is not possible to set the same row and column of a salable item"))
            else:
                # Display the custom PySide6 critical dialog box
                MessageBoxCritical(parent_widget, operation_title, error.code, msg, error.message)
        case _:
            # Handle any other unexpected exceptions gracefully
            MessageBoxCritical(parent_widget, operation_title, _tr("Error", "Unexpected error"), str(error))


@contextmanager
def gui_exception_context(parent_widget: Any,
                          operation_title: str,
                          messages: dict[str, str] | None = None
                          ) -> Generator[ContextOutcome, None, None]:
    """
    Shows the wait cursor, catches PyAppDBError exceptions, translates PostgreSQL
    SQLSTATE codes into user-friendly localized messages, and displays a critical dialog.
    messages maps a constraint name or a SQLSTATE code to a translated
    message for the user of a form, shown as a warning; the constraint
    name is checked first because many constraints share the same code
    Use it as: with gui_exception_context(...) as outcome: ... if not outcome.ok: ...
    """
    outcome = ContextOutcome()
    QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
    try:
        yield outcome
    except Exception as error:
        remove_wait_cursor()
        if isinstance(error, PyAppDBError) and not isinstance(error, PyAppDBConnectionError):
            # reset the transaction before the message: Abort can close the connection
            _rollback()
        with no_wait_cursor_context():  # outer contexts can have their own wait cursor
            _showError(parent_widget, operation_title, messages, error)
    except BaseException:
        remove_wait_cursor()
        raise
    else:
        remove_wait_cursor()
        outcome.ok = True


def _showReportError(parent_widget: Any, error: Exception) -> None:
    "Show an error caught by report_exception_context"
    match error:
        case NoOrderReportParameters():
            msg = f"{_tr('ReportException', 'No print parameters available for computer name')}: {session['hostname']}"
            QMessageBox.information(parent_widget,
                                    _tr('MessageDialog', "Error"),
                                    msg)
        case NotEnoughtReportParameters():
            msg = _tr('ReportException', 'Not enought print parameters available')
            QMessageBox.information(parent_widget,
                                    _tr('MessageDialog', "Error"),
                                    msg)
        case ReportNoDataError():
            QMessageBox.information(parent_widget,
                                    _tr('MessageDialog', "Information"),
                                    _tr('ReportException', "No data to render"))
        case ReportException():
            msg = f"{_tr('ReportException', 'Unhandled report exception')}: {error}"
            QMessageBox.critical(parent_widget,
                                 _tr('MessageDialog', "Critical"),
                                 msg)
        case _:
            MessageBoxCritical(parent_widget,
                               _tr("Error", "Report Error"),
                               _tr("Error", "Unexpected error"),
                               str(error))


@contextmanager
def report_exception_context(parent_widget: Any) -> Generator[ContextOutcome, None, None]:
    """
    Shows the wait cursor while a report is generated and shows the right
    localized message for report errors; the outcome tells if the block succeeded
    """
    outcome = ContextOutcome()
    QGuiApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
    try:
        yield outcome
    except Exception as error:
        remove_wait_cursor()
        with no_wait_cursor_context():  # outer contexts can have their own wait cursor
            _showReportError(parent_widget, error)
    except BaseException:
        remove_wait_cursor()
        raise
    else:
        remove_wait_cursor()
        outcome.ok = True
