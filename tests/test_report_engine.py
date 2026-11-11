"""Report engines: number format; driver engine sorting and summaries on the shipped definitions

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
from App.Report import ReportEngineEscPos as E


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


class FormatNumberTest(unittest.TestCase):

    CASES = ((Decimal('1234.5'), 2, '1.234,50'),
             (Decimal('2.675'), 2, '2,68'),         # half up, as for money
             (2.675, 2, '2,68'),                    # the float 2.67499... is not rounded down
             (Decimal('-1234.005'), 2, '-1.234,01'),
             (0.1 + 0.2, 2, '0,30'),
             (1234567, 0, '1.234.567'),
             (Decimal('12.5'), 0, '13'),
             (3, 3, '3,000'),
             (None, 2, '0,00'))

    def test_both_engines(self) -> None:
        for engine in (R, E):
            for value, decimals, expected in self.CASES:
                with self.subTest(engine=engine.__name__, value=value, decimals=decimals):
                    self.assertEqual(engine.format_number(value, decimals, '.', ','), expected)

    def test_english_separators(self) -> None:
        self.assertEqual(R.format_number(Decimal('1234567.891'), 2, ',', '.'), '1,234,567.89')


class BarcodeTest(unittest.TestCase):
    "Driver reports draw barcodes as bars from python-barcode, no barcode font"

    def test_code128_modules(self) -> None:
        "Start code B, then the stop pattern 1100011101011 at the end"
        modules = R.barcode_modules('Code128', 'PS001000000123')
        self.assertTrue(modules.startswith('11010010000'))
        self.assertTrue(modules.endswith('1100011101011'))
        self.assertEqual(set(modules), {'0', '1'})

    def test_code39_has_no_check_character(self) -> None:
        "Like the old font encoding: start, the text, stop"
        self.assertEqual(len(R.barcode_modules('Code39', 'ORD-15')), (len('ORD-15') + 2) * 16 - 1)

    def test_invalid_characters(self) -> None:
        with self.assertRaises(R.ReportException):
            R.barcode_modules('Code39', 'A#B')

    def test_qrcode_square_in_the_field(self) -> None:
        "A QR code field paints the matrix as the largest square that fits, centered"
        from PySide6.QtCore import Qt, QRectF
        from PySide6.QtGui import QImage, QPainter
        renderer = R.BaseRenderer.__new__(R.BaseRenderer)
        renderer.barcode, renderer.value, renderer.color = 'QRCode', 'PS001000000123', '???'
        self.assertTrue(renderer.isBarcode())
        image = QImage(200, 100, QImage.Format.Format_RGB32)
        image.fill(Qt.GlobalColor.white)
        painter = QPainter(image)
        renderer.renderBarcode(painter, QRectF(0, 0, 200, 100))
        painter.end()
        dark = lambda x, y: image.pixelColor(x, y).lightness() < 128
        # finder patterns: dark top left corner of the 100x100 square at x 50
        self.assertTrue(dark(51, 1) and dark(148, 1) and dark(51, 98))
        self.assertFalse(any(dark(x, 50) for x in range(0, 49)))


if __name__ == '__main__':
    unittest.main()
