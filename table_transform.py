import os
import json
import pdb

from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData

from TransformField import TransformField
import data_quality_specific_functions as dqs
import data_quality_utilities as dqu
# import specific_transform_functions




def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config

# function to deal with z13 ISBN/ISSN code special case
def get_isbn_issn_code(column, row_dict):
    isbn_issn_column = 'in_z13_isbn_issn_code'
    optional_isbn_code = None
    if column == isbn_issn_column:
        # get ISBN code from first three chars, save code to var
        isbn_issn_code = row_dict[isbn_issn_column][0:2]
    # column name contains ISBN_ISSN, optional_isbn_code = isbn_code
    if column == 'in_z13_isbn_issn':
        # get ISBN code from first three chars, save code to var
        isbn_issn_code = row_dict[isbn_issn_column][0:2]
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


def dict_from_module(module):
    context = {}
    for setting in dir(module):
        # you can write your filter here
        if setting.islower() and setting.isalpha():
            context[setting] = getattr(module, setting)
    return context



def execute_dq_function(function_name, arg, input, dq_funcs_dict):
    try:
        function = dq_funcs_dict[function_name]
        if not arg:
            is_passing = function(input)
        else:
            is_passing = function(input, arg)
        return is_passing
    except KeyError:
        # dq func name missing from dq_funcs_dict
        print('temp')



def check_data_quality(field, dq_funcs_dict, obj):
    '''
    execute dq check for current object and handle replacement values
    '''
    # find dq checks to run
    try:
        pdb.set_trace()
        dq_list = obj.get('Data Quality Info', {}).get('data_quality_checks')
        # run dq checks
        for check in dq_list:
            function_name = check.get('specific_dq_function')
            arg = check.get('specific_dq_function_param_1')
            is_passing = execute_dq_function(function_name, arg, field.value, dq_funcs_dict)
            if is_passing:
                field_dq_result = field.value
            else:
                replacement_value = check.get('replacement_value')
                if replacement_value:
                    field_dq_result = replacement_value
                    print("deal with dimension_link_to_records")
            return field_dq_result

    except KeyError:
        # missing
        print('No dq check for ' + field.name)
        return field.value

def run_dq_checks(field, dq_funcs_dict, source_col_sorted_dict):
    objs = source_col_sorted_dict[field.name]
    for obj in objs:
        check_data_quality(field, dq_funcs_dict, obj)


def run_transformation(function_name, arg, input):
    module_name = 'data_quality_specific_functions'
    # parse out dw prefixes from function na
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

    # run pp
    result = preprocess(field, source_col_sorted_dict)
    field.record_pp(result)

    # set up dq
    dq_funcs_dict = dict_from_module(dqs).update(dict_from_module(dqu))

    # run dq
    dq_result = check_data_quality(field, dq_funcs_dict, source_col_sorted_dict)
    field.record_dq(dq_result)


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
