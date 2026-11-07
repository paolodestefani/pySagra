"""Behaviour of the filters in SortFilterDialog and PrintDialog

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# PySide6
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QApplication, QLineEdit, QWidget

# application modules
from App import session
from App.Widget import Dialog
from App.Widget import ExceptionHandler
from App.Widget import FilterGrid


app = QApplication.instance() or QApplication([])
COLUMNS = [('id', 'Id', True, 'int'),
           ('name', 'Name', False, 'str'),
           ('price', 'Price', False, 'decimal'),
           ('created_at', 'Date', True, 'date')]


class Model:
    "The part of QueryModel used by SortFilterDialog"

    def __init__(self, reference: dict|None = None) -> None:
        self.columns = COLUMNS
        self.limitCondition = None
        self.whereCondition: list = []
        self.orderByExpression: list = []
        if reference is not None:
            self.reference = reference

    def addWhere(self, condition: str, argument=None) -> None:
        self.whereCondition.append((condition, argument))

    def addOrderBy(self, expression: str) -> None:
        self.orderByExpression.append(expression)


class DialogTestCase(unittest.TestCase):

    def setUp(self) -> None:
        session.update(user='u', l10n='it', can_edit_sortfilters=True,
                       can_edit_reports=False, is_admin=False)
        self.parent = QWidget()
        for name, value in (('list_adaptation', lambda *a: []),
                            ('get_adapt_default', lambda *a: None),
                            ('get_report_list', lambda *a: []),
                            ('report_class_adapt_list', lambda *a: [])):
            patcher = mock.patch.object(Dialog, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)


class SortFilterDialogTest(DialogTestCase):

    def dialog(self, model: Model) -> Dialog.SortFilterDialog:
        return Dialog.SortFilterDialog('Test', model, self.parent)

    def cell(self, dialog: Dialog.SortFilterDialog, column: int) -> QWidget:
        return dialog.ui.layoutFilters.itemAtPosition(0, column).widget()

    def operators(self, dialog: Dialog.SortFilterDialog) -> list[str]:
        combo = self.cell(dialog, FilterGrid.ff.OPERATOR)
        return [combo.itemText(i) for i in range(combo.count())]

    def test_decimal_column_has_operators(self) -> None:
        dialog = self.dialog(Model({}))
        self.cell(dialog, FilterGrid.ff.FIELD).setCurrentData('price')
        self.assertEqual(len(self.operators(dialog)), len(FilterGrid.filterOperators()['decimal']))

    def test_from_list_needs_a_reference_list(self) -> None:
        for model in (Model(), Model({})):
            dialog = self.dialog(model)
            self.cell(dialog, FilterGrid.ff.FIELD).setCurrentData('id')
            self.assertNotIn('From list', self.operators(dialog))
        dialog = self.dialog(Model({'id': lambda: [(1, 'One')]}))
        self.cell(dialog, FilterGrid.ff.FIELD).setCurrentData('id')
        self.assertIn('From list', self.operators(dialog))

    def test_date_filter_compares_the_day(self) -> None:
        dialog = self.dialog(Model({}))
        self.cell(dialog, FilterGrid.ff.FIELD).setCurrentData('created_at')
        self.cell(dialog, FilterGrid.ff.OPERATOR).setCurrentOperatorKey('=#DE')
        dialog.applySortFilter()
        self.assertEqual(dialog.model.whereCondition[0][0], '(created_at)::date = %s')

    def test_other_fields_are_not_cast(self) -> None:
        dialog = self.dialog(Model({}))
        self.cell(dialog, FilterGrid.ff.FIELD).setCurrentData('id')
        self.cell(dialog, FilterGrid.ff.OPERATOR).setCurrentOperatorKey('=#SB')
        dialog.applySortFilter()
        self.assertEqual(dialog.model.whereCondition[0][0], 'id = %s')


class SortFilterFieldsTest(DialogTestCase):
    "The fields each dialog gives to the grid"

    def test_only_columns_with_a_type_are_filters(self) -> None:
        model = Model({})
        model.columns = COLUMNS + [('hidden', 'Hidden', True, None)]
        dialog = Dialog.SortFilterDialog('Test', model, self.parent)
        self.assertEqual([f[0] for f in dialog._filterFields()], ['id', 'name', 'price', 'created_at'])

    def test_reference_lists_only_on_int_columns(self) -> None:
        values = lambda: [(1, 'One')]
        dialog = Dialog.SortFilterDialog('Test', Model({'id': values, 'name': values}), self.parent)
        fields = {f[0]: f[3] for f in dialog._filterFields()}
        self.assertIs(fields['id'], values)
        self.assertIsNone(fields['name'])

    def test_save_keeps_the_database_format(self) -> None:
        dialog = Dialog.SortFilterDialog('Test', Model({}), self.parent)
        dialog.ui.comboBoxSetting.blockSignals(True)
        dialog.ui.comboBoxSetting.addItem('A', 1)
        dialog.ui.comboBoxSetting.blockSignals(False)
        dialog.filters.rows[0].field.setCurrentData('id')
        dialog.filters.rows[0].operator.setCurrentOperatorKey('=#SB')
        dialog.filters.rows[0].operand.setValue(5)
        saved = {}
        with mock.patch.object(Dialog, 'set_adapt_setting', lambda cid, columns: saved.update(columns=columns)), \
             mock.patch.object(Dialog, 'set_adapt_limit', lambda *a: None), \
             mock.patch.object(Dialog.QMessageBox, 'information'):
            dialog.updateSettings()
        self.assertEqual(saved['columns'], [(1, None, None, None, None, 'F', 0, 'id', False, '=#SB', '5')])


class ListEditTest(unittest.TestCase):

    def state(self, editor: QWidget, text: str) -> QValidator.State:
        return editor.validator().validate(text, 0)[0]

    def test_invalid_text_can_not_be_typed(self) -> None:
        ints, decimals = FilterGrid.LineEditInts(), FilterGrid.LineEditDecimals()
        for editor, text in ((ints, '1,a'), (ints, '1.5'), (ints, '1-2'), (decimals, '1,a'), (decimals, '1.2.3')):
            with self.subTest(text=text):
                self.assertEqual(self.state(editor, text), QValidator.State.Invalid)
        for editor, text in ((ints, '1, 2,-3'), (ints, '1,'), (decimals, '1.5, -2'), (decimals, '.5')):
            with self.subTest(text=text):
                self.assertEqual(self.state(editor, text), QValidator.State.Acceptable)

    def test_values(self) -> None:
        ints, decimals = FilterGrid.LineEditInts(), FilterGrid.LineEditDecimals()
        ints.setText('1, 2,')
        self.assertEqual(ints.value(), [1, 2])
        decimals.setText('1.5, -2')
        self.assertEqual(decimals.value(), [1.5, -2.0])

    def test_invalid_saved_values_are_skipped(self) -> None:
        "setText does not go through the validator"
        ints = FilterGrid.LineEditInts()
        ints.setText('1,abc')
        self.assertEqual(ints.value(), [1])


class PrintDialogTest(DialogTestCase):

    def dialog(self) -> Dialog.PrintDialog:
        return Dialog.PrintDialog(self.parent, 'TEST')

    def test_operators_customize_nothing_but_choose_the_printer(self) -> None:
        dialog = self.dialog()
        self.assertTrue(dialog.ui.tabWidget.widget(Dialog.pti.OPTION).isEnabled())
        self.assertFalse(dialog.ui.tabWidget.widget(Dialog.pti.CUSTOMIZE).isEnabled())
        self.assertTrue(dialog.ui.comboBoxReportAdaptations.isEnabled())

    def test_authorized_users_can_customize(self) -> None:
        session['can_edit_reports'] = True
        self.assertTrue(self.dialog().ui.tabWidget.widget(Dialog.pti.CUSTOMIZE).isEnabled())

    def test_float_condition_uses_the_decimal_operators(self) -> None:
        dialog = self.dialog()
        dialog.filters.setFields([('x', 'X', 'float', None)])
        field = dialog.ui.layoutFilters.itemAtPosition(0, FilterGrid.ff.FIELD).widget()
        field.setCurrentIndex(1)
        operator = dialog.ui.layoutFilters.itemAtPosition(0, FilterGrid.ff.OPERATOR).widget()
        self.assertEqual(operator.count(), len(FilterGrid.filterOperators()['decimal']))

    def report(self, **attributes) -> SimpleNamespace:
        return SimpleNamespace(conditions={}, parameter={}, query=None, data=[1], **attributes)

    def test_generate_error_stops_the_print(self) -> None:
        dialog = self.dialog()
        dialog.report = self.report(generate=mock.Mock(side_effect=ValueError('broken')))
        with mock.patch.object(ExceptionHandler, 'MessageBoxCritical'):
            self.assertFalse(dialog.generateReport())

    def test_generate_success(self) -> None:
        dialog = self.dialog()
        dialog.report = self.report(generate=mock.Mock())
        self.assertTrue(dialog.generateReport())

    def test_adaptation_with_a_removed_parameter(self) -> None:
        dialog = self.dialog()
        dialog.ui.comboBoxReportAdaptations.blockSignals(True)
        dialog.ui.comboBoxReportAdaptations.addItem('A', 1)
        dialog.ui.comboBoxReportAdaptations.blockSignals(False)
        settings = ([('P', 5, None, None, None, 'value')], [], [])
        with mock.patch.object(Dialog, 'get_report_from_adapt', lambda a: ('D', 1, 'C', 'it', 'Report', 'it')), \
             mock.patch.object(Dialog, 'get_adapt_sorting', lambda a: 0), \
             mock.patch.object(Dialog, 'get_adapt_setting', lambda a: settings):
            dialog.setAdaptationSettings()


class ReportParametersTest(DialogTestCase):
    "Saved parameter values follow the parameter name, not its row"

    def dialog_with(self, names: list[str]) -> Dialog.PrintDialog:
        dialog = Dialog.PrintDialog(self.parent, 'TEST')
        dialog.ui.comboBoxReportList.blockSignals(True)
        dialog.ui.comboBoxReportList.addItem('Report', ('D', 1))
        dialog.ui.comboBoxReportList.blockSignals(False)
        dialog.ui.comboBoxReportAdaptations.blockSignals(True)
        dialog.ui.comboBoxReportAdaptations.addItem('A', 1)
        dialog.ui.comboBoxReportAdaptations.blockSignals(False)
        for row, name in enumerate(names):
            editor = QLineEdit(dialog)
            editor.param = name
            dialog.ui.layoutParameters.addWidget(QWidget(dialog), row, 0)
            dialog.ui.layoutParameters.addWidget(editor, row, 1)
        dialog.ui.layoutParameters.setRowStretch(len(names), 1)
        return dialog

    def editors(self, dialog: Dialog.PrintDialog) -> dict[str, QLineEdit]:
        layout = dialog.ui.layoutParameters
        return {item.widget().param: item.widget() for row in range(layout.rowCount())
                if (item := layout.itemAtPosition(row, 1)) is not None}

    def restore(self, dialog: Dialog.PrintDialog, params: list) -> None:
        with mock.patch.object(Dialog, 'get_report_from_adapt', lambda a: ('D', 1, 'C', 'it', 'Report', 'it')), \
             mock.patch.object(Dialog, 'get_adapt_sorting', lambda a: 0), \
             mock.patch.object(Dialog, 'get_adapt_setting', lambda a: (params, [], [])):
            dialog.setAdaptationSettings()

    def test_values_follow_the_names(self) -> None:
        dialog = self.dialog_with(['first', 'second'])
        self.editors(dialog)['first'].setText('one')
        self.editors(dialog)['second'].setText('two')
        saved = {}
        with mock.patch.object(Dialog, 'update_adaptation'), \
             mock.patch.object(Dialog, 'set_adapt_setting', lambda cid, columns: saved.update(columns=columns)), \
             mock.patch.object(Dialog.QMessageBox, 'information'):
            dialog.saveReportAdaptation()
        params = [c[5:] for c in saved['columns'] if c[5] == 'P']
        self.assertEqual([(p[2], p[5]) for p in params], [('first', 'one'), ('second', 'two')])
        # the report now has the parameters in the opposite order
        reordered = self.dialog_with(['second', 'first'])
        self.restore(reordered, [p[:3] + (None, None, p[5]) for p in params])
        self.assertEqual({k: e.text() for k, e in self.editors(reordered).items()},
                         {'first': 'one', 'second': 'two'})

    def test_old_saves_use_the_row(self) -> None:
        dialog = self.dialog_with(['first', 'second'])
        self.restore(dialog, [('P', 1, None, None, None, 'by row')])
        self.assertEqual(self.editors(dialog)['second'].text(), 'by row')

    def test_removed_parameter_is_skipped(self) -> None:
        dialog = self.dialog_with(['first'])
        self.restore(dialog, [('P', 0, 'gone', None, None, 'x')])
        self.assertEqual(self.editors(dialog)['first'].text(), '')


class PrintPreviewTest(DialogTestCase):

    def test_error_while_painting_is_shown(self) -> None:
        "The preview calls the paint slot: an error must be shown, not lost or raised"
        dialog = Dialog.PrintDialog(self.parent, 'TEST')
        report = mock.Mock(spec=Dialog.ReportEscpos)
        report.print.side_effect = ValueError('broken page')
        dialog.report = report
        dialog.generateReport = lambda: True
        preview = mock.MagicMock()
        preview.paintRequested.connect.side_effect = lambda slot: setattr(preview, 'slot', slot)
        preview.exec.side_effect = lambda: preview.slot(mock.Mock())
        with mock.patch.object(Dialog, 'QPrintPreviewDialog', return_value=preview), \
             mock.patch.object(ExceptionHandler, 'MessageBoxCritical') as critical:
            dialog.printPreview()
        critical.assert_called_once()
        report.receipt_page_layout.assert_called_once()


if __name__ == '__main__':
    unittest.main()
