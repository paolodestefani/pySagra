"""Layouts, settings and CSV export of EnhancedTableView

Run from the project root with: python -m unittest discover tests
"""

# standard library
import csv
import os
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from unittest import mock

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# PySide6
from PySide6.QtCore import QAbstractTableModel, QDate, QLocale, QModelIndex, QSettings, Qt, QTime
from PySide6.QtGui import QGuiApplication
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMessageBox

# application modules
from App import session
from App.Widget import View


app = QApplication.instance() or QApplication([])


class Model(QAbstractTableModel):
    "The DisplayRole of bool columns is None, as in TableModel"

    heads = ['Id', 'Done', 'Price', 'Rate', 'Time', 'Date']

    def __init__(self) -> None:
        super().__init__()
        self.rows = [[1, True, Decimal('1234.50'), 1.5, QTime(12, 30), QDate(2026, 1, 2)],
                     [2, False, Decimal('3.00'), 2.25, None, None]]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.heads)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        value = self.rows[index.row()][index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            return None if isinstance(value, bool) else value
        if role == Qt.ItemDataRole.CheckStateRole and isinstance(value, bool):
            return Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.heads[section]
        return None


class ViewTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.columns: list = []
        self.saved: dict = {}
        patches = {'list_adaptation': lambda *a: [(1, 'Saved', True)],
                   'get_adapt_default': lambda *a: 1,
                   'get_view_columns': lambda view_id: self.columns,
                   'set_adapt_setting': lambda view_id, columns: self.saved.update(columns=columns)}
        for name, value in patches.items():
            patcher = mock.patch.object(View, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.dict(session, {'can_edit_views': True, 'user': 'u', 'qlocale': QLocale('it')})
        patcher.start()
        self.addCleanup(patcher.stop)

    def view(self) -> View.EnhancedTableView:
        view = View.EnhancedTableView(None)
        view.setModel(Model())
        view.resize(700, 200)
        view.show()
        QTest.qWaitForWindowExposed(view)
        self.addCleanup(view.deleteLater)
        return view


class LayoutTest(ViewTestCase):

    def test_form_settings_survive_the_layout(self) -> None:
        "FormViewManager.setView makes columns movable and sortable, then the form sets the layout name"
        view = self.view()
        view.horizontalHeader().setSectionsMovable(True)
        view.setSortingEnabled(True)
        view.setLayoutName('Test')
        QTest.qWait(30)
        self.assertTrue(view.horizontalHeader().sectionsMovable())
        self.assertTrue(view.cm_movable.isChecked())
        self.assertTrue(view.isSortingEnabled())

    def test_saved_order_and_visibility(self) -> None:
        order = [3, 0, 5, 1, 4, 2]
        self.columns = [(c, order[c], c != 4, 90) for c in range(6)]
        view = self.view()
        view.setLayoutName('Test')
        QTest.qWait(30)
        header = view.horizontalHeader()
        self.assertEqual([header.visualIndex(c) for c in range(6)], order)
        self.assertTrue(view.isColumnHidden(4))

    def test_view_deleted_before_the_layout_timer(self) -> None:
        view = View.EnhancedTableView(None)
        view.setModel(Model())
        view.setLayoutName('Test')
        view.deleteLater()
        QApplication.sendPostedEvents(None, 0)
        QTest.qWait(30)  # must not raise on a deleted object


class SettingsDialogTest(ViewTestCase):

    def test_show_a_hidden_column(self) -> None:
        view = self.view()
        view.hideColumn(2)
        dialog = View.ViewSettingsDialog(view)
        # through the model, as the check box delegate does
        model = dialog.ui.tableWidget.model()
        for row in range(model.rowCount()):
            if model.index(row, 0).data() == 2:
                model.setData(model.index(row, 3), True, Qt.ItemDataRole.EditRole)
        dialog.accept()
        self.assertFalse(view.isColumnHidden(2))
        self.assertGreater(view.columnWidth(2), 0)


class ExportTest(ViewTestCase):

    def export(self, locale: str) -> list[list[str]]:
        session['qlocale'] = QLocale(locale)
        folder = tempfile.mkdtemp()
        file_name = os.path.join(folder, 'out.csv')
        settings = mock.MagicMock()
        with mock.patch.object(View, 'QSettings', return_value=settings), \
             mock.patch.object(View.QFileDialog, 'getSaveFileName', lambda *a: (file_name, '')), \
             mock.patch.object(View.QMessageBox, 'question', lambda *a: QMessageBox.StandardButton.No):
            self.view().exportView()
        self.settings = settings
        with open(file_name, encoding='utf-8') as f:
            return list(csv.reader(f, delimiter=';'))

    def test_values_with_the_user_locale(self) -> None:
        rows = self.export('it')
        self.assertEqual(rows[0], Model.heads)
        self.assertEqual(rows[1][:4], ['1', 'I', '1234,50', '1,5'])
        self.assertEqual(rows[2][:4], ['2', 'O', '3,00', '2,25'])
        self.assertEqual(rows[1][4], QLocale('it').toString(QTime(12, 30), QLocale.FormatType.ShortFormat))
        self.assertEqual(rows[2][4:], ['', ''])

    def test_english_locale(self) -> None:
        rows = self.export('en')
        self.assertEqual(rows[1][2:4], ['1234.50', '1.5'])

    def test_export_folder_is_remembered(self) -> None:
        self.export('it')
        key = 'EnhancedTableView/ExportPath'
        self.settings.value.assert_called_with(key, mock.ANY)
        self.settings.setValue.assert_called_with(key, mock.ANY)


class CursorTest(ViewTestCase):
    "Questions and messages must not show the wait cursor"

    def cursor_during(self, method: str, *patches) -> list:
        view = self.view()
        view.setLayoutName('Test')
        QTest.qWait(30)
        seen = []

        def dialog(*args, **kwargs):
            cursor = QGuiApplication.overrideCursor()
            seen.append(cursor.shape() if cursor else None)
            return QMessageBox.StandardButton.Yes

        with mock.patch.object(View, 'is_system_object', lambda *a: False), \
             mock.patch.object(View, 'delete_adaptation'), \
             mock.patch.object(View, 'set_adapt_user_default'), \
             mock.patch.object(View, 'set_adapt_class_default'), \
             mock.patch.object(View.QMessageBox, 'question', dialog), \
             mock.patch.object(View.QMessageBox, 'information', dialog):
            getattr(view, method)()
        return seen

    def test_layout_management(self) -> None:
        for method in ('deleteViewLayout', 'updateViewLayout', 'setUserDefaultLayout', 'setClassDefaultLayout'):
            with self.subTest(method=method):
                seen = self.cursor_during(method)
                self.assertTrue(seen)
                self.assertEqual(seen, [None] * len(seen))


class RemoveTest(ViewTestCase):

    def test_no_question_without_a_row(self) -> None:
        view = self.view()
        view.setCurrentIndex(QModelIndex())
        with mock.patch.object(View.QMessageBox, 'question') as question:
            view.remove()
        question.assert_not_called()


if __name__ == '__main__':
    unittest.main()
