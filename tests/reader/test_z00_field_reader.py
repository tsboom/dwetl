import unittest
from tests.temporary_test_file import TemporaryTestFile
from dwetl.reader.z00_field_reader import Z00FieldReader


class TestZ00FieldReader(unittest.TestCase):
    def test_simple_z00_field(self):

        lines = [
            'H\tDW Extract Job Number(work on this)\t2019-09-25 14:14:29\tdata/20190925/mai01_z800_20190925_141428_b',
            'z00_doc_number\tz30_marc_rec_field_cd\tUNUSED\tz00_marc_rec_field_txt',
            '000031180 FMT   L BK',
        ]

        expected_line1 = {'z00_doc_number': '000031180', 'z30_marc_rec_field_cd': 'FMT', 'UNUSED': 'L', 'z00_marc_rec_field_txt': 'BK'}

        with TemporaryTestFile(lines) as tempFilePath:
            z00_field_reader = Z00FieldReader(tempFilePath)
            line1 = next(iter(z00_field_reader))
            self.assertEqual(expected_line1, line1)

    def test_long_marc_txt_z00_field(self):

        lines = [
            'H\tDW Extract Job Number(work on this)\t2019-09-25 14:14:29\tdata/20190925/mai01_z800_20190925_141428_b',
            'z00_doc_number\tz30_marc_rec_field_cd\tUNUSED\tz00_marc_rec_field_txt',
            '000031180 77608 L $$iOnline version:$$tUniversals and particulars.$$b[1st ed.].$$dGarden City, N.Y., Anchor Books, 1970$$w(OCoLC)608874271'
        ]

        expected_result = {
            'z00_doc_number': '000031180',
            'z30_marc_rec_field_cd':'77608',
            'UNUSED': 'L',
            'z00_marc_rec_field_txt': '$$iOnline version:$$tUniversals and particulars.$$b[1st ed.].$$dGarden City, N.Y., Anchor Books, 1970$$w(OCoLC)608874271'
        }

        with TemporaryTestFile(lines) as tempFilePath:
            z00_field_reader = Z00FieldReader(tempFilePath)
            line = next(iter(z00_field_reader))
            self.assertEqual(expected_result, line)
    
