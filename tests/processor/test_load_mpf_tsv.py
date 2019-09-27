import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.load_mpf_tsv import LoadMpfTsv
from dwetl.job_info import JobInfo


class TestLoadMpfTsv(unittest.TestCase):
    def test_load_mpf_tsv(self):

        sample_data = [
            {'collection_cd': 'MSTCK',
            'lbry_entity_cd': 'BC-BC',
            'collection_name': 'Media Stacks / Request to Pick-up at Home Library',
            'db_operation_cd': 'U',
            'lbry_staff_lms_user_id': 'hhanson',
            'db_operation_effective_date': '2019-08-19'}
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user' , '1', '1')

        logger = None

        step = LoadMpfTsv(reader, writer, job_info, logger)

        step.execute()

        results = writer.list

        self.assertEqual(len(sample_data), len(results))

        expected_keys = sorted([
            'collection_cd', 'collection_name', 'lbry_entity_cd', 'db_operation_cd', 'usmai_mbr_lbry_cd',
            'lbry_staff_lms_user_id', 'db_operation_effective_date',
            'em_create_dw_prcsng_cycle_id', 'em_create_dw_job_exectn_id',
            'em_create_dw_job_name', 'em_create_dw_job_version_no',
            'em_create_user_id', 'em_create_tmstmp'
        ])
        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual("BC", results[0]['usmai_mbr_lbry_cd'])

    def test_usmai_mbr_lbry_cd(self):
        self.assertEqual('HS', LoadMpfTsv.usmai_mbr_lbry_cd('HS-HS'))
        self.assertEqual('BC', LoadMpfTsv.usmai_mbr_lbry_cd('BC-BC'))
        self.assertEqual('CP', LoadMpfTsv.usmai_mbr_lbry_cd('CPMCK'))
        with self.assertRaises(ValueError):
            LoadMpfTsv.usmai_mbr_lbry_cd('')
        with self.assertRaises(TypeError):
            LoadMpfTsv.usmai_mbr_lbry_cd(None)
        #self.assertEqual(None, LoadMpfTsv.usmai_mbr_lbry_cd(None))
