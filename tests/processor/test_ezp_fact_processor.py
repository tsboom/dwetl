import unittest
import datetime
import dwetl
import dwetl.processor.ezproxy_fact_processor
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.ezproxy_fact_processor import EzproxyFactProcessor
from tests import test_logger
import logging
import pdb


class TestEzproxyFactProcessor(unittest.TestCase):
    maxDif= None
    @classmethod
    def setUpClass(cls):
        cls.logger = test_logger.logger
        cls.max_ezp_sessns_snap_fact_key = 1
        cls.invalid_keys = ['_sa_instance_state']
        cls.primary_keys = ['em_create_dw_prcsng_cycle_id', 'in_ezp_sessns_snap_tmstmp', 'in_mbr_lbry_cd']
        cls.em_create_keys = ['em_create_dw_job_exectn_id', 'em_create_dw_job_name', 'em_create_dw_job_version_no', 'em_create_user_id', 'em_create_tmstmp']
        cls.em_metadata_keys = ['em_update_dw_job_exectn_id', 'em_create_dw_job_version_no', 'em_update_user_id' ]

        cls.job_info = JobInfo(-1, 'test_user', '1', '1')

        cls.sample_data = [{'em_create_dw_job_exectn_id': 1,
                        'em_create_dw_job_name': 'CopyStage1ToStage2',
                        'em_create_dw_job_version_no': '1.0.0',
                        'em_create_dw_prcsng_cycle_id': 1,
                        'em_create_tmstmp': datetime.datetime(2020, 5, 13, 15, 40, 10, 575382),
                        'em_create_user_id': 'thschone',
                        'in_ezp_sessns_snap_actv_sessns_cnt': 20,
                        'in_ezp_sessns_snap_tmstmp': '20200509-0000',
                        'in_ezp_sessns_virtual_hosts_cnt': 2718,
                        'in_mbr_lbry_cd': 'ub'}]

    def test_process_item(self):
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        reader = ListReader(self.sample_data)
        error_writer = ListWriter()
        ezproxy_fact_processor = EzproxyFactProcessor(reader, writer, job_info, self.logger, self.max_ezp_sessns_snap_fact_key, error_writer)
        ezproxy_fact_processor.execute()
        results = ezproxy_fact_processor.writer.list
        expected_keys = sorted([
            'em_create_dw_prcsng_cycle_id', 'in_ezp_sessns_snap_tmstmp', 'in_mbr_lbry_cd',
            'em_create_dw_job_exectn_id', 'em_create_dw_job_name', 'em_create_dw_job_version_no',
            'em_create_user_id', 'em_create_tmstmp',  'ezp_sessns_snap_fact_key'
            ])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))


