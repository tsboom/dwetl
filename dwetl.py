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
import table_mappings
from dotenv import load_dotenv
load_dotenv()

def run(input_directory):

    #create logger
    today = datetime.datetime.now().strftime('%Y%m%d')
    logger = logging.getLogger('dwetl')
    file_handler = logging.FileHandler(f'logs/dwetl.log.{today}')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    time_started = datetime.datetime.now()
    logger.info(f'DWETL.py started')
    logger.info(f'input directory: {input_directory}')  
    print(f'DWETL.py started')
    print(f'input directory: {input_directory}') 
    '''
    create job_info for current process
    '''
        
    db_session_creator = dwetl.database_session
    
    with db_session_creator() as session:
        try: 
            job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
        except KeyError as e: 
            sys.exit("dw_prcsng_cycle was not found. The database probably didn't have any tables in it. If you're developing locally, did you initialize the database and reset it?")
        # TODO: should we get the processing cycle id from the max of the reporting db final table
        # like we do in ezproxy_etl?
        # This would ensure we don't use the same processing cycle id twice. 
        # We had some issues in test when reseting the etl db, the processing cycle ids go back to 1. 
        # in dw-etl-test, if ezproxy_etl is run first, then the db_prcsng_cycle table has the accurate processing cycle id based on the reporting max. 
        job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)
        
    # print processing cycle id
    logger.info(f'processing cycle id: {job_info.prcsng_cycle_id}\n')  
    print(f'processing cycle id: {job_info.prcsng_cycle_id}\n')

    '''
    load_stage_1
    '''
    load_stage_1.load_stage_1(job_info, input_directory, logger, table_mappings.stg_1_table_mapping, db_session_creator)
    '''
    load_stage_2
    load 'in_' values from stg1 to stg 2 tables
    load 'in_' values
    '''
    load_stage_2.load_stage_2(job_info, logger, table_mappings.stg_1_to_stg_2_table_mapping, db_session_creator)

    '''
    stg 2 intertable processing DQ and T
    '''
    stage_2_intertable_processing.stage_2_intertable_processing(job_info, logger, table_mappings.stg_2_table_dim_mapping, db_session_creator)



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
    # give hint if --help
    if '--help' in arguments:
        print('Usage: ')
        print('\tdwetl.py [YYYYMMDD] [test (if you want to run dwetl with the test db)]')
        sys.exit(1)
    if len(arguments) == 2:
        today = arguments[1]
    
    # TODO: for local dev uncomment the following today to test only one date
    today = "20191204" # tiff's local test date
    #today = "20191211" # nima's local test date

    # get input directory from .env file. 
    input_directory = os.getenv("INPUT_DIRECTORY")+f"/{today}"
    
    
    # TODO: move processed file to processed directory
    # and when an already processed file is run, use the processed input directory
    run(input_directory)
