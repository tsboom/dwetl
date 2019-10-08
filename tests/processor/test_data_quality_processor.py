import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.preprocess import Preprocess
import pdb

class TestDataQualityProcessor(unittest.TestCase):
    def test_data_quality_processor(self):
        """
        tests if
        """
        sample_data = [
            {
                 'db_operation_cd': 'I',
                 'dw_stg_2_aleph_lbry_name': 'mai39',
                 'in_z00_data': '',
                 'in_z00_data_len': '000464',
                 'in_z00_doc_number': '000025289',
                 'in_z00_no_lines': '0010',
                 'pp_z00_data': None,
                 'pp_z00_data_len': '000464',
                 'pp_z00_doc_number': None,
                 'pp_z00_no_lines': None,
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
