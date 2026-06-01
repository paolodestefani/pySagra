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

"""Database - Adaptation management

This module provides functions to manage adaptations in the database, including
creating, deleting, listing, exporting, importing adaptations and their settings.   

"""

# standard library
import logging
from typing import List, Tuple, Any

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Core.Database import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def create_adaptation(adapt_type: str,
                      adapt_class: str, 
                      description: str, 
                      report_id: int | None = None,
                      system: bool = False) -> int:
    """Create a new adaptation returning the generated id"""
    script = t"""
INSERT INTO system.adaptation (
    type,
    class,
    description,
    report_id,
    is_system_object)
VALUES (
    {adapt_type},
    {adapt_class}, 
    {description}, 
    {report_id},
    {system})
RETURNING adaptation_id;"""
    # Unified context managers ensuring proper evaluation order:
    # 1. Error trapping -> 2. Transaction lifecycle -> 3. Cursor allocation
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        result = cur.execute(script).fetchone()
        if result:
            return result[0]
        else:                    
            # Custom exception raised manually if the INSERT returns no rows
            raise PyAppDBError('00000', 'Failed to create adaptation')


def is_system_object(adapt_id: int) -> bool:
    """Check if the adaptation id is a system object"""
    script = t"""
SELECT adaptation_id
FROM system.adaptation
WHERE adaptation_id = {adapt_id}
    AND is_system_object IS true;"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        # Using fetchone() is safer than rowcount for SELECT queries in psycopg 3
        return cur.fetchone() is not None


def delete_adaptation(adapt_id: int) -> None:
    """Delete adaptation of given id and reset related sequences"""
    # Also delete adaptation settings (handled via cascade constraint in DB)
    script1 = t"""
DELETE FROM system.adaptation
WHERE adaptation_id = {adapt_id}
    AND is_system_object = false;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 1),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.execute(script2)
        cur.execute(script3)
    
    
def clear_adaptation() -> None:
    """Delete all adaptations and reset all related sequences"""
    # Also delete adaptation settings and user defaults (handled via cascade constraints in DB)
    script1 = """
DELETE FROM system.adaptation;"""
    script2 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script3 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 1),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    script4 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_user_default', 'adaptation_user_default_id'),
    COALESCE((SELECT max(adaptation_user_default_id) FROM system.adaptation_user_default), 1),
    (SELECT max(adaptation_user_default_id) IS NOT NULL FROM system.adaptation_user_default)
);"""
    # Unified context managers ensuring atomic execution of all clean-up statements
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        for statement in (script1, script2, script3, script4):
            cur.execute(statement)


def list_adaptation(adapt_type: str, adapt_class: str) -> List[Tuple[Any, ...]]:
    """Get available adaptations for the given type and class"""
    script = t""" 
SELECT
    adaptation_id,
    description,
    is_default_for_class
FROM system.adaptation
WHERE 
        type  = {adapt_type}
    AND class = {adapt_class}
ORDER BY class_sorting;"""
    # Unified context managers in the recommended sequence
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()
    

def export_adaptation() -> List[Tuple[Any, ...]]:
    """List all adaptation records for export"""
    # System objects query
    script = """ 
SELECT
    adaptation_id,
    type, 
    class, 
    description, 
    class_sorting, 
    is_default_for_class,
    report_id,
    row_count_limit,
    is_system_object
FROM system.adaptation
ORDER BY adaptation_id;
"""
    # Unified context managers for safe execution and clean tracking
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()


def export_adaptation_setting() -> List[Tuple[Any, ...]]:
    """List all adaptation_setting records for export"""
    script = """ 
SELECT
    adaptation_setting_id,
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value
FROM system.adaptation_setting
ORDER BY adaptation_setting_id;"""
    # Unified context managers handling error trapping, transaction lifecycle, and cursor
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()


def import_adaptation(adaptations: List[Tuple[Any, ...]], 
                      adaptsettings: List[Tuple[Any, ...]]) -> None:
    """Import all records into adaptation and adaptation_setting tables"""
    # For executemany, traditional placeholder syntax (%s) is required
    script1 = """
DELETE FROM system.adaptation;"""  # Also deletes adaptation settings via cascade
    script2 = """
ALTER TABLE system.adaptation ALTER COLUMN adaptation_id RESTART WITH 1;"""
    script3 = """
