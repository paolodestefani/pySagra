from __future__ import annotations
import re
from dataclasses import dataclass, field

import barcode as pybarcode
import qrcode
from qrcode import constants as qrc
from PySide6.QtCore import Qt, QRectF, QPointF, QMarginsF, QSizeF
from PySide6.QtGui import (QFont, QPainter, QPainterPath, QPolygonF, QColor, QPen,
                           QPageSize, QPageLayout)

FONT = "Courier New"              # works on every platform
DPI = 203
CELL_H = {'a': 24, 'b': 17}       # character cell height (points)
LINE_H = {'a': 30, 'b': 24}       # row height with line spacing
LAYOUT_SLACK = 60                 # extra margin at the top of the page
SPLIT_SLACK = 20                  # margin used when a page breaks

_BC_NAMES = {'UPC-A': 'upca', 'EAN13': 'ean13', 'EAN8': 'ean8', 'CODE39': 'code39',
             'ITF': 'itf', 'NW7': 'codabar', 'CODE128': 'code128'}
_QR_EC = {0: qrc.ERROR_CORRECT_L, 1: qrc.ERROR_CORRECT_M,
          2: qrc.ERROR_CORRECT_Q, 3: qrc.ERROR_CORRECT_H}


class Metrics:
    "Geometry derived from the printer profile, plus font cache"
    def __init__(self, dev):
        data = dev.profile.profile_data
        fonts = data.get('fonts', {})
        self.cols = {'a': fonts.get('0', {}).get('columns', 48),
                     'b': fonts.get('1', {}).get('columns', 64)}
        try:
            self.dots = int(data['media']['width']['pixels'])
        except (KeyError, TypeError, ValueError):
            self.dots = 576
        self.cell_w = {f: self.dots / c for f, c in self.cols.items()}
        self._fonts: dict = {}

    def font(self, face: str, bold: bool = False, pixel: int | None = None) -> QFont:
        key = (face, bold, pixel)
        if key not in self._fonts:
            f = QFont(FONT)
            f.setStyleHint(QFont.StyleHint.Monospace)
            f.setPixelSize(pixel or int(self.cell_w[face] / 0.6))
            f.setBold(bold)
            self._fonts[key] = f
        return self._fonts[key]


# ---------------------------------------------------------------- lines

class Line:
    "Base: each row knows its own height and knows how to draw itself"
    h: float = 0.0
    is_cut = False

    def paint(self, p: QPainter, y: float, m: Metrics) -> None:
        raise NotImplementedError


@dataclass
class TextLine(Line):
    chars: list = field(default_factory=list)     # (font, style, cell width)
    w: float = 0.0
    h: float = LINE_H['a']
    align: str = 'left'

    def touch(self, st: dict, lh: float) -> None:
        "Line height and alignment from the incoming text style"
        if not self.chars:
            self.h, self.align = lh, st['align']
        else:
            self.h = max(self.h, lh)

    def add(self, ch: str, st: dict, cw: float) -> None:
        self.chars.append((ch, st, cw))
        self.w += cw

    def paint(self, p, y, m):
        x = {'left': 0.0, 'center': (m.dots - self.w) / 2,
             'right': m.dots - self.w}.get(self.align, 0.0)
        for ch, st, cw in self.chars:
            bw, bh = m.cell_w[st['font']], CELL_H[st['font']]
            p.save()
            p.translate(x, y)
            p.scale(st['wm'], st['hm'])
            if st['invert']:
                p.fillRect(QRectF(0, 0, bw, bh + 2), Qt.GlobalColor.black)
                p.setPen(Qt.GlobalColor.white)
            else:
                p.setPen(Qt.GlobalColor.black)
            p.setFont(m.font(st['font'], st['bold']))
            p.drawText(QRectF(0, 0, bw, bh), Qt.AlignmentFlag.AlignCenter, ch)
            if st['underline']:
                uy = bh + 2
                p.fillRect(QRectF(0, uy, bw, 1.5 * st['underline']), p.pen().color())
            p.restore()
            x += cw


@dataclass
class CutLine(Line):
    h: float = 30
    is_cut = True

    def paint(self, p, y, m):
        cy = y + self.h / 2
        p.setPen(QPen(QColor("#888"), 1, Qt.PenStyle.DashLine))
        p.drawLine(QPointF(28, cy), QPointF(m.dots, cy))     # The line starts after the scissors
        p.setPen(QColor("#888"))
        f = QFont(FONT)
        f.setPixelSize(48)
        p.setFont(f)
        p.drawText(QRectF(0, y, 28, self.h), Qt.AlignmentFlag.AlignCenter, "\u2702") # scissors character


