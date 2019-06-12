#import dw_etl
import os
import pdb
<<<<<<< HEAD
import table_transform
import unittest



=======
import unittest

from table_transform import *
>>>>>>> 2b1064dc57f3e8aaf4e135fba6c9166e159e637e


'''
Unit tests for table_transform.py
'''
<<<<<<< HEAD
VALID_TEST_TSV_PATH = os.path.join('tests','data','mai50_z305_20181115_172016_1.tsv')


# check to see if tsv can be imported into not empty dataframe
#def test_load_table_config():
#    assert table_config['title'] == 'z30'
class TestTableTransform(unittest.TestCase):
    def test_load_table_config(self):
        TABLE_PATH = os.path.join('tests','data','test_table_config_z30.json')
        table_config = table_transform.load_table_config(TABLE_PATH)
        self.assertEqual(table_config['title'],'z30')
=======

class TestTableTransform(unittest.TestCase):

    def test_check_data_quality():
>>>>>>> 2b1064dc57f3e8aaf4e135fba6c9166e159e637e

        # when there's no dq check, field.value is used

<<<<<<< HEAD
#VALID_TEST_TSV_PATH = os.path.join('tests','data','test_mai50_z305_20181115_172016_1.tsv')
#df = dwetl.read_tsv_into_dataframe(VALID_TEST_TSV_PATH)
=======
        # each dq check is called with its parameters provided
>>>>>>> 2b1064dc57f3e8aaf4e135fba6c9166e159e637e

        # field.value is used whenever a dq check is passing
        self.assertTrue(data_quality_utilities.is_valid_length(5634563, 7))

        # replacement_value is used whenever dq check is failing

        







if __name__ == '__main__':
    unittest.main()
####
'''

input type -> target type change
field name change
data quality checks executed
gets put in the target dimension
possible field-unique conversion function
one field broken up into multiple in target
'''
