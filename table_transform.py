import os
import json
import pdb
import pprint
import inspect

from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData

from TransformField import TransformField
import data_quality_specific_functions as dqs
import data_quality_utilities as dqu

import specific_transform_functions as stf
from colorama import init, Fore, Back, Style



# use pdb.set_trace() to set breakpoint

"""
Scroll down to the main function: transform_stg2_table
Start there if you want to understand this file.
"""


def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config

# function to deal with z13 ISBN/ISSN code special case (used in transform_row function)
# TO DO: probably should figure out a better way to do this check only for z13, not other tables.
def get_isbn_issn_code(column, row_dict):
    optional_isbn_code = None
    # column name contains ISBN_ISSN, optional_isbn_code = isbn_code
    if column == 'in_z13_isbn_issn':
        # get ISBN code from first three chars, save code to var
        isbn_issn_code = row_dict['in_z13_isbn_issn_code'][0:3]
        optional_isbn_code = isbn_issn_code
        return optional_isbn_code
    return optional_isbn_code

# creates array of TransformField objects which takes into account ISBN/ISSN code
def transform_row(sa_row):
    # fields to transform
    fields = []
    row_dict = sa_row.__dict__
    table_name = sa_row.__table__.name
    for column in sa_row.__table__.columns.keys():
        if column.startswith('in_'):
            field_value = row_dict[column]
            optional_isbn_code = get_isbn_issn_code(column, row_dict)
            fields.append(TransformField(column, field_value, table_name, isbn_issn_code=optional_isbn_code))
    return fields


# Write field transform log to stage 2 db
def write_log(field_name, log):
    print('write log temp')

def preprocess(field, table_config):
    try:
        obj = table_config[field.name[3:]]

        # only process the first object which is info for first transformation
        if obj['preprocessing_info']['pre_action'] == 'Trim':
            return dqu.trim(field.value)
        return field.value
    except KeyError:
        # print(field.name + " does not exist in table_config")
        print('No preprocessing for ' + field.name)
        return field.value

def functions_from_module(module):
    functions = inspect.getmembers(module, inspect.isfunction)
    return functions


def execute_dq_function(current_function, arg, input, dq_funcs_list):
    is_passing = ''
    # search for function in dq list, execute with params
    for function in dq_funcs_list:
        function_object = function[1]
        dq_function = function[0]
        # execute dq function for the matching current function in dq_funcs_list
        if current_function == dq_function:
            if not arg:
                is_passing = function_object(input)
            else:
                is_passing = function_object(input, arg)
            break
    return is_passing

def get_replacement_value(check):
    result = ''
    replacement_value = check.get('replacement_value')
    if replacement_value:
        if replacement_value == "(null)":
            result = None
        elif replacement_value == 'N/A':
            result = ''
        else:
            result =  replacement_value
    return result



def check_data_quality(check, dq_funcs_list, field):
    '''
    execute dq check for current object and handle replacement values
    '''
    # find dq checks to run
    function_name = check.get('specific_dq_function')
    target_col_name = check.get('target_column_name')
    arg = check.get('specific_dq_function_param_1')
    # suspend_record = convert_suspend_record_bool(check.get('suspend_record'))


    # is_passing is an empty string if no dq check is found, otherwise is True or False.
    is_passing = execute_dq_function(function_name, arg, field.value, dq_funcs_list)
    if is_passing is True:
        field_dq_result = field.value
    elif is_passing is False:
        # print(Fore.RED + 'DQ '+ function_name +' FAILED for source(' + field.name + ') target('  + target_col_name + ') - ' + field.value)

        field_dq_result = get_replacement_value(check)

        # print("deal with dimension_link_to_records. replacement_value is: " + field_dq_result)
    else:
        # print('DQ check' + function_name + ' was not found in dq functions.')

        field_dq_result = 'ERROR no result'

    # save name and result of dq check
    print(Style.RESET_ALL)
    result = {'name': function_name, 'result': field_dq_result, 'target_col_name': target_col_name, 'check_passed': is_passing}
    return result



def run_dq_checks(field, dq_funcs_list, table_config):
    try:
        # find matching transform information from table_config for current field
        transform_info = table_config[field.name[3:]]
        # find list of dq checks for that object
        dq_list = transform_info['dataquality_info']
        for check in dq_list:
            result = check_data_quality(check, dq_funcs_list, field)
            field.record_dq(result)
    except KeyError:
        print(field.name +' has no DQ checks.')



