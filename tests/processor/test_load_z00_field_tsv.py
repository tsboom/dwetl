import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.load_z00_field_tsv import LoadZ00FieldTsv
from dwetl.job_info import JobInfo


class TestLoadZ00FieldTsv(unittest.TestCase):
    def test_load_z00_field_tsv(self):

        sample_data = [
            {'z00_doc_number': '000025252',
            'z00_marc_rec_field_cd': 'FMT',
            'UNUSED': 'L',
            'z00_marc_rec_field_txt': 'BK',
            }
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user' , '1', '1')

        logger = None

        step = LoadZ00FieldTsv(reader, writer, job_info, logger)

        step.execute()

        results = writer.list

        self.assertEqual(len(sample_data), len(results))

        expected_keys = sorted([
            'rec_type_cd', 'db_operation_cd', 'rec_trigger_key','z00_doc_number',
            'dw_stg_1_marc_rec_field_seq_no', 'z00_marc_rec_field_cd', 'z00_marc_rec_field_txt',
            'em_create_dw_prcsng_cycle_id', 'em_create_dw_job_exectn_id',
            'em_create_dw_job_name', 'em_create_dw_job_version_no',
            'em_create_user_id', 'em_create_tmstmp'
        ])
        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual(1, results[0]['dw_stg_1_marc_rec_field_seq_no'])

    def test_marc_rec_field_seq_no(self):
        """
        tests to see if sequence number increments when the same
        z00_doc_number comes in. resets sequence number to 1 if new z00_doc_number
        """
        sample_data = [
            {'z00_doc_number': '000025252',
            'z00_marc_rec_field_cd': 'FMT',
            'UNUSED': 'L',
            'z00_marc_rec_field_txt': 'BK',
            },
            {'z00_doc_number': '000025252',
            'z00_marc_rec_field_cd': 'LDR',
            'UNUSED': 'L',
            'z00_marc_rec_field_txt': '^^^^^cam^^2200493^^^4500',
            },
            {'z00_doc_number': '000090849',
            'z00_marc_rec_field_cd': 'FMT',
            'UNUSED': 'L',
            'z00_marc_rec_field_txt': 'BK',
            },
        ]
        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user' , '1', '1')

        logger = None

        step = LoadZ00FieldTsv(reader, writer, job_info, logger)

        step.execute()

        results = writer.list

        self.assertEqual(len(sample_data), len(results))

        self.assertEqual(1, results[0]['dw_stg_1_marc_rec_field_seq_no'])
        self.assertEqual(2, results[1]['dw_stg_1_marc_rec_field_seq_no'])
        self.assertEqual(1, results[2]['dw_stg_1_marc_rec_field_seq_no'])