ALTER TABLE system.adaptation_setting ALTER COLUMN adaptation_setting_id RESTART WITH 1;"""
    script4 = """
INSERT INTO system.adaptation (
    adaptation_id,
    type,
    class,
    description,
    class_sorting,
    is_default_for_class,
    report_id,
    row_count_limit,
    is_system_object)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    script5 = """
INSERT INTO system.adaptation_setting (
    adaptation_setting_id, 
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    script6 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation', 'adaptation_id'),
    COALESCE((SELECT max(adaptation_id) FROM system.adaptation), 1),
    (SELECT max(adaptation_id) IS NOT NULL FROM system.adaptation)
);"""
    script7 = """
SELECT setval(
    pg_get_serial_sequence('system.adaptation_setting', 'adaptation_setting_id'),
    COALESCE((SELECT max(adaptation_setting_id) FROM system.adaptation_setting), 1),
    (SELECT max(adaptation_setting_id) IS NOT NULL FROM system.adaptation_setting)
);"""
    # Unified context managers ensure that if any batch insert or sequence reset fails,
    # the entire database import operation undergoes a clean rollback.
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.execute(script2)
        cur.execute(script3)
        cur.executemany(script4, adaptations)
        cur.executemany(script5, adaptsettings)
        cur.execute(script6)
        cur.execute(script7)


def get_adapt_limit(adapt_id: int) -> int | None:
    """Get row count limit for the given adaptation_id"""
    script = t"""
SELECT 
    row_count_limit
FROM system.adaptation
WHERE adaptation_id = {adapt_id};"""
    # Unified context managers including the transaction block for consistency
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        result = cur.execute(script).fetchone()
        if result:
            return result[0]
        return None


def set_adapt_limit(adapt_id: int, limit: int | None) -> None:
    """Set row count limit for the given adaptation_id"""
    script = t"""
UPDATE system.adaptation
SET row_count_limit = {limit}
WHERE adaptation_id = {adapt_id};"""
    
    # Unified context managers ensuring proper execution order and atomicity
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
    

def get_adapt_setting(adapt_id: int) -> Tuple[List[Tuple[Any, ...]], List[Tuple[Any, ...]], List[Tuple[Any, ...]]]:
    """Get available adaptation settings for the given id split by type"""
    script = t"""
SELECT 
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value
FROM system.adaptation_setting
WHERE adaptation_id = {adapt_id}
ORDER BY layout_row;"""
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        records = cur.fetchall()
        # Safe empty state check instead of relying on cur.rowcount
        if not records:
            return [], [], []  # No customization found 
        # Split records dynamically into Parameters, Filters, and Sorting lists
        p = [row for row in records if row[0] == 'P']  # Parameters
        f = [row for row in records if row[0] == 'F']  # Filters
        s = [row for row in records if row[0] == 'S']  # Sorting
        return p, f, s


def set_adapt_setting(adapt_id: int, columns: List[Tuple[Any, ...]]) -> None:
    """Set available adaptation settings for the given id by rewriting them"""
    # For executemany operations, traditional placeholder syntax (%s) is required
    # First, delete all existing settings associated with this adapt_id
    script1 = t"""
DELETE FROM system.adaptation_setting
WHERE adaptation_id = {adapt_id};"""
    # Then, insert the new bulk configuration settings
    script2 = """
INSERT INTO system.adaptation_setting (
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    # Unified context managers guarantee that the DELETE and the bulk INSERT
    # occur within a single atomic transaction block. If any insert fails,
    # the previous settings are automatically preserved via rollback.
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.executemany(script2, columns)


def get_adapt_sorting(adapt_id: int) -> int:
    """Returns adaptation sorting index or 0 if not found"""
    script = t"""
SELECT class_sorting
FROM system.adaptation
WHERE adaptation_id = {adapt_id};"""
    
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        result = cur.execute(script).fetchone()
        if result:
            return result[0]
        return 0


def set_adapt_sorting(adapt_id: int, sorting: int) -> None:
    "Set adaptation sorting index"
    script = t"""
UPDATE system.adaptation
SET class_sorting = {sorting}
WHERE adaptation_id = {adapt_id};"""
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
    

def get_adapt_class_default(adapt_type: str, adapt_class: str) -> int | None:
    """Get the default adaptation_id for the given type and class"""
    script = t"""
