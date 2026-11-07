"""Record.update_record / delete_record: optimistic concurrency, without a database

Run from the project root with: python -m unittest discover tests
"""

# standard library
import contextlib
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# application modules
from App.Database import Utility as U
from App.Database.Exceptions import PyAppDBConcurrencyError


class FakeCursor:
    "UPDATE ... RETURNING returns `row`, DELETE affects `rowcount` rows"

    def __init__(self, row=None, rowcount: int = 1) -> None:
        self.row, self.rowcount = row, rowcount
        self.statements: list = []

    def execute(self, script: str, args=None) -> None:
        self.statements.append((script, dict(args)))

    def fetchone(self):
        return self.row


class RecordTest(unittest.TestCase):

    def run_with(self, cursor: FakeCursor, action) -> FakeCursor:
        conn = mock.Mock()
        conn.transaction.return_value = contextlib.nullcontext()
        conn.cursor.return_value = contextlib.nullcontext(cursor)
        with mock.patch.object(U, 'appconn', conn):
            action()
        return cursor

    def record(self) -> U.Record:
        r = U.Record('company.settings', ('company_id',))
        r.update(company_id=10, covers=2, object_version=4)
        return r

    def test_update_checks_the_version_in_the_same_statement(self) -> None:
        r = self.record()
        cursor = self.run_with(FakeCursor(row={'company_id': 10, 'covers': 2, 'object_version': 5}), r.update_record)
        script, args = cursor.statements[0]
        self.assertIn('SET covers = %(covers)s\nWHERE company_id = %(company_id)s AND object_version = %(object_version)s',
                      script)
        self.assertEqual(r['object_version'], 5)

    def test_stale_update_is_refused(self) -> None:
        "The old check only tested that the row existed, a changed version passed"
        with self.assertRaises(PyAppDBConcurrencyError):
            self.run_with(FakeCursor(row=None), self.record().update_record)

    def test_delete(self) -> None:
        cursor = self.run_with(FakeCursor(rowcount=1), self.record().delete_record)
        self.assertEqual(cursor.statements[0][0],
                         'DELETE FROM company.settings\nWHERE company_id = %(company_id)s AND object_version = %(object_version)s;')
        with self.assertRaises(PyAppDBConcurrencyError):
            self.run_with(FakeCursor(rowcount=0), self.record().delete_record)

    def test_without_version_key_only(self) -> None:
        r = U.Record('company.rec', ('id',))
        r['id'] = 1
        cursor = self.run_with(FakeCursor(rowcount=1), r.delete_record)
        self.assertEqual(cursor.statements[0][0], 'DELETE FROM company.rec\nWHERE id = %(id)s;')


if __name__ == '__main__':
    unittest.main()
