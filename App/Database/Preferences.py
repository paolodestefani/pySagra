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

"""Database - User preferences

This module provides classes and functions for user preferences database management

"""

# standard library
import logging

# application modules
from App.Core.ExceptionHandler import db_exception_context
from App.Database.Connect import appconn


# logger
logger = logging.getLogger(__name__)


def load_preferences(user_code: str) -> tuple:
    "Load all preferences parameters for the given user"
    script = t"""
SELECT 
    style_theme,
    color_scheme,
    icon_theme,
    font_family,
    font_size,
    tool_button_style,
    tab_position
FROM system.app_user
WHERE user_code = {user_code};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
        return cur.fetchall()[0]


def save_preferences(user_code: str,
                     style: str,
                     color: str,
                     icon: str,
                     ffamily: str | None,
                     fsize: int,
                     tbstyle: str,
                     tabposition: str
                     ) -> None:
    "Save all preferences for the given user"
    script = t"""
UPDATE system.app_user
SET style_theme = {style},
    color_scheme = {color},
    icon_theme = {icon},
    font_family = {ffamily},
    font_size = {fsize},
    tool_button_style= {tbstyle},
    tab_position = {tabposition}
WHERE user_code = {user_code};"""
    # Unified context managers in the recommended evaluation order
    with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
        cur.execute(script)
