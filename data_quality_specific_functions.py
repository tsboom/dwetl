import csv
import os
import pdb
import data_quality_utilities




def dq_z13u_user_defined_10_valid_holding_own_code(code):
    holding_own_dict = data_quality_utilities.create_dict_from_csv('holding_own_code.csv')
    try:
        return holding_own_dict[code]
    except KeyError as error:
        print(error, ': Incorrect holding own code.')


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
