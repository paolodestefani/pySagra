"""ESC/POS report engine: definition, generation and rendering

Run from the project root with: python -m unittest discover tests
"""

# standard library
import io
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

# other
from PIL import Image as PILImage
from PySide6.QtCore import QByteArray, QLocale
from PySide6.QtWidgets import QApplication

# application modules
from App import session
from App.Report import ReportEngineEscPos as E


app = QApplication.instance() or QApplication([])
SETTINGS = {'quantity_decimal_places': 2, 'price_decimal_places': 2,
            'amount_decimal_places': 2, 'currency_symbol': '€'}


def xml(body: str, columns: tuple = ('name', 'qty'), extra: str = '') -> str:
    "A report definition with the given bands"
    fields = ''.join(f'<field_name>{c}</field_name>' for c in columns)
    return (f'<report version="1.0" print_method="ESC/POS">'
            f'<options><printer_profile type="str">TM-T20II</printer_profile></options>'
            f'{extra}<columns>{fields}</columns>{body}</report>')


ROW = '<details><band><row><field width="20">name</field><field width="6" align="right">qty</field></row></band></details>'


class EngineTestCase(unittest.TestCase):

    def setUp(self) -> None:
        for target, name, value in ((E, 'Settings', lambda: SETTINGS),):
            patcher = mock.patch.object(target, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.dict(session, {'qlocale': QLocale('it'), 'company_description': 'Company',
                                            'event_description': 'Event'})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_report(self, definition: str, data: list) -> E.ReportEscpos:
        report = E.ReportEscpos(definition)
        report.data = data
        report.generate()
        return report

    @staticmethod
    def text(report: E.ReportEscpos) -> str:
        return ''.join(op[1] for op in report.buffer.ops if op[0] == 'text')


class DefinitionTest(EngineTestCase):

    def test_details_are_optional(self) -> None:
        "The cover copy prints its header only"
        report = self.run_report(xml('<header><band><row><label width="10">Cover</label></row></band></header>'),
                                 [('a', 1)])
        self.assertIn('Cover', self.text(report))


class TextStyleTest(EngineTestCase):
    "Bytes sent to the printer, the preview does not show a missing reset"

    def output(self, *labels: str) -> bytes:
        rows = ''.join(f'<row>{label}</row>' for label in labels)
        return self.run_report(xml(f'<details><band>{rows}</band></details>'), [('a', 1)]).buffer.output

    def printer_state(self, output: bytes) -> dict:
        "Style of the printer at the first character of each word, following the commands"
        size = font = bold = underline = 0
        states, i = {}, 0
        while i < len(output):
            match output[i:i + 2]:
                case b'\x1b!':     # print mode: font, bold, size and underline together
                    n = output[i + 2]
                    font, bold, size, underline = n & 1, bool(n & 8), n & 0x30, bool(n & 0x80)
                    i += 3
                case b'\x1bE':
                    bold = bool(output[i + 2]); i += 3
                case b'\x1b-':
                    underline = bool(output[i + 2]); i += 3
                case b'\x1bM':
                    font = output[i + 2]; i += 3
                case c if c[:1] in (b'\x1b', b'\x1d'):
                    i += 3
                case _:
                    if output[i:i + 1].isalpha() and not output[i - 1:i].isalpha():
                        word = output[i:].split()[0].decode()
                        states[word] = (size, font, bool(bold), bool(underline))
                        i += len(word)
                    else:
                        i += 1
        return states

    def test_size_goes_back_to_normal(self) -> None:
        for size, code in (('double_width', 0x20), ('double_height', 0x10)):
            with self.subTest(size=size):
                states = self.printer_state(self.output(f'<label width="10" {size}="true">BIG</label>',
                                                        '<label width="10">small</label>'))
                self.assertEqual(states, {'BIG': (code, 0, False, False), 'small': (0, 0, False, False)})

    def test_both_sizes_together_and_one_after_the_other(self) -> None:
        states = self.printer_state(self.output(
            '<label width="10" double_width="true" double_height="true">BOTH</label>',
            '<label width="10" double_height="true">HIGH</label>',
            '<label width="10" double_width="true">WIDE</label>'))
        self.assertEqual([s[0] for s in states.values()], [0x30, 0x10, 0x20])

    def test_size_change_keeps_font_bold_and_underline(self) -> None:
        style = 'width="10" font="b" bold="true" underline="1"'
        states = self.printer_state(self.output(f'<label {style}>one</label>',
                                                f'<label {style} double_height="true">two</label>',
                                                f'<label {style}>three</label>'))
        self.assertEqual(states, {'one': (0, 1, True, True), 'two': (0x10, 1, True, True),
                                  'three': (0, 1, True, True)})


class OmittedFieldTest(EngineTestCase):

    def test_columns_stay_in_place(self) -> None:
        "Empty, invisible and suppressed fields keep their width, on wrapped lines too"
        for attribute, value in (('', None), (' is_visible="false"', 'x')):
            with self.subTest(attribute=attribute):
                report = self.run_report(xml('<details><band><row><field width="10">a</field>'
                                             f'<field width="10"{attribute}>b</field>'
                                             '<field width="10">c</field></row></band></details>', ('a', 'b', 'c')),
                                         [('one two three', value, 'four five six')])
                self.assertEqual(self.text(report).split('\n')[:2],
                                 ['one two' + ' ' * 13 + 'four five ', 'three' + ' ' * 15 + 'six       '])


class GenerationTest(EngineTestCase):

    def test_sort_reverse_false_is_ascending(self) -> None:
        report = self.run_report(xml(ROW, extra='<sorting><sort field="name" reverse="false"/></sorting>'),
                                 [('b', 1), ('a', 2), ('c', 3)])
        names = [line.split()[0] for line in self.text(report).split('\n') if line.strip()]
        self.assertEqual(names, ['a', 'b', 'c'])

    def test_sort_reverse_true_is_descending(self) -> None:
        report = self.run_report(xml(ROW, extra='<sorting><sort field="name" reverse="true"/></sorting>'),
                                 [('b', 1), ('a', 2), ('c', 3)])
        names = [line.split()[0] for line in self.text(report).split('\n') if line.strip()]
        self.assertEqual(names, ['c', 'b', 'a'])

    def test_summary_in_the_report_footer(self) -> None:
        footer = '<footer><band><row><summary width="10" function="sum">qty</summary></row></band></footer>'
        report = self.run_report(xml(ROW + footer), [('a', 2), ('b', 3)])
        self.assertIn('5', self.text(report).split('\n')[-2])

    def test_summary_skips_null_values(self) -> None:
        footer = '<footer><band><row><summary width="10" function="sum">qty</summary></row></band></footer>'
        report = self.run_report(xml(ROW + footer), [('a', 2), ('b', None), ('c', 3)])
        self.assertIn('5', self.text(report).split('\n')[-2])

    def test_script_after_only(self) -> None:
        band = ('<details><band><row><field width="20">name</field></row>'
                '<execute trigger="after">record["seen"] = True</execute></band></details>')
        self.run_report(xml(band), [('a', 1)])


class BlockTest(EngineTestCase):

    def test_code128_barcode_from_an_int_field(self) -> None:
        band = '<details><band><barcode type="field" barcode_type="CODE128">qty</barcode></band></details>'
        report = self.run_report(xml(band), [('a', 12345)])
        self.assertIn(('barcode', '{B12345'), [op[:2] for op in report.buffer.ops])

    def test_qrcode_from_an_int_field(self) -> None:
        band = '<details><band><qrcode type="field">qty</qrcode></band></details>'
        report = self.run_report(xml(band), [('a', 12345)])
        self.assertIn(('qr', '12345'), [op[:2] for op in report.buffer.ops])

    def test_image_from_a_field(self) -> None:
        png = io.BytesIO()
        PILImage.new('RGBA', (40, 20), (255, 0, 0, 0)).save(png, 'PNG')
        band = '<details><band><image type="field">qty</image></band></details>'
        report = self.run_report(xml(band), [('a', QByteArray(png.getvalue()))])
        images = [op for op in report.buffer.ops if op[0] == 'image']
        self.assertEqual(len(images), 1)
        self.assertIsNotNone(images[0][1])
        self.assertEqual(images[0][1].getpixel((0, 0)), (255, 255, 255))  # transparency became white

    def test_fragment_height_from_the_definition(self) -> None:
        band = '<details><band><image type="field" fragment_height="480">qty</image></band></details>'
        report = E.ReportEscpos(xml(band))
        self.assertEqual(report.details[0][0].fragment_height, 480)


class RealReportTest(EngineTestCase):

    def test_sales_summary_group_totals(self) -> None:
        "The shipped report 63 with two days of one event"
        with zipfile.ZipFile(ROOT / 'Report' / '63_escpos_sales_summary_en_US.rpt.zip') as archive:
            definition = archive.read('xml').decode()
        report = E.ReportEscpos(definition)
        columns = len(report.column)
        day = [1, 'Sagra', None, None, None] + [Decimal('10.00')] * (columns - 5)
        report.data = [tuple(day), tuple(day)]
        report.generate()
        self.assertIn('20,00', self.text(report))


if __name__ == '__main__':
    unittest.main()
