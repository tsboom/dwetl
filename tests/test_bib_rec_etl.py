import unittest
import dwetl.database_credentials as database_credentials
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
from dwetl.job_info import JobInfo
import dwetl

from dwetl.writer.list_writer import ListWriter
from dwetl.reader.list_reader import ListReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import json
import pdb
import stage_2_intertable_processing
import load_stage_1
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from stage_2_intertable_processing import stage_2_intertable_processing

class TestBibRecEtl(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    
    @classmethod
    def setUpClass(cls):
        cls.bib_record_dimension_sample_data_z00 = bib_record_dimension_sample_data.bib_rec_sample_data_z00
        cls.bib_record_dimension_sample_data_z13 = bib_record_dimension_sample_data.bib_rec_sample_data_z13
        
        cls.logger = test_logger.logger
        
        
        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_json_config = json.load(json_file)
        
    # # if preprocessing writes data to pp values in stage 2
    # def test_preprocessing_pp_values_exist(self):
    # 
    #     # currently testing end to end
    #     with dwetl.test_database_session() as test_session:
    #         # TODO: we need to add z13 and z13u to these . and mai01 vs mai39
    # 
    # 
    #         error_writer = SqlAlchemyWriter(test_session, dwetl.Base.classes['dw_db_errors'])
    #         job_info = JobInfo(-1, 'thschone', '1.0.0', 1)
    # 
    #         '''
    #         load stage 1
    #         '''
    #         reader = ListReader(self.bib_record_dimension_sample_data_z00)
    #         table = 'dw_stg_1_mai01_z00'
    #         writer = SqlAlchemyWriter(test_session, dwetl.Base.classes[table])
    #         processor = LoadAlephTsv(reader, writer, job_info, self.logger, error_writer)
    #         processor.execute()
    #         pdb.set_trace()
    # 
    # 
    #         '''
    #         test stage 2
    #         '''
    #         table = 'dw_stg_2_bib_rec_z00'
    #         # gets SA base class for the current table
    #         stage2_table_class = dwetl.Base.classes[table]
    #         # gets list of PKs for the current table
    #         pk_list = [pk.name for pk in stage2_table_class.__table__.primary_key]
    #         writer = SqlAlchemyWriter(test_session, stage2_table_class)
    # 
    #         logger=self.logger
    #         json_config = self.bib_rec_json_config
    #         error_writer = self.error_writer
    # 
    # 
    # 
    #         stage_2_intertable_processing.stage_2_intertable_processing(reader, writer, job_info, logger, json_config, pk_list, error_writer)
    #         pdb.set_trace()
    # 
    # 
    # 
    #         # query the results in the databse for the 3 items in the sample data for z00
    #         pdb.set_trace()
    #         results = test_session.query(table_base_class).all()