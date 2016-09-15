import csv
import mock
from unittest import TestCase

import app.file_generator as fg


class TestJsonGenerator(TestCase):

    @mock.patch('app.file_generator.json.dumps', return_value='test')
    def test_generate_json_empty_data(self, jsn):
        test_data = []
        temp = fg.generate_json(test_data)
        self.assertEqual(temp.read(), 'test')
        jsn.assert_called_once_with(test_data, indent=None)

    @mock.patch('app.file_generator.json.dumps', return_value='test')
    def test_generate_json(self, jsn):
        test_data = {'test': 'data'}
        temp = fg.generate_json(test_data, indent=4)
        self.assertFalse(temp.closed)
        self.assertEqual(temp.tell(), 0)
        self.assertEqual(temp.read(), 'test')
        temp.close()
        jsn.assert_called_once_with(test_data, indent=4)


class TestCsvGenerator(TestCase):

    def test_generate_csv_empty_data(self):
        test_data = []
        temp = fg.generate_csv(test_data, delimiter=',',
                               quoting=csv.QUOTE_NONE)
        self.assertFalse(temp.closed)
        self.assertEqual(temp.readlines(), test_data)

    @mock.patch('app.file_generator.csv')
    def test_generate_csv(self, dictwr):
        test_data = [{'test': 'data'}]
        temp = fg.generate_csv(test_data, delimiter=',',
                               quoting=dictwr.QUOTE_NONE)
        self.assertFalse(temp.closed)
        dictwr.DictWriter.assert_called_once_with(temp,
                                                  delimiter=',',
                                                  fieldnames=['test'],
                                                  quoting=dictwr.QUOTE_NONE)
        dictwr.DictWriter.return_value.writerow.\
            assert_called_once_with(test_data[0])


class TestPdfGenerator(TestCase):

    @mock.patch('app.file_generator.render_template', return_value='pdftemp')
    @mock.patch('app.file_generator.pisa.CreatePDF', return_value='pdf')
    def test_generate_pdf_empty_data(self, pdf, template):
        test_data = []
        temp = fg.generate_pdf(test_data, template='/testtemplate.html')
        self.assertFalse(temp.closed)
        template.assert_called_once_with('/testtemplate.html', items=test_data)
        pdf.assert_called_once_with(template.return_value, dest=temp)

    @mock.patch('app.file_generator.render_template', return_value='pdftemp')
    @mock.patch('app.file_generator.pisa.CreatePDF', return_value='pdf')
    def test_generate_pdf(self, pdf, template):
        test_data = [{'test': 'data'}]
        temp = fg.generate_pdf(test_data, template='/testtemplate.html')
        self.assertFalse(temp.closed)
        template.assert_called_once_with('/testtemplate.html', items=test_data)
        pdf.assert_called_once_with(template.return_value, dest=temp)
