from dwetl.processor.create_file_equivalent_table import CreateFileEquivalentTable
from dwetl.reader.tsv_file_reader import TsvFileReader
from dwetl.reader.mpf_file_reader import MpfFileReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import datetime
import dwetl

base_data_file_directory = '/Users/dsteelma/Desktop/DWETL/TSV/20190914/'

tsv_file_to_table_mapping = {
    'mai01_z00_data': 'dw_stg_1_mai01_z00',
    'mai50_z30_data': 'dw_stg_1_mai50_z30'
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

for tsv_file, table_name in tsv_file_to_table_mapping.items():
    tsv_file_path = base_data_file_directory + tsv_file
    with dwetl.database_session() as session:
        table_class = dwetl.Base.classes[table_name]
        reader = TsvFileReader(tsv_file_path)
        writer = SqlAlchemyWriter(session, table_class)
        processor = CreateFileEquivalentTable.create(reader, writer, job_info, logger)
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
