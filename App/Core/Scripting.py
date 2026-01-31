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

# PySide6
from PySide6.QtWidgets import QMessageBox

# application modules
from App import session
from App.Database.Scripting import get_script


# scripting management
def scriptInit(instanceReference):
    "Returns a dictionary of string command for scripting purpose"
    script = get_script(instanceReference.__class__.__name__)
    # execute init script after if any
    globalsParameters = {'session': session,
                         'self': instanceReference}
    try:
        exec(script.get(('__init__', 'A'), ''), globalsParameters)
    except Exception as er:
        QMessageBox.critical(None,
                             'Script engine',
                             f'Error executing __init__ script: \n{er}')
    return script


def scriptMethod(method):
    "Execute before/after script if any"

    def wrapper(*args, **kwargs):
        globalsParameters = {'session': session,
                             'self': args[0]}  # first argument of a method is instance reference
        # execute script before
        try:
            exec(args[0].script.get((method.__name__, 'B'), ''), globalsParameters)
        except Exception as er:
            QMessageBox.critical(None,
                                 'Script engine',
                                 f'Error executing before script: \n{er}')
        # execute script instead
        if args[0].script.get((method.__name__, 'I')):
            try:
                exec(args[0].script.get((method.__name__, 'I'), ''), globalsParameters)
            except Exception as er:
                QMessageBox.critical(None,
                                     'Script engine',
                                     f'Error executing instead script: \n{er}')
        else:
            # execute method
            method(*args, **kwargs)

        # execute script after
        try:
            exec(args[0].script.get((method.__name__, 'A'), ''), globalsParameters)
        except Exception as er:
            QMessageBox.critical(None,
                                 'Script engine',
                                 f'Error executing after script: \n{er}')

    return wrapper

