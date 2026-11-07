"""Filter of the order reports

Run from the project root with: python -m unittest discover tests
"""

# standard library
import os
import sys
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# application modules
from App.Report import NotEnoughtReportParameters
from App.Report.Order import _orderConditions


def report(**conditions) -> SimpleNamespace:
    "A report whose conditions are field: code"
    return SimpleNamespace(conditions={field: SimpleNamespace(code=code) for field, code in conditions.items()})


class OrderConditionsTest(unittest.TestCase):

    def test_order_and_department(self) -> None:
        where = _orderConditions(report(**{'oh.order_header_id': 'order_id', 'ohd.department_id': 'department_id',
                                           'oh.delivery': 'delivery_type'}), 5, 2)
        self.assertEqual(where, [('oh.order_header_id = %s', 5), ('ohd.department_id = %s', 2)])

    def test_report_without_order_id_is_refused(self) -> None:
        "It would print every order of the archive"
        with self.assertLogs('App.Report.Order', 'ERROR'), self.assertRaises(NotEnoughtReportParameters):
            _orderConditions(report(**{'ohd.department_id': 'department_id'}), 5, 2)

    def test_shipped_order_reports_have_order_id(self) -> None:
        import xml.etree.ElementTree as ET
        for path in sorted((ROOT / 'Report').glob('*.rpt.zip')):
            with zipfile.ZipFile(path) as archive:
                report_class = archive.read('class').decode().strip()
                if report_class not in ('ORDER_CUSTOMER', 'ORDER_DEPARTMENT', 'ORDER_COVER'):
                    continue
                codes = {c.attrib.get('code') for c in ET.fromstring(archive.read('xml')).iter('condition')}
            with self.subTest(report=path.name):
                self.assertIn('order_id', codes)


if __name__ == '__main__':
    unittest.main()
