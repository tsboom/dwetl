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
#^^ the first if seems like it will always return NONE, correct?
#^^ updated to return substring 0:3 because it does say you need the first three characters, yes?
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

def preprocess(field, source_col_sorted_dict):
    try:
        objs = source_col_sorted_dict[field.name]
        # only process the first object which is info for first transformation
        if objs[0]['Preprocessing Info']['pre_action'] == 'Trim':
            return dqu.trim(field.value)
        return field.value
    except KeyError:
        print(field.name + " does not exist in source_col_sorted_dict")
        print('No preprocessing for ' + field.name)
        return field.value

def functions_from_module(module):
    functions = inspect.getmembers(module, inspect.isfunction)
    return functions


def execute_dq_function(current_function, arg, input, dq_funcs_list):
    is_passing = ''
    # search for function in dq list, execute with params
    print(function_name)
    print(arg)
    print(str(arg))
    print(len(arg))
    print(input)
    pdb.set_trace()
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


def check_data_quality(field, dq_funcs_list, obj):
    '''
    execute dq check for current object and handle replacement values
    '''
    # find dq checks to run
    try:
        dq_list = obj['Data Quality Info']['data_quality_checks']
        print(dq_list)
        # run dq checks
        for check in dq_list:
            function_name = check.get('specific_dq_function')
            arg = check.get('specific_dq_function_param_1')
            # is_passing is an empty string if no dq check is found, otherwise is True or False.
            is_passing = execute_dq_function(function_name, arg, field.value, dq_funcs_list)
            print("IS PASSING VARIABLE IS" + is_passing)
            if is_passing:
                field_dq_result = field.value
            elif is_passing is False:
                print('DQ '+ function_name +' FAILED')
                replacement_value = check.get('replacement_value')
                if replacement_value:
                    field_dq_result = replacement_value
                    print("deal with dimension_link_to_records")
            else:
                continue
            # save name and result of dq check
            if field_dq_result:
                result = {'name': function_name, 'result': field_dq_result}
            return result
    except KeyError:
        # missing
        print('No dq check for ' + field.name)
        return field.value



def run_dq_checks(field, dq_funcs_list, source_col_sorted_dict):
    try:
        objs = source_col_sorted_dict[field.name]
        for obj in objs:
            result = check_data_quality(field, dq_funcs_list, obj)
            field.record_dq(result)
    except KeyError:
        print('Field name ' + field.name +' is not a source column so there are no dq checks. \n\n\n')


def execute_transform(current_function, arg1, arg2, input, transformations_list):
    result = ''
    for function in transformations_list:
        function_object = function[1]
        transform_function = function[0]
        if current_function == transform_function:
            if not arg1 and not arg2:
                result = function_object(input)
            elif arg1 and arg2:
                result = function_object(input, arg1, arg2)
            elif arg1:
                result = function_object(input, arg1)
            else:
                continue
        return result

def check_transform(field, transformations_list, obj):
    ''''
    execute the transforms per source column name, updating the TransformField object
    '''
    # find the corresponding transformation in dimension json
    try:
        specific_transform_function = obj['Transformation Info']['specific_transform_function']
        pdb.set_trace()
        arg = 'temp'
    except KeyError:
        print('This source field does not exist in the source to target json.')


def run_transformations(field, transformations_list, source_col_sorted_dict):
    try:
        objs = source_col_sorted_dict[field.name]
        for obj in objs:
            pdb.set_trace()
            result = check_transform(field, transformations_list, obj)
            field.record_transforms(result)
    except KeyError:
        print('Field name ' + field.name +' is not a source column so there are no transformations. \n\n\n')





def transform_field(field, source_col_sorted_dict):
    '''
    Using the field name and value, run transformations and log to the field's log
    '''
#^^do we think it is wise to have a function with the same name as a class and additional python file? Or does it not matter?
    # run pp
    result = preprocess(field, source_col_sorted_dict)
    field.record_pp(result)


    # set up dq by creating list of dq function objects from utilities
    # and data quality specific functions
    dq_funcs_list = functions_from_module(dqs) + functions_from_module(dqu)
    # run dq
    run_dq_checks(field, dq_funcs_list, source_col_sorted_dict)

    # set up list of transformation functions from module
    transformations_list = functions_from_module(stf)
    # run transformations
    run_transformations(field, transformations_list, source_col_sorted_dict)



    # # run transformation
    #     # determine which transforms to run, call that func's transform function
    #
    # field.record_transforms(tf_name, result)...
    #
    #
    # '''
    # After transforming and logging, write log to database
    # '''
    #
    # write_log(field.name, field.log) # writes to stage 2 db



def transform_stg2_table(engine, source_col_sorted_dict, table, dwetl_logger):
    '''
    main function to load stg_2 table PP, DQ, T1, T2.. etc
    '''
    Session = sessionmaker(bind=engine)
    session = Session()

    for row in session.query(table).all():
        row_fields = transform_row(row)
        for field in row_fields:
            transform_field(field, source_col_sorted_dict)
