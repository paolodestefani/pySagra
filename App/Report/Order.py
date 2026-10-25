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
from PySide6.QtGui import QGuiApplication
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtPrintSupport import QPrinterInfo

# other imported
from escpos.printer import Dummy
from escpos.printer import Network

# application modules
from App import session
from App.Core.Escpos import escpos_printer
from App.Database.Settings import Settings
from App.Database.OrderPrintSettings import order_print_settings
from App.Database.Report import get_report_xml
from App.Database.Report import report_xml
from App.Database.Report import report_query
from App.Report.ReportEngine import Report
from App.Report.ReportEngineEscPos import ReportEscpos
from App.Report.ReportEngineEscPos import PreviewDevice
from App.Widget.Dialog import PlainTextPreviewDialog


class OrderReportException(Exception):
    pass

class NoOrderReportParameters(OrderReportException):
    pass



def printOrderReport(print_type: str, department_id: int | None, order_id: int | None) -> None:
    "Generate a print report (driver or escpos) for the provided order_id"
    # get all print parameters
    if  (pars := order_print_settings(print_type, department_id)): 
        print_copy, print_method, copies, drv_report, drv_printer, esc_report, esc_printer = pars # for current computer name
    else:
        raise NoOrderReportParameters(f"No parameters available for computer {session['hostname']}")
    if not print_copy:
        return
    match print_method:
        case 'D': # DRIVER
            # driver report and printer
            report_drv = Report(get_report_xml(print_method, drv_report, session['l10n']))
            # report definition on condition fields must have code for order_id and department_id
            where = []
            for i in report_drv.conditions:
                if report_drv.conditions[i].code == 'order_id':
                    where.append((f"{i} = %s", order_id))
                if report_drv.conditions[i].code == 'department_id':
                    where.append((f"{i} = %s", department_id))
            report_drv.data = report_query(report_drv, where)
            report_drv.generate()
            if drv_printer:
                # print
                printer = QPrinter(QPrinterInfo.printerInfo(drv_printer))
                printer.setCopyCount(copies)
                report_drv.print(printer)
            else:
                # print preview
                # restore cursor if necessary
                if QGuiApplication.overrideCursor() is not None:
                    if QGuiApplication.overrideCursor().shape() == Qt.CursorShape.WaitCursor:
                        QGuiApplication.restoreOverrideCursor()
                # create the preview
                dialog = QPrintPreviewDialog(session['mainwin'])
                # start
                dialog.paintRequested.connect(report_drv.print)
                dialog.exec()
        case 'E': # ESC/POS
            # escpos report and printer
            report_esc = ReportEscpos(get_report_xml(print_method, esc_report, session['l10n']))
            # report definition on condition fields must have code for order_id and department_id
            where = []
            for i in report_esc.conditions:
                if report_esc.conditions[i].code == 'order_id':
                    where.append((f"{i} = %s", order_id))
                if report_esc.conditions[i].code == 'department_id':
                    where.append((f"{i} = %s", department_id))
            report_esc.data = report_query(report_esc, where)
            report_esc.generate()
            if esc_printer:
                # print
                printer = escpos_printer(esc_printer)
                report_esc.print(printer)
            else:
                # print preview
                preview = PreviewDevice()
                report_esc.print(preview)
                dlg = PlainTextPreviewDialog(session['mainwin'], preview.get_preview())
                dlg.exec()
    

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