@dataclass
class BoxLine(Line):
    "Dashed box with a label: fallback for anything that cannot be drawn"
    label: str = ''
    h: float = 60

    def paint(self, p, y, m):
        p.setPen(QPen(QColor("#888"), 1, Qt.PenStyle.DashLine))
        p.drawRect(QRectF(2, y + 4, m.dots - 4, self.h - 8))
        p.setFont(m.font('a', pixel=18))
        p.drawText(QRectF(0, y, m.dots, self.h), Qt.AlignmentFlag.AlignCenter, self.label)


@dataclass
class ImageLine(Line):
    "Generic icon instead of an image"
    h: float = 110

    def paint(self, p, y, m):
        w = self.h * 1.4
        r = QRectF((m.dots - w) / 2, y + 6, w, self.h - 12)
        p.setPen(QPen(QColor("#888"), 2))
        p.setBrush(QColor("#eee"))
        p.drawRect(r)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#aaa"))
        p.drawEllipse(QPointF(r.left() + r.width() * 0.25, r.top() + r.height() * 0.3),
                      r.height() * 0.1, r.height() * 0.1)
        p.drawPolygon(QPolygonF([
            QPointF(r.left() + 4, r.bottom() - 4),
            QPointF(r.left() + r.width() * 0.4, r.top() + r.height() * 0.4),
            QPointF(r.left() + r.width() * 0.6, r.top() + r.height() * 0.65),
            QPointF(r.left() + r.width() * 0.75, r.top() + r.height() * 0.5),
            QPointF(r.right() - 4, r.bottom() - 4)]))
        p.setBrush(Qt.BrushStyle.NoBrush)


def _runs_path(rows, x0, y0, mw, mh) -> QPainterPath:
    "A single path for the black modules (connecting the horizontal segments): no white lines"
    path = QPainterPath()
    path.setFillRule(Qt.FillRule.WindingFill)
    for r, row in enumerate(rows):
        i, n = 0, len(row)
        while i < n:
            if row[i] in ('1', True):
                j = i
                while j < n and row[j] in ('1', True):
                    j += 1
                path.addRect(QRectF(x0 + i * mw, y0 + r * mh, (j - i) * mw, mh))
                i = j
            else:
                i += 1
    return path


@dataclass
class BarcodeLine(Line):
    mods: str = ''
    mw: float = 3
    bar_h: float = 64
    text: str = ''
    above: bool = False
    below: bool = True
    h: float = 0

    @staticmethod
    def from_op(op, m: Metrics) -> Line:
        _, code, bc, height, width, pos = op
        if bc.upper() == 'CODE128':            # prefisso di subset aggiunto da escpos
            code = re.sub(r'^\{[ABC]', '', code)
        name = _BC_NAMES.get(bc.upper())
        try:
            cls = pybarcode.get_barcode_class(name)
            obj = cls(code, add_checksum=False) if name == 'code39' else cls(code)
            mods = obj.build()[0]
        except Exception:                       # simbologia non supportata o codice non valido
            return BoxLine(label=f'BARCODE {bc}: {code}', h=90)
        above, below = pos in ('ABOVE', 'BOTH'), pos in ('BELOW', 'BOTH')
        mw = min(width, m.dots / len(mods))
        return BarcodeLine(mods, mw, height, code, above, below,
                           h=height + 24 * (above + below) + 12)

    def paint(self, p, y, m):
        x0 = (m.dots - len(self.mods) * self.mw) / 2
        top = y + 6 + (24 if self.above else 0)
        p.fillPath(_runs_path([self.mods], x0, top, self.mw, self.bar_h),
                   Qt.GlobalColor.black)
        p.setPen(Qt.GlobalColor.black)
        p.setFont(m.font('a', pixel=20))
        if self.above:
            p.drawText(QRectF(0, y + 4, m.dots, 24), Qt.AlignmentFlag.AlignCenter, self.text)
        if self.below:
            p.drawText(QRectF(0, top + self.bar_h + 2, m.dots, 24),
                       Qt.AlignmentFlag.AlignCenter, self.text)


