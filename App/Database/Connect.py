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

"""database - connection functions

This module provide all the facilities to connect/dsconnect to the db server

"""

# standard library
import logging
#from collections.abc import Generator, Iterator
from typing import Iterator, Any, Optional, ContextManager

# psycopg
import psycopg

# PySide6
from PySide6.QtCore import QDateTime

# Application modules
from App import APPNAME
from App import APPVERSIONMAJOR
from App import APPVERSIONMINOR
from App import session
from App.Database import MRV_PGSQL

from App.Database import EWADB

# exceptions
from App.Database.Exceptions import PyAppDBConnectionError
from App.Database.Exceptions import PyAppDBError

# REGISTER CUSTOM PSYCOPG TYPES
import App.Database.Psycopg

# logger
logger = logging.getLogger(__name__)


# ******************************* #
#                                 #
#  connection to database server  #
#                                 #
# ******************************* #


class AppConnection():
    "Database and application connection class"

    def __init__(self) -> None:
        self._conn: psycopg.Connection # psycopg connection instance
        self._par: dict = dict() # store connection parameter

    def connect(self, par: dict) -> None:
        "Open a db connection and then an application connection trought an sql function"
        self._logging = False
        # FIRST: DATABASE CONNECTION
        logging.info("Starting database connection with parameters:")
        logging.info("host = %(server)s", par)
        logging.info("port = %(port)s", par)
        logging.info("database = %(database)s", par)
        logging.info("dbuser = %(db_user)s", par)
        logging.info("dbuser password = ********")
        logging.info("application_name = %s", APPNAME)
        try:
            self._conn = psycopg.connect(host=par['server'],
                                         port=par['port'],
                                         dbname=par['database'],
                                         user=par['db_user'],
                                         password=par['db_password'],
                                         autocommit=True,
                                         application_name=APPNAME)
        except psycopg.OperationalError as er:
            logging.critical("Psycopg operational error: %s", str(er))
            raise PyAppDBConnectionError(er)
        except psycopg.Error as er:
            logging.critical("Psycopg error: %s", str(er))
            raise PyAppDBError(er.diag.sqlstate, str(er))
        else:
            logging.info("Database connection established")

        # OK START A NEW APPLICATION CONNECTION, if posible
        
        # check if it's an application db - if has a pa_connect function in system schema
        sql = """
SELECT EXISTS(SELECT 1 
    FROM pg_proc pr
    JOIN pg_namespace ns ON pr.pronamespace = ns.oid
    WHERE pr.proname = 'pa_connect' 
        AND ns.nspname = 'system');"""
        try:
            with self._conn.cursor() as cur:
                if self._logging:
                    logging.info(sql)
                cur.execute(sql)
                if not cur.fetchone():
                    logging.critical("Database '%s' is not an application database", par['database'])
                    raise PyAppDBError(EWADB, f"Database '{par['database']}' is not an application database")
                logging.info("DB is verified as an application database")
        except psycopg.Error as er:
            logging.critical("Psycopg error: %s", str(er))
            raise PyAppDBError(er.diag.sqlstate, str(er))
        # connect to the applicationdb
        logging.info("Calling application connection function with parameters:")
        logging.info("pgminver = %s", MRV_PGSQL)
        logging.info("appname = %s", APPNAME)
        logging.info("appversion = %s.%s", APPVERSIONMAJOR, APPVERSIONMINOR)
        logging.info("user = ********")
        logging.info("password = ********")
        logging.info("hostname = %(hostname)s", par)
        try:
            with self._conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                script = t"""
                SELECT * FROM system.pa_connect(
                    {MRV_PGSQL},
                    {APPNAME},
                    {APPVERSIONMAJOR},
                    {APPVERSIONMINOR},
                    {par['user']},
                    {par['password']},
                    {par['hostname']});"""
                cur.execute(script)
                # postgres search path is set to system, common, company by pa_connect
                # update session parameters
                session.update(par)
                session.update(next(cur))
                logging.info("DB Application connection established")
        except psycopg.Error as er:
            logging.error("Psycopg error: %s", str(er))
            raise PyAppDBError(er.diag.sqlstate, str(er))
        self._par.update(par)

    def change_company(self, company: int) -> None:
        "Set or change the working company"
        try:
            with self._conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                cur.execute(t"SELECT * FROM system.pa_company_change({company});")
                session.update(next(cur))
        except psycopg.Error as er:
            logging.error("Psycopg error: %s", str(er))
            raise PyAppDBError(er.diag.sqlstate, str(er))

    def cursor(self, row_factory: Optional[psycopg.rows.RowFactory[Any]] = None,
                binary: bool = False
               ) -> psycopg.Cursor[Any]|psycopg.ServerCursor[Any]:
        "Returns a new cursor"
        if row_factory is None:
            return self._conn.cursor(binary=binary)
        else:
            return self._conn.cursor(row_factory=row_factory, binary=binary)

    def transaction(self, savepoint: str|None = None, force_rollback: bool = False
                    ) -> ContextManager[psycopg.Transaction]:
        "Returns a new transaction object"
        return self._conn.transaction(savepoint, force_rollback)

    def commit(self) -> None:
        "Commit transaction"
        self._conn.commit()

    def rollback(self) -> None:
        "Rollback transaction"
        self._conn.rollback()

    def close(self) -> None:
        "Close application and db connection"
        # log out
        try:
            with self._conn.cursor() as cur:
                cur.execute("SELECT system.pa_disconnect();")
        except psycopg.Error as er:
            logging.error("Psycopg error: %s", str(er))
            raise PyAppDBConnectionError(er)
        # close db connection
        self._conn.close()

    def restart(self) -> None:
        self.connect(self._par)


