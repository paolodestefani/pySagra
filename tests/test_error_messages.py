"""Messages for the user on database errors, given by each form

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
from PySide6.QtWidgets import QApplication

# application modules
from App import session
from App.Database.Exceptions import PyAppDBError
from App.Common import ExceptionHandler
from App.Widget import Form


app = QApplication.instance() or QApplication([])
USED = PyAppDBError(code='23503', message='update or delete violates foreign key',
                    constraint='order_line_item_fk')


class GuiExceptionContextTest(unittest.TestCase):

    def setUp(self) -> None:
        self.dialogs = {}
        for name in ('appconn', 'MessageBoxCritical'):
            patcher = mock.patch.object(ExceptionHandler, name)
            self.dialogs[name] = patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(ExceptionHandler.QMessageBox, 'warning')
        self.dialogs['warning'] = patcher.start()
        self.addCleanup(patcher.stop)

    def run_context(self, error: Exception, messages: dict | None) -> None:
        with ExceptionHandler.gui_exception_context(None, 'Delete', messages):
            raise error

    def warned(self) -> str | None:
        warning = self.dialogs['warning']
        return warning.call_args.args[2] if warning.called else None

    def test_constraint_message(self) -> None:
        self.run_context(USED, {'order_line_item_fk': 'used in orders', '23503': 'used'})
        self.assertEqual(self.warned(), 'used in orders')
        self.dialogs['MessageBoxCritical'].assert_not_called()
        self.dialogs['appconn'].rollback.assert_called_once()

    def test_code_message(self) -> None:
        self.run_context(USED, {'23503': 'used'})
        self.assertEqual(self.warned(), 'used')

    def test_no_message_keeps_the_critical_dialog(self) -> None:
        for messages in (None, {}, {'23505': 'duplicate'}):
            with self.subTest(messages=messages):
                self.dialogs['warning'].reset_mock()
                self.dialogs['MessageBoxCritical'].reset_mock()
                self.run_context(USED, messages)
                self.assertIsNone(self.warned())
                self.dialogs['MessageBoxCritical'].assert_called_once()

    def test_errors_without_constraint(self) -> None:
        self.run_context(PyAppDBError(code='23503', message='x'), {'': 'empty key', '23503': 'used'})
        self.assertEqual(self.warned(), 'used')

    def test_old_positional_arguments(self) -> None:
        error = PyAppDBError('PA0002', 'not an application database')
        self.assertEqual((error.code, error.constraint), ('PA0002', ''))


class FormMessagesTest(unittest.TestCase):

    def test_form_delete_uses_its_messages(self) -> None:
        form = Form.FormIndexManager(None, (True, True, True))
        form.ui = mock.Mock(spec=[])
        form.model = mock.Mock(isEditable=True)
        form.model.submitAll.side_effect = USED
        form.reload = mock.Mock()
        form.errorMessages = {'23503': 'The item has been used, it can not be deleted'}
        with mock.patch.dict(session, {'mainwin': mock.Mock()}), \
             mock.patch.object(Form, 'appconn'), \
             mock.patch.object(ExceptionHandler, 'appconn'), \
             mock.patch.object(ExceptionHandler.QMessageBox, 'warning') as warning:
            form.delete()
        self.assertEqual(warning.call_args.args[2], 'The item has been used, it can not be deleted')
        form.reload.assert_called_once()


if __name__ == '__main__':
    unittest.main()
