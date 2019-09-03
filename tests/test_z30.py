import unittest
from table_transform import *
import os
from .data.test_variables import *
from TransformField import *


class Test_z30_rec_key(unittest.TestCase):

    def setUp(self):
        # load table config JSON
        table_config_path = os.path.join('table_config', 'library_item_dimension.json')
        table_config = table_transform.load_table_config(table_config_path)


    def test_valid_z30_rec_key(self):
        # create dict
        z30_rec_key = {'in_z30_rec_key': '000001200000020'}

        # feed into something
        result = table_transform.transform_field(z30_rec_key, table_config)
        self.assertEqual('000001200000020', result['t1_z30_rec_key__lbry_item_source_system_id'])
        # self.assertEqual('000001200000020', result['pp_z30_rec_key'])
        # self.assertEqual('000001200000020', result['dq_z30_rec_key'])

    # do replacement value checks later
    # def test_missing_z30_rec_key(self):


if __name__ == '__main__':
    unittest.main()
