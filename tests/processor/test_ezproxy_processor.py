import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.ezproxy_processor import EzproxyProcessor
from tests import test_logger
import logging
import pdb


class TestEzproxyProcessor(unittest.TestCase):
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
        
    def test_convert_timestemp(self):
        
        result = EzproxyProcessor.convert_timestamp(self.sample_data[0])
        
        expected_result =  datetime.datetime.strptime('20200509-0000', '%Y%m%d-%H%M')
        
        self.assertEqual(expected_result, result)
        
    def test_library_dim_lookup(self):
        result = EzproxyProcessor.library_dim_lookup(self.sample_data[0])
        expected_result = 10
        
        self.assertEqual(expected_result, result)
        
    def test_clndr_dt_dim_lookup(self):
        result = EzproxyProcessor.clndr_dt_dim_lookup(self.sample_data[0])
        expected_result = 14740
        
        self.assertEqual(expected_result, result)
    
    def test_transform(self):
        result = EzproxyProcessor.transform(self.sample_data[0], self.logger)
        expected_keys = sorted(['em_create_dw_job_exectn_id', 'em_create_dw_job_name',
            'em_create_dw_job_version_no', 'em_create_dw_prcsng_cycle_id', 
            'em_create_tmstmp','em_create_user_id', 't1_ezp_sessns_snap_actv_sessns_cnt', 
            't1_ezp_sessns_snap_clndr_dt_dim_key', 't1_ezp_sessns_virtual_hosts_cnt',
            't1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key', 't2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp'])
        
        self.assertEqual(expected_keys, sorted(list(result.keys())))
        self.assertEqual('CopyStage1ToStage2', result['em_create_dw_job_name'])
        self.assertEqual(20, result['t1_ezp_sessns_snap_actv_sessns_cnt'])
        self.assertEqual(14740, result['t1_ezp_sessns_snap_clndr_dt_dim_key'])
        self.assertEqual(2718, result['t1_ezp_sessns_virtual_hosts_cnt'])    
        self.assertEqual(10, result['t1_mbr_lbry_cd__ezp_sessns_snap_mbr_lbry_dim_key'])
        self.assertEqual(datetime.datetime(2020, 5, 9, 0, 0), result['t2_ezp_sessns_snap_tmstmp__ezp_sessns_snap_tmstmp'])
        
    def test_end_to_end(self):
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        
        reader = ListReader(self.sample_data[0])
        
        ezproxy_processor = EzproxyProcessor(reader, writer, job_info, self.logger)
        ezproxy_processor.execute()
        
        results = ezproxy_processor.writer.list

        expected_result = []
        