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

"""Database - Utilities

Database utilities

"""

# standard library
import logging

# psycopg
import psycopg

# application modules
from App.Database import OVFIELD
from App.Database.Connect import appconn
from App.Database.Exceptions import db_exception_context
from App.Database.Exceptions import PyAppDBConcurrencyError
from App.Database.Exceptions import PyAppDBConcurrencyError


# logger
logger = logging.getLogger(__name__)


class Record(dict):
    """The Record class is a dictionary subclass and stores a record of a
    database table. The constructor keep a reference of the table name and
    primary key fields. The dictionary keys are fields name of the database
    table.
    4 additional methods are added to the dictionary class:
        - select_record for select one record from the database table based on a primary key
        - insert_record for inserting the record in the table
        - update_record for update the record in the table based on the primary key
        - delete_record for delete the record in the table based on the primary key
    """
    OVFIELD = 'object_version'

    def __init__(self, table: str, pkey: list|tuple = []) -> None:
        """- table = table name
           - pkey = list of primary key's fields for update/delete"""
        self.table = table
        self.pkey = pkey

    def commit(self) -> None:
        "Commit transaction without requiring a appconn reference"
        appconn.commit()

    def rollback(self) -> None:
        "Rollback transaction without requiring a appconn reference"
        appconn.rollback()

    def select_record(self) -> None:
        "Select a record of a table based on primay key value"
        script = (f"SELECT * FROM {self.table} "
                  f"WHERE {' AND '.join([f'{i} = %({i})s' for i in self.pkey])};")
        # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(script, self)
            result = next(cur, None)
            if result:
                self.update(result)
                
    def insert_record(self) -> None:
        "Insert a record base on primary key"
        script = (f"INSERT INTO {self.table} ({', '.join(self.keys())})\n"
                  f"VALUES ({', '.join([f'%({i})s ' for i in self.keys()])})\n"
                  f"RETURNING {', '.join([i for i in self.keys() if i not in self.pkey] + list(self.pkey))};")
        # primary key fields are always returned to self dict
        # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(script, self)
            result = next(cur, None)
            if result:
                self.update(result)
        
    def update_record(self) -> None:
        "Update a record base on primary key, raise an exception if modified before"
        # check object_version
        if OVFIELD in self:
            where = " AND ".join([f"{i} = %({i})s" for i in self.pkey])
            args = {k:self[k] for k in self.pkey} # primary key fields
            args[OVFIELD] = self[OVFIELD]
            script = (f"SELECT {OVFIELD} = %({OVFIELD})s\n"
                      f"FROM {self.table}\n"
                      f"WHERE {where};")
            # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            cur.execute(script, args)
            result = next(cur, None)
            if not result:
                raise PyAppDBConcurrencyError()
        # update
        script = (f"UPDATE {self.table}\n"
                  f"SET {', '.join([f'{i} = %({i})s' for i in self if i not in self.pkey])}\n"
                  f"WHERE {' AND '.join([f'{i} = %({i})s' for i in self.pkey])}\n"
                  f"RETURNING {OVFIELD};")
        # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(script, self)
            result = next(cur, None)
            if result:
                self.update(result)

    def delete_record(self) :
        "Delete one record base on primary key, raise an exception if modified before"
        # check row_timestamp
        if OVFIELD in self:
            where = " AND ".join([f"{i} = %({i})s" for i in self.pkey])
            args = {k:self[k] for k in self.pkey}
            script = (f"SELECT {OVFIELD} = {self[OVFIELD]}\n"
                      f"FROM {self.table}\n"
                      f"WHERE {where};")
            # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor() as cur:
            cur.execute(script, args)
            result = cur.fetchone()[0]
            if not result:
                raise PyAppDBConcurrencyError()
        # delete
        script = (f"DELETE FROM {self.table}\n"
                  f"WHERE {' AND '.join([f'{i} = %({i})s' for i in self.pkey])}")
        # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(script, self)


class RecordSet(list):
    """A list of record of a database table. Each record is a Record instance"""

    def __init__(self, table: str, pkey: list[str] | tuple[str]) -> None:
        """table = database table
           pkey = list of primary key fields"""
        self.table = table
        self.pkey = pkey

    def insert_records(self) -> None:
        "Insert a list of records"
        if not self:
            return # empty list, nothing to do
        script = (f"INSERT INTO {self.table} ({', '.join(self[0].keys())})\n"
                  f"VALUES ({', '.join([f'%({i})s ' for i in self[0].keys()])})\n"
                  f"RETURNING {', '.join([i for i in self[0].keys() if i not in self.pkey] + list(self.pkey))};")
        # primary key fields are always returned to self dict
        # script constructor based on the first item of the list
        # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            for r in self:
                cur.execute(script, r)
                r.update(cur.fetchone())
        
    def select_records(self) -> None:
        "Select a record of a table based on primay key value"
        script = (f"SELECT * \n"
                  f"FROM {self.table}\n"
                  f"WHERE {' AND '.join([f'{i} = %({i})s' for i in self.pkey])};")
        self.clear()
        # Unified context managers in the recommended evaluation order
        with db_exception_context(logger), appconn.transaction(), appconn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(script)
            for r in cur:
                self.append(r)
