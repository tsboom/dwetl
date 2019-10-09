import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.preprocess import Preprocess
import pdb

class TestPreprocess(unittest.TestCase):
    def test_preprocess(self):
        """
        tests the case where there's no whitespace
        """
        sample_data = [
            {   # pk data
                'db_operation_cd': 'U',
                'dw_stg_2_aleph_lbry_name': 'mai60',
                'em_create_dw_prcsng_cycle_id': '-1',
                # z00 don't have trims
                'in_z00_doc_number': '000019087',
                'in_z00_no_lines': '0011',
                'in_z00_data_len': '000400',
                # z13 has trims
                'in_z13_title': 'A literary history of America',
                'in_z13_author': 'Wendell, Barrett, 1855-1921',
                'in_z13_imprint': 'New York, Haskell House Publishers, 1968'
            }
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        logger = None

        sample_json_config = {
            'z00_doc_number': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z00_no_lines': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'in_z00_data_len': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z13_title': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            },
            'z13_author': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            },
            'z13_imprint': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            }
        }


        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        step = Preprocess(reader, writer, job_info, logger, sample_json_config, pk_list)
        step.execute()
        results = step.writer.list

        expected_keys = sorted([
                'in_z00_doc_number', 'pp_z00_doc_number', 'dw_stg_2_aleph_lbry_name', 'db_operation_cd',
                'pp_z00_no_lines', 'pp_z13_title', 'pp_z13_author',
                'pp_z00_data_len', 'pp_z13_imprint',
                'em_update_dw_prcsng_cycle_id', 'em_update_dw_job_exectn_id',
                'em_update_dw_job_name', 'em_update_dw_job_version_no',
                'em_update_user_id', 'em_update_tmstmp', 'em_create_dw_prcsng_cycle_id'
                ])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual("000019087", results[0]['pp_z00_doc_number'])
        self.assertEqual('0011', results[0]['pp_z00_no_lines'])
        self.assertEqual('000400', results[0]['pp_z00_data_len'])



    def test_preprocess_lots_of_whitespace_and_none(self):
        """
        tests the case where whitespace exists
        """
        sample_data = [
            {
                # pk data
                'db_operation_cd': 'U',
                'dw_stg_2_aleph_lbry_name': 'mai60',
                'em_create_dw_prcsng_cycle_id': '-1',
                # z00 don't have trims
                'in_z00_doc_number': '  000019087 ',
                'in_z00_no_lines': None,
                'in_z00_data_len': None,
                # z13 has trims
                'in_z13_title': '  A literary history of America   ',
                'in_z13_author': '  Wendell, Barrett, 1855-1921  ',
                'in_z13_imprint': '  New York, Haskell House Publishers, 1968     '
            }
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        logger = None

        sample_json_config = {
            'z00_doc_number': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z00_no_lines': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z00_data_len': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z13_title': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            },
            'z13_author': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            },
            'z13_imprint': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            }
        }


        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        step = Preprocess(reader, writer, job_info, logger, sample_json_config, pk_list)
        step.execute()
        results = step.writer.list

        expected_keys = sorted([
            'in_z00_doc_number', 'pp_z00_doc_number', 'dw_stg_2_aleph_lbry_name', 'db_operation_cd',
            'pp_z00_no_lines', 'pp_z13_title', 'pp_z13_author',
            'pp_z00_data_len', 'pp_z13_imprint',
            'em_update_dw_prcsng_cycle_id', 'em_update_dw_job_exectn_id',
            'em_update_dw_job_name', 'em_update_dw_job_version_no',
            'em_update_user_id', 'em_update_tmstmp', 'em_create_dw_prcsng_cycle_id'
        ])
        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual("  000019087 ", results[0]['pp_z00_doc_number'])
        self.assertEqual("A literary history of America", results[0]['pp_z13_title'])
        self.assertEqual("Wendell, Barrett, 1855-1921", results[0]['pp_z13_author'])
        self.assertEqual(None, results[0]['pp_z00_no_lines'])
        self.assertEqual(None, results[0]['pp_z00_data_len'])

    def test_z00_pp(self):

        sample_data = [
            {
             'db_operation_cd': 'U',
             'in_z00_data': '',
             'in_z00_data_len': '001726',
             'in_z00_doc_number': '000181506',
             'in_z00_no_lines': '0038',
             'dw_stg_2_aleph_lbry_name': 'mai01',
             'em_create_dw_prcsng_cycle_id': '-1',
             }
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        logger = None

        sample_json_config =    {'z00_doc_number': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z00_no_lines': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z00_data_len': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            }}

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        step = Preprocess(reader, writer, job_info, logger, sample_json_config, pk_list)
        step.execute()
        results = step.writer.list

        expected_keys = sorted([
            'in_z00_doc_number', 'pp_z00_doc_number', 'dw_stg_2_aleph_lbry_name', 'db_operation_cd',
            'pp_z00_no_lines',
            'pp_z00_data_len', 'pp_z00_data',
            'em_update_dw_prcsng_cycle_id', 'em_update_dw_job_exectn_id',
            'em_update_dw_job_name', 'em_update_dw_job_version_no',
            'em_update_user_id', 'em_update_tmstmp', 'em_create_dw_prcsng_cycle_id'
        ])
        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual("000181506", results[0]['pp_z00_doc_number'])
        self.assertEqual("0038", results[0]['pp_z00_no_lines'])
        self.assertEqual("001726", results[0]['pp_z00_data_len'])
        self.assertEqual("", results[0]['pp_z00_data'])
