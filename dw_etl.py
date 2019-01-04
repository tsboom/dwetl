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
from sqlalchemy.orm import Session
import psycopg2
from database_config import *






# download files
#filename = 'data/mai50_z30_20181212_034002_data' #line 5600 is messed up
filename = 'data/mai50_z30_20190102_034001_data'
# filename = os.path.join('data','mai50_z305_20181115_172016_1.tsv')
tc_path = os.path.join('table_config', 'z30.json')


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

# def tsv_has_valid_headers(filename):
#
#
#
#
# def tsv_has_valid_footer(filename):



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



# put data in dataframe ignore first header line and footer line
def read_tsv_into_dataframe(filename):
    dataframe = pd.read_csv(filename, engine='python', sep='\t', header=1, skipfooter=1, error_bad_lines=False)
    return dataframe

dataframe = read_tsv_into_dataframe(filename)


# def tsv_has_valid_row_count(dataframe):
#     return len(dataframe) > 3



'''
load file equivalent table
'''
def create_db_engine():
    # connect to database
    engine = create_engine(DB_CONNECTION_STRING, echo=False)
    return engine

DB_CONNECTION_STRING = 'postgresql+psycopg2://usmai_dw:B1gUmD4ta@pgcommondev.lib.umd.edu:5439/usmai_dw_etl'

# use automap to reflect existing db into model
# https://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html
Base = automap_base()

engine = create_db_engine()

# reflect existing table from db
Base.prepare(engine, reflect=True)
pdb.set_trace()
# assign reflected table to class name
Z30 = Base.classes.dw_stg_1_mai50_z30

session = Session(engine)
# print (session.dw_stg_1_mai50_z30_collection)








pdb.set_trace()

#dataframe.to_sql('dw_stg_1_mai50_z30', engine, if_exists='replace')
dataframe.to_sql('test_z30', engine, if_exists='replace')






'''
transform
'''

# table_config = load_table_config(tc_path)
# print(json.dumps(table_config, indent=4))
# # Use a function which uses the table metadata config files and performs the transformations
#
# transform_field(df, table_config)


# write to the intermediate database




# load to intermediate database



# load to dimension dw database
