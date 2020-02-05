import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.transformation_info import TransformationInfo
from dwetl.processor.transformation_processor import TransformationProcessor
import datetime
import logging
import pdb
import pprint

class TestTransformationProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.bib_rec_sample_data = [
            # bad data missing value
            {
                'db_operation_cd': 'U',
                'dq_z00_data': None,
                'dq_z00_data_len': None,
                'dq_z00_doc_number': 'SUS',
                'dq_z00_no_lines': None,
                'dw_stg_2_aleph_lbry_name': 'mai01',
                'em_update_dw_job_name': 'Preprocessing',
                'in_z00_data': '',
                'in_z00_data_len': '001970',
                'in_z00_doc_number': '', # empty doc number
                'in_z00_no_lines': '0049',
                'pp_z00_data': '',
                'pp_z00_data_len': '001970',
                'pp_z00_doc_number': '', # empty doc number
                'pp_z00_no_lines': '0049',
                'rm_dq_check_excptn_cnt': 0,
                'rm_suspend_rec_flag': 'Y',
                'rm_suspend_rec_reason_cd': None,
                't1_z00_data__bib_rec_marc_rec_data_cntnt_txt': None,
                't1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt': None,
                't1_z00_doc_number__bib_rec_source_system_id': None,
                't1_z00_no_lines__bib_rec_marc_rec_field_cnt': None
            },
            {
                'db_operation_cd': 'U',
                'dq_z00_data': None,
                'dq_z00_data_len': None,
                'dq_z00_doc_number': 'SUS',
                'dq_z00_no_lines': None,
                'dw_stg_2_aleph_lbry_name': 'mai01',
                'em_update_dw_job_name': 'Preprocessing',
                'in_z00_data': '',
                'in_z00_data_len': '001970',
                'in_z00_doc_number': '000053', # too short fails length check
                'in_z00_no_lines': '0049',
                'pp_z00_data': '',
                'pp_z00_data_len': '001970',
                'pp_z00_doc_number': '000053', # too short fails length check
                'pp_z00_no_lines': '0049',
                'rm_dq_check_excptn_cnt': 0,
                'rm_suspend_rec_flag': 'Y',
                'rm_suspend_rec_reason_cd': None,
                't1_z00_data__bib_rec_marc_rec_data_cntnt_txt': None,
                't1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt': None,
                't1_z00_doc_number__bib_rec_source_system_id': None,
                't1_z00_no_lines__bib_rec_marc_rec_field_cnt': None
            },
            # good data
            {
                'db_operation_cd': 'U',
                'dq_z00_data': None,
                'dq_z00_data_len': '001970',
                'dq_z00_doc_number': '000053939',
                'dq_z00_no_lines': '0049',
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
                ],
                "transformation_steps": [
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
                }
            }
    def test_get_transformations_for_key(self):
        key = 'dq_z00_doc_number'

        json_config = self.bib_rec_sample_json_config

        result = TransformationProcessor.get_transformations_for_key(key, json_config)
        
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
        
    def test_transform_bib_rec(self):
        # item
        reader = ListReader(self.bib_rec_sample_data)
        
        writer = ListWriter()
        
        job_info = job_info = JobInfo(-1, 'test_user', '1', '1')
        
        #create test logger
        today = datetime.datetime.now().strftime('%Y%m%d')
        logger = logging.getLogger('dwetl')
        file_handler = logging.FileHandler(f'logs/test.dwetl.log.{today}')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        
        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        transformation_processor = TransformationProcessor(reader, writer, job_info, logger, self.bib_rec_sample_json_config, pk_list)
        transformation_processor.execute()
        results = transformation_processor.writer.list
        pdb.set_trace()
        
        # expected_result = 
        
        
        
        
        

