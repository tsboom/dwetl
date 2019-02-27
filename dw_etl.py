import pdb
import re
import csv
import json
import sql
import os
from os import walk
import logging
import datetime
import sqlalchemy
from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
# import database_config
import database_credentials

import TableTransform
import extract



logging.basicConfig(filename='dwetl.log', level=logging.DEBUG)
logging.info('Started logging at ', datetime.datetime.now())

'''
set files for processing
'''

# use filenames in a specific directory to process
# in this case i put the bib rec files in data/bib_rec
files = []
for (dirpath, dirnames, filenames) in walk('data/bib_rec'):
    for file in filenames:
        files.append(os.path.join(dirpath, file))

def is_not_empty(file):
    return os.stat(file).st_size > 0

tsvs_to_process = [f for f in files if is_not_empty(f)]




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

# # create class names for each base class that was automapped
# mai50_z30 = Base.classes.dw_stg_1_mai50_z30
#
# # bib record dimension file-equivalent-tables
bib_rec_stg1_tables = {
    'mai01_z00': Base.classes.dw_stg_1_mai01_z00, #has data
    'mai39_z00': Base.classes.dw_stg_1_mai39_z00, #has data
    'mai01_z13': Base.classes.dw_stg_1_mai01_z13, #has data
    'mai39_z13': Base.classes.dw_stg_1_mai39_z13, # file is empty
    'mai01_z13u': Base.classes.dw_stg_1_mai01_z13u #has data
}


logging.info('Successfully mapped postgres tables to Base classes.')
# doesn't exist
# mai39_z13u = Base.classes.dw_stg_1_mai39_z13u
#
# # inspect table that was created for debugging
# insp = inspect(engine)
# insp.get_columns('dw_stg_1_mai01_z13u')



'''

extract data and load file-equivalent table for all TSVs that are configured

'''
for filename in tsvs_to_process:
    extract.load_file_equivalent_table(filename, engine, bib_rec_stg1_tables)


'''
create stg 2 tables

'''

pdb.set_trace()




'''
transform
'''

table_config = TableTransform.load_table_config(tc_path)
print(json.dumps(table_config, indent=4))
# Use a function which uses the table metadata config files and performs the transformations

# with open(filename as f):


# stg 2 to transform_field(df, table_config)




# load to stg 3



# load to dimension dw database

# load fact