@dataclass
class QrLine(Line):
    matrix: list = field(default_factory=list)
    mod: float = 3
    h: float = 0

    @staticmethod
    def from_op(op, m: Metrics) -> Line:
        _, content, ec, size = op
        try:
            q = qrcode.QRCode(error_correction=_QR_EC.get(ec, qrc.ERROR_CORRECT_L), border=0)
            q.add_data(content)
            q.make(fit=True)
            matrix = q.get_matrix()
        except Exception:
            return BoxLine(label=f'QRCODE: {content}', h=130)
        mod = min(size, m.dots / (len(matrix) + 8))
        return QrLine(matrix, mod, h=len(matrix) * mod + 8 * mod)

    def paint(self, p, y, m):
        n = len(self.matrix)
        p.fillPath(_runs_path(self.matrix, (m.dots - n * self.mod) / 2, y + 4 * self.mod,
                              self.mod, self.mod), Qt.GlobalColor.black)


# ---------------------------------------------------------------- anteprima

class ReceiptPreview:
    "Converts the Dummy Device's 'oops' into lines and draws them onto a QPaintDevice"

    def __init__(self, dev, paper_width_mm: float = 80.0):
        self.m = Metrics(dev)
        self.paper_mm = paper_width_mm
        self.lines = self._build(dev.ops)

    # -- row construction
    def _build(self, ops) -> list[Line]:
        m, lines = self.m, []
        cur = TextLine()

        def newline(force=True):
            nonlocal cur
            if cur.chars or force:
                lines.append(cur)
                cur = TextLine()

        for op in ops:
            match op[0]:
                case 'text':
                    _, txt, st = op
                    cw = m.cell_w[st['font']] * st['wm']
                    lh = LINE_H[st['font']] * st['hm']
                    for i, part in enumerate(txt.split('\n')):
                        if i:
                            newline()
                        cur.touch(st, lh)
                        for ch in part:
                            if cur.w + cw > m.dots + 0.5:      # a capo automatico
                                newline(False)
                                cur.touch(st, lh)
                            cur.add(ch, st, cw)
                case 'feed':
                    newline(False)
                    lines += [TextLine() for _ in range(op[1])]
                case 'barcode':
                    newline(False); lines.append(BarcodeLine.from_op(op, m))
                case 'qr':
                    newline(False); lines.append(QrLine.from_op(op, m))
                case 'cut':
                    newline(False); lines.append(CutLine())
                case 'box':                                    # immage
                    newline(False); lines.append(ImageLine())
        newline(False)
        return lines

    def _pages(self, max_h: float | None = None) -> list[list[Line]]:
        "One page per receipt (it separates at the perforation); it may also break if it is too tall"
        pages, cur, h = [], [], 0.0
        for ln in self.lines:
            if max_h and cur and h + ln.h > max_h and not ln.is_cut:
                pages.append(cur); cur, h = [], 0.0
            cur.append(ln); h += ln.h
            if ln.is_cut:
                pages.append(cur); cur, h = [], 0.0
        if cur:
            pages.append(cur)
        return pages

    # -- public API
    def page_layout(self) -> QPageLayout:
        "A scrolling page as tall as the longest receipt"
        tallest = max((sum(l.h for l in pg) for pg in self._pages()), default=0) + LAYOUT_SLACK
        size = QSizeF(self.paper_mm, tallest / DPI * 25.4)
        return QPageLayout(QPageSize(size, QPageSize.Unit.Millimeter),
                           QPageLayout.Orientation.Portrait, QMarginsF(0, 0, 0, 0))

    def paint(self, device) -> None:
        # actual physical dimensions of the device, whatever layout the dialog has chosen
        paper_dots = device.widthMM() / 25.4 * DPI
        k = device.width() / paper_dots
        pages = self._pages(max_h=device.height() / k - SPLIT_SLACK)

        p = QPainter(device)
        try:
            p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            for i, page in enumerate(pages):
                if i:
                    device.newPage()
                p.save()
                p.scale(k, k)
                p.translate((paper_dots - self.m.dots) / 2, 0)
                p.fillRect(QRectF(0, 0, self.m.dots, sum(l.h for l in page) + SPLIT_SLACK),
                           Qt.GlobalColor.white)
                y = 0.0
                for ln in page:
                    ln.paint(p, y, self.m)
                    y += ln.h
                p.restore()
        finally:
            p.end()