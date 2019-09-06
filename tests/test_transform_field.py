import pdb
import unittest
from TransformField import *

class TestTransformField(unittest.TestCase):

    # def test_load_table_config(self):
    #     TABLE_PATH = os.path.join('tests','data','test_table_config_z30.json')
    #     table_config = load_table_config(TABLE_PATH)
    #     self.assertEqual(table_config['title'],'z30')

    def test_is_valid(self):
        field = TransformField('in_z30_rec_key', '000001200000020')
        field.record_dq({'check_passed': True})
        field.record_dq({'check_passed': True})
        field.record_dq({'check_passed': True})
        self.assertTrue(field.is_valid())

        field = TransformField('in_z30_rec_key', '000001200000020')
        field.record_dq({'check_passed': True})
        field.record_dq({'check_passed': False})
        field.record_dq({'check_passed': True})
        self.assertFalse(field.is_valid())

        field = TransformField('in_z30_rec_key', '000001200000020')
        self.assertTrue(field.is_valid())



if __name__ == '__main__':
    unittest.main()
