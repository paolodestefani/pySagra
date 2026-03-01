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

"""Application Actions

This module contains actions definitions

"""

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtCore import QKeyCombination
from PySide6.QtGui import QAction
from PySide6.QtGui import QKeySequence

# application modules
from App import APPNAME
from App import actionDefinition
from App.Core.L10n import _tr

# application slots
from App.System.User import changePassword
from App.System.Help import help
from App.System.Help import faq
from App.System.About import about
from App.System.About import systemInfo
from App.System.About import aboutQt
from App.System.Preferences import preferences
from App.System.Connection import connection
from App.System.Connection import connectionHistory
from App.System.Company import company
from App.System.Profile import profile
from App.System.User import user
from App.System.Menu import menu
from App.System.Toolbar import toolbar
from App.System.Report import report
from App.System.Scripting import scripting
from App.System.Customization import customization
from App.CashDesk import cashDesk
from App.Printer import printer
from App.Department import department
from App.SeatMap import seatMap
from App.Item import item
from App.PriceList import priceList
from App.Event import event
from App.UpdateWebOrderServer import updateWebOrderServer
from App.WebOrder import webOrder
from App.OrderArchive import orderArchive
from App.OrderNumbering import orderNumbering
from App.Settings import settings
from App.Inventory import inventory
from App.OrderProgress import orderProgress

from App.OrderEntry import orderEntry
from App.Statistics import statisticsAnalysis, statisticsPrint, statisticsExport
from App.OrderedDelivered import orderedDelivered
from App.SalesSummary import salesSummary
from App.Tool import eventBasedTool
from App.Tool import deleteTool
from App.Tool import copyTool


# 0 description
# 1 slot
# 2 checkable
# 3 icon name
# 4 standard shortcut
# 5 tooltip
# 6 status tip
# 7 what's this
# 8 menu role


