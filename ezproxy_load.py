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
from dwetl.processor.ezproxy_processor import EzproxyProcessor
from dwetl.processor.ezproxy_fact_processor import EzproxyFactProcessor
from dwetl.processor.ezproxy_reporting_fact_processor import EzproxyReportingFactProcessor
from dwetl.processor.copy_stage1_to_stage2 import CopyStage1ToStage2
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import func
import pprint

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
    logger.info('Finished EZProxy loading stage 2 .... ')

def intertable_processing(job_info, logger):
    logger.info('EZProxy intertable processing starts...')
    stage2_table = dwetl.Base.classes['dw_stg_2_ezp_sessns_snap']
    processing_cycle_id = job_info.prcsng_cycle_id

    with dwetl.database_session() as session:
        reader = SqlAlchemyReader(session, stage2_table, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
        writer = SqlAlchemyWriter(session, stage2_table)
        processor = EzproxyProcessor(reader, writer, job_info, logger)
        processor.execute()
    logger.info('Finished EZProxy intertable processing .... ')

def load_fact_table(job_info, logger):
    logger.info('Loading to the fact table.... ')
    stage2_table = dwetl.Base.classes['dw_stg_2_ezp_sessns_snap']
    fact_table = dwetl.Base.classes['fact_ezp_sessns_snap']
    processing_cycle_id = job_info.prcsng_cycle_id

    # get max value for fact key from the reporting db
    with dwetl.reporting_database_session() as session2:
        reporting_fact_table = dwetl.ReportingBase.classes['fact_ezp_sessns_snap']
        max_ezp_sessns_snap_fact_key = session2.query(func.max(reporting_fact_table.ezp_sessns_snap_fact_key)).scalar()

    if max_ezp_sessns_snap_fact_key is None:
        max_ezp_sessns_snap_fact_key = 1

    # load etl ezp fact table
    with dwetl.database_session() as session:
        reader = SqlAlchemyReader(session, stage2_table, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
        writer = SqlAlchemyWriter(session, fact_table)
        processor = EzproxyFactProcessor(reader, writer, job_info, logger, max_ezp_sessns_snap_fact_key)
        processor.execute()
    logger.info('Finished loading to the fact table.... ')


def copy_new_facts_to_reporting_db(job_info, logger):
    etl_fact_table = dwetl.Base.classes['fact_ezp_sessns_snap']
    processing_cycle_id = job_info.prcsng_cycle_id

    # query and select records from etl fact table
    # should we use the create update processing cycle ID? or the Update processing cycle id?
    with dwetl.database_session() as session:
        reader = SqlAlchemyReader(session, etl_fact_table, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
        session.expunge_all()

    # insert records into reporting db ezp fact table
    with dwetl.reporting_database_session() as session2:
        reporting_fact_table = dwetl.ReportingBase.classes['fact_ezp_sessns_snap']
        writer = SqlAlchemyWriter(session2, reporting_fact_table)
        processor = EzproxyReportingFactProcessor(reader, writer, job_info, logger)
        processor.execute()
        