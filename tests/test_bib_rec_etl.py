import unittest
import dwetl.database_credentials as database_credentials
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
from dwetl.job_info import JobInfo
import dwetl
import datetime
from dwetl.writer.list_writer import ListWriter
from dwetl.reader.list_reader import ListReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.job_info import JobInfoFactory
import json
import csv
import pdb
import stage_2_intertable_processing
import load_stage_1
import load_stage_2
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from sqlalchemy.inspection import inspect



'''
This file tests the entire bib rec dimension using the data from tsv files in tests/data/incoming_test/aleph/20210123

We have purposefully created data that failes DQ checks in the first lines of these files. 

In mai01_z00, the first line of the data file contains a missing z00_doc_number. The second line contains an invalid z00_doc_number.
In mai01_z13, the first line contains a missing z13_open_date, and a missing z13_update_date. The second line contains an invalid date for both fields. 
In mai01_z13u, we have a missing user_defined_2 in line one, and the second line contains an invalid user_defined_2 which tests its custom dq function.
'''

class TestBibRecEtl(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    
    @classmethod
    def setUpClass(cls):

        cls.logger = test_logger.logger

        bib_rec_sample_data = []
        bib_rec_sample_data.append({'mai'})
        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_json_config = json.load(json_file)

        # run ETL using sample data and write to the test postgres database (usmai_dw_etl_test)
        # currently testing end to end
        test_input_directory = 'tests/data/incoming_test/aleph/20210123'
        
        cls.db_session_creator = dwetl.test_database_session

        # create job info from test database session
        with cls.db_session_creator() as session:
            job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
            cls.job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)

        cls.prcsng_cycle_id = cls.job_info.prcsng_cycle_id
        
        cls.stg_1_table_mapping = {
            "ALEPH_TSV_TABLE_MAPPING": 
                {"mai01_z00_data": "dw_stg_1_mai01_z00",
                "mai39_z00_data": "dw_stg_1_mai39_z00",
                "mai01_z13_data": "dw_stg_1_mai01_z13",
                "mai39_z13_data": "dw_stg_1_mai39_z13",
                "mai01_z13u_data": "dw_stg_1_mai01_z13u",
                "mai39_z13u_data": "dw_stg_1_mai39_z13u"
                }
            }
        
            
        cls.logger.info(f'TEST DWETL.py started')
        
        
        
        '''
        load_stage_1
        '''
        load_stage_1.load_stage_1(cls.job_info, test_input_directory, cls.logger, cls.stg_1_table_mapping, cls.db_session_creator)

        '''
        load_stage_2
        '''
        cls.stage1_to_stage2_table_mapping = {
            "dw_stg_1_mai39_z13": "dw_stg_2_bib_rec_z13",
            'dw_stg_1_mai01_z13': "dw_stg_2_bib_rec_z13",
            "dw_stg_1_mai01_z13u": "dw_stg_2_bib_rec_z13u",
            "dw_stg_1_mai39_z13u": "dw_stg_2_bib_rec_z13u",
            "dw_stg_1_mai01_z00": "dw_stg_2_bib_rec_z00",
            "dw_stg_1_mai39_z00": "dw_stg_2_bib_rec_z00"
        }
        
        load_stage_2.load_stage_2(cls.job_info, test_input_directory, cls.logger, cls.stage1_to_stage2_table_mapping, cls.db_session_creator)
        
        '''
        stg 2 intertable processing
        '''
        cls.stg_2_table_config_mapping = {
            'dw_stg_2_bib_rec_z00': 'bibliographic_record_dimension',
            'dw_stg_2_bib_rec_z13': 'bibliographic_record_dimension',
            'dw_stg_2_bib_rec_z13u': 'bibliographic_record_dimension',
            'dw_stg_2_bib_rec_z00_field': 'bibliographic_record_dimension'
        }
        stage_2_intertable_processing.stage_2_intertable_processing(cls.job_info, cls.logger, cls.stg_2_table_config_mapping, cls.db_session_creator)
        
    # @classmethod
    # def tearDownClass(cls):
    #     # when tests are over, delete all the data from these bib rec tests 
    #     with dwetl.test_database_session() as session:
    #         prcsng_cycle_id = cls.prcsng_cycle_id
    # 
    #         # iterate over stage 1 tables and delete records with the current processing cycle id
    #         for file, table in cls.stg_1_table_mapping['ALEPH_TSV_TABLE_MAPPING'].items():
    #             table_base_class = dwetl.Base.classes[table]
    #             stg_1_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
    #             stg_1_results.delete()
    # 
    #         # iterate over stage 2 tables and delete all records added in this test file
    #         for stg_2_table, dimension in cls.stg_2_table_config_mapping.items():
    #             table_base_class = dwetl.Base.classes[stg_2_table]
    #             stg_2_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
    #             stg_2_results.delete()
    # 
    #         # commit all changes
    #         session.commit()
    def test_bib_rec_stage_1(self):
        # check to see if same amount of values from 20210123 in z00, z13, z13u 
        # were written to the stage 1 table. 
        with dwetl.test_database_session() as session:
            
            prcsng_cycle_id = self.__class__.prcsng_cycle_id
            
            # iterate over stage 1 tables and compare input rows in file to rows in stg 1 tables 
            for file, table in self.__class__.stg_1_table_mapping['ALEPH_TSV_TABLE_MAPPING'].items():
                table_base_class = dwetl.Base.classes[table]
                # compare count of input records to records written
                tsv_rows = sum(1 for line in open(f'tests/data/incoming_test/aleph/20210123/{file}'))
                if tsv_rows == 0:
                    input_record_count = 0
                else: 
                    input_record_count = sum(1 for line in open(f'tests/data/incoming_test/aleph/20210123/{file}'))- 3 #metadata rows
                stg_1_row_count = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id).count()
                # TODO: log test failure reasons
                self.assertEqual(input_record_count, stg_1_row_count)
            
    def test_bib_rec_stage_2_load_stage_2(self):
        # check to see if stage 2 tables contain the correct amount of records combined from stage 1 aleph libraries
        with dwetl.test_database_session() as session:
    
            prcsng_cycle_id = self.__class__.prcsng_cycle_id
    
            # capture total records for stage 2 combining diff aleph libraries into aleph tables (z00, z13, z13u)
            # example: {'dw_stg_2_bib_rec_z13': 344}
            stg_2_aleph_table_totals_expected = {}
    
            # because there are multiple stg 1 tables combining into stg 2 it's helpful to keep track of
            # the previous aleph table and previous total
            prev_aleph_table = None
            prev_aleph_table_total = 0
            # iterate over stg 1, stg 2 tables to compare records written per table
            for stg_1_table, stg_2_table in self.__class__.stage1_to_stage2_table_mapping.items():
                stg_1_table_base_class = dwetl.Base.classes[stg_1_table]
                stg_2_table_base_class = dwetl.Base.classes[stg_2_table]
                # query number of records in stg 2 and stge 2
                stg_1_count = session.query(stg_1_table_base_class).filter(stg_1_table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id).count()
                # stg 2 contains the totals from 2 stage 1 tables since they are combined per aleph table.
                stg_2_count = session.query(stg_2_table_base_class).filter(stg_2_table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id).count()
    
                # we should only count the totals of the combined stage 1 tables
                if prev_aleph_table:
                    # add to the totals expected dict per stg 2 table
                    if stg_2_table == prev_aleph_table:
                        stg_2_aleph_table_totals_expected[stg_2_table]  = stg_2_aleph_table_totals_expected[stg_2_table] + stg_1_count
                        self.assertEqual(stg_2_aleph_table_totals_expected[stg_2_table], stg_2_count)
                        prev_aleph_table = None
                    else:
                        # if the loop encounters a new table reset the prev_aleph_table
                        prev_aleph_table = None
                else:
                    # keep track of the first stg_2 total
                    prev_aleph_table = stg_2_table
                    stg_2_aleph_table_totals_expected[stg_2_table] = stg_1_count
                    self.assertEqual(stg_2_aleph_table_totals_expected[stg_2_table], stg_1_count)
                # TODO log test failures
    
    def test_bib_rec_stage_2_pp(self):
        # check to see if pp values are written
        with dwetl.test_database_session() as session:
    
            prcsng_cycle_id = self.__class__.prcsng_cycle_id
    
            # choose a few random IDs and check if the PP values are written 
            for stg_2_table, dimension in self.__class__.stg_2_table_config_mapping.items():
                stg_2_table_base_class = dwetl.Base.classes[stg_2_table]
    
                results = session.query(stg_2_table_base_class).filter(stg_2_table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
    
                # get unique ID from pk of the table 
                pk = stg_2_table_base_class.__table__.primary_key.columns.values()[2].name
    
                for item in results.all():
                    for key in item.__dict__.keys():
                        if key[:2] == 'pp':
                            # check if pp is there for records with in values
                            in_key = 'in_'+'_'.join(key.split('_')[1:])
    
                            # make sure pp value is not none
                            if item.__dict__[in_key]:
                                message = f'Record {pk}: {item.__dict__[pk]} is missing the PP value for {item.__dict__[key]}'
                                self.assertIsNotNone(item.__dict__[key], message)
    
    def test_bib_rec_stage_2_dq(self):
        # check to see if dq values are written
        with dwetl.test_database_session() as session:
    
            prcsng_cycle_id = self.__class__.prcsng_cycle_id
    
            # check if the PP values are written 
            for stg_2_table, dimension in self.__class__.stg_2_table_config_mapping.items():
                stg_2_table_base_class = dwetl.Base.classes[stg_2_table]
    
                results = session.query(stg_2_table_base_class).filter(stg_2_table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
    
                # get unique ID from pk of the table 
                pk = stg_2_table_base_class.__table__.primary_key.columns.values()[2].name
    
                for item in results.all():
                    for key in item.__dict__.keys():
                        
                        if key[:2] == 'dq':
                            # check if pp is there for records with in values
                            in_key = 'in_'+'_'.join(key.split('_')[1:])
                            
                            
                            if in_key == 'in_z00_doc_number':
                                # make sure null records are suspended
                                if item.__dict__[key] == None:
                                    self.assertEqual(item.__dict__[key], 'SUS')
                            # if in_key == 'in_z13_open_date' or in_key == 'in_z13_update_date':
                            #     # if it comes in None, dq should be None
                            # 
                            #     # query error table too? 
                            # 
                            #     # if it comes in a wrong date, dq should be None
                            # 
                            #     # query error table
                            # if in_key == 'in_z13u_user_defined_2':
                            # 
                            # # make sure the pp value equals the dq value for all other fields
                            # if item.__dict__[in_key]:
                            #     pp_key = in_key.replace('in_', 'pp_')
                            #     # message = f'Record {pk}, {item.__dict__[pk]}, is missing the DQ value for {key}'
                            #     self.assertEqual(item.__dict__[in_key], item.__dict__[pp_key])
    

                            
    
                

        
    
    
        
