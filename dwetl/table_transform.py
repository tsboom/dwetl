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

# from dwetl.transform_field import TransformField
# import dwetl.data_quality_specific_functions as dqs
# import dwetl.data_quality_utilities as dqu
# 
# import dwetl.specific_transform_functions as stf



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
    for column in sa_row.__table__.columns.keys():
        if column.startswith('in_'):
            field_value = row_dict[column]
            optional_isbn_code = get_isbn_issn_code(column, row_dict)
            fields.append(TransformField(column, field_value, isbn_issn_code=optional_isbn_code))
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
        field_dq_result = get_replacement_value(check)
    else:
        field_dq_result = 'ERROR no result'

    # save name and result of dq check
    result = {'name': function_name, 'result': field_dq_result, 'target_col_name': target_col_name, 'check_passed': is_passing}
    return result



def run_dq_checks(field, dq_funcs_list, table_config):
    # find matching transform information from table_config for current field
    transform_info = table_config[field.name[3:]]
    # find list of dq checks for that object
    dq_list = transform_info['dataquality_info']
    for check in dq_list:
        result = check_data_quality(check, dq_funcs_list, field)
        field.record_dq(result)
        if result['check_passed'] == False:
            break


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
            # get the name of the target column
            target_col_name = transform_obj['target_col_name']
            t_result = execute_transform(specific_transform_function, arg1, arg2, field, transformations_list)
            result = {'name': specific_transform_function, 'result': t_result, 'target_col_name': target_col_name}
            return result
    except:
        pass


def run_transformations(field, transformations_list, table_config):
    obj = table_config[field.name[3:]]
    transform_list = obj['transformation_steps']
    for transform_obj in transform_list:
        t_result = check_transform(field, transformations_list, transform_obj)
        field.record_transform(t_result)



def transform_field(field, table_config):
    '''
    Using the field name and value, run transformations and log to the field's record
    '''
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
        # pprint.pprint(field.record)
        # write_log(field.name, field.log) # writes to stage 2 db


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

    for check in field.record['dq']:
        if check['check_passed'] == False:
            for dq in field_config['dataquality_info']:
                is_suspend = convert_suspend_record_bool(dq['suspend_record'])
                if check['name'] == dq['specific_dq_function'] and is_suspend:
                    result = True
    return result

def suspend_record(field):
    # write suspend metadata to the record
    print('temp')




'''

main function to load stg_2 table PP, DQ, T1, T2.. etc

'''
def transform_stg2_table(engine, table_config, table, dwetl_logger):

    Session = sessionmaker(bind=engine)
    session = Session()

    # process the row, iterate over each field in the row and transform
    for row in session.query(table).all():
        row_fields = transform_row(row)
        suspend_exists = False
        check_exception_count = 0

        for field in row_fields:
            transform_field(field, table_config)
            if not field.is_valid():
                # find out if record needs to be suspended, suspend it
                # create dict of properties that neec to be written to the record
                if is_suspend_record(field, table_config):
                    rm_props = { 'rm_suspend_rec_flag': 'Y', 'rm_suspend_rec_reason_cd': '', 'rm_dq_check_exception_cnt': 0}
                # testing sa



                print('temp')
                # set exceptions count
