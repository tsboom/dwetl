import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.identity_processor import IdentityProcessor


class TestIdentityProcessor(unittest.TestCase):
    # TODO: is this class necessary?
    def test_identity_processor(self):
        sample_data = [
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000007520' },
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000147967'}
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        # Using negative processing_cycle_id so having real data in the
        # tables won't interfere with the tests.
        processing_cycle_id = -1

        job_info = {
                'em_create_dw_prcsng_cycle_id': processing_cycle_id,
                'em_create_dw_job_exectn_id': 1,
                'em_create_dw_job_name': 'TEST',
                'em_create_dw_job_version_no': '0.0',
                'em_create_user_id': 'test_user',
                'em_create_tmstmp': datetime.datetime.now()
        }

        logger = None
        error_writer = ListWriter()

        step = IdentityProcessor(reader, writer, job_info, logger, error_writer)

        step.execute()

        results = writer.list

        self.assertEqual(len(sample_data), len(results))
        self.assertEqual('000007520', results[0]['rec_trigger_key'])
        self.assertEqual('000147967', results[1]['rec_trigger_key'])

        # job_info keys are not expected, because IdentityProcessing only
        # passes data unchanged from reader to writer
        expected_keys = [
            'rec_type_cd', 'db_operation_cd', 'rec_trigger_key'
        ]
        self.assertEqual(expected_keys, list(results[0].keys()))
