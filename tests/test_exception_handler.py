"""Wait cursor and messages of the exception contexts

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QApplication

# application modules
from App import session
from App.Database.Exceptions import PyAppDBConnectionError, PyAppDBError
from App.Report import ReportNoDataError
from App.Widget import ExceptionHandler as EH


app = QApplication.instance() or QApplication([])
WAIT = Qt.CursorShape.WaitCursor


def cursor_stack() -> list:
    "Empty the override cursor stack and return it, top first"
    shapes = []
    while (cursor := QGuiApplication.overrideCursor()) is not None:
        shapes.append(cursor.shape())
        QGuiApplication.restoreOverrideCursor()
    return shapes


class ContextTestCase(unittest.TestCase):

    def setUp(self) -> None:
        cursor_stack()
        self.events: list = []
        self.appconn = mock.Mock()
        self.appconn.rollback.side_effect = lambda: self.events.append('rollback')
        record = lambda name: lambda *a, **k: self.events.append((name, QGuiApplication.overrideCursor()))
        for target, name, value in ((EH, 'appconn', self.appconn),
                                    (EH, 'MessageBoxCritical', record('critical')),
                                    (EH.QMessageBox, 'warning', record('warning')),
                                    (EH.QMessageBox, 'information', record('information')),
                                    (EH.QMessageBox, 'critical', record('qcritical'))):
            patcher = mock.patch.object(target, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.dict(session, {'hostname': 'pc1'})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(cursor_stack)
        # an outer context, as wait_cursor_context while moving to a record
        QGuiApplication.setOverrideCursor(QCursor(WAIT))

    def run_gui(self, error: BaseException | None = None, messages: dict | None = None) -> None:
        with EH.gui_exception_context(None, 'Operation', messages):
            self.assertEqual(QGuiApplication.overrideCursor().shape(), WAIT)
            if error is not None:
                raise error

    def messages_shown(self) -> list:
        return [e for e in self.events if isinstance(e, tuple)]


class GuiExceptionContextTest(ContextTestCase):

    def test_success_leaves_the_outer_cursor(self) -> None:
        self.run_gui()
        self.assertEqual(cursor_stack(), [WAIT])

    def test_critical_error_without_wait_cursor(self) -> None:
        self.run_gui(PyAppDBError(code='42P01', message='missing table'))
        self.assertEqual(self.events, ['rollback', ('critical', None)])
        self.assertEqual(cursor_stack(), [WAIT])

    def test_form_message_without_wait_cursor(self) -> None:
        self.run_gui(PyAppDBError(code='23503', message='used'), {'23503': 'The item has been used'})
        self.assertEqual(self.events, ['rollback', ('warning', None)])
        self.assertEqual(cursor_stack(), [WAIT])

    def test_connection_error_has_no_rollback(self) -> None:
        self.run_gui(PyAppDBConnectionError(code='08006', message='gone'))
        self.assertEqual(self.events, [('critical', None)])

    def test_failed_rollback_does_not_escape(self) -> None:
        "The connection can be already closed"
        self.appconn.rollback.side_effect = RuntimeError('connection closed')
        with self.assertLogs(EH.logger, 'ERROR'):
            self.run_gui(PyAppDBError(code='57P01', message='terminated'))
        self.assertEqual(self.messages_shown(), [('critical', None)])

    def test_unexpected_error(self) -> None:
        self.run_gui(ValueError('broken'))
        self.assertEqual(self.events, [('critical', None)])
        self.assertEqual(cursor_stack(), [WAIT])

    def test_exit_is_not_caught(self) -> None:
        with self.assertRaises(KeyboardInterrupt):
            self.run_gui(KeyboardInterrupt())
        self.assertEqual(cursor_stack(), [WAIT])


class ReportExceptionContextTest(ContextTestCase):

    def run_report(self, error: Exception | None = None) -> None:
        with EH.report_exception_context(None):
            if error is not None:
                raise error

    def test_success(self) -> None:
        self.run_report()
        self.assertEqual(cursor_stack(), [WAIT])

    def test_no_data(self) -> None:
        self.run_report(ReportNoDataError())
        self.assertEqual(self.events, [('information', None)])
        self.assertEqual(cursor_stack(), [WAIT])

    def test_unexpected_error(self) -> None:
        self.run_report(ValueError('broken'))
        self.assertEqual(self.events, [('critical', None)])


if __name__ == '__main__':
    unittest.main()
