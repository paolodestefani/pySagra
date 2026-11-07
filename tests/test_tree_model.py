"""TreeModel: editing rules and the statements of submitAll, without a database

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
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

# application modules
from App.Database.AbstractModels import TreeModel as T
from App.Database.Exceptions import PyAppDBConcurrencyError
from App.Database.Models import MenuItemTreeModel


app = QApplication.instance() or QApplication([])


class FakeCursor:
    "Record the statements; `referenced` are the child codes still used by some row"

    def __init__(self, rowcount: int = 1, referenced: tuple = ()) -> None:
        self.rowcount = rowcount
        self.referenced = referenced
        self.statements: list[tuple[str, object]] = []
        self._rows: list = []

    def execute(self, script: str, args=None) -> None:
        self.statements.append((script, args))
        self._rows = []
        if script.startswith('SELECT 1'):
            self._rows = [(1,)] if args[0] in self.referenced else []

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def fetchall(self):
        return self._rows


def menu() -> MenuItemTreeModel:
    "m_en > ffi > fficdk, as read from the database"
    model = MenuItemTreeModel()
    model.rootItem = T.TreeItem({i: None for i in range(len(model.columns))})
    model.rootItem.itemData[1] = 'm_en'
    for parent, code in ((model.rootItem, 'ffi'), (None, 'fficdk')):
        parent = parent or model.rootItem.childItems[0]
        node = T.TreeItem({i: None for i in range(len(model.columns))}, parent)
        node.itemData.update({0: parent.data(1), 1: code, 3: 1, 4: 'A'})
        node.pkey = {'parent': parent.data(1), 'child': code}
        node.objectVersion = 7
        node.state = T.stt.SYNC
        parent.appendChild(node)
    return model


class TreeModelTest(unittest.TestCase):

    def submit(self, model, cursor: FakeCursor, value='m_en') -> FakeCursor:
        conn = mock.Mock()
        conn.transaction.return_value = contextlib.nullcontext()
        conn.cursor.return_value = contextlib.nullcontext(cursor)
        with mock.patch.object(T, 'appconn', conn), mock.patch.object(model, 'filter'):
            model.submitAll(0, value)
        return cursor

    def test_editable_columns(self) -> None:
        model = menu()
        ffi = model.index(0, 0)
        editable = lambda index: bool(model.flags(index) & Qt.ItemFlag.ItemIsEditable)
        self.assertFalse(editable(model.index(0, 0)))      # parent: follows the tree
        self.assertFalse(editable(model.index(0, 1)))      # child of a saved row: part of the key
        self.assertTrue(editable(model.index(0, 2)))
        model.insertRow(0, ffi)
        self.assertTrue(editable(model.index(0, 1, ffi)))
        self.assertEqual(model.index(0, 0, ffi).data(), 'ffi')

    def test_update_and_insert_under_the_tree(self) -> None:
        model = menu()
        ffi = model.index(0, 0)
        model.setData(model.index(0, 2, ffi), 'Cash desks')
        model.insertRow(1, ffi)
        model.setData(model.index(1, 1, ffi), 'ffinew')
        statements = self.submit(model, FakeCursor()).statements
        self.assertTrue(statements[0][0].startswith('UPDATE system.menu_toolbar_item SET description = %(description)s'))
        self.assertIn('WHERE parent = %(parent)s AND child = %(child)s AND object_version = %(object_version)s',
                      statements[0][0])
        self.assertEqual(statements[0][1]['object_version'], 7)
        self.assertTrue(statements[1][0].startswith('INSERT INTO system.menu_toolbar_item (parent, child'))
        self.assertEqual((statements[1][1]['parent'], statements[1][1]['child']), ('ffi', 'ffinew'))

    def test_stale_update_is_refused(self) -> None:
        model = menu()
        model.setData(model.index(0, 2), 'File')
        with self.assertRaises(PyAppDBConcurrencyError):
            self.submit(model, FakeCursor(rowcount=0))

    def test_shared_submenu_keeps_its_items(self) -> None:
        model = menu()
        model.removeRow(0)
        statements = self.submit(model, FakeCursor(referenced=('ffi',))).statements
        self.assertEqual([s.split()[0] for s, _ in statements], ['DELETE', 'SELECT'])

    def test_unused_submenu_loses_its_items(self) -> None:
        model = menu()
        model.removeRow(0)
        statements = self.submit(model, FakeCursor()).statements
        self.assertEqual(statements[2], ('DELETE FROM system.menu_toolbar_item WHERE parent = %s RETURNING child;', ('ffi',)))

    def test_new_rows_are_not_deleted(self) -> None:
        model = menu()
        model.insertRow(0)
        model.removeRow(0)
        self.assertEqual(model.toDelete, [])

    def test_read_only_tree(self) -> None:
        "A system menu: no editable cell, no insert, no remove"
        model = menu()
        model.isEditable = False
        self.assertFalse(model.flags(model.index(0, 2)) & Qt.ItemFlag.ItemIsEditable)
        self.assertFalse(model.insertRow(0))
        self.assertFalse(model.removeRow(0))
        self.assertEqual(model.rowCount(), 1)


if __name__ == '__main__':
    unittest.main()
