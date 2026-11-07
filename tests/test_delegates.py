"""Behaviour of the custom delegates in App.Widget.Delegate

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from typing import Any
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# PySide6
from PySide6.QtCore import QAbstractTableModel, QByteArray, QLocale, QModelIndex, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QDoubleSpinBox, QStyleOptionViewItem, QWidget

# application modules
from App import session
from App.Widget import Delegate


app = QApplication.instance() or QApplication([])
LOADED, UNLOADED, STOCK, ORDERED, AVAILABLE, NEW_STOCK = 3, 4, 5, 6, 7, 8


class InventoryModel(QAbstractTableModel):
    "One inventory row, new stock is always NULL as in the real model"

    def __init__(self, loaded: str, unloaded: str, stock: str, ordered: str, available: str) -> None:
        super().__init__()
        self.row = [1, 1, 1, Decimal(loaded), Decimal(unloaded), Decimal(stock),
                    Decimal(ordered), Decimal(available), None]
        self.writes = 0

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.row)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        return self.row[index.column()]

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole) -> bool:
        self.row[index.column()] = value
        self.writes += 1
        return True


class NewStockDelegateTest(unittest.TestCase):

    def setUp(self) -> None:
        patcher = mock.patch.object(Delegate, 'Settings', lambda: {'quantity_decimal_places': 2})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.parent = QWidget()
        self.delegate = Delegate.NewStockDelegate(self.parent)

    def open_editor(self, model: InventoryModel) -> QDoubleSpinBox:
        index = model.index(0, NEW_STOCK)
        editor = self.delegate.createEditor(self.parent, QStyleOptionViewItem(), index)
        self.delegate.setEditorData(editor, index)
        return editor

    def commit(self, editor: QDoubleSpinBox, model: InventoryModel) -> None:
        self.delegate.setModelData(editor, model, model.index(0, NEW_STOCK))

    def test_editor_starts_from_the_current_stock(self) -> None:
        self.assertEqual(self.open_editor(InventoryModel('50', '20', '30', '10', '20')).value(), 30.0)

    def test_leaving_the_cell_untouched_writes_nothing(self) -> None:
        model = InventoryModel('50', '20', '30', '10', '20')
        self.commit(self.open_editor(model), model)
        self.assertEqual(model.writes, 0)

    def test_untouched_negative_stock_is_not_written(self) -> None:
        "The spin box can not show it: the stock must not become zero"
        model = InventoryModel('10', '15', '-5', '0', '-5')
        self.commit(self.open_editor(model), model)
        self.assertEqual(model.writes, 0)
        self.assertEqual(model.row[STOCK], Decimal('-5'))

    def test_new_stock_recalculates_loads_and_availability(self) -> None:
        model = InventoryModel('50', '20', '30', '10', '20')
        editor = self.open_editor(model)
        editor.setValue(25.0)
        self.commit(editor, model)
        self.assertEqual(model.row[LOADED], Decimal('45'))
        self.assertEqual(model.row[UNLOADED], Decimal('20'))
        self.assertEqual(model.row[STOCK], Decimal('25'))
        self.assertEqual(model.row[AVAILABLE], Decimal('15'))


class Row(QAbstractTableModel):
    "One row with one value, the column type comes from the columns attribute"

    def __init__(self, value: Any, kind: str = 'str') -> None:
        super().__init__()
        self.value = value
        self.columns = [('field', 'Field', False, kind)]
        self.writes: list[Any] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        return self.value

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole) -> bool:
        self.writes.append(value)
        self.value = value
        return True


class ChangeOnlyTest(unittest.TestCase):
    "Leaving a cell without changing it must not touch the model"

    def setUp(self) -> None:
        self.parent = QWidget()
        session['qlocale'] = QLocale('it')

    def editor(self, delegate, model: Row):
        index = model.index(0, 0)
        editor = delegate.createEditor(self.parent, QStyleOptionViewItem(), index)
        delegate.setEditorData(editor, index)
        return editor

    def assertUntouched(self, delegate, value: Any, kind: str = 'str') -> None:
        model = Row(value, kind)
        delegate.setModelData(self.editor(delegate, model), model, model.index(0, 0))
        self.assertEqual(model.writes, [])

    def test_generic_null_and_out_of_range_values(self) -> None:
        delegate = Delegate.GenericDelegate(self.parent)
        for value, kind in ((None, 'int'), (None, 'decimal'), (None, 'date'), (None, 'datetime'),
                            (None, 'str'), (-5, 'int'), (Decimal('1.255'), 'decimal')):
            with self.subTest(value=value, kind=kind):
                self.assertUntouched(delegate, value, kind)

    def test_number_delegates(self) -> None:
        self.assertUntouched(Delegate.IntegerDelegate(self.parent), None, 'int')
        delegate = Delegate.DecimalDelegate(self.parent, 2, 999.9)
        for value in (None, Decimal('-3.50'), Decimal('1500.00')):
            with self.subTest(value=value):
                self.assertUntouched(delegate, value, 'decimal')

    def test_generic_writes_a_changed_value(self) -> None:
        delegate = Delegate.GenericDelegate(self.parent)
        model = Row(None, 'int')
        editor = self.editor(delegate, model)
        editor.setValue(7)
        delegate.setModelData(editor, model, model.index(0, 0))
        self.assertEqual(model.writes, [7])

    def test_relation_value_missing_from_the_list(self) -> None:
        delegate = Delegate.RelationDelegate(self.parent, lambda: [(1, 'Bar'), (2, 'Cucina')])
        for value in (9, None):
            with self.subTest(value=value):
                self.assertUntouched(delegate, value, 'int')

    def test_relation_first_item_can_be_chosen(self) -> None:
        "With a missing value the combo box must not start on the first item"
        delegate = Delegate.RelationDelegate(self.parent, lambda: [(1, 'Bar'), (2, 'Cucina')])
        model = Row(9, 'int')
        editor = self.editor(delegate, model)
        self.assertEqual(editor.currentIndex(), -1)
        editor.setCurrentIndex(0)
        delegate.setModelData(editor, model, model.index(0, 0))
        self.assertEqual(model.writes, [1])

    def test_relation_null_item(self) -> None:
        delegate = Delegate.RelationDelegate(self.parent, lambda: [(1, 'Bar')], null=True)
        model = Row(None, 'int')
        self.assertEqual(self.editor(delegate, model).currentIndex(), 0)
        self.assertUntouched(delegate, None, 'int')

    def test_items_value_missing_from_the_list(self) -> None:
        delegate = Delegate.ItemsDelegate(self.parent, ['a', 'b'])
        for value in ('z', None):
            with self.subTest(value=value):
                self.assertUntouched(delegate, value)

    def test_printer_of_another_computer_is_kept(self) -> None:
        with mock.patch.object(Delegate.QPrinterInfo, 'availablePrinters', staticmethod(lambda: [])):
            delegate = Delegate.PrintersDelegate(self.parent)
        delegate.data = ['HP']
        self.assertUntouched(delegate, 'Epson')
        self.assertUntouched(delegate, None)

    def test_color_combo_keeps_and_writes_hex_strings(self) -> None:
        colors = [('#ff0000', 'Red'), ('#0000ff', 'Blue')]
        delegate = Delegate.ColorComboDelegate(self.parent, colors)
        self.assertUntouched(delegate, '#0000ff')
        self.assertUntouched(delegate, None)
        model = Row('#0000ff')
        editor = self.editor(delegate, model)
        self.assertEqual(editor.currentText(), 'Blue')
        editor.setCurrentIndex(0)
        delegate.setModelData(editor, model, model.index(0, 0))
        self.assertEqual(model.writes, ['#ff0000'])


class NoEditorTest(unittest.TestCase):
    "An editor would be committed as NULL or invert the value when the cell loses focus"

    def test_delegates_without_an_editor(self) -> None:
        parent = QWidget()
        for delegate in (Delegate.GenericDelegate(parent),
                         Delegate.BooleanDelegate(parent),
                         Delegate.ReadOnlyDelegate(parent),
                         Delegate.HideTextDelegate(parent, '***')):
            with self.subTest(delegate=type(delegate).__name__):
                model = Row(True, 'bool')
                self.assertIsNone(delegate.createEditor(parent, QStyleOptionViewItem(), model.index(0, 0)))

    def test_image_delegate_keeps_the_new_image(self) -> None:
        parent = QWidget()
        model = Row(QByteArray(b'old'))
        pixmap = QPixmap(2, 2)
        pixmap.fill(Qt.GlobalColor.red)
        dialog = mock.Mock()
        dialog.return_value.exec.return_value = QDialog.DialogCode.Accepted
        dialog.return_value.getImage.return_value = pixmap
        with mock.patch.object(Delegate, 'SelectImageDialog', dialog):
            editor = Delegate.ImageDelegate(parent).createEditor(parent, QStyleOptionViewItem(), model.index(0, 0))
        self.assertIsNone(editor)
        self.assertEqual(len(model.writes), 1)
        self.assertGreater(model.value.size(), 3)


if __name__ == '__main__':
    unittest.main()
