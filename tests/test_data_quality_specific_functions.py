import unittest
from dwetl import data_quality_specific_functions

'''
data_quality_specific_functions.py tests
'''

class TestDataQualitySpecificFunctions(unittest.TestCase):

    def test_dq_z30_temp_location(self):
        self.assertTrue(data_quality_specific_functions.dq_z30_temp_location('Y'))
        self.assertTrue(data_quality_specific_functions.dq_z30_temp_location('N'))
        self.assertFalse(data_quality_specific_functions.dq_z30_temp_location('NotYesOrNo'))

    def test_dq_z30_call_no_type__valid_cal_no_type(self):
        self.assertTrue(data_quality_specific_functions.dq_z30_call_no_type__valid_cal_no_type('1'))
        self.assertTrue(data_quality_specific_functions.dq_z30_call_no_type__valid_cal_no_type('-M'))
        self.assertFalse(data_quality_specific_functions.dq_z30_call_no_type__valid_cal_no_type('9'))
        self.assertFalse(data_quality_specific_functions.dq_z30_call_no_type__valid_cal_no_type(''))
        self.assertFalse(data_quality_specific_functions.dq_z30_call_no_type__valid_cal_no_type(None))

    def test_dq_z13u_user_defined_10__valid_holding_own_code(self):
        self.assertTrue(data_quality_specific_functions.dq_z13u_user_defined_10__valid_holding_own_code('SMHOL'))
        self.assertFalse(data_quality_specific_functions.dq_z13u_user_defined_10__valid_holding_own_code(''))
        self.assertFalse(data_quality_specific_functions.dq_z13u_user_defined_10__valid_holding_own_code(None))

    def test_dq_z13u_user_defined_2(self):
        self.assertTrue(data_quality_specific_functions.dq_z13u_user_defined_2('ocm00003739'))
        self.assertTrue(data_quality_specific_functions.dq_z13u_user_defined_2('ocn000037390'))
        self.assertTrue(data_quality_specific_functions.dq_z13u_user_defined_2('on0000037390'))
        self.assertTrue(data_quality_specific_functions.dq_z13u_user_defined_2(''))
        self.assertFalse(data_quality_specific_functions.dq_z13u_user_defined_2('doesntstartwithocstuff'))
        self.assertFalse(data_quality_specific_functions.dq_z13u_user_defined_2('lengthistoolong123940124814'))









if __name__ == '__main__':
    unittest.main()
