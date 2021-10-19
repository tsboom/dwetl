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
import load_stage_2
import stage_2_intertable_processing
from dotenv import load_dotenv
load_dotenv()

def run(input_directory, is_test_run):

    #create logger
    today = datetime.datetime.now().strftime('%Y%m%d')
    logger = logging.getLogger('dwetl')
    file_handler = logging.FileHandler(f'logs/dwetl.log.{today}')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    time_started = datetime.datetime.now()
    logger.info(f'DWETL.py started')

    '''
    create job_info for current process
    '''
    db_session_creator = dwetl.database_session
    
    with db_session_creator() as session:
        job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
        job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)



    '''
    load_stage_1
    '''
    load_stage_1.load_stage_1(job_info, input_directory, logger, table_mapping, db_session_creator)
    '''
    load_stage_2
    load 'in_' values from stg1 to stg 2 tables
    load 'in_' values
    '''
    load_stage_2.load_stage_2(job_info, logger, table_mapping, db_session_creator)

    '''
    stg 2 intertable processing
    '''
    stage_2_intertable_processing.stage_2_intertable_processing(job_info, logger, table_mapping, db_session_creator)



    '''
    end of job metadata writing
    '''

    endtime = datetime.datetime.now()
    # write end time to processing cycle table
    with dwetl.database_session() as session:
        job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
        # get row for current id and write end time to it
        max_prcsng_id = session.query(job_info_table_class).\
            filter(job_info_table_class.dw_prcsng_cycle_id == job_info.prcsng_cycle_id).\
            update({'dw_prcsng_cycle_exectn_end_tmstmp': endtime})

    elapsed_time = endtime - time_started
    print("elapsed time: ", str(elapsed_time))







'''
main function for running script from the command line
'''
if __name__=='__main__':
    arguments = sys.argv

    today = datetime.datetime.now().strftime('%Y%m%d')
    #today = "20201019"
    data_directory = os.getenv("DATA_DIRECTORY")
    # input_directory = f'{data_directory}/incoming/aleph/{today}/'


    # give hint if --help
    if '--help' in arguments:
        print('Usage: ')
        print('\tdwetl.py [YYYYMMDD]')
        sys.exit(1)
    if len(arguments) == 2:
        today = arguments[1]
        
    is_test_run = False
    input_directory = f'{data_directory}/incoming/{today}/'
    run(input_directory, is_test_run)
