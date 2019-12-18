import unittest
from dwetl.data_quality_info import DataQualityInfo
import dwetl.data_quality_utilities as dqu

class TestDataQualityInfo(unittest.TestCase):
    def setUp(self):
        pass

    def test_data_quality_info_no_missing_values(self):
        json_config = {
            'specific_dq_function': 'no_missing_values',
            'specific_dq_function_param_1': '',
            'suspend_record': 'No',
            'exception_message': 'Missing Value',
            'replacement_value': 'Missing Value'
        }

        dq = DataQualityInfo(json_config)

        self.assertFalse(dq.suspend_record)
        self.assertEqual('Missing Value', dq.exception_message)
        self.assertEqual('Missing Value', dq.replacement_value)

        self.assertTrue(dq.validate('ABCD'))
        self.assertFalse(dq.validate(None))
        self.assertFalse(dq.validate(' '))
        self.assertFalse(dq.validate(''))
        self.assertFalse(dq.validate('0'))

    def test_data_quality_info_no_leading_spaces(self):
        json_config = {
            'specific_dq_function': 'no_leading_space',
            'specific_dq_function_param_1': '',
            'suspend_record': 'No',
            'exception_message': 'Leading Spaces',
            'replacement_value': 'Leading Spaces in Value'
        }

        dq = DataQualityInfo(json_config)

        self.assertFalse(dq.suspend_record)
        self.assertEqual('Leading Spaces', dq.exception_message)
        self.assertEqual('Leading Spaces in Value', dq.replacement_value)

        self.assertTrue(dq.validate('ABCD'))
        self.assertFalse(dq.validate(' ABCD'))
        self.assertFalse(dq.validate('   '))
        self.assertTrue(dq.validate('0'))

    def test_data_quality_info_length_check(self):
        json_config = {
            'specific_dq_function': 'is_valid_length',
            'specific_dq_function_param_1': '15',
            'suspend_record': 'Yes',
            'exception_message': 'Incorrect Length',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)

        self.assertTrue(dq.suspend_record)
        self.assertEqual('Incorrect Length', dq.exception_message)
        self.assertEqual(None, dq.replacement_value)

        # Too short
        self.assertFalse(dq.validate(''))
        self.assertFalse(dq.validate('ABCD'))
        self.assertFalse(dq.validate('12345678901234'))

        # Correct length
        self.assertTrue(dq.validate('ABCDEFGHIJKLMNO'))
        self.assertTrue(dq.validate('123456789012345'))

        # Too long
        self.assertFalse(dq.validate('ABCDEFGHIJKLMNOP'))
        self.assertFalse(dq.validate('1234567890123456'))
        self.assertFalse(dq.validate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    def test_data_quality_info_is_numeric(self):
        json_config = {
            'specific_dq_function': 'is_numeric',
            'specific_dq_function_param_1': '',
            'suspend_record': 'Yes',
            'exception_message': 'Non-numeric Value',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)

        self.assertTrue(dq.suspend_record)
        self.assertEqual('Non-numeric Value', dq.exception_message)
        self.assertEqual(None, dq.replacement_value)

        self.assertFalse(dq.validate('ABCD'))
        self.assertTrue(dq.validate('1236717823681'))
        self.assertTrue(dq.validate('0000'))
        self.assertFalse(dq.validate(''))
        self.assertTrue(dq.validate('0'))
        self.assertFalse(dq.validate('a1d3'))

    def test_data_quality_info_suspect_flag(self):
        json_config = {
            'specific_dq_function': 'is_valid_length',
            'specific_dq_function_param_1': '15',
            'suspend_record': 'Yes',
            'exception_message': 'Incorrect Length',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)
        self.assertTrue(dq.suspend_record)

        json_config = {
            'specific_dq_function': 'is_valid_length',
            'specific_dq_function_param_1': '15',
            'suspend_record': 'No',
            'exception_message': 'Incorrect Length',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)
        self.assertFalse(dq.suspend_record)

    def test_data_quality_info_has_replacement_value(self):
        json_config = {
            'specific_dq_function': 'is_valid_length',
            'specific_dq_function_param_1': '15',
            'suspend_record': 'Yes',
            'exception_message': 'Incorrect Length',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)
        self.assertFalse(dq.has_replacement_value())
        self.assertIsNone(dq.replacement_value)

        json_config = {
            'specific_dq_function': 'is_valid_length',
            'specific_dq_function_param_1': '15',
            'suspend_record': 'Yes',
            'exception_message': 'Incorrect Length',
            'replacement_value': '(null)'
        }
        dq = DataQualityInfo(json_config)
        self.assertTrue(dq.has_replacement_value())
        self.assertEqual('(null)', dq.replacement_value)

        json_config = {
            'specific_dq_function': 'is_valid_length',
            'specific_dq_function_param_1': '15',
            'suspend_record': 'No',
            'exception_message': 'Incorrect Length',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)
        self.assertFalse(dq.suspend_record)

    def test_dq_z30_temp_location(self):
        self.assertTrue(dqu.dq_z30_temp_location('Y'))
        self.assertTrue(dqu.dq_z30_temp_location('N'))
        self.assertFalse(dqu.dq_z30_temp_location('NotYesOrNo'))

    def test_dq_z30_call_no_type__valid_cal_no_type(self):
        self.assertTrue(dqu.dq_z30_call_no_type__valid_cal_no_type('1'))
        self.assertTrue(dqu.dq_z30_call_no_type__valid_cal_no_type('-M'))
        self.assertFalse(dqu.dq_z30_call_no_type__valid_cal_no_type('9'))
        self.assertFalse(dqu.dq_z30_call_no_type__valid_cal_no_type(''))
        self.assertFalse(dqu.dq_z30_call_no_type__valid_cal_no_type(None))

    def test_dq_z13u_user_defined_10__valid_holding_own_code(self):
        self.assertTrue(dqu.dq_z13u_user_defined_10__valid_holding_own_code('SMHOL'))
        self.assertFalse(dqu.dq_z13u_user_defined_10__valid_holding_own_code(''))
        self.assertFalse(dqu.dq_z13u_user_defined_10__valid_holding_own_code(None))

    def test_dq_z13u_user_defined_2(self):
        self.assertTrue(dqu.dq_z13u_user_defined_2('ocm00003739'))
        self.assertTrue(dqu.dq_z13u_user_defined_2('ocn000037390'))
        self.assertTrue(dqu.dq_z13u_user_defined_2('on0000037390'))
        self.assertTrue(dqu.dq_z13u_user_defined_2(''))
        self.assertFalse(dqu.dq_z13u_user_defined_2('doesntstartwithocstuff'))
        self.assertFalse(dqu.dq_z13u_user_defined_2('lengthistoolong123940124814'))
