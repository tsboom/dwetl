import unittest
from tests.temporary_test_file import TemporaryTestFile
from dwetl.reader.mpf_file_reader import MpfFileReader


class TestMpfFileReader(unittest.TestCase):
    def test_simple_mpf(self):
        lines = [
            'field1\tfield2\tfield3',
            'A\tB\tC',
            'One\tTwo\tThree',
        ]

        expected_line1 = {'field1': 'A', 'field2': 'B', 'field3': 'C'}
        expected_line2 = {'field1': 'One', 'field2': 'Two', 'field3': 'Three'}

        with TemporaryTestFile(lines) as tempFilePath:
            mpf_file_reader = MpfFileReader(tempFilePath)
            line1 = next(iter(mpf_file_reader))
            line2 = next(iter(mpf_file_reader))
            self.assertEqual(expected_line1, line1)
            self.assertEqual(expected_line2, line2)

    def test_simple_mpf_with_incomplete_row(self):
        lines = [
            'field1\tfield2\tfield3',
            'A\tB\tC',
            'One',
        ]

        expected_line1 = {'field1': 'A', 'field2': 'B', 'field3': 'C'}
        expected_line2 = {'field1': 'One'}

        with TemporaryTestFile(lines) as tempFilePath:
            mpf_file_reader = MpfFileReader(tempFilePath)
            line1 = next(iter(mpf_file_reader))
            line2 = next(iter(mpf_file_reader))
            self.assertEqual(expected_line1, line1)
            self.assertEqual(expected_line2, line2)

    def test_mpf_item_process_status_dimension(self):
        expected_line = {
            'Member Library Code': 'BC',
            'IPS Code': 'WA',
            'IPS Public Description': 'withdrawn',
            'IPS Internal Description': 'Shared Print item withdrawn for allowed reason',
            'Data Maintenance Operation Code': 'I',
            'LMS Staff Account Identifier': 'lseguin',
            'Effective Date': '2019-06-18',
        }

        tsv_file_reader = MpfFileReader('tests/data/mpf_item-process-status-dimension.txt')
        line1 = next(iter(tsv_file_reader))
        self.assertEqual(expected_line, line1)
