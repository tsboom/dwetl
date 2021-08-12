import unittest
import dwetl
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
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
    maxDiff = None
    @classmethod
    def setUpClass(cls):
        cls.bib_record_dimension_sample_data_z00 = bib_record_dimension_sample_data.bib_rec_sample_data_z00
        cls.bib_record_dimension_sample_data_z13 = bib_record_dimension_sample_data.bib_rec_sample_data_z13
        cls.bib_record_dimension_sample_data_z13u = bib_record_dimension_sample_data.bib_rec_sample_data_z13u

        cls.logger = test_logger.logger
        
        with dwetl.test_database_session() as session:
            cls.error_writer= SqlAlchemyWriter(session, dwetl.Base.classes.dw_db_errors)

        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_json_config = json.load(json_file)


    def test_get_dq_checks_for_key(self):
        """
        test get_dq_checks_for key using bib rec data z13_open_date, z13u_user_defined_2, z00_doc_number
        """
        
        json_config = self.bib_rec_json_config
        
        # test z13_open_date
        key = 'z13_open_date'
        
        result = DataQualityProcessor.get_dq_checks_for_key(key, self.bib_rec_json_config)
        
        expected_result = [{'additional_conditions': '',
              'aleph_library': 'MAI01, MAI39',
              'always': 'X',
              'application': 'H,I',
              'column_data_type': 'NUMBER(8)',
              'column_sub_component': '',
              'dimension_link_to_record': 'N/A',
              'exception_memorialization': 'Create Exception Record',
              'exception_message': 'Missing Value: Z13_OPEN_DATE',
              'format': 'YYYYMMDD',
              'instructions': '1) <null> 2) All zeros',
              'only_if_data_exists': '',
              'order': '1',
              'replacement_value': '(null)',
              'source_column_name': 'Z13_OPEN_DATE',
              'source_file': 'Z13',
              'specific_dq_function': 'no_missing_values',
              'specific_dq_function_param_1': '',
              'suspend_record': 'No',
              'target_column_name': '',
              'type': 'Missing Value'},
             {'additional_conditions': 'No previous Z13_OPEN_DATE DQ exception',
              'aleph_library': 'MAI01, MAI39',
              'always': '',
              'application': 'H,I',
              'column_data_type': 'NUMBER(8)',
              'column_sub_component': '',
              'dimension_link_to_record': 'N/A',
              'exception_memorialization': 'Create Exception Record',
              'exception_message': 'Invalid Date: Z13_OPEN_DATE',
              'format': 'YYYYMMDD',
              'instructions': 'Must be valid aleph date.',
              'only_if_data_exists': 'X',
              'order': '2',
              'replacement_value': '(null)',
              'source_column_name': 'Z13_OPEN_DATE',
              'source_file': 'Z13',
              'specific_dq_function': 'is_valid_aleph_year',
              'specific_dq_function_param_1': '',
              'suspend_record': 'No',
              'target_column_name': '',
              'type': 'Date check'}]
        
        self.assertEqual(expected_result, result)
        
        # test z13_open_date
        key='z00_doc_number'
        
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
        
        # test pp_z13u_user_defined_2
        key='z13u_user_defined_2'
        
        result = DataQualityProcessor.get_dq_checks_for_key(key, self.bib_rec_json_config)
        
        expected_result = [{'additional_conditions': '',
              'aleph_library': 'MAI01, MAI39',
              'always': 'x',
              'application': 'H,I',
              'column_data_type': 'VARCHAR2(500)',
              'column_sub_component': '',
              'dimension_link_to_record': 'N/A',
              'exception_memorialization': 'Create Exception Record',
              'exception_message': 'Invalid value: Z13_USER_DEFINED_2',
              'format': '',
              'instructions': '"ocm" followed by 8 digits or\n'
                              '"ocn" followed by 9 digits or \n'
                              '"on" followed by 10 digits or\n'
                              'empty field',
              'only_if_data_exists': '',
              'order': '1',
              'replacement_value': '-I',
              'source_column_name': 'Z13U_USER_DEFINED_2',
              'source_file': 'Z13U',
              'specific_dq_function': 'dq_z13u_user_defined_2',
              'specific_dq_function_param_1': '',
              'suspend_record': 'No',
              'target_column_name': '',
              'type': 'Format Check'}]
        

    def test_get_suspend_record_code(self):
        # z00 tests for MIS
        key = "pp_z00_doc_number"
        mis_json_config = self.bib_rec_json_config['z00_doc_number']['dataquality_info'][0]
        dq = DataQualityInfo(mis_json_config)
        result = DataQualityProcessor.get_suspend_record_code(key, dq)
        self.assertEqual("MIS", result)
        
        # z00 test for LEN
        len_json_config = self.bib_rec_json_config['z00_doc_number']['dataquality_info'][1]
        dq = DataQualityInfo(len_json_config)
        result = DataQualityProcessor.get_suspend_record_code(key, dq)
        self.assertEqual("LEN", result)
        
        # z13 tests 
        key='pp_z13_open_date'
        json_config = self.bib_rec_json_config['z13_open_date']['dataquality_info'][0]
        dq = DataQualityInfo(json_config)
        result = DataQualityProcessor.get_suspend_record_code(key, dq)
        self.assertEqual("MIS", result)


    def test_dataquality_bib_rec(self):
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        
        # z00
        json_config = self.bib_rec_json_config
        reader = ListReader(self.bib_record_dimension_sample_data_z00)

        z00_pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']
        
        data_quality_processor = DataQualityProcessor(reader, writer, job_info, self.logger, json_config, z00_pk_list, self.error_writer)
        data_quality_processor.execute()
        z00_results = data_quality_processor.writer.list
        
        z00_expected_keys = sorted([
            'db_operation_cd', 'dq_z00_data', 'dq_z00_data_len', 'dq_z00_doc_number', 
            'dq_z00_no_lines', 'dw_stg_2_aleph_lbry_name', 'em_create_dw_prcsng_cycle_id', 
            'em_update_dw_job_exectn_id', 'em_update_dw_job_name', 
            'em_update_dw_job_version_no', 'em_update_dw_prcsng_cycle_id', 
            'em_update_tmstmp', 'em_update_user_id', 'in_z00_doc_number', 
            'rm_dq_check_excptn_cnt', 'rm_suspend_rec_flag', 'rm_suspend_rec_reason_cd'
            ])

        self.assertEqual(z00_expected_keys, sorted(list(z00_results[1].keys())))
        self.assertEqual('000053939', z00_results[2]['dq_z00_doc_number'])
        
        # test z00_doc_number missing values
        self.assertEqual("SUS", z00_results[0]['dq_z00_doc_number'])
        self.assertEqual(1, z00_results[0]['rm_dq_check_excptn_cnt'])
        self.assertEqual("MIS", z00_results[0]['rm_suspend_rec_reason_cd'])
        
        # test z00_doc_number length 
        self.assertEqual("SUS", z00_results[1]['dq_z00_doc_number'])
        self.assertEqual(1, z00_results[1]['rm_dq_check_excptn_cnt'])
        self.assertEqual("LEN", z00_results[1]['rm_suspend_rec_reason_cd'])
        
        
        
        
        # z13
        reader = ListReader(self.bib_record_dimension_sample_data_z13)
        z13_pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z13_rec_key', 'em_create_dw_prcsng_cycle_id']
        data_quality_processor = DataQualityProcessor(reader, writer, job_info, self.logger, json_config, z13_pk_list, self.error_writer)
        data_quality_processor.execute()
        z13_results = data_quality_processor.writer.list
        
        
        
        # z13u
        reader = ListReader(self.bib_record_dimension_sample_data_z13u)
        z13u_pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z13u_rec_key', 'em_create_dw_prcsng_cycle_id']

        data_quality_processor = DataQualityProcessor(reader, writer, job_info, self.logger, json_config, z13u_pk_list, self.error_writer)
        data_quality_processor.execute()
        z13u_results = data_quality_processor.writer.list



        z13_expected_keys = sorted([
            'db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z13_rec_key', 'dq_z13_year', 'dq_z13_open_date', 'dq_z13_update_date',
            'dq_z13_author', 'dq_z13_title', 'em_update_dw_prcsng_cycle_id', 'em_update_user_id', 'em_update_dw_job_exectn_id',
            'em_update_dw_job_version_no', 'em_update_dw_job_name', 'em_update_tmstmp','rm_dq_check_excptn_cnt', 'rm_suspend_rec_flag', 'rm_suspend_rec_reason_cd'])

        
        self.assertEqual(z13_expected_keys, sorted(list(z13_results[0].keys())))
        self.assertEqual(z13_expected_keys, sorted(list(z13_results[1].keys())))

        

        self.assertEqual(None, z13_results[0]['dq_z13_open_date'])
        self.assertEqual(1, z13_results[0]['rm_dq_check_excptn_cnt'])
        self.assertEqual("MIS", z13_results[0]['rm_suspend_rec_reason_cd'])

        self.assertEqual(None, z13_results[1]['dq_z13_open_date'])
        self.assertEqual(1, results[1]['rm_dq_check_excptn_cnt'])
        self.assertEqual("LEN", results[1]['rm_suspend_rec_reason_cd'])


        self.assertEqual('0049', results[0]['dq_z00_no_lines'])
        self.assertEqual('001970', results[0]['dq_z00_data_len'])
        self.assertEqual('20130222', results[1]['dq_z13_update_date'])
        self.assertEqual('1969', results[2]['dq_z13_year'])

        self.assertEqual('20021124', results[2]['pp_z13_open_date'])
    
    
