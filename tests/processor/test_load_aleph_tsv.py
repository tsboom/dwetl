import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.load_aleph_tsv import LoadAlephTsv
from dwetl.job_info import JobInfo


class TestLoadAlephTsv(unittest.TestCase):
    def test_load_aleph_tsv(self):
        sample_data = [
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000007520' },
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000147967'}
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user' , '1', '1')

        logger = None

        step = LoadAlephTsv(reader, writer, job_info, logger)

        step.execute()

        results = writer.list

        self.assertEqual(len(sample_data), len(results))
        self.assertEqual('000007520', results[0]['rec_trigger_key'])
        self.assertEqual('000147967', results[1]['rec_trigger_key'])

        expected_keys = sorted([
            'rec_type_cd', 'db_operation_cd', 'rec_trigger_key',
            'em_create_dw_prcsng_cycle_id', 'em_create_dw_job_exectn_id',
            'em_create_dw_job_name', 'em_create_dw_job_version_no',
            'em_create_user_id', 'em_create_tmstmp'
        ])
        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
