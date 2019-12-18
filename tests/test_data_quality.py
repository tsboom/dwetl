# from dwetl import dw_etl
import datetime
import csv
import unittest
from dwetl import data_quality_utilities




'''
data_quality_utilities.py tests
'''

class TestDataQualityUtilities(unittest.TestCase):
    #test if right exceptions are thrown when given bad data

    #def test_is_numeric(self):

    def test_is_valid_length(self):
        #Test that matching len passes for stringified int
        self.assertTrue(data_quality_utilities.is_valid_length(5634563, 7))

        #test that too large len fails for stringified int
        self.assertFalse(data_quality_utilities.is_valid_length(5634563, 8))

        #Test that matching len passes
        self.assertTrue(data_quality_utilities.is_valid_length("mustard", 7))

        #Test that too small len fails
        self.assertFalse(data_quality_utilities.is_valid_length("mustard", 2))

        #Test that too large len fails
        self.assertFalse(data_quality_utilities.is_valid_length("mustard", 20))

    def test_is_less_than_eq_to_length(self):
        #Test that equal for string works
        self.assertTrue(data_quality_utilities.is_less_than_eq_to_length("mustard", 7))

        #Test that "less than" for string works
        self.assertTrue(data_quality_utilities.is_less_than_eq_to_length("must", 7))

        #Test that equal for stringified len works
        self.assertTrue(data_quality_utilities.is_less_than_eq_to_length(1234567, 7))

        #Test that "less than" for stringified len works
        self.assertTrue(data_quality_utilities.is_less_than_eq_to_length(2, 7))

        #Test that non-matching len fails for string
        self.assertFalse(data_quality_utilities.is_less_than_eq_to_length("mustard", 2))

        #Test that non-matching len fails for stringified int
        self.assertFalse(data_quality_utilities.is_less_than_eq_to_length(1234587, 2))

    def test_no_missing_values(self):
        # test None
        self.assertFalse(data_quality_utilities.no_missing_values(None))
        # test ''
        self.assertFalse(data_quality_utilities.no_missing_values(''))
        self.assertFalse(data_quality_utilities.no_missing_values(' '))
        self.assertFalse(data_quality_utilities.no_missing_values('      '))
        self.assertTrue(data_quality_utilities.no_missing_values('123'))
        self.assertFalse(data_quality_utilities.no_missing_values('0'))

    def test_trim(self):
        #Test leading and trailing space trimmed
        self.assertEqual(data_quality_utilities.trim("   mustard is cool   "), "mustard is cool")

        #Test that trailing space trimmed
        self.assertEqual(data_quality_utilities.trim("BL-BL "), "BL-BL")

        #Test that a not trimmed value is not returned
        self.assertNotEqual(data_quality_utilities.trim(" I can Haz Cheezburgr"), " I can Haz Cheezburgr")

    def test_is_valid_aleph_year(self):
        #Test that year in range passes function
        self.assertTrue(data_quality_utilities.is_valid_aleph_year(1999))

        #Test that current year passes function
        self.assertTrue(data_quality_utilities.is_valid_aleph_year(datetime.datetime.now().year))

        #Test that year outside range fails
        self.assertFalse(data_quality_utilities.is_valid_aleph_year(1899))

        #Test that string fails year check
        self.assertFalse(data_quality_utilities.is_valid_aleph_year("mustard"))

    # def test_is_valid_aleph_date():

    # def test_valid_aleph_date_redux(self):
    #     #Test that function run on stringified date for today returns True
    #     self.assertTrue(data_quality_utilities.is_valid_aleph_date_redux(datetime.datetime.now().strftime('%Y%m%d')))
    #
    #     #Test that invalid dates fail
    #     self.assertFalse(data_quality_utilities.is_valid_aleph_date_redux("02180101"))
    #
    #     # #Test int date
    #     # self.assertFalse(data_quality_utilities.is_valid_aleph_date_redux(20190101))
    #
    #     #Test impossible date
    #     with self.assertRaises(ValueError):
    #         data_quality_utilities.is_valid_aleph_date_redux("20190132")
    #     # This fails but throws a value error, should we plan to handle? Unittest handles with assertRaises, should function act accordingly?
    #
    #     #Test impossible date2
    #     with self.assertRaises(ValueError):
    #         data_quality_utilities.is_valid_aleph_date_redux("20190229")

#        with self.assertRaises(TypeError):
#            data_quality_utilities.is_valid_aleph_date_redux(20180101)
#        self.assertFalse(data_quality_utilities.is_valid_aleph_date_redux((datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')))

    def test_csv_to_dict(self):
        #Test that output is dict
        self.assertIsInstance(data_quality_utilities.create_dict_from_csv_redux("lookup_tables/call_no_type.csv"), dict)

        #Test that output is not int
        self.assertNotIsInstance(data_quality_utilities.create_dict_from_csv_redux("lookup_tables/call_no_type.csv"), int)

        #Test that output is not list
        self.assertNotIsInstance(data_quality_utilities.create_dict_from_csv_redux("lookup_tables/call_no_type.csv"), list)

        #Test that data count in dict matches data count in csv
        with open("lookup_tables/call_no_type.csv", "r") as file:
            csv_reader_object = csv.reader(file)
            row_count = sum(1 for row in csv_reader_object)
            self.assertEqual(len(data_quality_utilities.create_dict_from_csv_redux("lookup_tables/call_no_type.csv")), row_count)

    def test_is_valid_hour(self):
        #Tests based on sample data from Z35_EVENT_HOUR
        #Test that single character time stamp passes
        self.assertTrue(data_quality_utilities.is_valid_hour(5))

        #Test that 2-character time stamp passes
        self.assertTrue(data_quality_utilities.is_valid_hour(15))

        #Test that 3-character time stamp passes
        self.assertTrue(data_quality_utilities.is_valid_hour(730))

        #Test that 4-character time stamp passes
        self.assertTrue(data_quality_utilities.is_valid_hour(2050))

        #Test that out-of-range time stamp fails
        self.assertFalse(data_quality_utilities.is_valid_hour(2515))


#    def test_output_standard(self):
#        b = TransformField('')


if __name__ == '__main__':
    unittest.main()
