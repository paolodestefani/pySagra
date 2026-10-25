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

"""ESC/POS module

This module handles classes and functions related to ESC/POS printers.

"""

# standard library
from typing import Any

# PySide6
from PySide6.QtWidgets import QMessageBox

from escpos.printer import Dummy, Usb, Network

# application modules
from App import session
from App.Core.L10n import _tr
from App.Core.ExceptionHandler import gui_exception_context
from App.Database.Escpos import get_escpos_printer_params



# create an esc/pos printer from parameters stored in database
def escpos_printer(printer_id: int)-> Usb | Network:
    "Create an ESC/POS printer"
    pars: tuple[Any] | None
    if  (pars := get_escpos_printer_params(printer_id)): 
        (hostname, name, type, 
         host, port, connection_timeout,
         id_vendor, id_product, usb_timeout, in_endpoint, out_endpoint) = pars # for current computer name
    else:
        type = None
    match type:
        case 'N': # Network printer
            return Network(host=host, port=port, timeout=connection_timeout)
        case 'U': # Usb printer
            return Usb(idVendor=id_vendor, idProduct=id_product,timeout=usb_timeout, in_ep=in_endpoint, out_ep=out_endpoint)
        case _:  # no printer
            raise Exception("No printer available")
        