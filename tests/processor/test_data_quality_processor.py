import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.data_quality_info import DataQualityInfo
from dwetl.processor.data_quality_processor import DataQualityProcessor
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
import datetime
import logging
import pdb
import pprint
import json

class TestDataQualityProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bib_record_dimension_sample_data = bib_record_dimension_sample_data.bib_rec_sample_data
        
        cls.logger = test_logger.logger
        
        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_json_config = json.load(json_file)


    def test_get_dq_checks_for_key(self):
        """
        test get_dq_checks_for key using bib rec data
        """
        
        key = 'pp_z00_doc_number'
        json_config = self.bib_rec_json_config

        result = DataQualityProcessor.get_dq_checks_for_key(key, self.bib_rec_json_config)

        expected_result = [{'additional_conditions': '',
                            'aleph_library': 'MAI01,MAI39',
                            'always': 'x',
                            'application': 'H,I',
                            'column_data_type': 'CHAR(9)',
                            'column_sub_component': '',
                            'dimension_link_to_record': 'N/A',
                            'exception_memorialization': 'Create Exception Record',
                            'exception_message': 'Missing Value: Z00_DOC_NUMBER',
                            'format': '',
                            'instructions': '1) <null> 2) All spaces',
                            'only_if_data_exists': '',
                            'order': '1',
                            'replacement_value': 'N/A',
                            'source_column_name': 'Z00_DOC_NUMBER',
                            'source_file': 'Z00',
                            'specific_dq_function': 'no_missing_values',
                            'specific_dq_function_param_1': '',
                            'suspend_record': 'Yes',
                            'target_column_name': '',
                            'type': 'Missing Value'},
                           {'additional_conditions': 'No previous DQ exceptions',
                            'aleph_library': 'MAI01,MAI39',
                            'always': '',
                            'application': 'H,I',
                            'column_data_type': 'CHAR(9)',
                            'column_sub_component': '',
                            'dimension_link_to_record': 'N/A',
                            'exception_memorialization': 'Create Exception Record',
                            'exception_message': 'Invalid Value: Z00_DOC_NUMBER',
                            'format': '',
                            'instructions': 'Must equal 9',
                            'only_if_data_exists': 'x',
                            'order': '2',
                            'replacement_value': 'N/A',
                            'source_column_name': 'Z00_DOC_NUMBER',
                            'source_file': 'Z00',
                            'specific_dq_function': 'is_valid_length',
                            'specific_dq_function_param_1': '9',
                            'suspend_record': 'Yes',
                            'target_column_name': '',
                            'type': 'Length Check'}]

        
        self.assertEqual(expected_result, result)

    def test_get_suspend_record_code(self):
        key = "pp_z00_doc_number"
        
        whole_json_config = self.bib_rec_json_config
        
        json_config = whole_json_config['z00_doc_number']['dataquality_info'][0]

        dq = DataQualityInfo(json_config)

        expected_result = "MIS"
        result = DataQualityProcessor.get_suspend_record_code(key, dq)
        self.assertEqual(expected_result, result)


    def test_dataquality_bib_rec(self):

        json_config = self.bib_rec_json_config
        
        reader = ListReader(self.bib_record_dimension_sample_data)

        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        data_quality_processor = DataQualityProcessor(reader, writer, job_info, self.logger, json_config, pk_list)
        data_quality_processor.execute()
        results = data_quality_processor.writer.list

        expected_keys = sorted([
            'db_operation_cd', 'dq_z00_data', 'dq_z00_data_len', 'dq_z00_doc_number', 'dq_z00_no_lines', 'dw_stg_2_aleph_lbry_name',
            'em_update_dw_job_exectn_id', 'em_update_dw_job_name', 'em_update_dw_job_version_no',
            'em_update_dw_prcsng_cycle_id', 'em_update_tmstmp', 'em_update_user_id',
            'in_z00_doc_number', 'rm_dq_check_excptn_cnt', 'rm_suspend_rec_flag', 'rm_suspend_rec_reason_cd'
            ])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual(expected_keys, sorted(list(results[1].keys())))
        self.assertEqual("SUS", results[0]['dq_z00_doc_number'])
        self.assertEqual(1, results[0]['rm_dq_check_excptn_cnt'])
        self.assertEqual("MIS", results[0]['rm_suspend_rec_reason_cd'])

        self.assertEqual("SUS", results[1]['dq_z00_doc_number'])
        self.assertEqual(1, results[1]['rm_dq_check_excptn_cnt'])
        self.assertEqual("LEN", results[1]['rm_suspend_rec_reason_cd'])

        self.assertEqual('0049', results[0]['dq_z00_no_lines'])
        self.assertEqual('001970', results[0]['dq_z00_data_len'])

        self.assertEqual('000053939', results[2]['dq_z00_doc_number'])
