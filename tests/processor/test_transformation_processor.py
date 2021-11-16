import unittest
import dwetl
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.job_info import JobInfo
from dwetl.transformation_info import TransformationInfo
from dwetl.processor.transformation_processor import TransformationProcessor
from dwetl.processor.data_quality_processor import DataQualityProcessor
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import datetime
import json
import logging
import pdb
import pprint


class TestTransformationProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.bib_record_dimension_sample_data_z00 = bib_record_dimension_sample_data.bib_rec_sample_data_z00

        cls.bib_record_dimension_sample_data_z13u = bib_record_dimension_sample_data.bib_rec_sample_data_z13u

        cls.logger = test_logger.logger
        with dwetl.test_database_session() as session:
            cls.error_writer= SqlAlchemyWriter(session, dwetl.Base.classes.dw_db_errors)

        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_sample_json_config = json.load(json_file)

        with dwetl.test_database_session() as session:
            cls.error_writer= SqlAlchemyWriter(session, dwetl.Base.classes.dw_db_errors)


    def test_get_transformations_for_key(self):
        key = 'dq_z00_doc_number'

        json_config = self.bib_rec_sample_json_config

        result = TransformationProcessor.get_transformations_for_key(
            key, json_config)

        expected_result = [
            {
                "target_col_name": "bib_rec_source_system_id",
                "target_data_type": "Character(9)",
                "target_attribute": "- Bibliographic Record Identifier",
                "transformation_info": {
                    "chg_proc_type": "0",
                    "transform_action": "Move",
                    "action_specific": "As-Is",
                    "specific_transform_function": "",
                    "specific_transform_function_param1": "",
                    "specific_transform_function_param2": "",
                    "source_col_name": "z00_doc_number",
                    "source_data_type": "CHAR(9)",
                    "source_format": "",
                    "source_mandatory": None,
                    "aleph_table": "Z00",
                    "action_detailed_instructions": ""
                }
            }
        ]
        self.assertEqual(expected_result, result)


    def test_transform_bib_rec_z00(self):

        # dq check the sample data first before transforming
        reader = ListReader(self.bib_record_dimension_sample_data_z00)
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']
        data_quality_processor = DataQualityProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)
        data_quality_processor.execute()
        bib_rec_dq_results = data_quality_processor.writer.list

        # quick check that dq results are workign as expected for 'SUS'
        self.assertEqual('SUS', bib_rec_dq_results[0]['dq_z00_doc_number'])

        # item
        reader = ListReader(bib_rec_dq_results)
        writer = ListWriter()

        job_info = job_info = JobInfo(-1, 'test_user', '1', '1')

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        transformation_processor = TransformationProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)


        transformation_processor.execute()
        results = transformation_processor.writer.list

        expected_keys = sorted([
            'db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'em_update_dw_job_exectn_id', 'em_update_dw_job_name',
            'em_update_dw_job_version_no', 'em_update_dw_prcsng_cycle_id', 'em_update_tmstmp', 'em_update_user_id',
            'in_z00_doc_number'
        ])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual(expected_keys, sorted(list(results[1].keys())))

        self.assertEqual('TransformationProcessor', results[0]['em_update_dw_job_name'])

        # the third item in results has successful transforms
        self.assertEqual('', results[2]['t1_z00_data__bib_rec_marc_rec_data_cntnt_txt'])
        self.assertEqual('001970',results[2]['t1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt'] )
        self.assertEqual('000053939', results[2]['t1_z00_doc_number__bib_rec_source_system_id'])

        # # fourth index sample data item tests z13_open_date date format
        # self.assertEqual(None, results[3]['t1_z13_open_date__bib_rec_create_dt'])
        # self.assertEqual(None, results[4]['t1_z13_open_date__bib_rec_create_dt'])


    def test_transform_bib_rec_z13u(self):

        # dq check the sample data first before transforming
        reader = ListReader(self.bib_record_dimension_sample_data_z13u)
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z13u_rec_key', 'em_create_dw_prcsng_cycle_id']
        data_quality_processor = DataQualityProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)
        data_quality_processor.execute()
        bib_rec_dq_results = data_quality_processor.writer.list


        # do the transformation process using the bib_rec_dq_results
        reader = ListReader(bib_rec_dq_results)
        writer = ListWriter()

        job_info = job_info = JobInfo(-1, 'test_user', '1', '1')

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        transformation_processor = TransformationProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)


        transformation_processor.execute()
        results = transformation_processor.writer.list
<<<<<<< HEAD

        pdb.set_trace()
=======
>>>>>>> 3ad60b502cb9b0e43882f72c0ecba9821ca91181

        expected_keys = sorted([
            'db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'em_update_dw_job_exectn_id', 'em_update_dw_job_name',
            'em_update_dw_job_version_no', 'em_update_dw_prcsng_cycle_id', 'em_update_tmstmp', 'em_update_user_id',
            'in_z00_doc_number'
        ])
        #
        # self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        # self.assertEqual(expected_keys, sorted(list(results[1].keys())))
        #
        # self.assertEqual('TransformationProcessor', results[0]['em_update_dw_job_name'])
        #
        # # the third item in results has successful transforms
        # self.assertEqual('', results[2]['t1_z00_data__bib_rec_marc_rec_data_cntnt_txt'])
        # self.assertEqual('001970',results[2]['t1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt'] )
        # self.assertEqual('000053939', results[2]['t1_z00_doc_number__bib_rec_source_system_id'])

        # # fourth index sample data item tests z13_open_date date format
        # self.assertEqual(None, results[3]['t1_z13_open_date__bib_rec_create_dt'])
        # self.assertEqual(None, results[4]['t1_z13_open_date__bib_rec_create_dt'])
