import unittest
from table_transform import *
import os
from .data.test_variables import *
from TransformField import *


class Test_z30_rec_key(unittest.TestCase):

    # def setUp(self):



    def test_valid_z30_rec_key(self):
        # setUp
        # load table config JSON
        table_config_path = os.path.join('table_config', 'library_item_dimension.json')
        table_config = load_table_config(table_config_path)

        # create dict
        # z30_rec_key = {'in_z30_rec_key': '000001200000020'}
        z30_rec_key = TransformField('in_z30_rec_key', '000001200000020')

        # feed into something
        transform_field(z30_rec_key, table_config)

        # test pp
        self.assertEqual('000001200000020', z30_rec_key.record['pp'])
        # test dq
        expected_dqs = [
            {'name': 'no_missing_values', 'result': '000001200000020', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID'},
            {'name': 'is_valid_length', 'result': '000001200000020', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID'},
             {'name': 'is_numeric', 'result': '000001200000020', 'target_col_name': 'LBRY_ITEM_SOURCE_SYSTEM_ID'}
        ]
        self.assertEqual(expected_dqs, z30_rec_key.record['dq'])


        # test transforms
        expected_transforms = [
            None,
            {'name': 'substring','result': '000001200','target_col_name': 'lbry_item_adm_no'},
            {'name': 'substring', 'result': '000020', 'target_col_name': 'lbry_item_seq_no'}
        ]
        self.assertEqual(expected_transforms, z30_rec_key.record['transforms'])


    # do replacement value checks later
    # def test_missing_z30_rec_key(self):


if __name__ == '__main__':
    unittest.main()
