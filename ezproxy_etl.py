import dwetl
import datetime
import os
import sys
import shutil
import socket
from dotenv import load_dotenv
load_dotenv()
import dwetl.database_credentials as database_credentials
import logging
import sqlalchemy
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.writer.print_writer import PrintWriter
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import ezproxy_load
import pdb

def run(input_file):    
    #create logger
    today = datetime.datetime.now().strftime('%Y%m%d')
    logger = logging.getLogger('dwetl')
    file_handler = logging.FileHandler(f'logs/ezproxy.log.{today}')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    time_started = datetime.datetime.now()
    logger.info(f'EzProxy ETL started')
    logger.info(f'input file path {input_file}')    
    
    '''
    check current hostname environment configuration to prevent errors
    '''
    hostname= socket.gethostname()
    configured_host = database_credentials.configured_host()
    
    if hostname != configured_host:
       #quit program if env file hostname doesn't match with the current hostname
       print('ERROR: EzProxy ETL ended because .env contained an error. Please double check the configured host and db configuration.')
       logger.error(f'EzProxy ETL ended because .env contained an error. please double check the configured host and db configuration.')
       sys.exit()
    
    '''
    create job_info for current process
    '''
    with dwetl.database_session() as session:
        job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
        job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)




    '''
    load ezproxy stage 1 
    '''
    ezproxy_load.load_stage_1(job_info, input_file, logger)
    
    
    '''
    load ezproxy stage 2 
    '''
    ezproxy_load.load_stage_2(job_info, logger)
    
    
    '''
    stg 2 intertable processing
    '''
    ezproxy_load.intertable_processing(job_info, logger)
    
    '''
    fact table load
    '''
    ezproxy_load.load_fact_table(job_info, logger)
    
    
    '''
    copy new ezproxy data to reporting database 
    '''
    ezproxy_load.copy_new_facts_to_reporting_db(job_info, logger)
    
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
    print("Ezproxy ETL elapsed time: ", str(elapsed_time))
    logger.info(f'EzProxy ETL elapsed time: {str(elapsed_time)}')
    
    '''
    move data file to "processed" directory
    '''
    processed_dir = "/apps/dw/processed/ezproxy/"
    just_filename = input_file.split('/')[-1]
    shutil.move(input_file, processed_dir + just_filename)
    logger.info('Moved file to processed directory.')

'''
main function for running script from the command line
'''
if __name__=='__main__':
    arguments = sys.argv

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    day_to_process = yesterday.strftime('%Y%m%d')
    
    # give hint if --help
    if '--help' in arguments:
        print('Usage: ')
        print('\tezproxy_etl.py datestring')
        sys.exit(1)
    # if a date string is provided, load that date's ezproxy data
    if len(arguments) == 2:
        day_to_process = arguments[1]
        
    # otherwise process today's date, put together filename from date 
    filename = f"sessions.log.{day_to_process}"
    input_directory = os.getenv("EZPROXY_INPUT_DIRECTORY")  
    incoming_input_file = input_directory + filename
    processed_dir = "/apps/dw/processed/ezproxy/"
    processed_input_file = processed_dir + filename
    if os.path.exists(incoming_input_file):
        print(f'input file: {incoming_input_file}')
        run(incoming_input_file)
    elif os.path.exists(processed_input_file):
        print(f'input file: {processed_input_file}')
        run(processed_input_file)   
        # Print the message if the file path does not exist
    else:
        print (f'no data file found for {day_to_process}')

