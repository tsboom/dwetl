import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.data_quality_info import DataQualityInfo
from dwetl.processor.data_quality_processor import DataQualityProcessor
import pdb
import pprint

class TestDataQualityProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.bib_rec_sample_data = [
            {
                'db_operation_cd': 'U',
                'dq_z00_data': None,
                'dq_z00_data_len': None,
                'dq_z00_doc_number': None,
                'dq_z00_no_lines': None,
                'dw_stg_2_aleph_lbry_name': 'mai01',
                'em_update_dw_job_name': 'Preprocessing',
                'in_z00_data': '',
                'in_z00_data_len': '001970',
                'in_z00_doc_number': '000053939',
                'in_z00_no_lines': '0049',
                'pp_z00_data': '',
                'pp_z00_data_len': '001970',
                'pp_z00_doc_number': '000053939',
                'pp_z00_no_lines': '0049',
                'rm_dq_check_excptn_cnt': 0,
                'rm_suspend_rec_flag': 'N',
                'rm_suspend_rec_reason_cd': None,
                't1_z00_data__bib_rec_marc_rec_data_cntnt_txt': None,
                't1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt': None,
                't1_z00_doc_number__bib_rec_source_system_id': None,
                't1_z00_no_lines__bib_rec_marc_rec_field_cnt': None
            }
        ]

        cls.bib_rec_sample_json_config = {
            'z00_doc_number': {
                "source_col_name": "z00_doc_number",
                "dataquality_info": [
                    {
                        "aleph_library": "MAI01,MAI39",
                        "source_file": "Z00",
                        "source_column_name": "Z00_DOC_NUMBER",
                        "target_column_name": "",
                        "column_sub_component": "",
                        "column_data_type": "CHAR(9)",
                        "format": "",
                        "type": "Missing Value",
                        "instructions": "1) <null> 2) All spaces",
                        "specific_dq_function": "no_missing_values",
                        "specific_dq_function_param_1": "",
                        "application": "H,I",
                        "order": "1",
                        "always": "x",
                        "only_if_data_exists": "",
                        "additional_conditions": "",
                        "suspend_record": "Yes",
                        "exception_memorialization": "Create Exception Record",
                        "exception_message": "Missing Value: Z00_DOC_NUMBER",
                        "replacement_value": "N/A",
                        "dimension_link_to_record": "N/A"
                    },
                    {
                        "aleph_library": "MAI01,MAI39",
                        "source_file": "Z00",
                        "source_column_name": "Z00_DOC_NUMBER",
                        "target_column_name": "",
                        "column_sub_component": "",
                        "column_data_type": "CHAR(9)",
                        "format": "",
                        "type": "Length Check",
                        "instructions": "Must equal 9",
                        "specific_dq_function": "is_valid_length",
                        "specific_dq_function_param_1": "9",
                        "application": "H,I",
                        "order": "2",
                        "always": "",
                        "only_if_data_exists": "x",
                        "additional_conditions": "No previous DQ exceptions",
                        "suspend_record": "Yes",
                        "exception_memorialization": "Create Exception Record",
                        "exception_message": "Invalid Value: Z00_DOC_NUMBER",
                        "replacement_value": "N/A",
                        "dimension_link_to_record": "N/A"
                    }
                ]
            },
            'in_z00_data_len':
                {
                    "source_col_name": "z00_data_len",
                    "dataquality_info": {}
                },
            'in_z00_data':
                {
                    "source_col_name": "z00_data",
                    "dataquality_info": {}
                },
            'in_z00_no_lines':
                {
                    "source_col_name": "z00_no_lines",
                    "dataquality_info": {}
                }
            }

    def test_get_dq_checks_for_key(self):
        key = 'pp_z00_doc_number'

        json_config = self.bib_rec_sample_json_config

        result = DataQualityProcessor.get_dq_checks_for_key(key, json_config)

        expected_result = [
            {'additional_conditions': '',
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
              'type': 'Length Check'}
          ]

        self.assertEqual(expected_result, result)

    def test_get_suspend_record_code(self):
        key = "pp_z00_doc_number"
        
        json_config = {
            'specific_dq_function': 'no_missing_values',
            'specific_dq_function_param_1': '',
            'suspend_record': 'Yes',
            'type': 'Missing Value',
            'exception_message': 'Missing Value',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)

        expected_result = "MIS"
        result = DataQualityProcessor.get_suspend_record_code(key, dq)
        self.assertEqual(expected_result, result)

        
        

    def test_dataquality_bib_rec(self):

        reader = ListReader(self.bib_rec_sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        logger = None

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        step = DataQualityProcessor(reader, writer, job_info, logger, self.bib_rec_sample_json_config, pk_list)
        step.execute()
        results = step.writer.list

        expected_keys = sorted([
            'in_z00_doc_number', 'dw_stg_2_aleph_lbry_name', 'db_operation_cd',
            'dq_z00_no_lines', 'dq_z00_data_len', 'dq_z00_doc_number', 'dq_z00_data',
            'em_update_dw_prcsng_cycle_id', 'em_update_dw_job_exectn_id',
            'em_update_dw_job_name', 'em_update_dw_job_version_no',
            'em_update_user_id', 'em_update_tmstmp'
            ])


        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual("000053939", results[0]['dq_z00_doc_number'])
        self.assertEqual('0049', results[0]['dq_z00_no_lines'])
        self.assertEqual('001970', results[0]['dq_z00_data_len'])
