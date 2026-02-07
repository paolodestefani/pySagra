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

"""Application constants and parameters

"""

# python std library
from typing import Any
from collections import defaultdict

# PySide6
from PySide6.QtGui import QIcon
from PySide6.QtGui import QAction

# constants, language indipendent
APPNAME         = 'pySagra'
APPVERSIONMAJOR = 1
APPVERSIONMINOR = 0
APPVERSIONPATCH = 0
APPVERSIONTAG   = 'Alpha' #'"A new world"'
AUTHOR          = 'Paolo De Stefani'
EMAIL           = 'info@paolodestefani.it'
ORGANIZATION    = 'PDS Software'
WEBSITE         = 'www.paolodestefani.it'

# minumum required version
MRV_PYTHON  = 3, 12, 0 
MRV_PYSIDE  = 6, 9, 0
MRV_QT      = 6, 9, 0
MRV_PSYCOPG = 3, 3, 0
MRV_PGSQL   = 130000  # postgres minimum compatible version

# key for encoding/decoding stored database user and password
ENCKEY = "WgqvuDSWuW909HX9Cb0tNpo0IaINHRdsRkqxfImxYGQ="

# application session parameters
session: dict[str, Any] = dict()  # database and application user parameters

# dictionary for definition, current in use actions and icons
actionDefinition: dict[str, tuple] = dict()
currentAction: dict[str, QAction] = dict()
currentProfile: dict[str, str] = dict() # authorizations for current profile
currentIcon: defaultdict = defaultdict(QIcon)  # provide an invalid QIcon when an icon is not available
