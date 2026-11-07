"""Receipt preview of the ESC/POS reports

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# other
from escpos.printer import Dummy
from PIL import Image
from PySide6.QtGui import QPdfWriter
from PySide6.QtWidgets import QApplication

# application modules
from App.Report.EscposPreview import BarcodeLine, BoxLine, CutLine, ImageLine, QrLine, ReceiptPreview, TextLine


app = QApplication.instance() or QApplication([])
STYLE = {'font': 'a', 'wm': 1, 'hm': 1, 'invert': False, 'bold': False, 'underline': 0, 'align': 'left'}


def style(**changes) -> dict:
    return STYLE | changes


def preview(ops: list) -> ReceiptPreview:
    device = Dummy()
    device.ops = ops
    return ReceiptPreview(device)


def render(receipt: ReceiptPreview) -> int:
    "Paint on a PDF with the receipt layout, return the number of pages"
    path = os.path.join(tempfile.mkdtemp(), 'receipt.pdf')
    writer = QPdfWriter(path)
    writer.setPageLayout(receipt.page_layout())
    writer.setResolution(203)
    pages = []
    original = writer.newPage
    writer.newPage = lambda: pages.append(1) or original()
    receipt.paint(writer)
    del writer
    assert os.path.getsize(path) > 0
    return len(pages) + 1


class BuildTest(unittest.TestCase):

    def test_text_lines(self) -> None:
        lines = preview([('text', 'one\ntwo\n', STYLE)]).lines
        self.assertEqual([''.join(c[0] for c in l.chars) for l in lines], ['one', 'two'])

    def test_long_text_wraps_at_the_paper_width(self) -> None:
        receipt = preview([('text', 'x' * 100, STYLE)])
        columns = receipt.m.cols['a']   # from the printer profile
        self.assertEqual([len(l.chars) for l in receipt.lines], [columns, columns, 100 - 2 * columns])

    def test_double_width_text_wraps_earlier(self) -> None:
        receipt = preview([('text', 'x' * 30, style(wm=2))])
        half = receipt.m.cols['a'] // 2
        self.assertEqual([len(l.chars) for l in receipt.lines], [half, 30 - half])

    def test_feed_and_cut(self) -> None:
        receipt = preview([('text', 'a', STYLE), ('feed', 2), ('cut',)])
        self.assertEqual([type(l) for l in receipt.lines], [TextLine, TextLine, TextLine, CutLine])

    def test_codes(self) -> None:
        receipt = preview([('barcode', '{B12345', 'CODE128', 64, 3, 'BELOW'),
                           ('barcode', 'not a number', 'EAN13', 64, 3, 'BELOW'),
                           ('barcode', '123', 'UNKNOWN', 64, 3, 'BELOW'),
                           ('qr', 'https://example.com', 0, 6)])
        self.assertEqual([type(l) for l in receipt.lines], [BarcodeLine, BoxLine, BoxLine, QrLine])
        self.assertEqual(receipt.lines[0].text, '12345')  # the escpos subset prefix is removed

    def test_images(self) -> None:
        wide = Image.new('RGBA', (1200, 100), (255, 0, 0, 128))
        receipt = preview([('image', wide, True), ('image', None, False)])
        image, icon = receipt.lines
        self.assertEqual((image.dw, image.dh), (576, 48))  # scaled to the paper width
        self.assertIsNone(icon.qimage)


class PaintTest(unittest.TestCase):

    def test_everything_paints(self) -> None:
        ops = [('text', 'Title\n', style(align='center', bold=True, wm=2, hm=2)),
               ('text', 'inverted\n', style(invert=True, underline=1)),
               ('text', 'small font\n', style(font='b', align='right')),
               ('barcode', '{B12345', 'CODE128', 64, 3, 'BOTH'),
               ('qr', 'text', 1, 6),
               ('image', Image.new('L', (200, 80), 0), False),
               ('image', None, False),
               ('cut',)]
        self.assertEqual(render(preview(ops)), 1)

    def test_one_page_for_each_receipt(self) -> None:
        ops = [('text', 'first\n', STYLE), ('cut',), ('text', 'second\n', STYLE), ('cut',)]
        self.assertEqual(render(preview(ops)), 2)

    def test_empty_receipt(self) -> None:
        self.assertEqual(render(preview([])), 1)

    def test_very_long_receipt_breaks_into_pages(self) -> None:
        receipt = preview([('text', 'row\n' * 400, STYLE)])
        self.assertEqual(len(receipt._pages(max_h=1000)), 13)


if __name__ == '__main__':
    unittest.main()
