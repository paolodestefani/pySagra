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

"""Database parameters and constants

This module contains database related parameters and constants

"""

# minimum required version
MRV_PGSQL   = 130000  # postgres minimum compatible version

# database application error codes

EWDBS = 'PA001'  # wrong database server version (connect sp)
EWADB = 'PA002'  # wrong application database (connect sp)
EWAPV = 'PA003'  # wrong application database version (connect sp)
EUKNU = 'PA004'  # authentication failed, user does not exist (connect sp)
EPWDR = 'PA005'  # a password is required (connect sp)
EWPWD = 'PA006'  # authentication failed, wrong password (connect sp)
EUKNC = 'PA007'  # Unknown company (change company)
ENACR = 'PA008'  # No access rights to required company (change company)
ENKCC = 'PA009'  # Can not kill current connection (change company)
EDSAE = 'PA011'  # Database schema already exists (create company sp)
ECIAE = 'PA012'  # Company id already exists (create company sp)
ECIIU = 'PA013'  # Company is in use (drop company sp)

# other parameters

OVFIELD = 'object_version' # object versione field name for concurrency
COMPANYFIELD = 'company_id'  # default company id field name