import unittest
import datetime
import dwetl
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.ezproxy_processor import EzproxyProcessor
from tests import test_logger
import logging
import pdb


class TestEzproxyLoadProcessor(unittest.TestCase):
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
