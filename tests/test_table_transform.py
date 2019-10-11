# #import dw_etl
# import os
# import pdb
# import unittest
# from dwetl import table_transform
# from dwetl.transform_field import TransformField
# import dwetl.data_quality_specific_functions as dqs
# import dwetl.data_quality_utilities as dqu
#
# '''
# Unit tests for table_transform.py
# '''
#
# class TestTableTransform(unittest.TestCase):
#     @unittest.skip
#     def test_get_isbn_issn_code(self):
#         self.assertEqual(table_transform.get_isbn_issn_code('in_z13_isbn_issn', table_transform.data_get_isbn_issn_none),'   ')
#         self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_020),'020')
#         self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_022),'022')
#         self.assertEqual(get_isbn_issn_code('in_z13_isbn_issn',data_get_isbn_issn_0220),'022')
#
#     def test_preprocess(self):
#         # get table_config
#         TABLE_PATH = os.path.join('table_config', 'bibliographic_record_dimension.json')
#         table_config = table_transform.load_table_config(TABLE_PATH)
#         #testing trim preprocessing function
#         a = TransformField('in_z13_title','   A title with some extraneous spaces     ')
#         # pdb.set_trace()
#         self.assertEqual(table_transform.preprocess(a, table_config), 'A title with some extraneous spaces')
#
#         # testing date no preprocessing no output $$$this is a bad test as processing occurs after dq whoops
#         b = TransformField('in_z13_open_date',20021124)
#         self.assertEqual(table_transform.preprocess(b, table_config), 20021124)
#
#         # testing terminal output of no preprocessing
#         # c = TransformField('in_z13_upd_time_stamp',201708251637466)
#         # with self.assertRaises(KeyError):
#         #    preprocess(c,data_source_col_sorted)
#             #doesn't seem to be working with the KeyError?
#
#         #z13u preprocess test
#
#
#
# #    def test_run_dq_checks(self):
#
# #    def test_check_dq(self):
#
#     def test_exec_dq_func(self):
#
#         dq_funcs_list = table_transform.functions_from_module(dqs) + table_transform.functions_from_module(dqu)
#
#         #test no_missing_values
#         self.assertTrue(table_transform.execute_dq_function('no_missing_values', '', '20021124', dq_funcs_list))
#         self.assertFalse(table_transform.execute_dq_function('no_missing_values', '', '0', dq_funcs_list))
#
#         #test dq_z13_user_defined_2
#         self.assertTrue(table_transform.execute_dq_function('dq_z13u_user_defined_2','','ocm00024372',dq_funcs_list))
#         self.assertFalse(table_transform.execute_dq_function('dq_z13u_user_defined_2','','ocm333',dq_funcs_list))
#         self.assertTrue(table_transform.execute_dq_function('dq_z13u_user_defined_2','','ocn464584694',dq_funcs_list))
#         self.assertTrue(table_transform.execute_dq_function('dq_z13u_user_defined_2','','on1245789453',dq_funcs_list))
#
#
#
# #    def test_check_data_quality():
#
#         # when there's no dq check, field.value is used
#
#         # each dq check is called with its parameters provided
#
#         # field.value is used whenever a dq check is passing
# #        self.assertTrue(data_quality_utilities.is_valid_length(5634563, 7))
#
#         # replacement_value is used whenever dq check is failing
#
#     def test_get_replacement_value(self):
#         self.assertEqual(table_transform.get_replacement_value({}), '')
#         self.assertEqual(table_transform.get_replacement_value({'replacement_value': ''}), '')
#         self.assertEqual(table_transform.get_replacement_value({'replacement_value':'(null)'}), None)
#         self.assertEqual(table_transform.get_replacement_value({'replacement_value':'N/A'}), '')
#         self.assertEqual(table_transform.get_replacement_value({'replacement_value':'-M'}), '-M')
#
#     def test_is_suspend_record(self):
#         # get table_config
#         TABLE_PATH = os.path.join('table_config', 'library_item_dimension.json')
#         table_config = table_transform.load_table_config(TABLE_PATH)
#         # normal value
#         field = TransformField('in_z30_rec_key', '000001200000020')
#         table_transform.transform_field(field, table_config)
#         self.assertFalse(table_transform.is_suspend_record(field, table_config))
#
#         # testing field.value is empty
#         field = TransformField('in_z30_rec_key', ' ')
#         table_transform.transform_field(field, table_config)
#         self.assertTrue(table_transform.is_suspend_record(field, table_config))
#
#         # check record that fails dq, but isn't suspended
#         field = TransformField('in_z30_barcode', '    31430058801988       ')
#         table_transform.transform_field(field, table_config)
#         self.assertFalse(field.is_valid())
#         self.assertFalse(table_transform.is_suspend_record(field, table_config))
#
#
#     def test_convert_suspend_record_bool(self):
#         self.assertTrue(table_transform.convert_suspend_record_bool('Yes'))
#         self.assertFalse(table_transform.convert_suspend_record_bool('No'))
#         self.assertFalse(table_transform.convert_suspend_record_bool(''))
#
#
#
#
#
# if __name__ == '__main__':
#     unittest.main()
# ####
# '''
# input type -> target type change
# field name change
# data quality checks executed
# gets put in the target dimension
# possible field-unique conversion function
# one field broken up into multiple in target
# '''
