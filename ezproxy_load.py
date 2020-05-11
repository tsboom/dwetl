import datetime
import os
import sys
import pdb
import dwetl
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.reader.ezproxy_reader import EzproxyReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter

'''
load EZ Proxy file equivalent table (Stage 1)
'''


def load_stage_1(job_info, input_file):
    print('EZProxy Loading stage 1...')
    # logger.info('EZ Proxy Loading stage 1...')
    
    table = 'dw_stg_1_ezp_sessns_snap'

    with dwetl.database_session() as session:
        reader = EzproxyReader(input_file)
        # writer = PrintWriter()
        writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
        processor = LoadAlephTsv(reader, writer, job_info, logger)
        processor.execute()


'''
main function for running script from the command line
'''
if __name__ == '__main__':
    arguments = sys.argv

    if len(arguments) < 2 or len(arguments) > 3:
        print('Usage: ')
        print('\tezproxy_load.py [prcsng_cycle_id] [YYYYMMDD] ')
        sys.exit(1)

    today = datetime.datetime.now().strftime('%Y%m%d')
    prcsng_cycle_id = arguments[1]

    # give hint if --help
    if '--help' in arguments:
        print('Usage: ')
        print('\tezproxy_load.py [YYYYMMDD]')
        sys.exit(1)
    # if a date string is provided, load that date's ezproxy data
    if len(arguments) == 3:
        today = arguments[2]

    # put together filename from date
    filename = f"sessions.log.{today}"

    input_file = f'data/ezproxy/{filename}'

    job_info = JobInfoFactory.create_from_prcsng_cycle_id(prcsng_cycle_id)

    load_stage_1(job_info, input_file)
