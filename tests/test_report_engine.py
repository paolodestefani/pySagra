"""Driver report engine: sorting and summaries, on the shipped report definitions

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import unittest
import zipfile
from decimal import Decimal
from pathlib import Path
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# PySide6
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication

# application modules
from App import session
from App.Report import ReportEngine as R


app = QApplication.instance() or QApplication([])
SETTINGS = {'quantity_decimal_places': 2, 'price_decimal_places': 2,
            'amount_decimal_places': 2, 'currency_symbol': '€'}


def definition(name: str) -> str:
    with zipfile.ZipFile(ROOT / 'Report' / f'{name}.rpt.zip') as archive:
        return archive.read('xml').decode()


class EngineTestCase(unittest.TestCase):

    def setUp(self) -> None:
        patcher = mock.patch.object(R, 'Settings', lambda: SETTINGS)
        patcher.start()
        self.addCleanup(patcher.stop)
        patcher = mock.patch.dict(session, {'qlocale': QLocale('it'), 'company_description': 'Company',
                                            'event_description': 'Event', 'user': 'u', 'hostname': 'pc'})
        patcher.start()
        self.addCleanup(patcher.stop)


class SortingTest(EngineTestCase):

    def test_reverse_attribute(self) -> None:
        "reverse='False' was read as True"
        self.assertEqual({s.reverse for s in R.Report(definition('18_item_detail_it_IT')).sortings}, {False})
        self.assertEqual([s.reverse for s in R.Report(definition('13_event_en_US')).sortings], [True])
        self.assertEqual([s.reverse for s in R.Report(definition('47_statistic_sales_en_US')).sortings], [False])

    def test_item_detail_variants_in_ascending_order(self) -> None:
        report = R.Report(definition('18_item_detail_it_IT'))
        columns = list(report.column)
        rows = []
        for variant in ('Bianco', 'Rosso', 'Amabile'):
            row = {c: '' for c in columns}
            row.update(depsort=1, department='BAR', item_description='VINO', row_type='V',
                       variant_description=variant)
            rows.append(tuple(row[c] for c in columns))
        report.data = rows
        report.generate()
        position = report.column['variant_description']
        self.assertEqual([r[position] for r in report.data], ['Amabile', 'Bianco', 'Rosso'])


class SummaryTest(EngineTestCase):

    def test_null_values_are_skipped(self) -> None:
        report = R.Report(definition('45_sales_summary_en_US'))
        summary = next(s for s in report.summaries if s.function == 'sum')
        for value in (Decimal('2'), None, Decimal('3')):
            summary.update({summary.fieldName: value})
        self.assertEqual(summary.summary, Decimal('5'))
        self.assertEqual(summary.items, 2)


if __name__ == '__main__':
    unittest.main()
