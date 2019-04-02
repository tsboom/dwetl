import os
import json
import pdb
import TransformField
from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData


def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config

# function to deal with z13 ISBN/ISSN code special case
def get_isbn_issn_code(column, row_dict):
    isbn_issn_column = 'in_z13_isbn_issn_code'
    if column == isbn_issn_column:
        # get ISBN code from first three chars, save code to var
        isbn_issn_code = row_dict[isbn_issn_column][0:2]
    # column name contains ISBN_ISSN, optional_isbn_code = isbn_code
    if column == 'in_z13_isbn_issn':
        optional_isbn_code = isbn_issn_code
        return optional_isbn_code
    return optional_isbn_code is None


# creates array of TransformField objects which takes into account ISBN/ISSN code
def transform_row(sa_row):
    # fields to transform
    fields = []
    optional_isbn_code = None
    row_dict = sa_row.__dict__
    for column in sa_row.__table__.columns.keys():
        if column.startswith('in_'):
            field_value = row_dict[column]
            optional_isbn_code = get_isbn_issn_code(column, row_dict)
            fields.append(TransformField(column, field_value, isbn_issn_code=optional_isbn_code))
            print(fields)
            pdb.set_trace()



# now we have an array of field objects

# for field in fields:
#     transform_field(field)


# # Write field transform log to stage 2 db
# def write_log(field_name, log)
#
# def transform_field(field,):
#     '''
#     Using the field name and value, run transformations and log to the field's log
#     '''
#
#
#
#     # run pp
#
#     field.log_pp(result)
#
#
#     # run dq
#     field.log_dq(result)
#
#     # run transformation
#         # determine which transforms to run, call that func's tranfsorm function
#
#     field.log_transform_result(tf_name, result)...
#
#
#     '''
#     After transforming and logging, write log to database
#     '''
#
#     write_log(field.name, field.log) # writes to stage 2 db
#

'''
main function to load stg_2 table PP, DQ, T1, T1.. etc
'''
def transform_stg2_table(engine, table_config, table, dwetl_logger):
    Session = sessionmaker(bind=engine)
    session = Session()

    for row in session.query(table).all():
        transform_row(row)
