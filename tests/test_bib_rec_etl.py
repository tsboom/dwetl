import unittest
import dwetl.database_credentials as database_credentials
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
import dwetl
from dwetl.writer.list_writer import ListWriter
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import json

from stage_2_intertable_processing import preprocess_tables, dataquality_check_tables

class TestBibRecEtl(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    
    @classmethod
    def setUpClass(cls):
        cls.bib_record_dimension_sample_data_z00 = bib_record_dimension_sample_data.bib_rec_sample_data_z00
        cls.bib_record_dimension_sample_data_z13 = bib_record_dimension_sample_data.bib_rec_sample_data_z13
        
        cls.logger = test_logger.logger
        cls.error_writer = ListWriter()
        
        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_json_config = json.load(json_file)
        
    # if preprocessing writes data to pp values in stage 2
    def test_preprocessing_pp_values_exist(self):
        
        with dwetl.test_database_session() as test_session:
            pdb.set_trace()
            reader = self.bib_record_dimension_sample_data_z00
            table_base_class = dwetl.Base.classes['dw_stg_2_bib_rec_z00']
            writer = SqlAlchemyWriter(testsession, table_base_class)
            job_info = JobInfo(-1, 'thschone', '1.0.0', 1)
            logger=self.logger
            json_config = self.bib_rec_json_config
            error_writer = self.error_writer

            stage_2_intertable_processing.preprocess_tables(reader, writer, job_info, logger, json_config, pk_list, error_writer)
            pdb.set_trace()
            
            
        
            # query the results in the databse for the 3 items in the sample data for z00
            pdb.set_trace()
            results = test_session.query(table_base_class).all()