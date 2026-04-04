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

"""Database - Customizations



"""

# psycopg
import psycopg

# application modules
from App.Database.Exceptions import PyAppDBError
from App.Database.Connect import appconn



def get_itemview_adapt(setting: bool = False) -> list:
    "Returns all the item views customizations"
    if not setting:
        script = """
SELECT 
    itemview_adapt_id,
    description,
    itemview_class,
    is_default_for_class
FROM system.itemview_adapt
ORDER BY itemview_adapt_id;"""
    else:
        script = """
SELECT 
    itemview_adapt_id,
    column_number,
    sorting,
    is_visible,
    size
FROM system.itemview_adapt_setting
ORDER BY itemview_adapt_id, column_number;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

#def delete_itemview_customization():
    #"Delete all itemview customizations"
    #s1 = "DELETE FROM system.itemview_customize_setting;"
    #s2 = "DELETE FROM system.itemview_customize;"
    #try:
        #with appconn.conn:
            #with appconn.cursor() as cur:
                #for script in s1, s2:
                    #cur.execute(script)
    #except psycopg2.Error as er:
        #raise PyAppDBError(er.pgcode, er.pgerror)

def set_itemview_adapt(vid: int,
                       vdes: str,
                       vclass: str,
                       vdef: bool
                       ) -> None:
    "Set all the item views customizations"
    script1 = """
DELETE FROM system.itemview_adapt WHERE itemview_adapt_id = %s;"""
    script2 = """
INSERT INTO system.itemview_adapt (
        itemview_adapt_id,
        description,
        itemview_class,
        is_default_for_class)
VALUES (%s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (vid,))
                cur.execute(script2, (vid, vdes, vclass, vdef))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_itemview_adapt_setting(vid: int,
                               vcol: int,
                               vsort: str,
                               vvis: bool,
                               vsize: int
                               ) -> None:
    "Set all the item views customizations settings"
    script = """
INSERT INTO system.itemview_adapt_setting (
    itemview_adapt_id,
    column_number,
    sorting,
    is_visible,
    size)
VALUES (%s, %s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (vid, vcol, vsort, vvis, vsize))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_sortfilter_adapt(setting: bool = False) -> list:
    "Returns all the sort filter customizations"
    if not setting:
        script = """
SELECT 
    sortfilter_adapt_id,
    description,
    sortfilter_class,
    class_sorting
FROM system.sortfilter_adapt
ORDER BY sortfilter_adapt_id;"""
    else:
        script = """
SELECT 
    sortfilter_adapt_id,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value
FROM system.sortfilter_adapt_setting
ORDER BY sortfilter_adapt_id, element_type, layout_row;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

#def delete_sortfilter_customization():
    #"Delete all itemview customizations"
    #s1 = "DELETE FROM system.sortfilter_customize_setting;"
    #s2 = "DELETE FROM system.sortfilter_customize;"
    #try:
        #with appconn.conn:
            #with appconn.cursor() as cur:
                #for script in s1, s2:
                    #cur.execute(script)
    #except psycopg2.Error as er:
        #raise PyAppDBError(er.pgcode, er.pgerror)

def set_sortfilter_adapt(sid: int,
                         sdes: str,
                         sclass: str,
                         sdef: bool
                         ) -> None:
    "Set all the item views customizations"
    script1 = """
DELETE FROM system.sortfilter_adapt WHERE sortfilter_adapt_id = %s;"""
    script2 = """
INSERT INTO system.sortfilter_adapt (
    sortfilter_adapt_id,
    description,
    sortfilter_class,
    class_sorting)
VALUES (%s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script1, (sid,))
                cur.execute(script2, (sid, sdes, sclass, sdef))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_sortfilter_adapt_setting(sid: int,
                                 selem: str,
                                 slrow: int,
                                 scmb1: int,
                                 sneg: bool,
                                 scmb2: int,
                                 svv: str
                                 ) -> None:
    "Set all the item views customizations settings"
    script = """
