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

"""Order report utilities

This module contains functions to generate and print order-related reports.

"""

# standard library
from typing import Any

# PySide6
from PySide6.QtCore import QDate
from PySide6.QtCore import Qt
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtPrintSupport import QPrinterInfo

# application modules
from App import session
from App.Database.Setting import Setting
from App.Database.Report import get_report_id
from App.Database.Report import report_xml
from App.Database.Report import report_query
from App.Report.ReportEngine import Report


def printOrderReport(order_id: int, printer: str|None = None) -> None:
    setting = Setting()
    report_id = get_report_id(setting['customer_report'], session['l10n'])
    if not report_id:
        raise Exception("No customer report defined")
    report = Report(report_xml(report_id))
    # report definition on condition fields must have code for Order Id
    where = []
    for i in report.conditions:
        if report.conditions[i].code == 'order_id':
            where.append((f"{i} = %s", order_id))
    report.data = report_query(report, where)
    report.generate()
    if printer:
        prnt = QPrinter(QPrinterInfo.printerInfo(printer))
        prnt.setCopyCount(setting['customer_copies'])
        report.print(prnt)
    else:
        # print preview
        dialog = QPrintPreviewDialog(session['mainwin'])
        # start
        dialog.paintRequested.connect(report.print)
        dialog.exec()
        
        
def printOrderCoverReport(order_id: int, printer: str|None = None) -> None:
    setting = Setting()
    report_id = get_report_id(setting['cover_report'], session['l10n'])
    if not report_id:
        raise Exception("No customer report defined")
    report = Report(report_xml(report_id))
    # report definition on condition fields must have code for Order Id
    where = []
    for i in report.conditions:
        if report.conditions[i].code == 'order_id':
            where.append((f"{i} = %s", order_id))
    report.data = report_query(report, where)
    report.generate()
    if printer:
        prnt = QPrinter(QPrinterInfo.printerInfo(printer))
        prnt.setCopyCount(setting['cover_copies'])
        report.print(prnt)
    else:
        # print preview
        dialog = QPrintPreviewDialog(session['mainwin'])
        # start
        dialog.paintRequested.connect(report.print)
        dialog.exec()


def printOrderDepartmentReport(order_id: int, 
                               department: int|None = None,
                               printer: str|None = None) -> None:
    setting = Setting()
    report_id = get_report_id(setting['department_report'], session['l10n'])
    if not report_id:
        raise Exception("No customer report defined")
    report = Report(report_xml(report_id))
    # create condition
    # report definition on condition fields must have a code for Order Id and Order Department Id
    where = []
    for i in report.conditions:
        if report.conditions[i].code == 'order_id':
            where.append((f"{i} = %s", order_id))
        if report.conditions[i].code == 'department_id' and department is not None:
            where.append((f"{i} = %s", department))
    report.data = report_query(report, where)
    report.generate()
    if printer:
        prnt = QPrinter(QPrinterInfo.printerInfo(printer))
        #prnt.setFullPage(True)
        prnt.setCopyCount(setting['department_copies'])
        report.print(prnt)
    else:
        # print preview
        dialog = QPrintPreviewDialog(session['mainwin'])
        # start
        dialog.paintRequested.connect(report.print)
        dialog.exec()


def printStockUnloadReport(report_id: int,
                           printer: str|None = None,
                           copies: int = 1,
                           event: int|None = None,
                           day: QDate|None = None,
                           daypart: str|None = None) -> None:
    report = Report(report_xml(report_id))
    # create condition
    # report definition on condition fields must have a code for event, day, day_part and unload_control
    where: list[tuple[str, Any]] = []
    for i in report.conditions:
        match report.conditions[i].code:
            case 'event' if event is not None:
                where.append((f"{i} = %s", event))
            case 'event_date' if day is not None:
                where.append((f"{i} = %s", day))
            case 'day_part' if daypart is not None:
                where.append((f"{i} = %s", daypart))
            case _:
                pass
        if report.conditions[i].code == 'unload_control':
            where.append((f"{i} IS %s", True))
    report.data = report_query(report, where)
    report.generate()
    if printer:
        prnt = QPrinter(QPrinterInfo.printerInfo(printer))
        prnt.setCopyCount(copies)
        report.print(prnt)
    else:
        # print preview
        dialog = QPrintPreviewDialog(session['mainwin'])
        # start
        dialog.paintRequested.connect(report.print)
        dialog.exec()
