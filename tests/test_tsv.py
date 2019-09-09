from dwetl import loadstg1
import os
import pdb
import unittest


'''
TSV tests
'''
VALID_TEST_TSV_PATH = os.path.join('tests','data','mai50_z30_20190102_034001_data')
INVALID_MISSING_HEADER_TSV_PATH = os.path.join('tests','data','test_mai50_z30_20190102_034001_data_invalid_header')

#get_headers_footer
#validate_header1
#valideate_header2
#validate_footer
#
class TestTSV(unittest.TestCase):

    def test_parse_tsv_filename(self):
        hhf_dict = loadstg1.get_headers_footer(VALID_TEST_TSV_PATH)
        tsv_name_metadata = loadstg1.parse_tsv_filename(VALID_TEST_TSV_PATH, hhf_dict)
        self.assertEqual(tsv_name_metadata['library'],'mai50')
        self.assertEqual(tsv_name_metadata['table'],'z30')
        self.assertEqual(tsv_name_metadata['datetime'],'20190102034001')
    # assert tsv_name_metadata['counter'] == 1

# ensure TSV file has at least 3 rows (header, footer, content)
#    def test_tsv_file_row_count(self):
#        self.assertTrue(dwetl.tsv_has_valid_row_count(test_dataframe))

#    def test_tsv_contains_valid_header(self):
#        self.assertTrue(dwetl.tsv_has_header(test_tsv))
#        self.assertFalse(dwetl.tsv_has_header(test_tsv_missing_header))
