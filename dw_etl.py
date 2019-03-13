import pdb
import pprint
from colorama import init, Fore, Back, Style
init()
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
import loadstg1
import loadstg2
import importlib


# logging format
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def setup_logger(name, log_file, level=logging.DEBUG):
    # set up logging file
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# dwetl logger
# log file with today's date
logfile = datetime.datetime.now().strftime('dwetl.log.%Y%m%d')
dwetl_logger = setup_logger('dwetl_logger', logfile)
# sqlalchemy logger
sa_logfile = datetime.datetime.now().strftime('sqlalchemy.engine.log.%Y%m%d')
sa_engine_logger = setup_logger('sqlalchemy.engine', sa_logfile)


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





# Reflecting database with Automap (see chapter 10 of Essential SQLAlchemy 2nd edition)
Base = automap_base()
# reflect the entire database
Base.prepare(engine, reflect=True)
# # print a list of each table object
# print(Base.classes.keys())


# # bib record dimension file-equivalent-tables
bib_rec_stg1_tables = {
    'mai01_z00': Base.classes.dw_stg_1_mai01_z00, #has data
    'mai39_z00': Base.classes.dw_stg_1_mai39_z00, #has data
    'mai01_z13': Base.classes.dw_stg_1_mai01_z13, #has data
    'mai39_z13': Base.classes.dw_stg_1_mai39_z13, # file is empty
    'mai01_z13u': Base.classes.dw_stg_1_mai01_z13u #has data
}


# # inspect table that was created for debugging
# insp = inspect(engine)
# insp.get_columns('dw_stg_1_mai01_z13u')



# '''
#
# extract data and load file-equivalent table for all TSVs that are configured
#
# '''
# for filename in tsvs_to_process:
#     loadstg1.load_file_equivalent_table(filename, engine, bib_rec_stg1_tables)
#

'''
create stg 2 tables
read from stg1 tables

'''

bib_rec_stg2_tables = {
    'bib_rec_z00': Base.classes.dw_stg_2_bib_rec_z00,
    'bib_rec_z13': Base.classes.dw_stg_2_bib_rec_z13,
    'bib_rec_z13u': Base.classes.dw_stg_2_bib_rec_z13u,
    'bib_rec_z00_field': Base.classes.dw_stg_2_bib_rec_z00_field,
    }

# rethink this reload
importlib.reload(loadstg2)
loadstg2.load_stg2_table(engine, bib_rec_stg1_tables, bib_rec_stg2_tables, dwetl_logger)



'''
transform
'''

print('got to transform')

pdb.set_trace()

table_config = TableTransform.load_table_config(tc_path)
print(json.dumps(table_config, indent=4))
# Use a function which uses the table metadata config files and performs the transformations

# with open(filename as f):


# stg 2 to transform_field(df, table_config)




# load to stg 3



# load to dimension dw database

# load fact
