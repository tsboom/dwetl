import unittest
import datetime
import dwetl.database_credentials as database_credentials
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
from dwetl.job_info import JobInfo
from dwetl.job_info import JobInfoFactory
import dwetl
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from dwetl.job_info import JobInfo
import load_stage_1
import load_stage_2
from dwetl.processor.load_aleph_tsv import LoadAlephTsv

class TestLoadStage2(unittest.TestCase):
    # this test is commented out because it takes a really long time. I think test_bib_rec_etl.py 
    # and other per dimension end-to-end tests are more useful. This one was helpful during development.
    maxDiff= None
    @classmethod
    def setUpClass(cls):
        cls.logger = test_logger.logger

        cls.test_input_directory = 'tests/data/incoming_test/aleph/20210123'
        cls.db_session_creator = dwetl.test_database_session

        # create job info from test database session
        with cls.db_session_creator() as session:
            job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
            # cls.job_info = JobInfoFactory.create_job_info_from_reporting_db(session, job_info_table_class, reporting_max_prcsng_id, cls.logger)
            cls.job_info = JobInfoFactory.create_job_info_from_db(session, job_info_table_class)

        cls.prcsng_cycle_id = cls.job_info.prcsng_cycle_id

        cls.stg_1_table_mapping = {'ALEPH_TSV_TABLE_MAPPING': 
            {
            # "mai01_z00_data": "dw_stg_1_mai01_z00",
            # "mai39_z00_data": "dw_stg_1_mai39_z00",
            # "mai01_z13_data": "dw_stg_1_mai01_z13",
            # "mai39_z13_data": "dw_stg_1_mai39_z13",
            # "mai01_z13u_data": "dw_stg_1_mai01_z13u",
            # "mai39_z13u_data": "dw_stg_1_mai39_z13u",
            "mai60_z00_full_data": "dw_stg_1_mai60_z00",
            "mai60_z13_data": "dw_stg_1_mai60_z13",
            "mai60_z13u_data": "dw_stg_1_mai60_z13u",
            "mai60_z103_bib_data": "dw_stg_1_mai60_z103_bib",
            "mai50_z30_data": "dw_stg_1_mai50_z30",
            "mai50_z35_data": "dw_stg_1_mai50_z35",
            "mai50_z103_bib_data": "dw_stg_1_mai50_z103_bib_full"
            },

            # 'MPF_TABLE_MAPPING' : {
            #     "mpf_member-library-dimension.txt": "dw_stg_1_mpf_mbr_lbry",
            #     "mpf_library-entity-dimension.txt": "dw_stg_1_mpf_lbry_entity",
            #     "mpf_library-collection-dimension.txt": "dw_stg_1_mpf_collection",
            #     "mpf_item-status-dimension.txt": "dw_stg_1_mpf_item_status",
            #     "mpf_item-process-status-dimension.txt": "dw_stg_1_mpf_item_prcs_status",
            #     "mpf_material-form-dimension.txt": "dw_stg_1_mpf_matrl_form"
            # }
            }

        cls.stg_1_to_stg_2_table_mapping = {
        # "dw_stg_1_mai01_z00": "dw_stg_2_bib_rec_z00",
        # "dw_stg_1_mai39_z00": "dw_stg_2_bib_rec_z00",
        # "dw_stg_1_mai39_z13": "dw_stg_2_bib_rec_z13",
        # 'dw_stg_1_mai01_z13': "dw_stg_2_bib_rec_z13",
        # "dw_stg_1_mai01_z13u": "dw_stg_2_bib_rec_z13u",
        # "dw_stg_1_mai39_z13u": "dw_stg_2_bib_rec_z13u",
        "dw_stg_1_mai60_z00": "dw_stg_2_lbry_holding_z00",
        "dw_stg_1_mai60_z13": "dw_stg_2_lbry_holding_z13",
        "dw_stg_1_mai60_z13u": "dw_stg_2_lbry_holding_z13u",
        "dw_stg_1_mai50_z30": "dw_stg_2_lbry_item_z30",
        "dw_stg_1_mai50_z35": "dw_stg_2_lbry_item_event_z35",
        "dw_stg_1_mai50_z30_full": "dw_stg_2_lbry_item_fact_z30_full",
        "dw_stg_1_mai50_z103_bib_full": "dw_stg_2_lbry_item_fact_z103_bib_full",
        # "dw_stg_1_mpf_mbr_lbry": "dw_stg_2_mpf_mbr_lbry",
        # "dw_stg_1_mpf_lbry_entity": "dw_stg_2_mpf_lbry_entity",
        # "dw_stg_1_mpf_collection": "dw_stg_2_mpf_collection",
        # "dw_stg_1_mpf_item_status": "dw_stg_2_mpf_item_status",
        # "dw_stg_1_mpf_item_prcs_status": "dw_stg_2_mpf_item_prcs_status",
        # "dw_stg_1_mpf_matrl_form": "dw_stg_2_mpf_matrl_form"
        }

        cls.logger.info(f'TEST DWETL.py started')

        '''
        load_stage_1
        '''
        load_stage_1.load_stage_1(cls.job_info, cls.test_input_directory, cls.logger, cls.stg_1_table_mapping, cls.db_session_creator)

        # load stage 2
        load_stage_2.load_stage_2(cls.job_info, cls.logger, cls.stg_1_to_stg_2_table_mapping, cls.db_session_creator)

    @classmethod
    def tearDownClass(cls):
        # when tests are over, delete all the data from these tests
        with dwetl.test_database_session() as session:
            prcsng_cycle_id = cls.prcsng_cycle_id
    
            # iterate over stage 1 tables and delete records with the current processing cycle id
            for file, table in cls.stg_1_table_mapping['ALEPH_TSV_TABLE_MAPPING'].items():
                table_base_class = dwetl.Base.classes[table]
                stg_1_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
                stg_1_results.delete()
    
            # iterate over stage 2 tables and delete all records added in this test file
            for stg_1_table, stg_2_table in cls.cls.stg_1_to_stg_2_table_mapping.items():
                table_base_class = dwetl.Base.classes[stg_2_table]
                stg_2_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
                stg_2_results.delete()
    
            # delete errors from error table
            table_base_class = dwetl.Base.classes['dw_db_errors']
            error_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
            error_results.delete()
    
            # commit all changes
            session.commit()


        
    def test_load_stage_2(self):
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
            for stg_1_table, stg_2_table in self.__class__.stg_1_to_stg_2_table_mapping.items():
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
    

