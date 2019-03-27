from dwetl import dw_etl
import data_quality_utilities
import data_quality_specific_functions
'''
dataquality tests
'''

# test if right exceptions are thrown when given bad data

def test_is_numeric():
    assert data_quality_specific_functions.is_numeric(5634563) == True

# def test_is_valid_length():
#
#
# def test_is_less_than_eq_to_length():
#
# def test_no_missing_values():
#
#
# def test_trim():
#
#
# def test_is_valid_aleph_year():
#
#
# def test_is_valid_aleph_date():
#
# def test_is_valid_hour():
