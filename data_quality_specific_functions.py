import csv
import data_quality_utilities

def dq_z30_temp_location(in_value):
    return in_value in ('Y', 'N')

def dq_z30_call_no_type__valid_cal_no_type(code):
    call_no_type_dict = data_quality_utilities.create_dict_from_csv('call_no_type.csv')
    return code in call_no_type_dict

def dq_z13u_user_defined_10__valid_holding_own_code(code):
    holding_own_dict = data_quality_utilities.create_dict_from_csv('holding_own_code.csv')
    return code in holding_own_dict


def dq_z13u_user_defined_2(in_value):
    is_valid = False
    if in_value == '':
        is_valid = True
    elif in_value.startswith('ocm'):
        if len(in_value) == 11:
            is_valid = True
    elif in_value.startswith('ocn'):
        if len(in_value) == 12:
            is_valid = True
    elif in_value.startswith('on'):
        if len(in_value) == 12:
            is_valid = True
    return is_valid
