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

"""Database - Settings database management

"""

# standard library
import logging

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn

# application modules
from App import session
from App.Database.Utility import Record


# logger
logger = logging.getLogger(__name__)


class SettingClass():
    "A dict like class for get/set a single setting parmeter"

    def __getitem__(self, key: str) -> str|None:
        "Get value for key from setting table"
        # use fstring because field names are not used for cursor parameters
        # t-strings don't work as of psycopg 3.3.4
        script = f"""
SELECT {key}
FROM company.setting 
WHERE company_id = system.pa_current_company();"""
        try:
            with appconn.cursor() as cur:
                cur.execute(script)
                result = cur.fetchone()
                if result is None:
                    raise PyAppDBError("No data found", "No setting value found for key: " + key)
                return result[0]
        except psycopg.Error as er:
            logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
            raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))

    def __setitem__(self, key: str, value: str) -> None:
        "Set value for key in setting table"
        script = f"""
UPDATE company.setting
SET {key} = {value}
WHERE company_id = system.pa_current_company();"""
        try:
            with appconn.transaction():
                with appconn.cursor() as cur:
                    cur.execute(script)
        except psycopg.Error as er:
            logger.error("*** DATABASE ERROR ***\nSQL State: %s\n%s", er.diag.sqlstate, str(er))
            raise PyAppDBError(er.diag.sqlstate, er.diag.message_primary, str(er))

    def __repr__(self) -> str:
        return "Company setting get/set utility class"

#Setting = SettingClass()


class Setting(Record):
    "A Record (dict) subclass for load/seve settings from database"

    def __init__(self) -> None:
        super().__init__('company.setting', ('company_id',))
        self['company_id'] = session['current_company']
        self.load()

    def load(self) -> None:
        self.select_record()

    def save(self) -> None:
        self.update_record()
        self.commit()

