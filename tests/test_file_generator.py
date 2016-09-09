import csv
import json
from unittest import TestCase

import app.file_generator as fg


class TestJsonGenerator(TestCase):

    def test_generate_json_empty_data(self):
        test_data = []
        temp = fg.generate_json(test_data)
        self.assertEqual(temp.read(), json.dumps(test_data))

    def test_generate_json_invalid_indent(self):
        test_data = {'test': 'data'}
        self.assertRaises(TypeError, fg.generate_json,
                          test_data, indent='test')

    def test_generate_json(self):
        test_data = {'test': 'data'}
        temp = fg.generate_json(test_data)
        self.assertFalse(temp.closed)
        self.assertEqual(temp.tell(), 0)
        self.assertEqual(temp.read(), json.dumps(test_data))
        self.assertEqual(temp.read(), '')
        temp.seek(0)
        self.assertEqual(temp.read(), json.dumps(test_data))
        temp.close()
        self.assertTrue(temp.closed)


class TestCsvGenerator(TestCase):
    def test_generate_csv_empty_data(self):
        pass

    def test_generate_csv_invalid_args(self):
        pass

    def test_generate_csv(self):
        test_data = [{'test': 'data'}]
        temp = fg.generate_csv(test_data, delimiter=',',
                               quoting=csv.QUOTE_NONE)
        self.assertFalse(temp.closed)
        self.assertEqual(temp.tell(), 0)
        self.assertEqual(temp.read(), 'test\r\ndata\r\n')


class TestPdfGenerator(TestCase):

    def test_generate_pdf_empty_data(self):
        pass

    def test_generate_json_invalid_indent(self):
        pass

    def test_generate_pdf(self):
        pass