INSERT INTO system.sortfilter_adapt_setting (
    sortfilter_adapt_id,
    element_type,
    layout_row,
    combo1_index,
    negate_state,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (sid, selem, slrow, scmb1, sneg, scmb2, svv))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def get_report_adapt(setting: bool = False) -> list:
    "Returns all the report customizations"
    if not setting:
        script = """
SELECT 
    report_adapt_id,
    report_id,
    description,
    class_sorting
FROM system.report_adapt    
ORDER BY report_adapt_id;"""
    else:
        script = """
SELECT 
    report_adapt_id,
    adapt_type,
    layout_row,
    combo1_index,
    combo2_index,
    widget_value
FROM system.report_adapt_setting
ORDER BY report_adapt_id, adapt_type, layout_row;"""
    try:
        with appconn.cursor() as cur:
            cur.execute(script)
            return cur.fetchall()
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

#def delete_report_customization():
    #"Delete all itemview customizations"
    #s1 = "DELETE FROM system.report_customize_setting;"
    #s2 = "DELETE FROM system.report_customize;"
    #try:
        #with appconn.conn:
            #with appconn.cursor() as cur:
                #for script in s1, s2:
                    #cur.execute(script)
    #except psycopg2.Error as er:
        #raise PyAppDBError(er.pgcode, er.pgerror)

def set_report_adapt(rid: int,
                     rri: int,
                     rdes: str,
                     rcls: bool
                     ) -> None:
    "Set all the report customizations"
    script = """
DELETE FROM system.report_adapt WHERE report_adapt_id = %s;
INSERT INTO system.report_adapt (
    report_adapt_id,
    report_id,
    description,
    class_sorting)
VALUES (%s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (rid, rri, rdes, rcls))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def set_report_adapt_setting(raid: int,
                             ratyp: str,
                             rlrow: int,
                             rcmb1: int|None,
                             rcmb2: int|None,
                             rvv: str
                             ) -> None:
    "Set all the item views customizations settings"
    script = """
INSERT INTO system.report_adapt_setting (
    report_adapt_id,
    adapt_type,
    layout_row,
    combo1_index,
    combo2_index,
    widget_value)
VALUES (%s, %s, %s, %s, %s, %s);"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script, (raid, ratyp, rlrow, rcmb1, rcmb2, rvv))
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def clear_adapt(adapttype: str) -> None:
    "Clear customizations"
    scriptS = """
DELETE FROM system.sortfilter_adapt;
ALTER TABLE system.sortfilter_adapt ALTER COLUMN sortfilter_adapt_id RESTART WITH 1;"""
    scriptI = """
DELETE FROM system.itemview_adapt;
ALTER TABLE system.itemview_adapt ALTER COLUMN itemview_adapt_id RESTART WITH 1;"""
    scriptR = """
DELETE FROM system.report_adapt;
ALTER TABLE system.report_adapt ALTER COLUMN report_adapt_id RESTART WITH 1;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                match adapttype:
                    case 'S':
                        cur.execute(scriptS)
                    case 'I':
                        cur.execute(scriptI)
                    case 'R':
                        cur.execute(scriptR)    
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

def update_identity() -> None:
    "Update identity value to last present in all customization tables"
    script = """
DO $$
    DECLARE
    i integer;
    tt text[];
    BEGIN
        FOREACH tt SLICE 1 IN ARRAY ARRAY[
            ['system.itemview_adapt', 'itemview_adapt_id'],
            ['system.sortfilter_adapt', 'sortfilter_adapt_id'],
            ['system.report_adapt', 'report_adapt_id']
            ] 
        LOOP
            EXECUTE format('SELECT coalesce(max(%s), 0) + 1 FROM %s', tt[2], tt[1]) INTO i;
            EXECUTE format('ALTER TABLE %s ALTER COLUMN %s RESTART WITH %s', tt[1], tt[2], i) ;
        END LOOP;
    END;
$$
language plpgsql;"""
    try:
        with appconn.cursor() as cur:
            with appconn.transaction():
                cur.execute(script)
    except psycopg.Error as er:
        raise PyAppDBError(er.diag.sqlstate, str(er))

