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
import re
import csv
import json
import sql
import os
import sys
import logging
import datetime
import sqlalchemy
import dwetl.database_credentials as database_credentials
from dwetl.job_info import JobInfoFactory, JobInfo
import load_stage_1

def run(input_directory):
    time_started = datetime.datetime.now()

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


'''
main function for running script from the command line
'''
if __name__=='__main__':
    arguments = sys.argv

    today = datetime.datetime.now().strftime('%Y%m%d')
    input_directory = f'data/{today}/'

    # give hint if --help
    if '--help' in arguments:
        print('Usage: ')
        print('\tdwetl.py [data directory]')
        sys.exit(1)
    if len(arguments) == 2:
        input_directory = arguments[1]

    run(input_directory)