SELECT adaptation_id
FROM system.adaptation
WHERE 
        type  = {adapt_type} 
    AND class = {adapt_class};"""
    # Unified context managers ensuring consistent execution and clean exception trapping
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        result = cur.execute(script).fetchone()
        if result:
            return result
        return None


def set_adapt_class_default(adapt_id: int) -> None:
    """Set the adaptation class default for its specific type and class"""
    script1 = t"""
SELECT type, class 
FROM system.adaptation
WHERE adaptation_id = {adapt_id};"""
    script2 = """
UPDATE system.adaptation
SET is_default_for_class = false
WHERE type = %s AND class = %s;"""
    script3 = t"""
UPDATE system.adaptation
SET is_default_for_class = true
WHERE adaptation_id = {adapt_id};"""
    # Unified context managers guarantee that the initial SELECT and both UPDATE
    # statements are executed within a single, isolated atomic transaction block.
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        result = cur.execute(script1).fetchone()
        if not result:
            return None
        adapt_type = result[0]
        adapt_class = result[1]
        cur.execute(script2, (adapt_type, adapt_class))
        cur.execute(script3)


def get_adapt_user_default(adapt_type: str, adapt_class: str, user: str) -> int | None:
    """Get the default adaptation id if any for the given type, class, and user"""
    script = t"""
SELECT adaptation_id
FROM system.adaptation_user_default
WHERE 
        type  = {adapt_type}
    AND class = {adapt_class}
    AND app_user_code = {user};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        result = cur.execute(script).fetchone()
        if result:
            return result
        return None


def get_adapt_default(adapt_type: str, adapt_class: str, user: str) -> int | None:
    """Get the default adaptation for type/class/user, or fallback to type/class global default"""
    script1 = t"""
SELECT adaptation_id
FROM system.adaptation_user_default
WHERE 
        type = {adapt_type}
    AND class = {adapt_class}
    AND app_user_code = {user};"""
    script2 = t"""
SELECT adaptation_id
FROM system.adaptation
WHERE 
        type = {adapt_type}
    AND class = {adapt_class}
    AND is_default_for_class IS true;"""
    # Unified context managers execution within a single isolated transaction
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        # 1. Try to fetch user-specific default configuration
        result = cur.execute(script1).fetchone()
        if result:
            return result
        # 2. Fallback to system-wide default configuration
        result = cur.execute(script2).fetchone()
        if result:
            return result
        return None


def set_adapt_user_default(adapt_type: str, adapt_class: str, user: str, adapt_id: int) -> None:
    """Set the given adaptation id as the default configuration for a specific user"""
    # 1. Clear any pre-existing user default for this specific type and class
    script1 = t"""
DELETE FROM system.adaptation_user_default 
WHERE 
        type = {adapt_type} 
    AND class = {adapt_class}
    AND app_user_code = {user};"""
    # 2. Insert the new user default assignment
    script2 = t"""
INSERT INTO system.adaptation_user_default (
    type, 
    class, 
    app_user_code, 
    adaptation_id)
VALUES (
    {adapt_type},
    {adapt_class},
    {user},
    {adapt_id});"""
    # Unified context managers guarantee that both the DELETE and the INSERT
    # statement are executed within a single, isolated atomic transaction block.
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.execute(script2)


def get_view_columns(adapt_id: int) -> List[Tuple[Any, ...]]:
    """Returns the itemview configuration layout definition"""
    script = t"""
SELECT 	
    column_number,
    sorting,
    is_visible,
    size
FROM system.adaptation_setting
WHERE adaptation_id = {adapt_id}
ORDER BY sorting;"""
    # Unified context managers including the transaction block for structural consistency
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()


def set_view_columns(adapt_id: int, columns: List[Tuple[Any, ...]]) -> None:
    """Set the view configuration layout definition by overwriting old settings"""
    # For executemany operations, traditional placeholder syntax (%s) is required
    # First, clear any pre-existing column settings for this specific adapt_id
    script1 = t"""
DELETE FROM system.adaptation_setting
WHERE adaptation_id = {adapt_id};"""
    # Then, insert the new block of column configuration definitions
    script2 = """
INSERT INTO system.adaptation_setting (
    adaptation_id,
    column_number,
    sorting,
    is_visible,
    size)
VALUES (%s, %s, %s, %s, %s);"""
    # Unified context managers guarantee that both statements run in a single atomic transaction
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script1)
        cur.executemany(script2, columns)
