import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.create_file_equivalent_table import CreateFileEquivalentTable


class TestCreateFileEquivalentTable(unittest.TestCase):
    def test_create_file_equivalent_table(self):
        sample_data = [
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000007520' },
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000147967'}
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = {
                'em_create_dw_prcsng_cycle_id': 9999,
                'em_create_dw_job_exectn_id': 9999,
                'em_create_dw_job_name': 'TEST',
                'em_create_dw_job_version_no': '0.0',
                'em_create_user_id': 'test_user',
                'em_create_tmstmp': datetime.datetime.now()
        }

        logger = None

        step = CreateFileEquivalentTable(reader, writer, job_info, logger)

        step.execute()

        results = writer.list

        self.assertEqual(len(sample_data), len(results))
        self.assertEqual('000007520', results[0]['rec_trigger_key'])
        self.assertEqual('000147967', results[1]['rec_trigger_key'])

        expected_keys = [
            'rec_type_cd', 'db_operation_cd', 'rec_trigger_key',
            'em_create_dw_prcsng_cycle_id', 'em_create_dw_job_exectn_id',
            'em_create_dw_job_name', 'em_create_dw_job_version_no',
            'em_create_user_id', 'em_create_tmstmp'
        ]
        self.assertEqual(expected_keys, list(results[0].keys()))
