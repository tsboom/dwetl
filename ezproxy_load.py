import datetime
import os
import sys
import pdb
import dwetl
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.reader.ezproxy_reader import EzproxyReader
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from dwetl.processor.copy_stage1_to_stage2 import CopyStage1ToStage2
from dwetl.processor.ezproxy_processor import EzproxyProcessor
from dwetl.processor.ezproxy_fact_processor import EzproxyFactProcessor
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine

'''
load EZ Proxy file equivalent table (Stage 1)
'''


def load_stage_1(job_info, input_file, logger):
    print('EZProxy Loading stage 1...')
    logger.info('EZ Proxy Loading stage 1...')
    
    table = 'dw_stg_1_ezp_sessns_snap'

    with dwetl.database_session() as session:
        reader = EzproxyReader(input_file)
        # writer = PrintWriter()
        writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
        processor = LoadAlephTsv(reader, writer, job_info, logger)
        processor.execute()



def load_stage_2(job_info, logger):
    print('EZProxy Loading stage 2...')
    logger.info('EZProxy Loading stage 2...')
    
    processing_cycle_id = job_info.prcsng_cycle_id
    
    with dwetl.database_session() as session:
        stage1_table_class = dwetl.Base.classes["dw_stg_1_ezp_sessns_snap"]
        stage2_table_class = dwetl.Base.classes["dw_stg_2_ezp_sessns_snap"]
        reader = SqlAlchemyReader(session, stage1_table_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
        writer = SqlAlchemyWriter(session, stage2_table_class)
        # there is no aleph library for ez proxy data, but CopyStage1ToStage2 still will work
        library = ''
        processor = CopyStage1ToStage2.create(reader, writer, job_info, logger, library)
        processor.execute()
    
def intertable_processing(job_info, logger):
    stage2_table = dwetl.Base.classes['dw_stg_2_ezp_sessns_snap']
    processing_cycle_id = job_info.prcsng_cycle_id
    
    with dwetl.database_session() as session:
        reader = SqlAlchemyReader(session, stage2_table, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
        writer = SqlAlchemyWriter(session, stage2_table)


        processor = EzproxyProcessor(reader, writer, job_info, logger)
        processor.execute()
        
def load_fact_table(job_info, logger):
    stage2_table = dwetl.Base.classes['dw_stg_2_ezp_sessns_snap']
    fact_table = dwetl.Base.classes['fact_ezp_sessns_snap']
    processing_cycle_id = job_info.prcsng_cycle_id
    
    
    
    with dwetl.database_session() as session:
        reader = SqlAlchemyReader(session, stage2_table, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
        writer = SqlAlchemyWriter(session, fact_table)
        processor = EzproxyFactProcessor(reader, writer, job_info, logger)
        processor.execute()
        
    
    
    
    
# '''
# TODO: be able to load stage 1 from the command line using this one script
# main function for running script from the command line
# '''
# if __name__ == '__main__':
#     arguments = sys.argv
# 
#     if len(arguments) < 2 or len(arguments) > 3:
#         print('Usage: ')
#         print('\tezproxy_load.py [prcsng_cycle_id] [YYYYMMDD] ')
#         sys.exit(1)
# 
#     today = datetime.datetime.now().strftime('%Y%m%d')
#     prcsng_cycle_id = arguments[1]
# 
#     # give hint if --help
#     if '--help' in arguments:
#         print('Usage: ')
#         print('\tezproxy_load.py [YYYYMMDD]')
#         sys.exit(1)
#     # if a date string is provided, load that date's ezproxy data
#     if len(arguments) == 3:
#         today = arguments[2]
# 
#     # put together filename from date
#     filename = f"sessions.log.{today}"
# 
#     input_file = f'data/ezproxy/{filename}'
# 
#     job_info = JobInfoFactory.create_from_prcsng_cycle_id(prcsng_cycle_id)
# 
#     load_stage_1(job_info, input_file, logger)
