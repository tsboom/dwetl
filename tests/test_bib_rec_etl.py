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
from sqlalchemy import func
import pprint



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

        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_json_config = json.load(json_file)

        # run ETL using sample data and write to the test postgres database (usmai_dw_etl_test)
        # currently testing end to end
        test_input_directory = 'tests/data/incoming_test/aleph/20210123'

        cls.db_session_creator = dwetl.test_database_session

        # find max processing cycle id of the reporting fact table for bib rec
        # Determine processing cycle ID by using the reporting db as the authority
        with dwetl.reporting_database_session() as session2:
            reporting_dim_table = dwetl.ReportingBase.classes['dim_bib_rec']
            # query max processing id in ezproxy fact table in the reporting db
            reporting_max_prcsng_id = session2.query(func.max(reporting_dim_table.em_create_dw_prcsng_cycle_id)).scalar()
            # increment the processing cycle id by 1 if it starts as None
            if reporting_max_prcsng_id == None:
                reporting_max_prcsng_id = 1

        # create job info from test database session
        with cls.db_session_creator() as session:
            job_info_table_class = dwetl.Base.classes['dw_prcsng_cycle']
            # cls.job_info = JobInfoFactory.create_job_info_from_reporting_db(session, job_info_table_class, reporting_max_prcsng_id, cls.logger)
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

        load_stage_2.load_stage_2(cls.job_info, cls.logger, cls.stage1_to_stage2_table_mapping, cls.db_session_creator)

        '''
        stg 2 intertable processing (PP, DQ, T)
        '''
        cls.stg_2_table_config_mapping = {
            'dw_stg_2_bib_rec_z00': 'bibliographic_record_dimension',
            'dw_stg_2_bib_rec_z13': 'bibliographic_record_dimension',
            'dw_stg_2_bib_rec_z13u': 'bibliographic_record_dimension',
            'dw_stg_2_bib_rec_z00_field': 'bibliographic_record_dimension'
        }
        stage_2_intertable_processing.stage_2_intertable_processing(cls.job_info, cls.logger, cls.stg_2_table_config_mapping, cls.db_session_creator)

    @classmethod
    def tearDownClass(cls):
        # when tests are over, delete all the data from these bib rec tests
        with dwetl.test_database_session() as session:
            prcsng_cycle_id = cls.prcsng_cycle_id

            # iterate over stage 1 tables and delete records with the current processing cycle id
            for file, table in cls.stg_1_table_mapping['ALEPH_TSV_TABLE_MAPPING'].items():
                table_base_class = dwetl.Base.classes[table]
                stg_1_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
                stg_1_results.delete()

            # iterate over stage 2 tables and delete all records added in this test file
            for stg_2_table, dimension in cls.stg_2_table_config_mapping.items():
                table_base_class = dwetl.Base.classes[stg_2_table]
                stg_2_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
                stg_2_results.delete()

            # delete errors from error table
            table_base_class = dwetl.Base.classes['dw_db_errors']
            error_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)
            error_results.delete()

            # commit all changes
            session.commit()
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

            # check if the DQ values are written
            for stg_2_table, dimension in self.__class__.stg_2_table_config_mapping.items():
                stg_2_table_base_class = dwetl.Base.classes[stg_2_table]
                error_table_base_class = dwetl.Base.classes['dw_db_errors']

                results = session.query(stg_2_table_base_class).filter(stg_2_table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)

                # get unique ID from pk of the table
                pk = stg_2_table_base_class.__table__.primary_key.columns.values()[2].name


                for item in results.all():

                    for key in item.__dict__.keys():
                        # create message for later to print when tests fail
                        message = f'Record ({pk}: {item.__dict__[pk]}) in {stg_2_table} fails the {key} DQ test.'

                        #import pdb; pdb.set_trace()
                        if key[:2] == 'dq':
                            # check dq values and special cases
                            in_key = 'in_'+'_'.join(key.split('_')[1:])
                            pp_key = in_key.replace('in_', 'pp_')
                            dq_value = item.__dict__[key]
                            pp_value = item.__dict__[pp_key]
                            if in_key == 'in_z00_doc_number':
                                # make sure missing  are suspended
                                if dq_value == None or dq_value.isspace():
                                    self.assertEqual(dq_value, 'SUS', message)
                                    #pdb.set_trace()
                                continue
                            if in_key == 'in_z13_open_date' or in_key == 'in_z13_update_date':
                                # if date comes in None, dq should be None
                                dq_check_result = dwetl.data_quality_utilities.no_missing_values(pp_value)
                                #pdb.set_trace()
                                if dq_check_result == False:
                                    self.assertEqual(dq_value, None, message)
                                    continue
                                # if it comes in a wrong date, dq should be None
                                dq_check_result = dwetl.data_quality_utilities.is_valid_aleph_date(pp_value)

                                if dq_check_result == False:
                                    self.assertEqual(dq_value, None, message)
                                continue
                            if in_key == 'in_z13u_user_defined_2':
                                # if it comes in None, dq should be '-M'
                                if pp_value == None:
                                    self.assertEqual(dq_value, '-M', message)
                                    break
                                # if the value is invalid, dq should be '-I'
                                dq_check_result = dwetl.data_quality_utilities.dq_z13u_user_defined_2(pp_value)
                                if dq_check_result is False:
                                    self.assertEqual(dq_value, '-I', message)
                                continue

                            if in_key =='in_z00_no_lines' or in_key =='in_z00_data_len':
                                if pp_value:
                                    # ignore leading zeros
                                    pp_val_int = int(pp_value.lstrip('0'))
                                    # remove leading zeros and compare with dq value
                                    self.assertEqual(pp_val_int, dq_value)
                                continue

                            # for all other values make sure the pp value equals the dq value
                            self.assertEqual(pp_value, dq_value, message)

    def test_bib_rec_stage_2_t(self):
        # check to see if T values are written
        with dwetl.test_database_session() as session:

            prcsng_cycle_id = self.__class__.prcsng_cycle_id

            # check if the DQ values are written
            for stg_2_table, dimension in self.__class__.stg_2_table_config_mapping.items():
                stg_2_table_base_class = dwetl.Base.classes[stg_2_table]
                error_table_base_class = dwetl.Base.classes['dw_db_errors']

                results = session.query(stg_2_table_base_class).filter(stg_2_table_base_class.em_create_dw_prcsng_cycle_id==prcsng_cycle_id)

                # get unique ID from pk of the table
                pk = stg_2_table_base_class.__table__.primary_key.columns.values()[2].name

                for item in results.all():
                    for key in item.__dict__.keys():

                        # test only the transform keys against their dq value from stage 2
                        if key[:1] == 't':
                            orig_key = key.split('__')[0][3:]
                            dq_key = 'dq_'+ orig_key
                            dq_value = item.__dict__[dq_key]

                            # create message for later to print when tests fail
                            message = f'Record ({pk}: {item.__dict__[pk]}) in {stg_2_table} fails the {key} transformation test.'

                            t_value = item.__dict__[key]


                            # check z00 transforms (none use specific functions


                            # check special transform cases for bib rec
                            # save isbn_issn_code dq value for the transformation aftewards (isbn_txt, and associated issns)
                            if key == 't1_z13_isbn_issn_code__bib_rec_isbn_txt':
                                code = item.__dict__['dq_z13_isbn_issn_code']
                                dq_value = item.__dict__['dq_z13_isbn_issn']
                                # the t_value in the db should match the transformed field result
                                t_check_result = dwetl.specific_transform_functions.isbn_code_020(code, dq_value)
                                self.assertEqual(t_check_result, t_value, message)

                            if key == 't2_z13_isbn_issn_code__bib_rec_all_associated_issns_txt':
                                code = item.__dict__['dq_z13_isbn_issn_code']
                                dq_value = item.__dict__['dq_z13_isbn_issn']
                                t_check_result = dwetl.specific_transform_functions.isbn_code_022(code, dq_value)
                                self.assertEqual(t_check_result, t_value, message)

                            if key == 't1_z13u_user_defined_2__bib_rec_oclc_no':
                                t_check_result = dwetl.specific_transform_functions.remove_ocm_ocn_on(dq_value)
                                self.assertEqual(t_check_result, t_value, message)

                            if key == 't1_z13u_user_defined_3__bib_rec_marc_rec_leader_field_txt':
                                # first transformation moves user_defined_3 as-is
                                self.assertEqual(dq_value, t_value, message)
                            if key == 't2_z13u_user_defined_3__bib_rec_type_cd':
                                t_check_result = dwetl.specific_transform_functions.substring(dq_value, 6, 7)
                                self.assertEqual(t_check_result, t_value, message)

                            if key == 't3_z13u_user_defined_3__bib_rec_bib_type_desc':
                                t_check_result = dwetl.specific_transform_functions.lookup_record_type(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't4_z13u_user_defined_3__bib_rec_bib_lvl_cd':
                                # uses substring method with params
                                t_check_result = dwetl.specific_transform_functions.substring(dq_value, 7, 8)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't5_z13u_user_defined_3__bib_rec_bib_lvl_desc':
                                # uses substring method with params
                                t_check_result = dwetl.specific_transform_functions.lookup_bibliographic_level(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't6_z13u_user_defined_3__bib_rec_encoding_lvl_cd':
                                # uses substring method with params
                                t_check_result = dwetl.specific_transform_functions.substring(dq_value, 17, 18)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't7_z13u_user_defined_3__bib_rec_encoding_lvl_desc':
                                # uses substring method with params
                                t_check_result = dwetl.specific_transform_functions.lookup_encoding_level(dq_value)
                                self.assertEqual(t_check_result, t_value, message)



                            # #
                            if key == 't1_z13u_user_defined_4__bib_rec_marc_rec_008_field_txt':
                                t_check_result = dwetl.specific_transform_functions.remove_ocm_ocn_on(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't2_z13u_user_defined_4__bib_rec_language_cd':
                                # uses substring
                                t_check_result = dwetl.specific_transform_functions.remove_ocm_ocn_on(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't1_z13u_user_defined_5__bib_rec_issn':
                                t_check_result = dwetl.specific_transform_functions.remove_ocm_ocn_on(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            # # z13u_user_defined_6
                            if key == 't1_z13u_user_defined_6__bib_rec_display_suppressed_flag':
                                t_check_result = dwetl.specific_transform_functions.is_suppressed(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't2_z13u_user_defined_6__bib_rec_acquisition_created_flag':
                                t_check_result = dwetl.specific_transform_functions.is_acq_created(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't3_z13u_user_defined_6__bib_rec_circulation_created_flag':
                                t_check_result = dwetl.specific_transform_functions.is_circ_created(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            if key == 't4_z13u_user_defined_6__bib_rec_provisional_status_flag':
                                t_check_result = dwetl.specific_transform_functions.is_provisional(dq_value)
                                self.assertEqual(t_check_result, t_value, message)
                            #
                            #
                            #
                            # if orig_key== 'z13u_user_defined_3':
                            #     t_check_result = dwetl.specific_transform_functions.lookup_record_type(dq_value)
                            #     self.assertEqual(t_check_result, t_value, message)
                            #



                            else:
                                # all other items are moved as-is during transformations (like all z00s)
                                print(dq_key)
                                self.assertEqual(dq_value, t_value)
