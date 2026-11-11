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

# cryptography
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

# PySide6
from PySide6.QtCore import QSettings

# application modules
from App import ENCKEY


# QSettings key of the per-computer Fernet key
LOCAL_KEY_SETTING = "LogIn/LocalKey"


# shared values: ENCKEY is public (it is in the source code), so this is only
# obfuscation, not protection. It can not be replaced by a per-computer key
# because these values are stored in the database and read by every computer

def string_encode(token: str|object) -> str:
    "Cryptography Fernet"
    token = str(token)
    return Fernet(ENCKEY).encrypt(token.encode('utf-8')).decode('utf-8')

def string_decode(token: str|object) -> str:
    "Cryptography Fernet"
    token = str(token)
    return Fernet(ENCKEY).decrypt(token.encode('utf-8')).decode('utf-8')


# local values: these are stored in QSettings and read only by this computer.
# The key is kept in QSettings too, so this is still obfuscation against casual
# reading, but the key is not public and differs on every computer

def _local_fernet() -> Fernet:
    "Return the Fernet instance of this computer, creating its key on first use"
    st = QSettings()
    key = str(st.value(LOCAL_KEY_SETTING, ""))
    try:
        return Fernet(key)
    except ValueError:  # missing or corrupted key
        key = Fernet.generate_key().decode('ascii')
        st.setValue(LOCAL_KEY_SETTING, key)
        return Fernet(key)

def local_encode(token: str|object) -> str:
    "Encrypt a value that is stored only on this computer"
    return _local_fernet().encrypt(str(token).encode('utf-8')).decode('utf-8')

def local_decode(token: str|object) -> str:
    """Decrypt a value that is stored only on this computer

    Values saved by previous versions use ENCKEY, they are accepted here and
    get encrypted with the local key the next time they are saved.
    Raise InvalidToken if the value can not be decrypted
    """
    data = str(token).encode('utf-8')
    try:
        return _local_fernet().decrypt(data).decode('utf-8')
    except InvalidToken:
        return Fernet(ENCKEY).decrypt(data).decode('utf-8')

