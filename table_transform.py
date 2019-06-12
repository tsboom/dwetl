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
import specific_transform_functions




def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config

# function to deal with z13 ISBN/ISSN code special case
def get_isbn_issn_code(column, row_dict):
    isbn_issn_column = 'in_z13_isbn_issn_code'
    optional_isbn_code = None
    if column == 'in_z13_isbn_issn':
        # get ISBN code from first three chars, save code to var
        optional_isbn_code = row_dict[isbn_issn_column][0:3]
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
        print('No preprocessing for ' + field.name)
        return field.value

def functions_from_module(module):
    functions = inspect.getmembers(module, inspect.isfunction)
    return functions



def execute_dq_function(function_name, arg, input, dq_funcs_list):
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
        if function_name is dq_function:
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
        dq_list = obj.get('Data Quality Info', {}).get('data_quality_checks')
        # run dq checks
        for check in dq_list:
            function_name = check.get('specific_dq_function')
            arg = check.get('specific_dq_function_param_1')
            is_passing = execute_dq_function(function_name, arg, field.value, dq_funcs_list)
            print("IS PASSING VARIABLE IS" + is_passing)
            if is_passing:
                field_dq_result = field.value
            else:
                replacement_value = check.get('replacement_value')
                if replacement_value:
                    field_dq_result = replacement_value
                    print("deal with dimension_link_to_records")
            result =  {'name': function_name, 'result': field_dq_result}
            return result

    except TypeError:
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
        print('Field name ' + field.name +' is not a source column.')


def run_transformation(function_name, arg, input):
    module_name = 'data_quality_specific_functions'
    # parse out dw prefixes from function name
    f_string = function_name
    function = getattr(globals()[module_name], f_string)
    if not arg:
        is_passing = function(input)
    else:
        is_passing = function(input, arg)
    return is_passing



def transform_field(field, source_col_sorted_dict):
    '''
    Using the field name and value, run transformations and log to the field's log
    '''
#^^do we think it is wise to have a function with the same name as a class and additional python file? Or does it not matter?
    # run pp
    result = preprocess(field, source_col_sorted_dict)
    field.record_pp(result)
    # set up dq
    dq_funcs_list = functions_from_module(dqs) + functions_from_module(dqu)
    # run dq
    run_dq_checks(field, dq_funcs_list, source_col_sorted_dict)



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
        print(row)
        row_fields = transform_row(row)
        for field in row_fields:
            transform_field(field, source_col_sorted_dict)
            print(field.value)
            print(field.record)
