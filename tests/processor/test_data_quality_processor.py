import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.data_quality_info import DataQualityInfo
from dwetl.processor.data_quality_processor import DataQualityProcessor
import datetime
import logging
import pdb
import pprint
import json

class TestDataQualityProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("hello")


    def test_get_dq_checks_for_key(self):
        key = 'pp_z00_doc_number'
        #json_config = self.bib_rec_sample_json_config
        with open('table_config/bibliographic_record_dimension.json') as json_file:
            json_config = json.load(json_file)
        with open('tests/data/test2_bib_rec_z00.json') as json_file:
            data_raw = json.load(json_file)
            expected_result = data_raw['expected_result']

        result = DataQualityProcessor.get_dq_checks_for_key(key, json_config)
        #pdb.set_trace()
        self.assertEqual(expected_result, result)

    def test_get_suspend_record_code(self):
        key = "pp_z00_doc_number"
        with open('table_config/bibliographic_record_dimension.json') as json_file:
            json_config = json.load(json_file)

        json_config = {
            'specific_dq_function': 'no_missing_values',
            'specific_dq_function_param_1': '',
            'suspend_record': 'Yes',
            'type': 'Missing Value',
            'always':'x',
            'only_if_data_exists': '',
            'exception_message': 'Missing Value',
            'replacement_value': 'N/A'
        }

        dq = DataQualityInfo(json_config)

        expected_result = "MIS"
        result = DataQualityProcessor.get_suspend_record_code(key, dq)
        self.assertEqual(expected_result, result)


    def test_dataquality_bib_rec(self):

        with open('table_config/bibliographic_record_dimension.json') as json_file:
            config = json.load(json_file)

        with open('tests/data/test2_bib_rec_z00.json') as json_file:
            data_raw = json.load(json_file)
            data = data_raw['bib_rec_sample_data']
            for key , val in data[0].items(): #removing single quotes around None values
                print("hello")
                if val == "None":
                    data[0][key] =None;




        reader = ListReader(data)

        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        #create test logger
        today = datetime.datetime.now().strftime('%Y%m%d')
        logger = logging.getLogger('dwetl')
        file_handler = logging.FileHandler(f'logs/test.dwetl.log.{today}')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        data_quality_processor = DataQualityProcessor(reader, writer, job_info, logger, config, pk_list)
        data_quality_processor.execute()
        results = data_quality_processor.writer.list

        expected_keys = sorted([
            'db_operation_cd', 'dq_z00_data', 'dq_z00_data_len', 'dq_z00_doc_number', 'dq_z00_no_lines', 'dw_stg_2_aleph_lbry_name',
            'em_update_dw_job_exectn_id', 'em_update_dw_job_name', 'em_update_dw_job_version_no',
            'em_update_dw_prcsng_cycle_id', 'em_update_tmstmp', 'em_update_user_id',
            'in_z00_doc_number', 'rm_dq_check_excptn_cnt', 'rm_suspend_rec_flag', 'rm_suspend_rec_reason_cd'
            ])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual(expected_keys, sorted(list(results[1].keys())))
        self.assertEqual("SUS", results[0]['dq_z00_doc_number'])
        self.assertEqual(1, results[0]['rm_dq_check_excptn_cnt'])
        self.assertEqual("MIS", results[0]['rm_suspend_rec_reason_cd'])

        self.assertEqual("SUS", results[1]['dq_z00_doc_number'])
        self.assertEqual(1, results[1]['rm_dq_check_excptn_cnt'])
        self.assertEqual("LEN", results[1]['rm_suspend_rec_reason_cd'])

        self.assertEqual('0049', results[0]['dq_z00_no_lines'])
        self.assertEqual('001970', results[0]['dq_z00_data_len'])

        self.assertEqual('000053939', results[2]['dq_z00_doc_number'])
