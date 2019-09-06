# from dwetl import dw_etl

import sys
from data_quality_utilities import *
from data_quality_specific_functions import *
from specific_transform_functions import *
from TransformField import TransformField
import unittest
#from unittest import mock
import datetime
import csv

'''
dataquality tests
'''

class TestDQ(unittest.TestCase):
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

# #spcific_transform_function tests
#     def test_substring(self):
#         self.assertEqual(specific_transform_functions())

#data_quality_specific_functions
    def test_dq_z13u_holding_code(self):

        #Test known value
        self.assertEqual(dq_z13u_user_defined_10__valid_holding_own_code("CP"), True)

        #Is it sufficient to run a test on a hard-coded value or is it better to dynamically pull data from source?
    def test_dq_z13u_user_defined_2(self):

        #test ocm number
        self.assertTrue(dq_z13u_user_defined_2("ocm00265003"))

        #test fail ocm len
        self.assertFalse(dq_z13u_user_defined_2("ocm0026500"))

        #test ocn number
        self.assertTrue(dq_z13u_user_defined_2("ocn464584694"))

        #test fail ocn len
        self.assertFalse(dq_z13u_user_defined_2("ocn46458469"))

        #test on number
        self.assertTrue(dq_z13u_user_defined_2("on1245789453"))

        #test None
        #self.assertTrue(dq_z13u_user_defined_2(''))
        #Should the above test pass? Unclear from reading the function.

#specific_transform_functions
    def test_transform_sub(self):
        #Test field substring
        a = TransformField('245','This is an exceptionally long title but we are using it as an example')
        self.assertEqual(substring(a,0,35),'This is an exceptionally long title')

#    def test_output_standard(self):
#        b = TransformField('')

    def test_remove_ocm_ocn_on(self):
        #test ocn recognition and transform
        c = TransformField('z13u_user_defined_2','ocn748578120')
        self.assertEqual(remove_ocm_ocn_on(c),'748578120')

        #test ocm recognition and transform
        d = TransformField('z13u_user_defined_2','ocm00003739')
        self.assertEqual(remove_ocm_ocn_on(d),'00003739')

        #test on recognition and transform
        e = TransformField('z13u_user_defined_2','on1038022607')
        self.assertEqual(remove_ocm_ocn_on(e),'1038022607')

    def test_isAcqCreated(self):
        #test to confirm is_acq_created works with upper, lower, mixed, and fail
        i = TransformField('z13u_user_defined_6','acq-created ||')
        j = TransformField('z13u_user_defined_6','ACQ-CREATED ||')
        k = TransformField('z13u_user_defined_6','NOT-acq-created')
        l = TransformField('z13u_user_defined_6','Shpoomples')
        self.assertEqual(is_acq_created(i),'Y')
        self.assertEqual(is_acq_created(j),'Y')
        self.assertEqual(is_acq_created(k),'Y')
        self.assertEqual(is_acq_created(l),'N')

    def test_isCircCreated(self):
        #test to confirm is_circ_created works with upper, lower, mixed, and fail
        m = TransformField('z13u_user_defined_6','circ-created suppressed ||')
        n = TransformField('z13u_user_defined_6','CIRC-CREATED SUPPRESSED || ')
        o = TransformField('z13u_user_defined_6','Shpoomples')
        self.assertEqual(is_circ_created(m),'Y')
        self.assertEqual(is_circ_created(n),'Y')
        self.assertEqual(is_circ_created(o),'N')

    def test_isProvisional(self):
        #test to confirm is_provisional works with upper, lower, mixed, and fail
        p = TransformField('z13u_user_defined_6','provisional')
        q = TransformField('z13u_user_defined_6','pRoViSiOnAl')
        r = TransformField('z13u_user_defined_6','Shpoomples')
        self.assertEqual(is_provisional(p),'Y')
        self.assertEqual(is_provisional(q),'Y')
        self.assertEqual(is_provisional(r),'N')

    def test_isSuppressed(self):
        #test to confirm is_suppressed works with upper, lower, mixed, and fail
        s = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG','suppressed')
        t = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG','SuPpReSsEd')
        u = TransformField('LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG','Shpoomples')
        self.assertEqual(is_suppressed(s),'Y')
        self.assertEqual(is_suppressed(t),'Y')
        self.assertEqual(is_suppressed(u),'N')
#^^should test value be LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG or z13u_user_defined_6?

    # def test_subLookUp(self):
    #     #test code lookup from CSV table
    #     f = TransformField('z13u_user_defined_3','750424m19769999wiub^^^^^b^^^^001^0^eng^^')
    #     self.assertEqual(subLookUp(f,'lookup_tables/encoding_level.csv',17,18),'Unknown')
    #     self.assertEqual(subLookUp(f,'lookup_tables/bibliographic_level.csv',6,7),'Monograph/Item')
    #     #blank vs ^? is there an established protocol for our data b/c there's a disagreement between data & lookups

    # TODO: Write z13 condition
    def test_isbn_code_020(self):
        #test isbn_issn check function
        g = TransformField('z13_isbn_issn','177091921X','020')
        self.assertEqual(isbn_code_020(g),'177091921X')

        h = TransformField('z13_isbn_issn','177091921X','022')
        self.assertEqual(issn_code_022(h),'177091921X')

if __name__ == '__main__':
    unittest.main()
