import unittest
from table_transform import *
import os
from .data.test_variables import *
from TransformField import *


class Test_z30_rec_key(unittest.TestCase):

    def setUp(self):
        # load table config JSON
        table_config_path = os.path.join('table_config', 'library_item_dimension.json')
        self.table_config = load_table_config(table_config_path)


    def test_valid_z30_rec_key(self):
        # create field object
        z30_rec_key = TransformField('in_z30_rec_key', '000001200000020')

        # feed into something
        transform_field(z30_rec_key, self.table_config)

        # test pp
        self.assertEqual('000001200000020', z30_rec_key.record['pp'])
        # test dq
        expected_dqs = [
            {'name': 'no_missing_values', 'result': '000001200000020', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID', 'check_passed': True},
            {'name': 'is_valid_length', 'result': '000001200000020', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID', 'check_passed': True},
            {'name': 'is_numeric', 'result': '000001200000020', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID', 'check_passed': True}
        ]
        self.assertEqual(expected_dqs, z30_rec_key.record['dq'])


        # test transforms
        expected_transforms = [
            None,
            {'name': 'substring','result': '000001200','target_col_name': 'lbry_item_adm_no'},
            {'name': 'substring', 'result': '000020', 'target_col_name': 'lbry_item_seq_no'}
        ]
        self.assertEqual(expected_transforms, z30_rec_key.record['transforms'])


    def test_missing_z30_rec_key(self):
        z30_rec_key = TransformField('in_z30_rec_key', '')
        transform_field(z30_rec_key, self.table_config)

        # test expected dqs
        # Decide what DQ failed result should be
        expected_dqs = [
            {'name': 'no_missing_values', 'result': '', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID', 'check_passed': False},
            {'name': 'is_valid_length', 'result': '', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID',
             'check_passed': False},
            {'name': 'is_numeric', 'result': '', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID',
             'check_passed': False}

        ]
        self.assertEqual(expected_dqs, z30_rec_key.record['dq'])




if __name__ == '__main__':
    unittest.main()
