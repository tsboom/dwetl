#import dw_etl
import os
import pdb
import unittest
from table_transform import *
from .data.test_variables import *
from TransformField import *

'''
Unit tests for table_transform.py
'''

class TestTableTransform(unittest.TestCase):

    def test_load_table_config(self):
        TABLE_PATH = os.path.join('tests','data','test_table_config_z30.json')
        table_config = load_table_config(TABLE_PATH)
        self.assertEqual(table_config['title'],'z30')

    def test_get_isbn_issn_code(self):
        self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_none),'   ')

        self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_020),'020')

        self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_022),'022')

        self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_0220),'022')

    def test_preprocess(self):
        #testing trim preprocessing function
        a = TransformField('in_z13_title','   A title with some extraneous spaces     ')
        self.assertEqual(preprocess(a,data_source_col_sorted),'A title with some extraneous spaces')

        #testing date no preprocessing no output $$$this is a bad test as processing occurs after dq whoops
        b = TransformField('in_z13_open_date',20021124)
        self.assertEqual(preprocess(b,data_source_col_sorted),20021124)

        #testing terminal output of no preprocessing
        #c = TransformField('in_z13_upd_time_stamp',201708251637466)
        #with self.assertRaises(KeyError):
        #    preprocess(c,data_source_col_sorted)
            #doesn't seem to be working with the KeyError?

        #z13u preprocess test

#    def test_dq_func_list(self):

    def test_func_from_mod(self):
        dqu_check = functions_from_module(dqu)
        dqs_check = functions_from_module(dqs)

        #test output is list
        self.assertIsInstance(dqu_check, list)
        self.assertIsInstance(dqs_check, list)

        '''test sys generated list of function name matches established test variable, if new checks are added, this test will fail, so a nice check on future wor;
        I'm honestly not sure how to work with the regularly returned output of functions_from_module '''
        func_names = []
        for i in dqu_check:
            func_names.append(i[0])
        for i in func_names:
            self.assertTrue(i in dqu_func_names_list)

        spec_func_names = []
        for i in dqs_check:
            spec_func_names.append(i[0])
        for i in spec_func_names:
            self.assertTrue(i in dqs_func_names_list)

#    def test_run_dq_checks(self):

#    def test_check_dq(self):

    def test_exec_dq_func(self):

        dq_funcs_list = functions_from_module(dqs) + functions_from_module(dqu)

        #test no_missing_values
        self.assertTrue(execute_dq_function('no_missing_values','',20021124,dq_funcs_list))
        self.assertFalse(execute_dq_function('no_missing_values','',0,dq_funcs_list))

        #test dq_z13_user_defined_2
        self.assertTrue(execute_dq_function('dq_z13u_user_defined_2','','ocm00024372',dq_funcs_list))
        self.assertFalse(execute_dq_function('dq_z13u_user_defined_2','','ocm333',dq_funcs_list))
        self.assertTrue(execute_dq_function('dq_z13u_user_defined_2','','ocn464584694',dq_funcs_list))
        self.assertTrue(execute_dq_function('dq_z13u_user_defined_2','','on1245789453',dq_funcs_list))

#    def test_check_data_quality():

        # when there's no dq check, field.value is used

        # each dq check is called with its parameters provided

        # field.value is used whenever a dq check is passing
#        self.assertTrue(data_quality_utilities.is_valid_length(5634563, 7))

        # replacement_value is used whenever dq check is failing

#







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
