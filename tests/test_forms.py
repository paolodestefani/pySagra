"""Saving and deleting in the form managers

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
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QAbstractItemView, QApplication, QLineEdit, QTableView, QWidget

# application modules
from App import session
from App.Common import ExceptionHandler
from App.Widget import Form
from App.Database import SYSFIELD


app = QApplication.instance() or QApplication([])


class Model(QStandardItemModel):
    "An editable model that records what submitAll saves"

    userDataChanged = Signal()

    def __init__(self, values: list[str]) -> None:
        super().__init__(len(values), 1)
        for row, value in enumerate(values):
            self.setItem(row, 0, QStandardItem(value))
        self.isEditable = True
        self.saved: list[list[str]] = []
        self.fail: Exception | None = None

    def submitAll(self, *args) -> bool:
        if self.fail:
            raise self.fail
        self.saved.append([self.item(r, 0).text() for r in range(self.rowCount())])
        return True

    def revertAll(self) -> None:
        pass


class FormTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.mainwin = mock.Mock()
        patcher = mock.patch.dict(session, {'mainwin': self.mainwin})
        patcher.start()
        self.addCleanup(patcher.stop)
        for name in ('MessageBoxCritical',):
            patcher = mock.patch.object(ExceptionHandler, name)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(ExceptionHandler, 'appconn')
        patcher.start()
        self.addCleanup(patcher.stop)


class ViewForm(Form.FormViewManager):

    def __init__(self, model: Model) -> None:
        super().__init__(None, (True, True, True))
        self.availableStatus = (True,) * 12
        self.setModel(model)
        self.view = QTableView(self)
        self.setView(self.view)
        self.view.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)


class FormViewManagerTest(FormTestCase):

    def form(self, values: list[str]) -> tuple[ViewForm, Model]:
        model = Model(values)
        with mock.patch.object(Form, 'SortFilterDialog'):
            form = ViewForm(model)
        form.show()
        QTest.qWaitForWindowExposed(form)
        return form, model

    def test_save_includes_the_cell_being_edited(self) -> None:
        "The toolbar button does not take the focus: the editor is still open"
        form, model = self.form(['old'])
        index = model.index(0, 0)
        form.view.setCurrentIndex(index)
        form.view.edit(index)
        QTest.qWait(20)
        editor = QApplication.focusWidget()
        self.assertIsInstance(editor, QLineEdit)
        editor.selectAll()
        QTest.keyClicks(editor, 'new')
        form.save()
        self.assertEqual(model.saved, [['new']])

    def test_delete_failure_without_selection(self) -> None:
        form, model = self.form(['a'])
        form.view.clearSelection()
        model.fail = ValueError('broken')
        form.delete()  # must not raise


class Relation(Model):
    def filter(self, *args) -> None:
        pass


class IndexForm(Form.FormIndexManager):

    def __init__(self, model: Model, relation: Relation) -> None:
        super().__init__(None, (True, True, True))
        self.ui = mock.Mock(spec=[])
        self.availableStatus = (True,) * 12
        self.model = model
        self.addDetailRelation(relation, 0, 0)
        self.reload = mock.Mock()


class FormIndexManagerTest(FormTestCase):

    def test_master_delete_failure_keeps_the_details(self) -> None:
        "Details and master are deleted in one transaction"
        model, relation = Model(['master']), Relation(['d1', 'd2'])
        model.fail = ValueError('foreign key')
        form = IndexForm(model, relation)
        calls = []
        transaction = mock.MagicMock()
        transaction.__enter__.side_effect = lambda: calls.append('begin')
        transaction.__exit__.side_effect = lambda *exc: calls.append(f'end {exc[0].__name__ if exc[0] else "ok"}')
        relation.submitAll = mock.Mock(side_effect=lambda *a: calls.append('details'))
        with mock.patch.object(Form, 'appconn') as appconn:
            appconn.transaction.return_value = transaction
            form.delete()
        self.assertEqual(calls, ['begin', 'details', 'end ValueError'])
        form.reload.assert_called()

    def test_failed_delete_stays_on_the_record(self) -> None:
        "reload finds the record again, moving to the previous one is for a successful delete"
        model = Model(['master'])
        model.fail = ValueError('foreign key')
        form = IndexForm(model, Relation([]))
        form.indexMapper = mock.Mock()
        with mock.patch.object(Form, 'appconn'):
            form.delete()
        form.reload.assert_called_once()
        form.indexMapper.setCurrentIndex.assert_not_called()
        form.indexMapper.toFirst.assert_not_called()

    def test_successful_delete_moves_to_the_previous_record(self) -> None:
        model = Model(['master'])
        form = IndexForm(model, Relation([]))
        form.indexMapper = mock.Mock()
        form.indexMapper.currentIndex.return_value = 2
        form.indexModel = mock.Mock()
        form.indexModel.rowCount.return_value = 5
        with mock.patch.object(Form, 'appconn'):
            form.delete()
        form.indexMapper.setCurrentIndex.assert_called_once_with(1)

    def test_new_needs_write_permission(self) -> None:
        model = Model(['master'])
        form = IndexForm(model, Relation([]))
        form.write_perm = False
        form.new()
        self.assertEqual(form.state, Form.ev.VIEW)


class FormManagerTest(FormTestCase):

    def test_master_delete_failure_keeps_the_details(self) -> None:
        model, relation = Model(['master']), Relation(['d1'])
        model.fail = ValueError('foreign key')
        with mock.patch.object(Form, 'SortFilterDialog'):
            form = Form.FormManager(None, (True, True, True))
            form.ui = mock.Mock(spec=[])
            form.setModel(model)
        form.addDetailRelation(relation, 0, 0)
        form.mapper.setCurrentIndex(0)
        form.reload = mock.Mock()
        calls = []
        transaction = mock.MagicMock()
        transaction.__enter__.side_effect = lambda: calls.append('begin')
        transaction.__exit__.side_effect = lambda *exc: calls.append(f'end {exc[0].__name__ if exc[0] else "ok"}')
        relation.submitAll = mock.Mock(side_effect=lambda *a: calls.append('details'))
        with mock.patch.object(Form, 'appconn') as appconn:
            appconn.transaction.return_value = transaction
            form.delete()
        self.assertEqual(calls, ['begin', 'details', 'end ValueError'])
        form.reload.assert_called()


class RecordProtectionTest(FormTestCase):
    "System records: the user's right and the record protection are separate"

    def status(self, write: bool = True, readOnly: bool = False, undeletable: bool = False,
               editing: bool = False) -> list[bool]:
        "New and Delete as shown while viewing, Save while editing"
        model = Model(['a'])
        with mock.patch.object(Form, 'SortFilterDialog'):
            form = ViewForm(model)
        form.write_perm = write
        if editing:
            form.state = Form.ev.EDIT
        form.recordReadOnly, form.recordUndeletable = readOnly, undeletable
        form.updateEditStatus()
        status = self.mainwin.updateEditStatus.call_args.args[0]
        return [status[Form.es.NEW], status[Form.es.SAVE], status[Form.es.DELETE]]

    def test_system_record_still_allows_new(self) -> None:
        "One system company only: New must stay available"
        self.assertEqual(self.status(readOnly=True), [True, False, False])
        self.assertFalse(self.status(readOnly=True, editing=True)[1])

    def test_undeletable_record_can_be_saved(self) -> None:
        self.assertEqual(self.status(undeletable=True), [True, False, False])
        self.assertTrue(self.status(undeletable=True, editing=True)[1])
        self.assertTrue(self.status()[2])

    def test_read_only_user(self) -> None:
        self.assertEqual(self.status(write=False), [False, False, False])

    def system_form(self, system: bool, policy: str | None = 'readonly') -> ViewForm:
        "A model with the SYSFIELD column, its only row selected"
        model = Model(['a'])
        model.setColumnCount(2)
        model.setData(model.index(0, 1), system, Qt.ItemDataRole.EditRole)
        model.columns = (('code', 'Code', False, 'str'), (SYSFIELD, 'System', True, 'bool'))
        with mock.patch.object(Form, 'SortFilterDialog'):
            form = ViewForm(model)
        form.systemRecords = policy
        form.view.selectRow(0)
        return form

    def test_system_flag_is_read_from_the_model(self) -> None:
        "No code in the form: the SYSFIELD column protects the record"
        self.assertTrue(self.system_form(True).isSystemRecord())
        self.assertEqual((self.system_form(True).canSave(), self.system_form(True).canDelete()), (False, False))
        self.assertEqual((self.system_form(False).canSave(), self.system_form(False).canDelete()), (True, True))

    def test_system_policies(self) -> None:
        form = self.system_form(True, 'undeletable')
        self.assertEqual((form.canSave(), form.canDelete()), (True, False))
        form = self.system_form(True, None)
        self.assertEqual((form.canSave(), form.canDelete()), (True, True))

    def test_model_without_system_column(self) -> None:
        model = Model(['a'])
        with mock.patch.object(Form, 'SortFilterDialog'):
            form = ViewForm(model)
        self.assertFalse(form.isSystemRecord())

    def test_delete_refused_on_protected_record(self) -> None:
        model = Model(['a'])
        with mock.patch.object(Form, 'SortFilterDialog'):
            form = ViewForm(model)
        form.recordUndeletable = True
        with mock.patch.object(model, 'removeRows') as remove:
            form.delete()
        remove.assert_not_called()


if __name__ == '__main__':
    unittest.main()
