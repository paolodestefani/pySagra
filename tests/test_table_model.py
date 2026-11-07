"""TableModel.submitAll: optimistic concurrency and the generated SQL, without a database

Run from the project root with: python -m unittest discover tests
"""

# standard library
import contextlib
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# PySide6
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QApplication

# application modules
from App.Database.AbstractModels import TableModel as T
from App.Database.Exceptions import PyAppDBConcurrencyError


app = QApplication.instance() or QApplication([])


class FakeCursor:
    "Record every statement; UPDATE/DELETE affect `rowcount` rows"

    def __init__(self, rowcount: int) -> None:
        self.rowcount = rowcount
        self.statements: list[tuple[str, dict]] = []
        self._result = None

    def execute(self, script: str, args=None) -> None:
        self.statements.append((script, args))
        self._result = None
        if script.startswith('UPDATE') and self.rowcount:
            self._result = (args['code'],)
            # an AFTER trigger rewrites the row: one more version and a changed value
            self._row = (args['code'], args['description'] + ' by trigger', args['object_version'] + 2)
        elif script.startswith('SELECT'):
            self._result = self._row

    def fetchone(self):
        return self._result


class Model(T.TableModel):

    def __init__(self) -> None:
        super().__init__()
        self.table = 'test'
        self.primaryKey = ('code',)
        self.columns = (('code', 'Code', False, 'str'), ('description', 'Description', False, 'str'))
        self.dataSet = [T.Record({0: 'A', 1: 'first'}, {'code': 'A'}, 3)]


class SubmitAllTest(unittest.TestCase):

    def submit(self, model: Model, rowcount: int) -> FakeCursor:
        cursor = FakeCursor(rowcount)
        conn = mock.Mock()
        conn.transaction.return_value = contextlib.nullcontext()
        conn.cursor.return_value = contextlib.nullcontext(cursor)
        with mock.patch.object(T, 'appconn', conn):
            model.submitAll()
        return cursor

    def test_update_checks_the_version_in_the_same_statement(self) -> None:
        model = Model()
        model.setData(model.index(0, 1), 'changed')
        cursor = self.submit(model, 1)
        script, args = cursor.statements[0]
        self.assertIn('SET description = %(description)s WHERE code = %(code)s AND object_version = %(object_version)s',
                      script)
        self.assertEqual(args, {'description': 'changed', 'code': 'A', 'object_version': 3})
        self.assertFalse(model.dataSet[0].is_modified)

    def test_saved_rows_are_read_back(self) -> None:
        "What triggers write, AFTER ones included, reaches the model"
        model = Model()
        model.setData(model.index(0, 1), 'changed')
        cursor = self.submit(model, 1)
        self.assertEqual(cursor.statements[1],
                         ('SELECT code, description, object_version FROM test WHERE code = %(code)s;', {'code': 'A'}))
        self.assertEqual(model.dataSet[0][1], 'changed by trigger')
        self.assertEqual(model.dataSet[0].object_version, 5)

    def test_stale_update_is_refused(self) -> None:
        model = Model()
        model.setData(model.index(0, 1), 'changed')
        with self.assertRaises(PyAppDBConcurrencyError):
            self.submit(model, 0)
        self.assertTrue(model.dataSet[0].is_modified)

    def test_delete_checks_the_version(self) -> None:
        model = Model()
        model.removeRows(0, 1)
        cursor = self.submit(model, 1)
        self.assertEqual(cursor.statements,
                         [('DELETE FROM test WHERE code = %(code)s AND object_version = %(object_version)s;',
                           {'code': 'A', 'object_version': 3})])

    def test_stale_delete_is_refused(self) -> None:
        model = Model()
        model.removeRows(0, 1)
        with self.assertRaises(PyAppDBConcurrencyError):
            self.submit(model, 0)
        self.assertEqual(len(model.toDelete), 1)

    def test_identity_realigned_only_after_a_delete(self) -> None:
        model = Model()
        model.automaticPKey = True
        model.setData(model.index(0, 1), 'changed')
        self.assertFalse(any('setval' in script for script, _ in self.submit(model, 1).statements))
        model.removeRows(0, 1)
        self.assertTrue(any('setval' in script for script, _ in self.submit(model, 1).statements))


class ClearDataTest(unittest.TestCase):

    def test_views_follow_clear_and_new_row(self) -> None:
        "Form.new() calls clearData() and then insertRow(0)"
        model = Model()
        model.dataSet.append(T.Record({0: 'B', 1: 'second'}, {'code': 'B'}, 1))
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(model)
        self.assertEqual(proxy.rowCount(), 2)
        model.clearData()
        self.assertEqual(proxy.rowCount(), 0)
        model.insertRow(0)
        self.assertEqual(proxy.rowCount(), 1)
        self.assertIsNone(proxy.index(0, 0).data())


if __name__ == '__main__':
    unittest.main()
