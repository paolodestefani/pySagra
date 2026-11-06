"""Behaviour of the custom controls in App.Widget.Control

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import unittest
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# PySide6
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

# application modules
from App.Widget.Control import CheckableComboBox
from App.Widget.Control import RelationalComboBox


app = QApplication.instance() or QApplication([])
ITEMS = [(1, 'Bar'), (2, 'Cucina'), (3, 'Griglia')]


def relational_combo(nullable: bool = False) -> RelationalComboBox:
    combo = RelationalComboBox(None)
    combo.setNullable(nullable)
    combo.setFunction(lambda: list(ITEMS))
    return combo


class RelationalComboBoxPopupTest(unittest.TestCase):
    "Opening the popup reloads the list and must not change the selection"

    def open_and_close(self, combo: RelationalComboBox) -> None:
        combo.showPopup()
        combo.hidePopup()

    def test_selection_survives_the_popup(self) -> None:
        combo = relational_combo()
        combo.modelDataStr = '2'
        self.open_and_close(combo)
        self.assertEqual(combo.currentText(), 'Cucina')
        self.assertEqual(combo.modelDataStr, '2')

    def test_null_selection_survives_the_popup(self) -> None:
        combo = relational_combo(nullable=True)
        combo.modelDataStr = None
        self.open_and_close(combo)
        self.assertEqual(combo.currentIndex(), 0)
        self.assertEqual(combo.modelDataStr, '')

    def test_empty_selection_stays_empty(self) -> None:
        combo = relational_combo()
        combo.setCurrentIndex(-1)
        self.open_and_close(combo)
        self.assertEqual(combo.currentIndex(), -1)

    def test_item_removed_from_the_list_selects_nothing(self) -> None:
        "A different item must not take the place of the removed one"
        items = list(ITEMS)
        combo = RelationalComboBox(None)
        combo.setFunction(lambda: list(items))
        combo.modelDataStr = '3'
        items.pop()
        self.open_and_close(combo)
        self.assertEqual(combo.currentIndex(), -1)

    def test_no_change_signal_from_the_popup(self) -> None:
        combo = relational_combo()
        combo.modelDataStr = '2'
        emitted = []
        combo.currentIndexChanged.connect(emitted.append)
        self.open_and_close(combo)
        self.assertEqual(emitted, [])


class CheckableComboBoxTest(unittest.TestCase):

    def test_click_outside_of_the_items(self) -> None:
        combo = CheckableComboBox()
        combo.addItems(['A', 'B'])
        viewport = combo.view().viewport()
        position = QPointF(5, viewport.height() + 500)
        event = QMouseEvent(QEvent.Type.MouseButtonRelease,
                            position,
                            QPointF(viewport.mapToGlobal(position)),
                            Qt.MouseButton.LeftButton,
                            Qt.MouseButton.NoButton,
                            Qt.KeyboardModifier.NoModifier)
        self.assertTrue(combo.eventFilter(viewport, event))
        self.assertEqual(combo.currentData(), [])


if __name__ == '__main__':
    unittest.main()
