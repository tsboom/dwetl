import dwetl
import os
import pdb
import unittest

from table_transform import *


'''
Unit tests for table_transform.py
'''

class TestTableTransform(unittest.TestCase):

    def test_check_data_quality():

        # when there's no dq check, field.value is used

        # each dq check is called with its parameters provided

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