def createActionDictionary(mw) -> None:
    "Create the action definition dictionary trough a function for translation requirement"

    # SYSTEM ACTIONS
    actionDefinition['sys_change_company'] = (
        _tr("Action", 'Change company'),
        mw.changeCompany,
        False,
        'system_change_company',
        QKeySequence.StandardKey.Open,
        _tr("Action", 'Change company'),
        _tr("Action", 'Switch to another company'),
        _tr("Action", 'Switch to another company'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['sys_change_password'] = (
        _tr("Action", 'Change password'),
        changePassword,
        False,
        'system_password',
        QKeySequence(QKeyCombination(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_X)),
        _tr("Action", 'Change password'),
        _tr("Action", 'Change password of the current user'),
        _tr("Action", 'Change password'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_preferences'] = (
        _tr("Action", 'Preferences'),
        preferences,
        False,
        'system_preferences',
        QKeySequence.StandardKey.Preferences,
        _tr("Action", 'Change Theme'),
        _tr("Action", 'Change the Qt Theme used'),
        _tr("Action", 'Change Theme'),
        QAction.MenuRole.PreferencesRole)
    
    actionDefinition['sys_connection'] = (
        _tr("Action", 'Current connections'),
        connection,
        False,
        'system_connections',
        None,
        _tr("Action", 'Current connections'),
        _tr("Action", 'Show/Edit curent connections'),
        _tr("Action", 'Current connections'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_connection_history'] = (
        _tr("Action", 'Connections history'),
        connectionHistory,
        False,
        'system_connections_history',
        None,
        _tr("Action", 'Connections history'),
        _tr("Action", 'Show connections history'),
        _tr("Action", 'Connections history'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_company'] = (
        _tr("Action", 'Manage companies'),
        company,
        False,
        'system_company',
        None,
        _tr("Action", 'Manage companies'),
        _tr("Action", 'Create/drop/modify companies'),
        _tr("Action", 'Manage companies'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_profile'] = (
        _tr("Action", 'Profiles'),
        profile,
        False,
        'system_profile',
        None,
        _tr("Action", 'Profiles management'),
        _tr("Action", 'Profiles management'),
        _tr("Action", 'Profiles management'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_user'] = (
        _tr("Action", 'Users'),
        user,
        False,
        'system_user',
        None,
        _tr("Action", 'Users management'),
        _tr("Action", 'Users management'),
        _tr("Action", 'Users management'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_menu'] = (
        _tr("Action", 'Menus'),
        menu,
        False,
        'system_menu',
        None,
        _tr("Action", 'Menus management'),
        _tr("Action", 'Menus management'),
        _tr("Action", 'Menus management'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_toolbar'] = (
        _tr("Action", 'Toolbars'),
        toolbar,
        False,
        'system_toolbar',
        None,
        _tr("Action", 'Toolbars management'),
        _tr("Action", 'Toolbars management'),
        _tr("Action", 'Toolbars management'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_report'] = (
        _tr("Action", 'Reports'),
        report,
        False,
        'system_report',
        None,
        _tr("Action", 'Create/Edit reports'),
        _tr("Action", 'Create/Edit reports'),
        _tr("Action", 'Create/Edit reports'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_scripting'] = (
        _tr("Action", 'Python scripting'),
        scripting,
        False,
        'system_scripting',
        None,
        _tr("Action", 'Create/Edit python scripts'),
        _tr("Action", 'Create/Edit python scripts'),
        _tr("Action", 'Create/Edit python scripts'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['sys_customization'] = (
        _tr("Action", 'Customizations'),
        customization,
        False,
        'system_customization',
        None,
        _tr("Action", 'Import/Export customizations'),
        _tr("Action", 'Import/Export customizations'),
        _tr("Action", 'Import/Export customizations'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['sys_quit'] = (
        _tr("Action", 'Quit'),
        mw.close,
        False,
        'system_quit',
        QKeySequence.StandardKey.Quit,
        _tr("Action", 'Quit'),
        _tr("Action", 'Close all windows and quit the application'),
        _tr("Action", 'Quit'),
        QAction.MenuRole.QuitRole)


    # EDIT ACTIONS
    actionDefinition['edit_new'] = (
        _tr("Action", 'New'),
        mw.new,
        False,
        'edit_new',
        QKeySequence.StandardKey.New,
        _tr("Action", 'New record'),
        _tr("Action", 'Insert new record'),
        _tr("Action", 'New record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_save'] = (
        _tr("Action", 'Save'),
        mw.save,
        False,
        'edit_save',
        QKeySequence.StandardKey.Save,
        _tr("Action", 'Save record'),
        _tr("Action", 'Save record'),
        _tr("Action", 'Save record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_delete'] = (
        _tr("Action", 'Delete'),
        mw.delete,
        False,
        'edit_delete',
        QKeySequence.StandardKey.Delete,
        _tr("Action", 'Delete record'),
        _tr("Action", 'Delete record'),
        _tr("Action", 'Delete record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_reload'] = (
        _tr("Action", 'Undo/Reload'),
        mw.reload,
        False,
        'edit_reload',
        QKeySequence.StandardKey.Refresh,
        _tr("Action", 'Undo last change/Reload data'),
        _tr("Action", 'Undo last change/Reload data'),
        _tr("Action", 'Undo last change/Reload data'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_first'] = (
        _tr("Action", 'First'),
        mw.toFirst,
        False,
        'edit_first',
        QKeySequence.StandardKey.MoveToStartOfDocument,
        _tr("Action", 'Go to first record'),
        _tr("Action", 'Go to first record'),
        _tr("Action", 'Go to first record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_previous'] = (
        _tr("Action", 'Previous'),
        mw.toPrevious,
        False,
        'edit_previous',
        QKeySequence.StandardKey.Back,
        _tr("Action", 'Go to previous record'),
        _tr("Action", 'Go to previous record'),
        _tr("Action", 'Go to previous record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_counter'] = (
        _tr("Action", 'Counter'),
        None,
        False,
        None,
        None,
        _tr("Action", 'Current view record counter'),
        _tr("Action", 'Current view record counter'),
        _tr("Action", 'Current view record counter'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_next'] = (
        _tr("Action", 'Next'),
        mw.toNext,
        False,
        'edit_next',
        QKeySequence.StandardKey.Forward,
        _tr("Action", 'Go to next record'),
        _tr("Action", 'Go to next record'),
        _tr("Action", 'Go to next record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_last'] = (
        _tr("Action", 'Last'),
        mw.toLast,
        False,
        'edit_last',
        QKeySequence.StandardKey.MoveToEndOfDocument,
        _tr("Action", 'Go to last record'),
        _tr("Action", 'Go to last record'),
        _tr("Action", 'Go to last record'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_filter'] = (
        _tr("Action", 'Filters'),
        mw.setFilters,
        False,
        'edit_filter',
        QKeySequence.StandardKey.Find,
        _tr("Action", 'Edit filters'),
        _tr("Action", 'Edit filters'),
        _tr("Action", 'Edit filters'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_change_view'] = (
        _tr("Action", 'Chenge view'),
        mw.changeView,
        False,
        'edit_change',
        None,
        _tr("Action", 'Change view'),
        _tr("Action", 'Change view'),
        _tr("Action", 'Change view'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_print'] = (
        _tr("Action", 'Print'),
        mw.print,
        False,
        'edit_print',
        QKeySequence.StandardKey.Print,
        _tr("Action", 'Generate a print report'),
        _tr("Action", 'Generate a print report'),
        _tr("Action", 'Generate a print report'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['edit_export'] = (
        _tr("Action", 'Export'),
        mw.export,
        False,
        'edit_export',
        None,
        _tr("Action", 'Export data'),
        _tr("Action", 'Export data to a csv file'),
        _tr("Action", 'Export data'),
        QAction.MenuRole.TextHeuristicRole)

    # HELP ACTIONS
    actionDefinition['help_index'] = (
        _tr("Action", 'Help'),
        help,
        False,
        'help_content',
        QKeySequence.StandardKey.HelpContents,
        _tr("Action", 'Help'),
        _tr("Action", 'Help index'),
        _tr("Action", 'Help'),
        QAction.MenuRole.NoRole)

    actionDefinition['help_faq'] = (
        _tr("Action", 'FAQ'),
        faq,
        False,
        'help_faq',
        None,
        _tr("Action", 'FAQ'),
        _tr("Action", 'Frequently Asked Questions'),
        _tr("Action", 'FAQ'),
        QAction.MenuRole.NoRole)

     # ABOUT ACTIONS
    actionDefinition['about_program'] = (
        _tr("Action", 'About {}').format(APPNAME),
        about,
        False,
        APPNAME,
        None,
        _tr("Action", 'About...'),
        _tr("Action", 'Information about {}').format(APPNAME),
        _tr("Action", 'About...'),
        QAction.MenuRole.AboutRole)

    actionDefinition['about_qt'] = (
        _tr("Action", 'About Qt'),
        aboutQt,
        False,
        'qt_logo',
        None,
        _tr("Action", 'About Qt'),
        _tr("Action", 'About Qt'),
        _tr("Action", 'About Qt'),
        QAction.MenuRole.AboutQtRole)

    actionDefinition['about_system_info'] = (
        _tr("Action", 'System informations'),
        systemInfo,
        False,
        'help_system_info',
        QKeySequence('CTRL+F1'),
        _tr("Action", 'System information'),
        _tr("Action", 'System information'),
        _tr("Action", 'System information'),
        QAction.MenuRole.NoRole)

    # APPLICATION SPECIFIC ACTIONS

    # file actions
    
    actionDefinition['app_file_cash_desk'] = (
        _tr("Action", 'Cash desk'),
        cashDesk,
        False,
        'file_cash_desk',
        None,
        _tr("Action", 'Cash desk'),
        _tr("Action", 'Manage cash desk names and parameters'),
        _tr("Action", 'Cash desk'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['app_file_printer'] = (
        _tr("Action", 'Printers'),
        printer,
        False,
        'file_printer',
        None,
        _tr("Action", 'Printer classes'),
        _tr("Action", 'Manage printer classes'),
        _tr("Action", 'Printer classes'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_event'] = (
        _tr("Action", 'Events'),
        event,
        False,
        'file_event',
        None,
        _tr("Action", 'Events'),
        _tr("Action", 'Events'),
        _tr("Action", 'Events'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['app_file_update_wo_server'] = (
        _tr("Action", 'Update W.O.Server'),
        updateWebOrderServer,
        False,
        'file_update_web_order',
        None,
        _tr("Action", 'Update W.O.Server'),
        _tr("Action", 'Update W.O.Server'),
        _tr("Action", 'Update W.O.Server'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_department'] = (
        _tr("Action", 'Departments'),
        department,
        False,
        'file_department',
        None,
        _tr("Action", 'Departments'),
        _tr("Action", 'Departments'),
        _tr("Action", 'Departments'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_seat_map'] = (
        _tr("Action", 'Seat map'),
        seatMap,
        False,
        'file_seat_map',
        None,
        _tr("Action", 'Seat map'),
        _tr("Action", 'Seat map'),
        _tr("Action", 'Seat map'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_item'] = (
        _tr("Action", 'Items'),
        item,
        False,
        'file_item',
        None,
        _tr("Action", 'Items'),
        _tr("Action", 'Items'),
        _tr("Action", 'Items'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_price_list'] = (
        _tr("Action", 'Price list'),
        priceList,
        False,
        'file_price_list',
        None,
        _tr("Action", 'Price list'),
        _tr("Action", 'Price list'),
        _tr("Action", 'Price list'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_order'] = (
        _tr("Action", 'Orders'),
        orderArchive,
        False,
        'file_order',
        None,
        _tr("Action", 'Orders'),
        _tr("Action", 'Orders'),
        _tr("Action", 'Orders'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_file_web_order'] = (
        _tr("Action", 'Web orders'),
        webOrder,
        False,
        'file_web_order',
        None,
        _tr("Action", 'Web orders'),
        _tr("Action", 'Web orders'),
        _tr("Action", 'Web orders'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['app_file_order_number'] = (
        _tr("Action", 'Order numbers'),
        orderNumbering,
        False,
        'file_order_number',
        None,
        _tr("Action", 'Order numbers'),
        _tr("Action", 'Manage order number current values'),
        _tr("Action", 'Order numbers'),
        QAction.MenuRole.TextHeuristicRole)
    
    actionDefinition['app_file_setting'] = (
        _tr("Action", 'Settings'),
        settings,
        False,
        'file_settings',
        None,
        _tr("Action", 'Settings'),
        _tr("Action", 'View/Modify application settings'),
        _tr("Action", 'Settings'),
        QAction.MenuRole.NoRole)

    # activities actions
    actionDefinition['app_activity_order_entry'] = (
        _tr("Action", 'Order entry'),
        orderEntry,
        False,
        'activities_order',
        None,
        _tr("Action", 'Order entry'),
        _tr("Action", 'Order entry'),
        _tr("Action", 'Order entry'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_activity_inventory'] = (
        _tr("Action", 'Inventory'),
        inventory,
        False,
        'activities_inventory',
        None,
        _tr("Action", 'Inventory'),
        _tr("Action", 'Inventory'),
        _tr("Action", 'Inventory'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_activity_order_progress'] = (
        _tr("Action", 'Order progress'),
        orderProgress,
        False,
        'activities_order_progress',
        None,
        _tr("Action", 'Order progress'),
        _tr("Action", 'Order progress'),
        _tr("Action", 'Order progress'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_activity_ordered_delivered'] = (
        _tr("Action", 'Ordered delivered'),
        orderedDelivered,
        False,
        'activities_ordered_delivered',
        None,
        _tr("Action", 'Ordered delivered'),
        _tr("Action", 'Ordered delivered'),
        _tr("Action", 'Ordered delivered'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_activity_sales_summary'] = (
        _tr("Action", 'Sales summary'),
        salesSummary,
        False,
        'activities_sales_summary',
        None,
        _tr("Action", 'Sales summary'),
        _tr("Action", 'Sales summary'),
        _tr("Action", 'Sales summary'),
        QAction.MenuRole.TextHeuristicRole)

    # statistics
    actionDefinition['app_statistics_analysis'] = (
        _tr("Action", 'Pivot table analysis'),
        statisticsAnalysis,
        False,
        'statistics_statistic',
        None,
        _tr("Action", 'Pivot table analysis'),
        _tr("Action", 'Pivot table analysis'),
        _tr("Action", 'Pivot table analysis'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_statistics_print'] = (
        _tr("Action", 'Print statistics'),
        statisticsPrint,
        False,
        'statistics_statistic',
        None,
        _tr("Action", 'Print statistics'),
        _tr("Action", 'Print statistics'),
        _tr("Action", 'Print statistics'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_statistics_export'] = (
        _tr("Action", 'Export statistic data'),
        statisticsExport,
        False,
        'statistics_statistic',
        None,
        _tr("Action", 'Export statistic data'),
        _tr("Action", 'Export statistic data'),
        _tr("Action", 'Export statistic data'),
        QAction.MenuRole.TextHeuristicRole)

    # tools actions
    actionDefinition['app_tool_event_based'] = (
        _tr("Action", 'Application event based tool'),
        eventBasedTool,
        False,
        'tools_tool',
        None,
        _tr("Action", 'Application event based utilities'),
        _tr("Action", 'Application event based utilities'),
        _tr("Action", 'Application event based utilities'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_tool_delete'] = (
        _tr("Action", 'Delete tool'),
        deleteTool,
        False,
        'tools_tool',
        None,
        _tr("Action", 'Delete company data'),
        _tr("Action", 'Delete company data'),
        _tr("Action", 'Delete company data'),
        QAction.MenuRole.TextHeuristicRole)

    actionDefinition['app_tool_copy'] = (
        _tr("Action", 'Copy tool'),
        copyTool,
        False,
        'tools_tool',
        None,
        _tr("Action", 'Copy data from another company'),
        _tr("Action", 'Copy data from another company'),
        _tr("Action", 'Copy data from another company'),
        QAction.MenuRole.TextHeuristicRole)

