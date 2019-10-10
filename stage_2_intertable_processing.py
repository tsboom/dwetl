from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.job_info import JobInfoFactory
import dwetl
import pdb
import json
import datetime
import os
import sys
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.processor.preprocess import Preprocess
from dwetl.processor.data_quality_processor import DataQualityProcessor
from dwetl.writer.print_writer import PrintWriter
import dwetl

def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config


def stage_2_intertable_processing(job_info):
    print("Stage 2 Intertable Processing...")

    STG_2_TABLE_CONFIG_MAPPING = {
        'dw_stg_2_bib_rec_z00': 'bibliographic_record_dimension',
        'dw_stg_2_bib_rec_z13': 'bibliographic_record_dimension',
        'dw_stg_2_bib_rec_z13u': 'bibliographic_record_dimension',
        'dw_stg_2_bib_rec_z00_field': 'bibliographic_record_dimension'
    }


    logger = None

    processing_cycle_id = job_info.prcsng_cycle_id

    for table, dimension in STG_2_TABLE_CONFIG_MAPPING.items():
        print(table)
        # get json_config for current dimension
        table_config_path = os.path.join('table_config', dimension + '.json')
        json_config = load_table_config(table_config_path)

        with dwetl.database_session() as session:
            # gets SA base class for the current table
            stage2_table_class = dwetl.Base.classes[table]
            # gets list of PKs for the current table
            pk_list = [pk.name for pk in stage2_table_class.__table__.primary_key]

            reader = SqlAlchemyReader(session, stage2_table_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
            writer = SqlAlchemyWriter(session, stage2_table_class)

            '''
            Preprocessing
            '''
            preprocessor = Preprocess(reader, writer, job_info, logger, json_config, pk_list)
            preprocessor.execute()

            '''
            # Data Quality Checks
            # '''
            data_quality_checker = DataQualityProcessor(reader, writer, job_info, logger, json_config, pk_list)
            data_quality_checker.execute()















'''
main function for running script from the command line
'''

if __name__=='__main__':
    arguments = sys.argv

    if len(arguments) != 2:
        print('Usage: ')
        print('\tload_stage_2.py [prcsng_cycle_id]')
        sys.exit(1)

    prcsng_cycle_id = arguments[1]

    job_info = JobInfoFactory.create_from_prcsng_cycle_id(prcsng_cycle_id)
    stage_2_intertable_processing(job_info)
