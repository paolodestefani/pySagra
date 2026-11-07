"""The critical dialog closes the application only when the user chooses Abort

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
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QDialogButtonBox

# application modules
from App import session
from App.Widget import MessageBox


app = QApplication.instance() or QApplication([])


def answer(action) -> None:
    "Act on the critical dialog as soon as it is open"
    def act() -> None:
        dialog = QApplication.activeModalWidget()
        if dialog is None:
            QTimer.singleShot(10, act)
            return
        action(dialog)
    QTimer.singleShot(10, act)


def press(button: QDialogButtonBox.StandardButton):
    return lambda dialog: dialog.ui.buttonBox.button(button).click()


class MessageBoxCriticalTest(unittest.TestCase):

    def setUp(self) -> None:
        patcher = mock.patch.object(MessageBox.QApplication, 'quit')
        self.quit = patcher.start()
        self.addCleanup(patcher.stop)
        self.mainwin = mock.Mock()
        self.mainwin.isVisible.return_value = False   # closing is accepted
        patcher = mock.patch.dict(session, {'mainwin': self.mainwin})
        patcher.start()
        self.addCleanup(patcher.stop)

    def show(self, action) -> bool:
        answer(action)
        return MessageBox.MessageBoxCritical(None, 'Title', 'CODE', 'Message', 'Detail')

    def test_ways_to_go_on(self) -> None:
        for name, action in (('Ignore', press(QDialogButtonBox.StandardButton.Ignore)),
                             ('Esc', lambda d: QTest.keyClick(d, Qt.Key.Key_Escape)),
                             ('close button', lambda d: d.close())):
            with self.subTest(way=name):
                self.assertFalse(self.show(action))
                self.mainwin.close.assert_not_called()
                self.quit.assert_not_called()

    def test_abort_closes_the_main_window(self) -> None:
        self.assertTrue(self.show(press(QDialogButtonBox.StandardButton.Abort)))
        self.mainwin.close.assert_called_once()
        self.quit.assert_called_once()

    def test_abort_refused_by_the_main_window(self) -> None:
        "The main window asks to quit: answering No goes on"
        self.mainwin.isVisible.return_value = True
        self.assertTrue(self.show(press(QDialogButtonBox.StandardButton.Abort)))
        self.mainwin.close.assert_called_once()
        self.quit.assert_not_called()

    def test_abort_when_closing_fails(self) -> None:
        "The logout fails with the database stopped: the application must quit anyway"
        self.mainwin.close.side_effect = RuntimeError('logout failed')
        with self.assertLogs(MessageBox.logger, 'ERROR'):
            self.assertTrue(self.show(press(QDialogButtonBox.StandardButton.Abort)))
        self.quit.assert_called_once()

    def test_no_wait_cursor_while_the_message_is_open(self) -> None:
        "Two nested contexts stacked a wait cursor each"
        wait = QCursor(Qt.CursorShape.WaitCursor)
        QGuiApplication.setOverrideCursor(wait)
        QGuiApplication.setOverrideCursor(wait)
        seen = []

        def look(dialog) -> None:
            seen.append(QGuiApplication.overrideCursor())
            dialog.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ignore).click()

        self.show(look)
        self.assertEqual(seen, [None])
        # the contexts can still remove their own cursors
        restored = []
        while QGuiApplication.overrideCursor() is not None:
            restored.append(QGuiApplication.overrideCursor().shape())
            QGuiApplication.restoreOverrideCursor()
        self.assertEqual(restored, [Qt.CursorShape.WaitCursor] * 2)

    def test_abort_before_the_main_window(self) -> None:
        "During the login there is no main window"
        del session['mainwin']
        self.assertTrue(self.show(press(QDialogButtonBox.StandardButton.Abort)))
        self.quit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
