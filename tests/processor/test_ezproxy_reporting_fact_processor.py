import unittest
import datetime
import dwetl
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.ezproxy_reporting_fact_processor import EzproxyReportingFactProcessor
from tests import test_logger
import logging
import pdb


class TestEzproxyReportingFactProcessor(unittest.TestCase):
    maxDif= None
    @classmethod
    def setUpClass(cls):

        cls.logger = test_logger.logger

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

    def test_process_item(self, cls.sample_data):
        result = EzproxyProcessor.transform(self.sample_data[0], self.logger)

        expected_keys = sorted([
            'em_create_dw_prcsng_cycle_id', 'in_ezp_sessns_snap_tmstmp',
            'in_mbr_lbry_cd',
            't1_ezp_sessns_snap_actv_sessns_cnt',
            't1_ezp_sessns_snap_tmstmp__ezp_sessns_snap_clndr_dt_dim_key', 't1_ezp_sessns_virtual_hosts_cnt',
            't1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key', 't2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp',
            't3_ezp_sessns_snap_tmstmp__ezp_sessns_snap_time_of_day_dim_key'
            ])

        self.assertEqual(expected_keys, sorted(list(result.keys())))
        self.assertEqual(20, result['t1_ezp_sessns_snap_actv_sessns_cnt'])
        self.assertEqual(14740, result['t1_ezp_sessns_snap_tmstmp__ezp_sessns_snap_clndr_dt_dim_key'])
        self.assertEqual(2718, result['t1_ezp_sessns_virtual_hosts_cnt'])
        self.assertEqual(10, result['t1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key'])
        self.assertEqual(datetime.datetime(2020, 5, 9, 0, 0), result['t2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp'])

            def job_name(self):
                return 'EzproxyFactProcessor'
