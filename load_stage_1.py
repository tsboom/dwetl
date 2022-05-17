import datetime
import os
import sys
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.reader.tsv_file_reader import TsvFileReader
from dwetl.reader.z00_field_reader import Z00FieldReader
from dwetl.writer.print_writer import PrintWriter
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from dwetl.processor.load_z00_field_tsv import LoadZ00FieldTsv
from dwetl.processor.load_mpf_tsv import LoadMpfTsv
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import dwetl
import pdb




def load_stage_1(job_info, input_directory, logger, table_mapping, session_creator):

    print('Loading stage 1...')
    logger.info('Loading stage 1...')




    '''
    load aleph tsv files minus z00_field tables
    '''
    loaded_record_count = 0

    # loop through files and load stage 1 tables
    for file, table in table_mapping['ALEPH_TSV_TABLE_MAPPING'].items():
        file_path = os.path.join(input_directory, file)
        logger.info(file_path)
        with session_creator() as session:
            reader = TsvFileReader(file_path)
            stg_1_table_base_class = dwetl.Base.classes[table]
            writer = SqlAlchemyWriter(session, stg_1_table_base_class)
            error_writer = SqlAlchemyWriter(session, dwetl.Base.classes['dw_db_errors'])
            processor = LoadAlephTsv(reader, writer, job_info, logger, error_writer)
            processor.execute()

            # count number records read from TSV and how many written to stage 1 table
            tsv_record_count = reader.record_count
            stage_1_record_count = session.query(stg_1_table_base_class).\
                filter(stg_1_table_base_class.em_create_dw_prcsng_cycle_id == job_info.prcsng_cycle_id).count()
            print(f'\t\n{tsv_record_count} records in {file} TSV. \n{stage_1_record_count} records loaded to {table}.')
            logger.info(f'\t\n{tsv_record_count} records in  {file} TSV. \n{stage_1_record_count} records loaded to {table}.')

            loaded_record_count = loaded_record_count + stage_1_record_count

    # exit DWETL if no records are loaded
    print(f'\nTotal records loaded in stage 1: {loaded_record_count}\n')
    logger.info(f'\nTotal records loaded in stage 1: {loaded_record_count}\n')
    if loaded_record_count == 0:
        print('\nNo records were loaded. Please check your input files and directory paths.')
        print('\nQuitting DWETL.\n-----\n')
        logger.error('\nNo records were loaded. Please check your input files and directory paths.\nQuitting DWETL.\n-----\n')
        quit()

    # '''
    # load mpf tsv files
    # '''
    #
    for file, table in table_mapping['MPF_TABLE_MAPPING'].items():
        file_path = os.path.join(input_directory, file)
        print(file_path)
        with dwetl.database_session() as session:
            # reader = TsvFileReader('data/20190920/mai50_z30_full_data')
            reader = TsvFileReader(file_path)
            #writer = PrintWriter()
            writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
            logger = None
            processor = LoadMpfTsv(reader, writer, job_info, logger, error_writer)

            processor.execute()

'''
main function for running script from the command line
'''
if __name__=='__main__':
    arguments = sys.argv

    if len(arguments) < 2 or len(arguments) > 3:
        print('Usage: ')
        print('\tload_stage_1.py [prcsng_cycle_id] [data_directory] ')
        sys.exit(1)

    prcsng_cycle_id = arguments[1]
    input_directory = os.path.dirname(os.path.realpath(__file__))
    today = datetime.datetime.now().strftime('%Y%m%d')
    # if 2nd argument isn't provided use today as data directory
    data_directory = os.path.join(input_directory,'data', today)

    # data directory can be specified as 2nd argument
    if len(arguments) == 3:
        data_directory = arguments[2]

    job_info = JobInfoFactory.create_from_prcsng_cycle_id(prcsng_cycle_id)
    load_stage_1(job_info, data_directory)
