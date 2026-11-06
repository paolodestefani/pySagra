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
from PySide6.QtCore import QEvent, QLocale, QPointF, Qt
from PySide6.QtGui import QIcon
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

# application modules
from App.Widget.Control import ButtonItem
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


class RelationalComboBoxItemsTest(unittest.TestCase):

    def test_items_without_icon(self) -> None:
        combo = relational_combo()
        self.assertEqual(combo.count(), 3)
        self.assertEqual((combo.itemText(1), combo.itemData(1)), ('Cucina', 2))

    def test_nullable_adds_an_empty_first_item(self) -> None:
        combo = relational_combo(nullable=True)
        self.assertEqual(combo.count(), 4)
        self.assertEqual((combo.itemText(0), combo.itemData(0)), ('', None))

    def test_items_with_icon(self) -> None:
        combo = RelationalComboBox(None)
        combo.setItemList([(QIcon(), 'A', 'Primo'), (QIcon(), 'B', 'Secondo')])
        self.assertEqual((combo.itemText(1), combo.itemData(1)), ('Secondo', 'B'))

    def test_function_with_icons_and_nullable(self) -> None:
        combo = RelationalComboBox(None)
        combo.setNullable(True)
        combo.setFunction(lambda: [(QIcon(), 'A', 'Primo')])
        self.assertEqual(combo.count(), 2)
        self.assertEqual((combo.itemText(1), combo.itemData(1)), ('Primo', 'A'))


class ButtonItemStockTextTest(unittest.TestCase):
    "The stock level is an integer scaled by the quantity decimal places"

    def level_text(self, level: int, language: str = 'it') -> str:
        QLocale.setDefault(QLocale(language))
        self.addCleanup(QLocale.setDefault, QLocale('C'))
        button = ButtonItem(None, 'Pasta', '#000000', '#90ee90', {'quantity_decimal_places': 2})
        button.hasInventory = True
        button.showLevel = True
        button.stockLevel = level
        return button.text().split('\n')[-1]

    def test_levels(self) -> None:
        for level, expected in ((1200, '(12)'), (1250, '(12,5)'), (1205, '(12,05)'), (0, '(0)'),
                                (-150, '(-1,5)'), (-200, '(-2)'), (-5, '(-0,05)')):
            with self.subTest(level=level):
                self.assertEqual(self.level_text(level), expected)

    def test_decimal_separator_follows_the_locale(self) -> None:
        self.assertEqual(self.level_text(1250, 'en'), '(12.5)')


if __name__ == '__main__':
    unittest.main()
