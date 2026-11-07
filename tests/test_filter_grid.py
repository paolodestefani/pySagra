"""Behaviour of the filter rows shared by the dialogs

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
from PySide6.QtCore import QDate, QDateTime, QTime
from PySide6.QtWidgets import QApplication, QGridLayout, QWidget

# application modules
from App.Widget.FilterGrid import FILTER_ROWS, FilterGrid, SpacerWidget, ff, filterOperators


app = QApplication.instance() or QApplication([])
VALUES = lambda: [(1, 'One'), (2, 'Two'), (3, 'Three')]
FIELDS = [('a', 'Int', 'int', None),
          ('b', 'List', 'int', VALUES),
          ('c', 'Decimal', 'decimal', None),
          ('d', 'String', 'str', None),
          ('e', 'Bool', 'bool', None),
          ('f', 'Date', 'date', None),
          ('g', 'Date time', 'datetime', None),
          ('h', 'Time', 'time', None),
          ('i', 'Reference', 'refstr', VALUES),
          ('j', 'Float', 'float', None),
          ('k', 'Old decimal', 'decimal2', None),
          ('l', 'Unknown', 'unknown', None)]


class GridTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.parent = QWidget()
        self.layout = QGridLayout(self.parent)
        self.grid = FilterGrid(self.layout, self.parent)
        self.grid.setFields(FIELDS)

    def choose(self, field: str, operator: str, row: int = 0) -> QWidget:
        "Choose a field and an operator, return the operand widget"
        self.grid.rows[row].field.setCurrentData(field)
        self.grid.rows[row].operator.setCurrentOperatorKey(operator)
        return self.grid.rows[row].operand


class ConditionsTest(GridTestCase):

    def test_no_filter_no_conditions(self) -> None:
        self.assertEqual(self.grid.conditions(), [])
        self.assertEqual(self.grid.settings(), [])

    def test_field_without_operator_is_ignored(self) -> None:
        self.grid.rows[0].field.setCurrentData('a')
        self.assertEqual(self.grid.conditions(), [])

    def test_operand_argument(self) -> None:
        self.choose('a', '=#SB').setValue(5)
        self.assertEqual(self.grid.conditions(), [('a = %s', 5)])

    def test_no_operand(self) -> None:
        self.choose('a', 'IS NULL#')
        self.assertEqual(self.grid.conditions(), [('a IS NULL', None)])

    def test_list_operand(self) -> None:
        self.choose('a', '= ANY(%s)#LEI').setText('1, 2')
        self.assertEqual(self.grid.conditions(), [('a = ANY(%s)', [1, 2])])

    def test_operator_with_placeholder(self) -> None:
        self.choose('d', "ilike '%%'||%s||'%%'#LE").setText('x')
        self.assertEqual(self.grid.conditions(), [("d ilike '%%'||%s||'%%'", 'x')])

    def test_negate(self) -> None:
        self.choose('a', '=#SB').setValue(5)
        self.grid.rows[0].negate.setChecked(True)
        self.assertEqual(self.grid.conditions(), [('NOT a = %s', 5)])

    def test_date_compares_the_day(self) -> None:
        self.choose('f', '<=#DE').setDate(QDate(2026, 1, 2))
        self.assertEqual(self.grid.conditions(), [('(f)::date <= %s', QDate(2026, 1, 2))])

    def test_datetime_is_not_cast(self) -> None:
        self.choose('g', '=#DTE')
        self.assertEqual(self.grid.conditions()[0][0], 'g = %s')

    def test_rows_keep_their_order(self) -> None:
        self.choose('a', '=#SB', row=2).setValue(2)
        self.choose('a', '=#SB', row=0).setValue(1)
        self.assertEqual(self.grid.conditions(), [('a = %s', 1), ('a = %s', 2)])


class FieldTypesTest(GridTestCase):

    def operators(self, field: str) -> list[str]:
        self.grid.rows[0].field.setCurrentData(field)
        combo = self.grid.rows[0].operator
        return [combo.itemText(i) for i in range(combo.count())]

    def test_report_types_use_the_decimal_operators(self) -> None:
        expected = [o[1] for o in filterOperators()['decimal']]
        for field in ('j', 'k'):
            with self.subTest(field=field):
                self.assertEqual(self.operators(field), expected)

    def test_from_list_needs_a_list(self) -> None:
        self.assertNotIn('From list', self.operators('a'))
        self.assertIn('From list', self.operators('b'))

    def test_unknown_type_has_no_operators(self) -> None:
        self.assertEqual(self.operators('l'), [])
        self.assertEqual(self.grid.conditions(), [])


class SettingsTest(GridTestCase):
    "Saved filters must come back as they were"

    def roundtrip(self, field: str, operator: str, setter, getter) -> None:
        setter(self.choose(field, operator))
        self.grid.rows[0].negate.setChecked(True)
        expected = getter(self.grid.rows[0].operand)
        saved = [('F', *setting) for setting in self.grid.settings()]
        self.grid.reset()
        self.assertEqual(self.grid.settings(), [])
        self.grid.restore(saved)
        self.assertEqual(getter(self.grid.rows[0].operand), expected)
        self.assertTrue(self.grid.rows[0].negate.isChecked())
        self.assertEqual(self.grid.rows[0].operator.currentOperatorKey(), operator)

    def test_every_operand_widget(self) -> None:
        cases = (('a', '=#SB', lambda w: w.setValue(7), lambda w: w.value()),
                 ('b', '=#LIST', lambda w: w.setCurrentIndex(2), lambda w: w.currentData()),
                 ('c', '=#DSB', lambda w: w.setValue(1.5), lambda w: w.value()),
                 ('d', '=#LE', lambda w: w.setText('x'), lambda w: w.text()),
                 ('d', 'ILIKE ANY(%s)#LES', lambda w: w.setText('x,y'), lambda w: w.text()),
                 ('a', '= ANY(%s)#LEI', lambda w: w.setText('1,2'), lambda w: w.text()),
                 ('c', '= ANY(%s)#LED', lambda w: w.setText('1.5'), lambda w: w.text()),
                 ('e', '=#CB', lambda w: w.setChecked(True), lambda w: w.isChecked()),
                 ('f', '=#DE', lambda w: w.setDate(QDate(2026, 1, 2)), lambda w: w.date()),
                 ('g', '=#DTE', lambda w: w.setDateTime(QDateTime(2026, 1, 2, 3, 4, 5)), lambda w: w.dateTime()),
                 ('h', '=#TE', lambda w: w.setTime(QTime(3, 4, 5)), lambda w: w.time()),
                 ('i', '=#SCB', lambda w: w.setCurrentIndex(1), lambda w: w.currentData()),
                 ('i', '= ANY(%s)#CCB', lambda w: w.setCheckedData([1, 3]), lambda w: w.currentData()))
        for field, operator, setter, getter in cases:
            with self.subTest(operator=operator):
                self.roundtrip(field, operator, setter, getter)
                self.grid.reset()

    def test_old_saves(self) -> None:
        "Operators without widget type and combo boxes saved by index"
        self.grid.restore([('F', 0, 'a', False, '=', '')])
        self.assertEqual(self.grid.rows[0].operator.currentOperator(), '=')
        self.grid.reset()
        self.grid.restore([('F', 0, 'b', False, '=#LIST', '9')])
        self.assertEqual(self.grid.rows[0].operand.currentIndex(), -1)

    def test_rows_outside_of_the_grid_are_skipped(self) -> None:
        self.grid.restore([('F', FILTER_ROWS, 'a', False, '=#SB', '1')])
        self.assertEqual(self.grid.settings(), [])

    def test_removed_field_is_ignored(self) -> None:
        self.grid.restore([('F', 0, 'gone', False, '=#SB', '1')])
        self.assertEqual(self.grid.conditions(), [])


class LayoutTest(GridTestCase):
    "SalesSummary and OrderedDelivered set the filters through the layout"

    def cell(self, row: int, column: int) -> QWidget:
        return self.layout.itemAtPosition(row, column).widget()

    def test_widgets_stay_in_their_columns(self) -> None:
        self.assertIs(self.cell(1, ff.FIELD), self.grid.rows[1].field)
        self.assertIs(self.cell(1, ff.NEGATE), self.grid.rows[1].negate)
        self.assertIs(self.cell(1, ff.OPERATOR), self.grid.rows[1].operator)
        self.assertIsInstance(self.cell(1, ff.OPERAND), SpacerWidget)

    def test_filter_set_through_the_layout(self) -> None:
        self.cell(0, 0).setCurrentIndex(1)
        self.cell(0, 2).setCurrentIndex(1)
        self.cell(0, 3).setValue(9)
        self.assertEqual(self.grid.conditions(), [('a = %s', 9)])

    def test_operand_is_replaced_in_the_layout(self) -> None:
        operand = self.choose('a', '=#SB')
        self.assertIs(self.cell(0, 3), operand)
        self.grid.rows[0].field.setCurrentIndex(0)
        self.assertIsInstance(self.cell(0, 3), SpacerWidget)

    def test_set_fields_clears_the_filters(self) -> None:
        self.choose('a', '=#SB')
        self.grid.setFields([('z', 'Z', 'str', None)])
        self.assertEqual(self.grid.conditions(), [])
        self.assertEqual(self.grid.rows[0].field.count(), 2)
        self.assertFalse(self.grid.rows[0].operator.isEnabled())


if __name__ == '__main__':
    unittest.main()
