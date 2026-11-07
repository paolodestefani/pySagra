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
from App.Widget import ExceptionHandler
from App.Widget import Form


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


if __name__ == '__main__':
    unittest.main()