def execute_transform(specific_transform_function, arg1, arg2, field, transformations_list):
    '''
    find current function in list of function object tuples, and execute it
    '''
    t_result = ''
    for function in transformations_list:
        function_object = function[1]
        transform_function = function[0]
        if specific_transform_function == transform_function:
            if not arg1 and not arg2:
                t_result = function_object(field)
            elif arg1 and arg2:
                t_result = function_object(field, arg1, arg2)
            elif arg1:
                t_result = function_object(field, arg1)
            else:
                print('Inconsistent number of arguments to transform_function')
                break
        else:
            continue
    return t_result

def check_transform(field, transformations_list, transform_obj):
    ''''
    execute the transforms per source column name, updating the TransformField object
    '''
    # find the corresponding transformation in dimension json
    try:
        specific_transform_function = transform_obj['transformation_info']['specific_transform_function']
        if specific_transform_function:
            arg1 = transform_obj.get('transformation_info', {}).get('specific_transform_function_param1')
            arg2 = transform_obj.get('transformation_info', {}).get('specific_transform_function_param2')
            print(field.name, arg1, arg2)
            # get the name of the target column
            target_col_name = transform_obj['target_col_name']
            t_result = execute_transform(specific_transform_function, arg1, arg2, field, transformations_list)
            result = {'name': specific_transform_function, 'result': t_result, 'target_col_name': target_col_name}
            return result
    except KeyError:
        print(field.name + ' - Transformation: Move As-Is.')


def run_transformations(field, transformations_list, table_config):
    try:
        obj = table_config[field.name[3:]]
        transform_list = obj['transformation_steps']
        for transform_obj in transform_list:
            t_result = check_transform(field, transformations_list, transform_obj)
            print(pprint.pprint(t_result))
            field.record_transform(t_result)
    except KeyError:
        print(field.name + ' - Transformation: Move As-Is.\n\n\n')


def transform_field(field, table_config):
    '''
    Using the field name and value, run transformations and log to the field's log
    '''
    try:
        # remove "in_" from field name
        field_name = field.name[3:]
        if table_config[field_name]:

            # run pp
            result = preprocess(field, table_config)
            field.record_pp(result)

            # set up dq by creating list of dq function objects from utilities
            # and data quality specific functions
            dq_funcs_list = functions_from_module(dqs) + functions_from_module(dqu)  # TODO, do this only once outside this func

            # run dq
            run_dq_checks(field, dq_funcs_list, table_config)

            # set up list of specific transformation functions from module
            transformations_list = functions_from_module(stf)  # TODO  same ^

            # run transformations
            run_transformations(field, transformations_list, table_config)
            pprint.pprint(field.record)
            # write_log(field.name, field.log) # writes to stage 2 db
    except KeyError:
        print("\n" + field.name + " is not in dimension being processed.\n")


def is_field_valid(field):
    # if all dq checks are good, continue
    result = True
    for check in field.record['dq']:
        if check['check_passed'] == False:
            result = False
            break
    return result

    # find which checks failed, and whether to suspend record

def convert_suspend_record_bool(suspend_record):
    if suspend_record == 'Yes':
        return True
    elif suspend_record == 'No':
        return False
    else:
        return False

def is_suspend_record(field, table_config):
    result = False

    # find current fields dq checks
    field_config = table_config[field.name[3:]]

    for dq in field_config['dataquality_info']:
        suspend_on_fail = convert_suspend_record_bool(dq['suspend_record'])
        if not suspend_on_fail:
            continue
        else:
            # get name of the function that failed
            for check in field.record['dq']:
                if check['check_passed'] == False:
                    result = True
                    break
    return result




def transform_stg2_table(engine, table_config, table, dwetl_logger):
    '''
    main function to load stg_2 table PP, DQ, T1, T2.. etc
    '''
    Session = sessionmaker(bind=engine)
    session = Session()

    # process the row, iterate over each field in the row and transform
    for row in session.query(table).all():
        row_fields = transform_row(row)
        for field in row_fields:
            transform_field(field, table_config)
            if not is_field_valid(field):
                # find out if record needs to be suspended
                # suspend it
                print('temp')
                # set exceptions count
