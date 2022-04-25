from dwetl.processor.copy_stage1_to_stage2 import CopyStage1ToStage2
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.job_info import JobInfoFactory
import dwetl
import sys
import re
import pdb
import pprint


def aleph_library(table_name):
    """
    Returns a string representing the Aleph library from the given table name

    :param table_name: the name of the table being processed
    :return: a string representing the Aleph library from the given table name
    """
    m = re.search('dw_stg_1_(.*?)_.*', table_name)
    library = m.group(1)

    if library == 'mpf':
        return None
    return library



def load_stage_2(job_info, logger, stage1_to_stage2_table_mapping, db_session_creator):

    print('Loading stage 2...\n')
    logger.info('Loading stage 2...\n')

    processing_cycle_id = job_info.prcsng_cycle_id

    # set of unique stage 2 tables to assist with counting totals
    stage2_table_list = set()
    # count up values from stage 2 tables
    loaded_record_count = 0

    for stage1_table, stage2_table in stage1_to_stage2_table_mapping.items():
        # create set of unique stage 2 values
        stage2_table_list.add(stage2_table)
        library = aleph_library(stage1_table)

        with db_session_creator() as session:
            stage1_table_class = dwetl.Base.classes[stage1_table]
            stg_1_count = session.query(stage1_table_class).filter(stage1_table_class.em_create_dw_prcsng_cycle_id==job_info.prcsng_cycle_id).count()
            print(f'\t\n{stg_1_count} records loaded to {stage1_table}.')
            logger.info(f'\t\n{stg_1_count} records loaded to {stage1_table}.')
            stage2_table_class = dwetl.Base.classes[stage2_table]
            reader = SqlAlchemyReader(session, stage1_table_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
            writer = SqlAlchemyWriter(session, stage2_table_class)
            error_writer = SqlAlchemyWriter(session, dwetl.Base.classes['dw_db_errors'])
            processor = CopyStage1ToStage2.create(reader, writer, job_info, logger, library, error_writer)
            processor.execute()

    # count up records in stg 2 tables
    with db_session_creator() as session:
        for table in stage2_table_list:
            stage2_table_class = dwetl.Base.classes[table]
            stg_2_count = session.query(stage2_table_class).filter(stage2_table_class.em_create_dw_prcsng_cycle_id==job_info.prcsng_cycle_id).count()
            print(f'\t\n{stg_2_count} records loaded to {table}.')
            logger.info(f'\t\n{stg_2_count} records loaded to {table}.')
            loaded_record_count = loaded_record_count + stg_2_count

    logger.info(f'Total records loaded in stage 2: {loaded_record_count}\n')
    print(f'Total records loaded in stage 2: {loaded_record_count}\n')





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
    load_stage_2(job_info)
