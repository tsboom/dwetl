#import dw_etl
import os
import pdb
import table_transform
import unittest





'''
Test Table Transform
'''
VALID_TEST_TSV_PATH = os.path.join('tests','data','mai50_z305_20181115_172016_1.tsv')


# check to see if tsv can be imported into not empty dataframe
#def test_load_table_config():
#    assert table_config['title'] == 'z30'
class TestTableTransform(unittest.TestCase):
    def test_load_table_config(self):
        TABLE_PATH = os.path.join('tests','data','test_table_config_z30.json')
        table_config = table_transform.load_table_config(TABLE_PATH)
        self.assertEqual(table_config['title'],'z30')


#VALID_TEST_TSV_PATH = os.path.join('tests','data','test_mai50_z305_20181115_172016_1.tsv')
#df = dwetl.read_tsv_into_dataframe(VALID_TEST_TSV_PATH)

# def test_transform_field():
    # check to see if target row increases when a field is transformed

    # check to see if source field exists, that target field is there

    # transform_field(df[3], target_row)
    # print(df[3])

# def test_field_exceptions():





####
'''

input type -> target type change
field name change
data quality checks executed
gets put in the target dimension
possible field-unique conversion function
one field broken up into multiple in target
'''

# target_row
# for field in row:
#     transform_field(source_field, target_row)
