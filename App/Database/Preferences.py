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

"""database - User preferences

This module provide all the facilities to manage user preferences

"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def load_preferences(user_code: str) -> tuple:
    "Load all preferences parameters for the given user"
    script = """
SELECT 
    style_theme,
    color_scheme,
    icon_theme,
    font_family,
    font_size,
    tool_button_style,
    tab_position
FROM system.app_user
WHERE user_code = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (user_code,))
                return cur.fetchall()[0]
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def save_preferences(user_code: str,
                     style: str,
                     color: str,
                     icon: str,
                     ffamily: str,
                     fsize: int,
                     tbstyle: str,
                     tabposition: str
                     ) -> None:
    "Save all preferences for the given user"
    script = """
UPDATE system.app_user
SET style_theme = %s,
    color_scheme = %s,
    icon_theme = %s,
    font_family = %s,
    font_size = %s,
    tool_button_style= %s,
    tab_position = %s
WHERE user_code = %s;"""
    try:
        with appconn.transaction():
            with appconn.cursor() as cur:
                cur.execute(script, (style,
                                     color,
                                     icon,
                                     ffamily,
                                     fsize,
                                     tbstyle,
                                     tabposition,
                                     user_code))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
