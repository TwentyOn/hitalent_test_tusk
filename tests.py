import datetime
import unittest
import xml.etree.ElementTree as ET

from main import build_yml, PRODUCTS, CATEGORIES


class TestF(unittest.TestCase):
    def setUp(self):
        xml = build_yml(PRODUCTS, CATEGORIES, datetime.datetime.today())
        self.xml = ET.fromstring(xml)

    def test_categories(self):
        self.assertIn('1', [item.get('id') for item in self.xml.findall('.//categories/category')])
        self.assertIn('2', [item.get('id') for item in self.xml.findall('.//categories/category')])
        self.assertNotIn('3', [item.get('id') for item in self.xml.findall('.//categories/category')])


    def test_offers(self):
        self.assertIn('101', [item.get('id') for item in self.xml.findall('.//offers/offer')])
        self.assertIn('102', [item.get('id') for item in self.xml.findall('.//offers/offer')])
        self.assertIn('107', [item.get('id') for item in self.xml.findall('.//offers/offer')])
        self.assertNotIn('103', [item.get('id') for item in self.xml.findall('.//offers/offer')])
        self.assertNotIn('104', [item.get('id') for item in self.xml.findall('.//offers/offer')])
        self.assertNotIn('105', [item.get('id') for item in self.xml.findall('.//offers/offer')])
        self.assertNotIn('106', [item.get('id') for item in self.xml.findall('.//offers/offer')])


if __name__ == '__main__':
    unittest.main()
