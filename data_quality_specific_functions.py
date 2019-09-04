import csv
import os
import pdb
import data_quality_utilities

def dq_z30_temp_location(input):
    if input == 'Y' or input == 'N':
        return True
    else:
        return False

def dq_z30_call_no_type__valid_cal_no_type(code):
    call_no_type_dict = data_quality_utilities.create_dict_from_csv('call_no_type.csv')
    try:
        result = call_no_type_dict[code]
        return True
    except KeyError:
        print('\tCall number code ' + code + 'is invalid.')
        return False


def dq_z13u_user_defined_10__valid_holding_own_code(code):
    holding_own_dict = data_quality_utilities.create_dict_from_csv('holding_own_code.csv')
    try:
        result = holding_own_dict[code]
        return True
    except KeyError:
        print('\tHolding own code ' + code + 'is invalid.')
        return False


def dq_z13u_user_defined_2(input):
    is_valid = False
    if input.startswith('ocm'):
        if len(input) == 11:
            is_valid = True
    elif input.startswith('ocn'):
        if len(input) == 12:
            is_valid = True
    elif input.startswith('on'):
        if len(input) == 12:
            is_valid = True
    elif input is None:
        is_valid = True
    return is_valid
