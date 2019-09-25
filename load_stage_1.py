import datetime
from dwetl.job_info import JobInfoFactory, JobInfo
from dwetl.reader.tsv_file_reader import TsvFileReader
from dwetl.reader.z00_field_reader import Z00FieldReader
from dwetl.writer.print_writer import PrintWriter
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from dwetl.processor.load_z00_field_tsv import LoadZ00FieldTsv
from dwetl.processor.load_mpf_tsv import LoadMpfTsv
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import dwetl




def load_stage_1(job_info, input_directory):


    '''
    file to table mapping
    '''

    ALEPH_TSV_TABLE_MAPPING = {
        "mai01_z00_data": "dw_stg_1_mai01_z00",
        "mai01_z13_data": "dw_stg_1_mai01_z13",
        "mai01_z13u_data": "dw_stg_1_mai01_z13u",
        "mai39_z00_data": "dw_stg_1_mai39_z00",
        "mai39_z13_data": "dw_stg_1_mai39_z13",
        "mai39_z13u_data": "dw_stg_1_mai39_z13u",
        "mai60_z00_data": "dw_stg_1_mai60_z00",
        "mai60_z13_data": "dw_stg_1_mai60_z13",
        "mai60_z13u_data": "dw_stg_1_mai60_z13u",
        "mai60_z103_bib_data": "dw_stg_1_mai50_z103_bib",
        "mai50_z30_data": "dw_stg_1_mai50_z30",
        "mai50_z35_data": "dw_stg_1_mai50_z35",
        # "mai50_z30_full_data": "dw_stg_1_mai50_z30_full",
        # "mai50_z103_bib_full_data": "dw_stg_2_lbry_item_z103_bib_full",

    }

    Z00_FIELD_TABLE_MAPPING = {
        "mai01_z00_field_data": "dw_stg_1_mai01_z00_field",
        "mai39_z00_field_data": "dw_stg_1_mai39_z00_field",
        "mai60_z00_field_data": "dw_stg_1_mai60_z00_field",
    }

    MPF_TABLE_MAPPING = {
        "mpf_member-library-dimension.txt": "dw_stg_1_mpf_mbr_lbry",
        "mpf_library-entity-dimension.txt": "dw_stg_1_mpf_lbry_entity",
        "mpf_library-collection-dimension.txt": "dw_stg_1_mpf_collection",
        "mpf_item-status-dimension.txt": "dw_stg_1_mpf_item_status",
        "mpf_item-process-status-dimension.txt": "dw_stg_1_mpf_item_prcs_status",
        "mpf_material-form-dimension.txt": "dw_stg_1_mpf_matrl_form"
    }

    '''
    load aleph tsv files minus z00_field tables
    '''

    for file, table in ALEPH_TSV_TABLE_MAPPING.items():
        file_path = input_directory + file
        print(file_path)
        with dwetl.database_session() as session:
            reader = TsvFileReader(file_path)
            # writer = PrintWriter()
            writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
            logger = None
            processor = LoadAlephTsv(reader, writer, job_info, logger)
            processor.execute()



    '''
    load z00 field files
    '''
    for file, table in Z00_FIELD_TABLE_MAPPING.items():
        file_path = input_directory + file
        print(file_path)
        with dwetl.database_session() as session:
            reader = Z00FieldReader(file_path)
            # writer = PrintWriter()
            writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
            logger = None
            processor = LoadZ00FieldTsv(reader, writer, job_info, logger)
            processor.execute()



    '''
    load mpf tsv files
    '''

    for file, table in MPF_TABLE_MAPPING.items():
        file_path = input_directory + file
        print(file_path)
        with dwetl.database_session() as session:
            # reader = TsvFileReader('data/20190920/mai50_z30_full_data')
            reader = TsvFileReader(file_path)
            #writer = PrintWriter()
            writer = SqlAlchemyWriter(session, dwetl.Base.classes[table])
            logger = None
            processor = LoadMpfTsv(reader, writer, job_info, logger)

            processor.execute()
