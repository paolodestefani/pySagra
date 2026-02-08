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

"""Cryptography module

This module manages cryptography functions

"""

# standard library
from cryptography.fernet import Fernet

# application modules
from App import ENCKEY

# encoding decoding password

def string_encode(token: str) -> str:
    "Cryptography Fernet"
    return Fernet(ENCKEY).encrypt(token.encode('utf-8')).decode('utf-8')

def string_decode(token: str) -> str:
    "Cryptography Fernet"
    return Fernet(ENCKEY).decrypt(token.encode('utf-8')).decode('utf-8')

