import dwetl
from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
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
import dwetl.database_credentials as database_credentials
from dwetl.job_info import JobInfoFactory, JobInfo
import load_stage_1


time_started = datetime.datetime.now()

'''
get today's date YYYYMMD to set input directory
'''

today = datetime.datetime.now().strftime('%Y%m%d')
input_directory = f'data/{today}/'

'''
create job_info for current process
'''
with dwetl.database_session() as session:
    job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
    job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)


'''
load_stage_1
'''
load_stage_1.load_stage_1(job_info, input_directory)


'''
load 'in_' values from stg1 to stg 2 tables
'''

endtime = datetime.datetime.now()
elapsed_time = endtime - time_started
print("elapsed time: ", str(elapsed_time))

# def setup_logger(name, log_file, level=logging.DEBUG):
#     # logging format
#     formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#     # set up logging file
#     handler = logging.FileHandler(log_file)
#     handler.setFormatter(formatter)
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#     return logger
#
# # dwetl logger
# # log file with today's date
# logfile = datetime.datetime.now().strftime('dwetl.log.%Y%m%d')
# dwetl_logger = setup_logger('dwetl_logger', 'logs/'+ logfile)
# # sqlalchemy logger
# sa_logfile = datetime.datetime.now().strftime('sqlalchemy.engine.log.%Y%m%d')
# sa_engine_logger = setup_logger('sqlalchemy.engine', 'logs/'+ sa_logfile)
