from dwetl.processor.create_file_equivalent_table import CreateFileEquivalentTable
from dwetl.processor.identity_processor import IdentityProcessor
from dwetl.processor.copy_stage1_to_stage2 import CopyStage1ToStage2
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.writer.print_writer import PrintWriter
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import datetime
import pdb
import dwetl

def aleph_library(table_name):
    '''
    Returns a string representing the Aleph library from the given table name
    
    :param table_name: the name of the table being processed 
    :return: a string representing the Aleph library from the given table name
    '''
    table_name.split('_')[0]
    return 'mai50'

# # See https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
# db_settings = database_credentials.db_settings()
# engine = create_engine(db_settings['DB_CONNECTION_STRING'])
# # connect to the database
# connection = engine.connect()
#
# # begin a non-ORM transaction
# # self.trans = self.connection.begin()
#
# # bind an individual Session to the connection
# s = sessionmaker()
# session = s(bind=connection)
#
# Base = automap_base()
# Base.prepare(engine, reflect=True)

base_data_file_directory = '/Users/dsteelma/Desktop/DWETL/TSV/20190914/'

stage1_to_stage2_table_mappings = {
# 'dw_stg_1_mai01_z00': 'dw_stg_2_bib_rec_z00',
 'dw_stg_1_mai50_z30': 'dw_stg_2_lbry_item_z30'
}

job_info = {
    'em_create_dw_prcsng_cycle_id': 9999,
    'em_create_dw_job_exectn_id': 9999,
    'em_create_dw_job_name': 'TEST',
    'em_create_dw_job_version_no': '0.0',
    'em_create_user_id': 'test_user',
    'em_create_tmstmp': datetime.datetime.now()
}

logger = None

processing_cycle_id = job_info['em_create_dw_prcsng_cycle_id']
for stage1_table, stage2_table in stage1_to_stage2_table_mappings.items():
    aleph_library = aleph_library(stage1_table)

    with dwetl.database_session() as session:
        stage1_table_class = dwetl.Base.classes[stage1_table]
        stage2_table_class = dwetl.Base.classes[stage2_table]
        reader = SqlAlchemyReader(session, stage1_table_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
 #       writer = PrintWriter()
        writer = SqlAlchemyWriter(session, stage2_table_class)
        processor = CopyStage1ToStage2.create(reader, writer, job_info, logger, aleph_library)
        processor.execute()

# mpf_file_to_table_mapping = {
#     'mpf_item-process-status-dimension.txt': Base.classes['dim_lbry_item_prcs_status']
# }
#
# for mpf_file, table_class in mpf_file_to_table_mapping.items():
#     mpf_file_path = base_data_file_directory + mpf_file
#     reader = MpfFileReader(mpf_file_path)
#     writer = SqlAlchemyWriter(session, table_class)
#     step = CreateFileEquivalentTable.create(reader, writer, job_info, logger)
#     step.execute()
