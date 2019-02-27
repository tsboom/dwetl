import dwetl
import os
import pdb




'''
TSV tests
'''
VALID_TEST_TSV_PATH = os.path.join('tests','data','mai50_z30_20190102_034001_data')
INVALID_MISSING_HEADER_TSV_PATH = os.path.join('tests','data','test_mai50_z30_20190102_034001_data_invalid_header')

def test_parse_tsv_filename():
    tsv_name_metadata = dwetl.parse_tsv_filename(VALID_TEST_TSV_PATH)
    assert tsv_name_metadata['library'] == 'mai50'
    assert tsv_name_metadata['table'] == 'z30'
    assert tsv_name_metadata['datetime'] == '20190102034001'
    # assert tsv_name_metadata['counter'] == 1

# ensure TSV file has at least 3 rows (header, footer, content)
def test_tsv_file_row_count():
    assert dwetl.tsv_has_valid_row_count(test_dataframe) == True

def test_tsv_contains_valid_header():
    assert dwetl.tsv_has_header(test_tsv) == True
    assert dwetl.tsv_has_header(test_tsv_missing_header) == False

# check to see if tsv can be imported into not empty dataframe
test_dataframe = None
test_dataframe_missing_header = None

def test_read_dataframe():
    test_dataframe = dwetl.read_tsv_into_dataframe(VALID_TEST_TSV_PATH)
    test_dataframe_missing_header = dwetl.read_tsv_into_dataframe(INVALID_MISSING_HEADER_TSV_PATH)
    assert test_dataframe.empty == False
