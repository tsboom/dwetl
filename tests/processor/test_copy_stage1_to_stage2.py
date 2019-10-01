import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.copy_stage1_to_stage2 import CopyStage1ToStage2
from dwetl.job_info import JobInfoFactory


class TestCopyStage1ToStage2(unittest.TestCase):
    def setUp(self):
        self.writer = ListWriter()
        self.job_info = JobInfoFactory.create_from_prcsng_cycle_id(-1)
        self.logger = None

    def test_copy_mai01_z00_stage1_to_stage2(self):
        sample_data = [
            {
                # Sample from dw_stg_1_mai01_z00
                '_sa_instance_state': '',
                'db_operation_cd': 'I',
                'em_create_dw_job_name': 'CreateFileEquivalentTable',
                'em_create_dw_prcsng_cycle_id': self.job_info.prcsng_cycle_id,
                'em_create_tmstmp': 'datetime.datetime(2019, 9, 17, 8, 53, 56, 619908)',
                'em_create_user_id': 'test_user',
                'em_create_dw_job_exectn_id': 1,
                'em_create_dw_job_version_no': '0.0',
                'rec_trigger_key': '006137019',
                'rec_type_cd': 'D',
                'z00_data': '',
                'z00_data_len': '005425',

        ]

        aleph_library = 'mai01'
        reader = ListReader(sample_data)
        processor = CopyStage1ToStage2.create(reader, self.writer, self.job_info, self.logger, aleph_library)
        processor.execute()
        results = self.writer.list

        self.assertEqual(len(sample_data), len(results))
        expected_keys = [
            'db_operation_cd',
            'dw_stg_2_aleph_lbry_name',
            'in_z00_doc_number',
            'in_z00_no_lines',
            'in_z00_data_len',
            'in_z00_data',
            'em_create_dw_prcsng_cycle_id',
            'em_create_dw_job_exectn_id',
            'em_create_dw_job_name',
            'em_create_dw_job_version_no',
            'em_create_user_id',
            'em_create_tmstmp'
        ]
        self.assertEqual(sorted(expected_keys), sorted(list(results[0].keys())))

        self.assertEqual('I', results[0]['db_operation_cd'])
        self.assertEqual('', results[0]['in_z00_data'])
        self.assertEqual('005425', results[0]['in_z00_data_len'])
        self.assertEqual('006137019', results[0]['in_z00_doc_number'])
        self.assertEqual('0047', results[0]['in_z00_no_lines'])
        self.assertEqual(processor.job_name(), results[0]['em_create_dw_job_name'])
        self.assertEqual('mai01', results[0]['dw_stg_2_aleph_lbry_name'])


    def test_copy_mai60_z00_field_stage1_to_stage2(self):
        sample_data = [
            {
                # Sample from dw_stg_1_mai60_z00_field
                '_sa_instance_state': '',
                'db_operation_cd': 'I',
                'em_create_dw_job_exectn_id': 1,
                'em_create_dw_job_name': 'CreateFileEquivalentTable',
                'em_create_dw_job_version_no': '0.0',
                'em_create_dw_prcsng_cycle_id': self.job_info.prcsng_cycle_id,
                'em_create_tmstmp': 'datetime.datetime(2019, 9, 17, 8, 53, 56, 619908)',
                'em_create_user_id': 'test_user',
                'rec_trigger_key': '000153121',
                'rec_type_cd': 'D',

            }
        ]

        aleph_library = 'mai50'
        reader = ListReader(sample_data)
        processor = CopyStage1ToStage2.create(reader, self.writer, self.job_info, self.logger, aleph_library)
        processor.execute()
        results = self.writer.list

        self.assertEqual(len(sample_data), len(results))
        expected_keys = [
            'db_operation_cd',
            'dw_stg_2_aleph_lbry_name',
            'in_z30_85x_type',
            'in_z30_alpha',
            'in_z30_arrival_date',
            'in_z30_barcode',
            'in_z30_call_no',
            'in_z30_call_no_2',
            'in_z30_call_no_2_key',
            'in_z30_call_no_2_type',
            'in_z30_call_no_key',
            'in_z30_call_no_type',
            'in_z30_cataloger',
            'in_z30_chronological_i',
            'in_z30_chronological_j',
            'in_z30_chronological_k',
            'in_z30_chronological_l',
            'in_z30_chronological_m',
            'in_z30_collection',
            'in_z30_copy_id',
            'in_z30_date_last_return',
            'in_z30_depository_id',
            'in_z30_description',
            'in_z30_enumeration_a',
            'in_z30_enumeration_b',
            'in_z30_enumeration_c',
            'in_z30_enumeration_d',
            'in_z30_enumeration_e',
            'in_z30_enumeration_f',
            'in_z30_enumeration_g',
            'in_z30_enumeration_h',
            'in_z30_expected_arrival_date',
            'in_z30_gap_indicator',
            'in_z30_hol_doc_number_x',
            'in_z30_hour_last_return',
            'in_z30_inventory_number',
            'in_z30_inventory_number_date',
            'in_z30_ip_last_return',
            'in_z30_ip_last_return_v6',
            'in_z30_issue_date',
            'in_z30_item_process_status',
            'in_z30_item_statistic',
            'in_z30_item_status',
            'in_z30_last_shelf_report_date',
            'in_z30_linking_number',
            'in_z30_maintenance_count',
            'in_z30_material',
            'in_z30_no_loans',
            'in_z30_note_circulation',
            'in_z30_note_internal',
            'in_z30_note_opac',
            'in_z30_on_shelf_date',
            'in_z30_on_shelf_seq',
            'in_z30_open_date',
            'in_z30_order_number',
            'in_z30_pages',
            'in_z30_price',
            'in_z30_process_status_date',
            'in_z30_rec_key',
            'in_z30_rec_key_2',
            'in_z30_rec_key_3',
            'in_z30_shelf_report_number',
            'in_z30_sub_library',
            'in_z30_supp_index_o',
            'in_z30_temp_location',
            'in_z30_upd_time_stamp',
            'in_z30_update_date',
            'em_create_dw_prcsng_cycle_id',
            'em_create_dw_job_exectn_id',
            'em_create_dw_job_name',
            'em_create_dw_job_version_no',
            'em_create_user_id',
            'em_create_tmstmp'
        ]
        self.assertEqual(sorted(expected_keys), sorted(list(results[0].keys())))

        self.assertEqual('U', results[0]['db_operation_cd'])
        self.assertEqual('$$hE185$$i.M43 1969a', results[0]['in_z30_call_no'])
        self.assertEqual('31430001459330                ', results[0]['in_z30_barcode'])
        self.assertEqual('                                   00000', results[0]['in_z30_rec_key_3'])
        self.assertEqual('BOOK ', results[0]['in_z30_material'])
        self.assertEqual('mai50', results[0]['dw_stg_2_aleph_lbry_name'])
        self.assertEqual(processor.job_name(), results[0]['em_create_dw_job_name'])

        def test_copy_mai50_z30_stage1_to_stage2(self):
            sample_data = [
                {
                    # Sample from dw_stg_1_mai50_z30
                    '_sa_instance_state': '',
                    'db_operation_cd': 'U',
                    'em_create_dw_job_exectn_id': 1,
                    'em_create_dw_job_name': 'CreateFileEquivalentTable',
                    'em_create_dw_job_version_no': '0.0',
                    'em_create_dw_prcsng_cycle_id': self.job_info.prcsng_cycle_id,
                    'em_create_tmstmp': 'datetime.datetime(2019, 9, 17, 8, 53, 56, 619908)',
                    'em_create_user_id': 'test_user',
                    'rec_trigger_key': '000000084000120',
                    'rec_type_cd': 'D',
                    'z30_85x_type': ' ',
                    'z30_alpha': 'L',
                    'z30_arrival_date': '00000000',
                    'z30_barcode': '31430001459330                ',
                    'z30_call_no': '$$hE185$$i.M43 1969a',
                    'z30_call_no_2': '',
                    'z30_call_no_2_key': '                                                                                ',
                    'z30_call_no_2_type': ' ',
                    'z30_call_no_key': 'E3185.-M43--41969-A                                                             ',
                    'z30_call_no_type': '0',
                    'z30_cataloger': '          ',
                    'z30_chronological_i': '',
                    'z30_chronological_j': '',
                    'z30_chronological_k': '',
                    'z30_chronological_l': '',
                    'z30_chronological_m': '',
                    'z30_collection': 'HOLD ',
                    'z30_copy_id': '     ',
                    'z30_date_last_return': '20190913',
                    'z30_depository_id': '     ',
                    'z30_description': 'v.1',
                    'z30_enumeration_a': '1',
                    'z30_enumeration_b': '',
                    'z30_enumeration_c': '',
                    'z30_enumeration_d': '',
                    'z30_enumeration_e': '',
                    'z30_enumeration_f': '',
                    'z30_enumeration_g': '',
                    'z30_enumeration_h': '',
                    'z30_expected_arrival_date': '00000000',
                    'z30_gap_indicator': ' ',
                    'z30_hol_doc_number_x': '001668394',
                    'z30_hour_last_return': '1157',
                    'z30_inventory_number': '',
                    'z30_inventory_number_date': '00000000',
                    'z30_ip_last_return': '128.8.44.58',
                    'z30_ip_last_return_v6': '',
                    'z30_issue_date': '00000000',
                    'z30_item_process_status': '  ',
                    'z30_item_statistic': '          ',
                    'z30_item_status': '01',
                    'z30_last_shelf_report_date': '00000000',
                    'z30_linking_number': '000000000',
                    'z30_maintenance_count': '000',
                    'z30_material': 'BOOK ',
                    'z30_no_loans': '010',
                    'z30_note_circulation': '',
                    'z30_note_internal': '',
                    'z30_note_opac': '',
                    'z30_on_shelf_date': '00000000',
                    'z30_on_shelf_seq': '000000',
                    'z30_open_date': '00000000',
                    'z30_order_number': '',
                    'z30_pages': '',
                    'z30_price': '          ',
                    'z30_process_status_date': '00000000',
                    'z30_rec_key': '000000084000120',
                    'z30_rec_key_2': '0000000000000000000',
                    'z30_rec_key_3': '                                   00000',
                    'z30_shelf_report_number': '                    ',
                    'z30_sub_library': 'CPOSS',
                    'z30_supp_index_o': '',
                    'z30_temp_location': 'N',
                    'z30_upd_time_stamp': '201909131157258',
                    'z30_update_date': '00000000',
                }
            ]

            aleph_library = 'mai50'
            reader = ListReader(sample_data)
            processor = CopyStage1ToStage2.create(reader, self.writer, self.job_info, self.logger, aleph_library)
            processor.execute()
            results = self.writer.list

            self.assertEqual(len(sample_data), len(results))
            expected_keys = [
                'db_operation_cd',
                'dw_stg_2_aleph_lbry_name',

                'em_create_dw_prcsng_cycle_id',
                'em_create_dw_job_exectn_id',
                'em_create_dw_job_name',
                'em_create_dw_job_version_no',
                'em_create_user_id',
                'em_create_tmstmp'
            ]
            self.assertEqual(sorted(expected_keys), sorted(list(results[0].keys())))

            self.assertEqual('U', results[0]['db_operation_cd'])
            self.assertEqual('$$hE185$$i.M43 1969a', results[0]['in_z30_call_no'])
            self.assertEqual('31430001459330                ', results[0]['in_z30_barcode'])
            self.assertEqual('                                   00000', results[0]['in_z30_rec_key_3'])
            self.assertEqual('BOOK ', results[0]['in_z30_material'])
            self.assertEqual('mai50', results[0]['dw_stg_2_aleph_lbry_name'])
            self.assertEqual(processor.job_name(), results[0]['em_create_dw_job_name'])
