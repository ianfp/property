from django.test import TestCase
from datetime import date
from tasks.services import _parse_last_done

class ImportCsvTest(TestCase):
    def test_parse_last_done(self):
        tests = {
            '2012': date(2012, 1, 1),
            '2012-01': date(2012, 1, 1),
            '2012-02': date(2012, 2, 1),
            '2012-06-01': date(2012, 6, 1),
            '2012-12-31': date(2012, 12, 31),
        }
        
        for string, expected in tests.items():
            result = _parse_last_done(string)
            self.assertIsInstance(result, date)
            self.assertEqual(expected, result)