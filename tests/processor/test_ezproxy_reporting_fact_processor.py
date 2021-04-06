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
        """
        cls.sample_data = [{'em_create_dw_job_exectn_id': 1,
                        'em_create_dw_job_name': 'CopyStage1ToStage2',
                        'em_create_dw_job_version_no': '1.0.0',
                        'em_create_dw_prcsng_cycle_id': 1,
                        'em_create_tmstmp': datetime.datetime(2020, 5, 13, 15, 40, 10, 575382),
                        'em_create_user_id': 'thschone',
                        'ezp_sessns_snap_clndr_dt_dim_key': 14740,
                        'in_ezp_sessns_snap_tmstmp': '20200509-0000',
                        'in_ezp_sessns_virtual_hosts_cnt': 2718,
                        'in_mbr_lbry_cd': 'ub'}]
        """
        cls.sample_data = [{ 'em_create_dw_job_exectn_id': 1,
                         'em_create_dw_job_name': 'EzproxyFactProcessor',
                         'em_create_dw_job_version_no': '1.0.0',
                         'em_create_dw_prcsng_cycle_id': 1,
                         'em_create_tmstmp': datetime.datetime(2020, 5, 27, 18, 6, 28, 183181),
                         'em_create_user_id': 'nasadi1',
                         'em_update_dw_job_exectn_id': None,
                         'em_update_dw_job_name': None,
                         'em_update_dw_job_version_no': None,
                         'em_update_dw_prcsng_cycle_id': None,
                         'em_update_reason_txt': None,
                         'em_update_tmstmp': None,
                         'em_update_user_id': None,
                         'ezp_sessns_snap_actv_sessns_cnt': 90,
                         'ezp_sessns_snap_clndr_dt_dim_key': 14740,
                         'ezp_sessns_snap_fact_key': 2,
                         'ezp_sessns_snap_mbr_lbry_dim_key': 14,
                         'ezp_sessns_snap_time_of_day_dim_key': 1,
                         'ezp_sessns_snap_tmstmp': datetime.datetime(2020, 5, 9, 0, 0)}]


    def test_end_to_end(self):
        writer = ListWriter()
        error_writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        reader = ListReader(self.sample_data)
        ezproxy_reporting_processor = EzproxyReportingFactProcessor(reader, writer, job_info, self.logger, error_writer)
        ezproxy_reporting_processor.execute()

        results = ezproxy_reporting_processor.writer.list

        expected_keys = sorted([
        'em_create_dw_job_exectn_id',
         'em_create_dw_job_name',
         'em_create_dw_job_version_no',
         'em_create_dw_prcsng_cycle_id',
         'em_create_tmstmp',
         'em_create_user_id',
         'em_update_dw_job_exectn_id',
         'em_update_dw_job_name',
         'em_update_dw_job_version_no',
         'em_update_dw_prcsng_cycle_id',
         'em_update_reason_txt',
         'em_update_tmstmp',
         'em_update_user_id',
         'ezp_sessns_snap_actv_sessns_cnt',
         'ezp_sessns_snap_clndr_dt_dim_key',
         'ezp_sessns_snap_fact_key',
         'ezp_sessns_snap_mbr_lbry_dim_key',
         'ezp_sessns_snap_time_of_day_dim_key',
         'ezp_sessns_snap_tmstmp',
         'rm_current_rec_flag',
         'rm_rec_effective_from_dt',
         'rm_rec_effective_to_dt',
         'rm_rec_type_cd',
         'rm_rec_type_desc',
         'rm_rec_version_no'
        ])

        self.assertEqual(None, results[0]['em_update_dw_job_exectn_id'])
        self.assertEqual(None, results[0]['em_update_dw_job_name'])
        self.assertEqual(None, results[0]['em_update_dw_job_version_no'])
        self.assertEqual(None, results[0]['em_update_dw_prcsng_cycle_id'])
        self.assertEqual(None, results[0]['em_update_reason_txt'])
        self.assertEqual(None, results[0]['em_update_tmstmp'])
        self.assertEqual(None, results[0]['em_update_user_id'])
        self.assertEqual('EzproxyReportingFactProcessor', results[0]['em_create_dw_job_name'])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
