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

"""Raw ESC/POS jobs delivery: one job at a time for each physical printer,
different printers work in parallel. It works inside one process only: two PCs
sending to the same printer are not coordinated by this module."""

import socket
from collections import deque

from escpos.printer import Network, Usb
from PySide6.QtCore import QCoreApplication, QObject, QThread, Signal

# waits (seconds) between connection attempts when the printer refuses the connection (busy)
RETRY_DELAYS = (0.3, 0.6, 1.0, 2.0, 3.0)


class PrinterSenderThread(QThread):
    "Send raw bytes to a network or usb printer, the connection is opened inside the thread"
    job_completed = Signal()
    print_error = Signal(str)

    def __init__(self, pd: Network | Usb, raw_bytes: bytes) -> None:
        super().__init__()
        self.pd = pd
        self.raw_bytes = raw_bytes
        if isinstance(pd, Network):
            self.host: str = pd.host
            self.port: int = pd.port
            self.net_timeout: float = pd.timeout if pd.timeout else 4.0

    def _connect(self) -> socket.socket:
        "Open the connection, retrying only if the printer refuses it"
        last: Exception | None = None
        for delay in (0.0, *RETRY_DELAYS):
            if delay:
                QThread.msleep(int(delay * 1000))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.net_timeout)
            try:
                s.connect((self.host, self.port))
                return s
            except (ConnectionRefusedError, ConnectionResetError) as e:
                last = e              # printer busy: try again
                s.close()
            except OSError:
                s.close()             # timeout, host unreachable: waiting longer is useless
                raise
        assert last is not None
        raise last

    def run(self) -> None:
        match self.pd:
            case Network():
                s: socket.socket | None = None
                try:
                    s = self._connect()
                    s.sendall(self.raw_bytes)     # no retry after this point: it could print twice
                    self.job_completed.emit()
                except socket.timeout:
                    self.print_error.emit(f"Timeout: the printer {self.host} is not responding.")
                except OSError as e:
                    self.print_error.emit(f"Network error: {e}")
                finally:
                    if s:
                        s.close()
            case Usb() as usb_dev:
                try:
                    usb_dev.open()
                    usb_dev._raw(self.raw_bytes)
                    self.job_completed.emit()
                except Exception as e:
                    self.print_error.emit(f"USB error: {e}")
                finally:
                    try:
                        usb_dev.close()
                    except Exception:
                        pass


class PrintScheduler(QObject):
    "One queue for each printer: jobs for the same printer are sent one at a time, in order"
    jobCompleted = Signal(str)        # printer key
    jobFailed = Signal(str, str)      # printer key, error message

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._pending: dict[str, deque] = {}
        self._busy: set[str] = set()

    @staticmethod
    def key(pd: Network | Usb) -> str:
        "Identify the physical printer"
        if isinstance(pd, Network):
            return f"net:{pd.host}:{pd.port}"
        args = getattr(pd, 'usb_args', {})
        return f"usb:{args.get('idVendor')}:{args.get('idProduct')}"

    def submit(self, pd: Network | Usb, raw: bytes) -> None:
        "Queue a job, call it from the main thread"
        k = self.key(pd)
        self._pending.setdefault(k, deque()).append((pd, bytes(raw)))
        if k not in self._busy:
            self._next(k)

    def _next(self, k: str) -> None:
        queue = self._pending.get(k)
        if not queue:
            self._busy.discard(k)
            return
        pd, raw = queue.popleft()
        self._busy.add(k)
        th = PrinterSenderThread(pd, raw)
        th.setParent(self)                    # the scheduler keeps the thread alive
        th.job_completed.connect(lambda k=k: self.jobCompleted.emit(k))
        th.print_error.connect(lambda msg, k=k: self.jobFailed.emit(k, msg))
        th.finished.connect(th.deleteLater)
        th.finished.connect(lambda k=k: self._next(k))
        th.start()

    def shutdown(self, timeout_ms: int = 5000) -> None:
        "Wait for the jobs in progress (queued jobs not yet started are lost)"
        for th in self.findChildren(QThread):
            th.wait(timeout_ms)


_scheduler: PrintScheduler | None = None


def print_scheduler() -> PrintScheduler:
    "The application scheduler, created on first use"
    global _scheduler
    if _scheduler is None:
        _scheduler = PrintScheduler(QCoreApplication.instance())
    return _scheduler