import pdb
import re
import csv
import json
import pandas as pd
import sql
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
# import database_config
import database_credentials
import logging
import TableTransform


# download files
#filename = 'data/mai50_z30_20181212_034002_data' #line 5600 is messed up
filename = 'data/mai50_z30_20190102_034001_data'
# filename = os.path.join('data','mai50_z305_20181115_172016_1.tsv')
tc_path = os.path.join('table_config', 'z30.json')

'''
set up SQLAlchemy to map to reflect existing tables in the database
'''
def create_db_engine():
    # connect to database
    engine = create_engine(database_credentials.DB_CONNECTION_STRING, echo=True)

    return engine

engine = create_db_engine()

def set_up_db_logging():
    # set up logging file
    handler = logging.FileHandler('sqlalchemy.engine.log')
    handler.level = logging.DEBUG
    logging.getLogger('sqlalchemy.engine').addHandler(handler)

set_up_db_logging()



# Reflecting database with Automap (see chapter 10 of Essential SQLAlchemy 2nd edition)
Base = automap_base()
# reflect the entire database
Base.prepare(engine, reflect=True)
# # print a list of each table object
# print(Base.classes.keys())

# create class names for each base class that was automapped
Z30 = Base.classes.dw_stg_1_mai50_z30_test

# bib record dimension file-equivalent-tables
mai01_z00 = Base.classes.dw_stg_1_mai01_z00_test
mai39_z00 = Base.classes.dw_stg_1_mai39_z00_test
mai01_z13 = Base.classes.dw_stg_1_mai01_z13_test
mai39_z13 = Base.classes.dw_stg_1_mai39_z13_test
mai01_z13U = Base.classes.dw_stg_1_mai01_z13u_test
mai39_z13U = Base.classes.dw_stg_1_mai39_z13u_test


# create job execution metadata record and other stuff (see file-equivalent table chart)

'''
preprocessing
'''
header_1 = ''
header_2 = ''
footer = ''

with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    header_1 = next(reader)
    header_2 = next(reader)
    for line in f:
        pass
    footer = line.strip().split('\t')

# # def tsv_has_valid_headers(filename):
# #
# #
# #
# #
# # def tsv_has_valid_footer(filename):
#
#
#
# columns are listed in header line 2. Ignore the first H field.
columns = header_2[1:]

def parse_tsv_filename(filename):
    # tsv filename is the fourth field in header 1. ignore subdirectory name
    tsv_name = header_1[3][9:]
    tsv_name_metadata = {}
    parts = tsv_name.split('_')
    tsv_name_metadata = {
        'library':parts[0],
        'table':parts[1],
        'datetime':parts[2]+parts[3]
    }
    #the counter doesn't exist in the current filename
    return tsv_name_metadata

tsv_name_metadata = parse_tsv_filename(filename)


'''
load tsv into file-equivalent table
'''

#create session
Session = sessionmaker(bind=engine)
session = Session()

# determine if csv row is a footer
def row_is_footer(row):
    return row[0] == 'T'

# parse values from csv row into dict
def parse_row(row, columns_header):
    if(row_is_footer(row)):
        raise StopIteration()
    else:
        row_dict = {}
        for i, field in enumerate(row):
            row_dict[columns_header[i]] = field
        return row_dict

# read each line of the csv ignoring 2 headers and last line and write to the db
with open(filename) as f:
    reader = csv.reader(f, delimiter='\t')
    header_1 = next(reader) # row 0
    header_2 = next(reader) # row 1

    # read all lines after lines one and two
    try:
        while True:
            row_dict = parse_row(next(reader), header_2)
            try:
                # insert the row
                record = Z30(**row_dict)
                session.add(record)
                session.commit()
            except:
                # should I create a db exception here?
                session.rollback()
    except StopIteration:
        pass



'''
transform
'''

table_config = TableTransform.load_table_config(tc_path)
print(json.dumps(table_config, indent=4))
# Use a function which uses the table metadata config files and performs the transformations

# with open(filename as f):


# transform_field(df, table_config)




# load to intermediate database



# load to dimension dw database
