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

"""database - printer class


"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn


#def update_printer(printer_class, computer, printer):
    #"Set printer name for given printer class and computer name"
    #script = """INSERT INTO printer_class_printer (class_id, computer, printer)
#VALUES (%s, %s, %s)
#ON CONFLICT ON CONSTRAINT printer_class_printer_unique DO
#UPDATE SET computer = EXCLUDED.computer, printer = EXCLUDED.printer;"""
    #try:
        #with appconn.conn:
            #with appconn.cursor() as cur:
                #cur.execute(script, (printer_class, computer, printer))
    #except psycopg2.Error as er:
        #raise PyAppDBError(er.pgcode, er.pgerror)

#def delete_printer(printer_class, computer):
    #"Delete printer name for given printer class and computer name"
    #script = """DELETE FROM printer_class_printer
#WHERE class_id = %s AND computer = %s;"""
    #try:
        #with appconn.conn:
            #with appconn.cursor() as cur:
                #cur.execute(script, (printer_class, computer))
    #except psycopg2.Error as er:
        #raise PyAppDBError(er.pgcode, er.pgerror)

def get_printer_name(class_id: int, computer: str) -> str|None:
    "Return the printer name of class_id"
    script = """SELECT printer
FROM printer_class_printer
WHERE printer_class_id = %s AND computer = %s;"""
    try:
            with appconn.cursor() as cur:
                cur.execute(script, (class_id, computer))
                pn = next(cur, None)
                if pn is not None:
                    return pn[0]
                else:
                    return None
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))
