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
from sqlalchemy import func
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
    logger.setLevel(logging.DEBUG)

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
       print(f'ERROR: EzProxy ETL ended because .env contained an error with the hostname {hostname}. Please double check the configured host and db configuration.')
       logger.error(f'EzProxy ETL ended because .env contained an error. please double check the configured host and db configuration.')
       sys.exit()
    
    '''
    create job_info for current process
    '''
    # Determine processing cycle ID by using the reporting db as the authority
    with dwetl.reporting_database_session() as session2:
        reporting_fact_table = dwetl.ReportingBase.classes['fact_ezp_sessns_snap']
        # query max processing id in ezproxy fact table in the reporting db
        reporting_prcsng_id = session2.query(func.max(reporting_fact_table.em_create_dw_prcsng_cycle_id)).scalar()
        # increment the processing cycle id by 1 if it starts as None
        if reporting_prcsng_id == None: 
            reporting_max_prcsng_id = 1
        else: 
            reporting_max_prcsng_id = reporting_prcsng_id + 1

    with dwetl.database_session() as session:
        job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
        # check to see if the processing cycle id from the reporting db (reporting_max_processing_id)
        # is already in the etl db, if it is, increment it by 1 to make it unique
        job_info = JobInfoFactory.create_job_info_from_reporting_db(session, job_info_table_class, reporting_max_prcsng_id, logger)
    pdb.set_trace()

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
    move data file to "processed" directory
    '''
    processed_dir = os.getenv("DATA_DIRECTORY") + "processed/ezproxy/"
    just_filename = input_file.split('/')[-1]
    try:
        shutil.move(input_file, processed_dir + just_filename)
        logger.info('Moved file to processed directory.')
    except Exception as e:
        print(e)
        logger.error('Failed to move file to processed directory: '  + str(e))

    
    '''
    report status and errors
    '''

    # query to find # of rows written to the error table during the current process
    with dwetl.database_session() as session:
        error_table_class = dwetl.Base.classes['dw_db_errors']
        # count number of records with the current process id
        error_count = session.query(error_table_class).\
            filter(error_table_class.em_create_dw_prcsng_cycle_id == job_info.prcsng_cycle_id).count()
        print(f"\n\nNumber of errors: {error_count}")


    # query to find # of rows written to the reporting db during the current process
    with dwetl.reporting_database_session() as session:
        reporting_fact_table = dwetl.ReportingBase.classes['fact_ezp_sessns_snap']
        # count number of records with the current process id
        fact_count = session.query(reporting_fact_table).\
            filter(reporting_fact_table.em_create_dw_prcsng_cycle_id == job_info.prcsng_cycle_id).count()
        print(f'\n\nNumber of facts written to the reporting db: \n{fact_count}')
        


    
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
    
    if error_count > 0:
        print("Completed with errors.")
    else: 
        print("Completed!")


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
        print('\tezproxy_etl.py YYYYMMDD')
        sys.exit(1)
    # if a date string is provided, load that date's ezproxy data
    if len(arguments) == 2:
        day_to_process = arguments[1]
        
    # otherwise process today's date, put together filename from date 
    filename = f"sessions.log.{day_to_process}"
    data_directory = os.getenv("DATA_DIRECTORY")
    input_directory = data_directory + 'incoming/ezproxy/'
    incoming_input_file = input_directory + filename
    processed_dir = data_directory + "processed/ezproxy/"
    processed_input_file = processed_dir + filename
    if os.path.exists(incoming_input_file):
        print(f'input file: {incoming_input_file}')
        run(incoming_input_file)
    elif os.path.exists(processed_input_file):
        print(f'input file: {processed_input_file}')
        run(processed_input_file)   
        # Print the message if the file path does not exist
    else:
        print (f'no data file found for {day_to_process}. Are you sure you provided the date like so? python ezproxy_etl.py YYYYMMDD')

