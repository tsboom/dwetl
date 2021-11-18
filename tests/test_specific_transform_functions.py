import unittest
from dwetl import specific_transform_functions



'''
specific_transform_functions.py tests
'''

class TestSpecificTransformFunctions(unittest.TestCase):

    # def test_isbn_code_020(self):
    #     #test isbn_issn check function
    #     field = TransformField('z13_isbn_issn','177091921X','020')
    #     self.assertEqual(specific_transform_functions.isbn_code_020(field),'177091921X')
    # 
    #     field = TransformField('z13_isbn_issn','177091921X','022')
    #     self.assertEqual(specific_transform_functions.issn_code_022(field),'177091921X')
    # def test_remove_ocm_ocn_on(self):
    #     self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('ocn748578120'),'748578120')
    #     self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('ocm00003739'),'00003739')
    #     self.assertEqual(specific_transform_functions.remove_ocm_ocn_on('on1038022607'),'1038022607')

    # testing lookup_tables/record_type_code.csv for bib rec z13u
    def test_lookup_record_type(self):
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^nam^^2200241d1^45^0'),'Language material')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^ncm^^2200241d1^45^0'),'Notated music')
        self.assertEqual(specific_transform_functions.lookup_record_type('^^^^^ndm^^2200241d1^45^0'),'Manuscript notated music')
        
    def test_lookup_bibliographic_level(self):
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nam^^2200241d1^45^0'),'Monograph/Item')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nab^^2200241d1^45^0'),'Serial component part')
        self.assertEqual(specific_transform_functions.lookup_bibliographic_level('^^^^^nac^^2200241d1^45^0'),'Collection')
    # def test_is_suppressed(self):
    #     #test to confirm is_suppressed works with upper, lower, mixed, and fail
    #     field = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG', 'suppressed')
    #     self.assertEqual(specific_transform_functions.is_suppressed(field),'Y')
    #     field = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG', 'SuPpReSsEd')
    #     self.assertEqual(specific_transform_functions.is_suppressed(field), 'Y')
    #     field = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG', 'Shpoomples')
    #     self.assertEqual(specific_transform_functions.is_suppressed(field),'N')

    # def test_is_acq_created(self):
    #     #test to confirm is_acq_created works with upper, lower, mixed, and fail
    #     field = TransformField('z13u_user_defined_6','acq-created ||')
    #     self.assertEqual(specific_transform_functions.is_acq_created(field),'Y')
    #     field = TransformField('z13u_user_defined_6','ACQ-CREATED ||')
    #     self.assertEqual(specific_transform_functions.is_acq_created(field),'Y')
    #     field = TransformField('z13u_user_defined_6','NOT-acq-created')
    #     self.assertEqual(specific_transform_functions.is_acq_created(field),'Y')
    #     field = TransformField('z13u_user_defined_6','Shpoomples')
    #     self.assertEqual(specific_transform_functions.is_acq_created(field),'N')
    # 
    # def test_is_circ_created(self):
    #     #test to confirm is_circ_created works with upper, lower, mixed, and fail
    #     field = TransformField('z13u_user_defined_6','circ-created suppressed ||')
    #     self.assertEqual(specific_transform_functions.is_circ_created(field),'Y')
    #     field = TransformField('z13u_user_defined_6','CIRC-CREATED SUPPRESSED || ')
    #     self.assertEqual(specific_transform_functions.is_circ_created(field),'Y')
    #     field = TransformField('z13u_user_defined_6','Shpoomples')
    #     self.assertEqual(specific_transform_functions.is_circ_created(field),'N')
    # 
    # def test_is_provisional(self):
    #     #test to confirm is_provisional works with upper, lower, mixed, and fail
    #     field = TransformField('z13u_user_defined_6', 'provisional')
    #     self.assertEqual(specific_transform_functions.is_provisional(field), 'Y')
    # 
    #     field = TransformField('z13u_user_defined_6', 'pRoViSiOnAl')
    #     self.assertEqual(specific_transform_functions.is_provisional(field), 'Y')
    # 
    #     field = TransformField('z13u_user_defined_6', 'Shpoomples')
    #     self.assertEqual(specific_transform_functions.is_provisional(field), 'N')



if __name__ == '__main__':
    unittest.main()
