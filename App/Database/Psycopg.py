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

"""Psycopg extentions


"""

# standard library
# import logging

# psycopg
import psycopg
from psycopg.adapt import Loader, Dumper


# PySide6
from PySide6.QtCore import QDate
from PySide6.QtCore import QTime
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QByteArray



# managing sql default values

class Default():

    def __conform__(self, proto):
        if proto is psycopg.extensions.ISQLQuote:
            return self

    def getquoted(self):
        return 'DEFAULT'

DEFAULT = Default()


# ************************************************ #
#   TYPE CONVERSION postres type <--> qt type
# ************************************************ #

# how to find OID of PostgreSQL types:
# SELECT pg_type.oid
# FROM pg_type
# JOIN pg_namespace ON typnamespace = pg_namespace.oid
# WHERE typname = 'time' AND nspname = 'pg_catalog';

#
# timestamptz <--> QDateTime
#

class TimestamptzQDateTimeLoader(Loader):
    def load(self, value: bytes) -> QDateTime:
        ds = bytes(value).decode()
        dt = QDateTime.fromString(ds[:23], "yyyy-MM-dd HH:mm:ss.zzz")
        if not dt.isValid(): # no milliseconds
            dt = QDateTime.fromString(ds[:19], "yyyy-MM-dd HH:mm:ss")
        return dt

psycopg.adapters.register_loader('timestamptz', TimestamptzQDateTimeLoader)

class QDateTimeTimestamptzDumper(Dumper):
    def dump(self, value: QDateTime|None) -> bytes|None:
        if value is None or not value.isValid():
            return None 
        return bytes(value.toString("yyyy-MM-dd HH:mm:ss.zzz"), 'utf-8')

psycopg.adapters.register_dumper(QDateTime, QDateTimeTimestamptzDumper)


#
# date <--> QDate
#

class DateQDateLoader(Loader):
    def load(self, value: bytes) -> QDate:
        return QDate.fromString(bytes(value).decode(), "yyyy-MM-dd")

psycopg.adapters.register_loader('date', DateQDateLoader)

class QDateDateDumper(Dumper):
    def dump(self, value: QDate) -> bytes:
        if not value.isValid():
            value = QDate.currentDate()
        return bytes(value.toString("yyyy-MM-dd"), 'utf-8')

psycopg.adapters.register_dumper(QDate, QDateDateDumper)


#
# time  (without time zone) <--> QTime
#

class TimeQTimeLoader(Loader):
    def load(self, value: bytes) -> QTime:
        ts = bytes(value).decode()
        if len(ts) > 8:
            ts = ts[:8]  # avoid milliseconds precision
        return QTime.fromString(ts, "hh:mm:ss")

psycopg.adapters.register_loader('time', TimeQTimeLoader)

class QTimeTimeDumper(Dumper):
    def dump(self, value: QTime) -> bytes:
        if not value.isValid():
            value = QTime.currentTime()
        return bytes(value.toString("hh:mm:ss"), 'utf-8')

psycopg.adapters.register_dumper(QTime, QTimeTimeDumper)


#
# bytea <--> QBytearray
#

class ByteaQByteArrayLoader(Loader):
    def load(self, value: bytes) -> QByteArray:
        return QByteArray.fromHex(bytes(value))

psycopg.adapters.register_loader('bytea', ByteaQByteArrayLoader)

class QByteArrayByteaDumper(Dumper):
    def dump(self, value: QByteArray) -> bytes:
        return bytes(f"\\x{value.toHex().data().decode('utf-8')}", 'utf-8')

psycopg.adapters.register_dumper(QByteArray, QByteArrayByteaDumper)


#
# inet --> str
#

class InetStrLoader(Loader):
    def load(self, value: bytes) -> str:
        return bytes(value).decode()

psycopg.adapters.register_loader('inet', InetStrLoader)

