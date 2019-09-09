import unittest
from dwetl import specific_transform_functions
from dwetl.transform_field import TransformField


'''
specific_transform_functions.py tests
'''

class TestSpecificTransformFunctions(unittest.TestCase):

    def test_isbn_code_020(self):
        #test isbn_issn check function
        field = TransformField('z13_isbn_issn','177091921X','020')
        self.assertEqual(specific_transform_functions.isbn_code_020(field),'177091921X')

        field = TransformField('z13_isbn_issn','177091921X','022')
        self.assertEqual(specific_transform_functions.issn_code_022(field),'177091921X')
    def test_remove_ocm_ocn_on(self):
        #test ocn recognition and transform
        c = TransformField('z13u_user_defined_2','ocn748578120')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on(c),'748578120')

        #test ocm recognition and transform
        d = TransformField('z13u_user_defined_2','ocm00003739')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on(d),'00003739')

        #test on recognition and transform
        e = TransformField('z13u_user_defined_2','on1038022607')
        self.assertEqual(specific_transform_functions.remove_ocm_ocn_on(e),'1038022607')

    def test_is_suppressed(self):
        #test to confirm is_suppressed works with upper, lower, mixed, and fail
        field = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG', 'suppressed')
        self.assertEqual(specific_transform_functions.is_suppressed(field),'Y')
        field = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG', 'SuPpReSsEd')
        self.assertEqual(specific_transform_functions.is_suppressed(field), 'Y')
        field = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG', 'Shpoomples')
        self.assertEqual(specific_transform_functions.is_suppressed(field),'N')

    def test_is_acq_created(self):
        #test to confirm is_acq_created works with upper, lower, mixed, and fail
        field = TransformField('z13u_user_defined_6','acq-created ||')
        self.assertEqual(specific_transform_functions.is_acq_created(field),'Y')
        field = TransformField('z13u_user_defined_6','ACQ-CREATED ||')
        self.assertEqual(specific_transform_functions.is_acq_created(field),'Y')
        field = TransformField('z13u_user_defined_6','NOT-acq-created')
        self.assertEqual(specific_transform_functions.is_acq_created(field),'Y')
        field = TransformField('z13u_user_defined_6','Shpoomples')
        self.assertEqual(specific_transform_functions.is_acq_created(field),'N')

    def test_is_circ_created(self):
        #test to confirm is_circ_created works with upper, lower, mixed, and fail
        field = TransformField('z13u_user_defined_6','circ-created suppressed ||')
        self.assertEqual(specific_transform_functions.is_circ_created(field),'Y')
        field = TransformField('z13u_user_defined_6','CIRC-CREATED SUPPRESSED || ')
        self.assertEqual(specific_transform_functions.is_circ_created(field),'Y')
        field = TransformField('z13u_user_defined_6','Shpoomples')
        self.assertEqual(specific_transform_functions.is_circ_created(field),'N')

    def test_is_provisional(self):
        #test to confirm is_provisional works with upper, lower, mixed, and fail
        field = TransformField('z13u_user_defined_6', 'provisional')
        self.assertEqual(specific_transform_functions.is_provisional(field), 'Y')

        field = TransformField('z13u_user_defined_6', 'pRoViSiOnAl')
        self.assertEqual(specific_transform_functions.is_provisional(field), 'Y')

        field = TransformField('z13u_user_defined_6', 'Shpoomples')
        self.assertEqual(specific_transform_functions.is_provisional(field), 'N')

    def test_sub_look_up(self):
        #test code lookup from CSV table
        f = TransformField('z13u_user_defined_3','750424m19769999wiub^^^^^b^^^^001^0^eng^^')
        self.assertEqual(specific_transform_functions.sub_look_up(f,'lookup_tables/encoding_level.csv',17,18),'Unknown')
        self.assertEqual(specific_transform_functions.sub_look_up(f,'lookup_tables/bibliographic_level.csv',6,7),'Monograph/Item')
        #blank vs ^? is there an established protocol for our data b/c there's a disagreement between data & lookups



if __name__ == '__main__':
    unittest.main()
