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

"""Message box

This module contains the critical error dialog with its expanding details.
It is separated from App.Widget.Dialog because the exception handler needs it
and App.Widget.Dialog needs the exception handler.

The dialog is for unhandled exceptions and serious errors only: it can be
resized, its details can be copied and Abort closes the application. Other
messages use the standard QMessageBox.

"""

# standard library
import logging
from typing import cast

# PySide6
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QAbstractButton
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import QWidget

# application modules
from App import session
from App.Common.Gui import no_wait_cursor_context
from App.Common.L10n import _tr
from App.Ui.MessageDialog import Ui_MessageDialog


# logger
logger = logging.getLogger(__name__)


class MessageBox(QDialog):
    "Custom message expanding dialog"

    def __init__(self, parent: QWidget|None = None) -> None:
        super().__init__(parent)
        self.ui = Ui_MessageDialog()
        self.ui.setupUi(self)
        app = cast(QApplication, QCoreApplication.instance())
        if not app:
            return
        sty = app.style()
        icon = sty.standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        self.ui.labelIcon.setPixmap(icon.pixmap(icon.actualSize(QSize(32, 32))))
        
        
def abortApplication() -> None:
    """Close the application in order: the main window asks to quit, closes
    the forms with their save requests, saves its settings and logs out"""
    mainwin = session.get('mainwin')
    if mainwin is not None:
        try:
            mainwin.close()
        except Exception:  # an error while closing must not leave the application without windows
            logger.exception("Error closing the main window, quitting anyway")
        if mainwin.isVisible():  # the user chose to go on
            return
    QApplication.quit()


def MessageBoxCritical(parent,
                       title: str|None = None,
                       ercode: str|None = None,
                       text: str|None = None,
                       detail: str|None = None
                       ) -> bool:
    """Show a critical message dialog with optional detail message.
    Return True if the user chose Abort; Ignore, Esc and the close button go on"""
    dlg = MessageBox(parent)
    dlg.setWindowTitle(title or _tr('Dialog', "Critical error"),)
    dlg.ui.labelErrorCode.setText(ercode or '')
    dlg.ui.labelMessage.setText(text or _tr('Dialog', "Unidentified critical error"),)
    if detail:
        detail = f"""
```python
{detail.strip()}
```
"""
    dlg.ui.textEditDetailMessage.setMarkdown(detail or "")
    # Esc and the close button reject the dialog as Abort does: only the button counts
    clicked: list[QAbstractButton] = []
    dlg.ui.buttonBox.clicked.connect(clicked.append)
    with no_wait_cursor_context():
        dlg.exec()
    aborted = bool(clicked) and dlg.ui.buttonBox.standardButton(clicked[-1]) == QDialogButtonBox.StandardButton.Abort
    if aborted:
        abortApplication()
    return aborted
