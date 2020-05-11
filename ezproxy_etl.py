import dwetl
import datetime
import os
import sys
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.writer.print_writer import PrintWriter
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import ezproxy_load
import pdb



def run(input_directory):
    
    #create logger
    today = datetime.datetime.now().strftime('%Y%m%d')
    logger = logging.getLogger('dwetl')
    file_handler = logging.FileHandler(f'logs/dwetl.log.{today}')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    time_started = datetime.datetime.now()
    logger.info(f'EzProxy etl started')

    '''
    create job_info for current process
    '''
    with dwetl.database_session() as session:
        job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
        job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)




    '''
    load ezproxy stage 1 
    '''
    ezproxy_load.load_stage_1(job_info, input_directory, logger)
    
    
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
        print('\tezproxy_etl.py datestring')
        sys.exit(1)
    # if a date string is provided, load that date's ezproxy data
    if len(arguments) == 2:
        today = arguments[1]
        
    # put together filename from date 
    filename = f"sessions.log.{today}"
    # input_directory = f'data/{today}/'
    input_directory = f'data/ezproxy/'
    
    input_file = f'data/ezproxy/{filename}'

    run(input_file)


    