appconn = AppConnection() # connection wrapper instance


def can_use_company(user: str, company: int) -> bool:
    "Return True if user has access rights to company"
    if user == session['app_system_user']:
        return True
    script = t"""
SELECT uc.profile_code
FROM system.app_user_company uc
WHERE uc.app_user_code = {user} AND uc.company_id = {company};"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return bool(cur.rowcount)
    except psycopg.Error as er:
        logging.error("Psycopg error: %s", str(er))
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))#

def has_companies_available(user: str) -> bool:
    """Returns True if user have available working company(ies)"""
    if user == session['app_system_user']:
        return True
    script = """
SELECT exists(
        SELECT company_id 
        FROM system.app_user_company 
        WHERE app_user_code = {user});"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return next(cur)[0]
    except psycopg.Error as er:
        logging.error("Psycopg error: %s", str(er))
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))

def get_companies_list(user: str|None = None) -> list[tuple[int, str]]:
    """Get the available company list for user or all companies"""
    # get companies list for user
    if user and user == session['app_system_user']:
        script = t"""
-- available companies
SELECT
    uc.company_id AS company_id,
    c.description AS company_description
FROM system.app_user_company uc
JOIN system.company c ON uc.company_id = c.company_id
WHERE uc.app_user_code = {user}
EXCEPT
-- exclude current company
SELECT
	n.company_id AS company_id,
	c.description AS company_description
FROM system.connection n
JOIN system.company c ON n.company_id = c.company_id 
WHERE session_id = pg_backend_pid();"""
        try:
            with appconn.cursor() as cur:
                cur.execute(script)
                return cur.fetchall()
        except psycopg.Error as er:
            logging.error("Psycopg error: %s", str(er))
            sqlstate = er.diag.sqlstate if er.diag else "Unknown"
            raise PyAppDBError(sqlstate, str(er))
    else: # all companies list
        script = """
SELECT 
    c.company_id, 
    c.description
FROM system.company c;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        logging.error("Psycopg error: %s", str(er))
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))

def get_company_desc(company: int) -> str:
    "Get company description"
    script = t"""
SELECT 
    c.description
FROM system.company c
WHERE c.company_id = {company};"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return next(cur)[0]
    except psycopg.Error as er:
        logging.error("Psycopg error: %s", str(er))
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))
    
def get_current_event() -> None:
    "Check if an event is available for current date, if true update session dictionary"
    session['event_id'] = None
    session['event_description'] = None
    session['event_image'] = None
    script = t"""
SELECT 
    event_id, 
    description, 
    image
FROM company.event
WHERE 
    company_id = system.pa_current_company()
    AND {QDateTime.currentDateTime()} BETWEEN start_date AND end_date"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)  # event based on client date
            event = cur.fetchone()
            if event:
                session['event_id'] = event[0] # code
                session['event_description'] = event[1] # description
                session['event_image'] = event[2] # image
    except psycopg.Error as er:
        logging.error("Psycopg error: %s", str(er))
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))


def database_information() -> list[tuple[str, str]]:
    "Returns connection informations"
    script = """
SELECT
    version() AS "DB Server",
    current_database() AS "Database",
    system.pa_setting('app_name') AS "DB application",
    system.pa_setting('app_description') AS "DB app. description",
    to_char(major, '00')||'.'||to_char(minor, '00')||'.'||to_char(patch, '0000')||' '||tag AS "DB app. version",
    installed_at::text AS "Last update",
    session_user AS "DB User",
    inet_client_addr() AS "Client IP",
    inet_client_port() AS "Client Port",
    inet_server_addr() AS "Server IP",
    inet_server_port() AS "Server Port",
    CAST(pg_postmaster_start_time() AS varchar) AS "Start time",
    pg_database_size(current_database()) AS "DB Size",
    pg_backend_pid() AS "PID"
FROM system.version
ORDER BY installed_at DESC
LIMIT 1;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            # Mypy security check
            if cur.description is None:
                return [] 
            colnames = [desc[0] for desc in cur.description]
            row = next(cur)
            if row is None:
                return [] 
            return list(zip(colnames, row))
    except psycopg.Error as er:
        logging.error("Psycopg error: %s", str(er))
        sqlstate = er.diag.sqlstate if er.diag else "Unknown"
        raise PyAppDBError(sqlstate, str(er))

