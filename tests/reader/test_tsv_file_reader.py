import unittest
from tests.temporary_test_file import TemporaryTestFile
from dwetl.reader.tsv_file_reader import TsvFileReader


class TestTsvFileReader(unittest.TestCase):
    def test_simple_tsv(self):
        lines = [
            'H\tHeader line 2',
            'field1\tfield2\tfield3',
            'A\tB\tC',
            'One\tTwo\tThree',
            'T\tFooter'
        ]

        expected_line1 = {'field1': 'A', 'field2': 'B', 'field3': 'C'}
        expected_line2 = {'field1': 'One', 'field2': 'Two', 'field3': 'Three'}

        with TemporaryTestFile(lines) as tempFilePath:
            tsv_file_reader = TsvFileReader(tempFilePath)
            line1 = next(iter(tsv_file_reader))
            line2 = next(iter(tsv_file_reader))
            self.assertEqual(expected_line1, line1)
            self.assertEqual(expected_line2, line2)

    def test_simple_tsv_with_incomplete_row(self):
        lines = [
            'H\tHeader line 2',
            'field1\tfield2\tfield3',
            'A\tB\tC',
            'One',
            'T\tFooter'
        ]

        expected_line1 = {'field1': 'A', 'field2': 'B', 'field3': 'C'}
        expected_line2 = {'field1': 'One'}

        with TemporaryTestFile(lines) as tempFilePath:
            tsv_file_reader = TsvFileReader(tempFilePath)
            results = []
            for row in tsv_file_reader:
                results.append(row)

            self.assertEqual(2, len(results))
            self.assertEqual(expected_line1, results[0])
            self.assertEqual(expected_line2, results[1])

    def test_empty_file(self):
        with TemporaryTestFile([]) as tempFilePath:
            tsv_file_reader = TsvFileReader(tempFilePath)
            results = []
            for row in tsv_file_reader:
                results.append(row)
            self.assertEqual(0, len(results))

    def test_mai50_z30_data_file(self):
        expected_line = {
            'rec_type_cd': 'D',
            'db_operation_cd': 'U',
            'rec_trigger_key': '000001056000030',
            'z30_rec_key': '000001056000030',
            'z30_barcode': '32061003025024                ',
            'z30_sub_library': 'SU-CR',
            'z30_material': 'BOOK ',
            'z30_item_status': '54',
            'z30_open_date': '20131010',
            'z30_update_date': '20190718',
            'z30_cataloger': 'UTILITY   ',
            'z30_date_last_return': '20190221',
            'z30_hour_last_return': '1240',
            'z30_ip_last_return': '136.160.120.106',
            'z30_no_loans': '014',
            'z30_alpha': 'L',
            'z30_collection': 'E    ',
            'z30_call_no_type': '1',
            'z30_call_no': '$$hSEU',
            'z30_call_no_key': 'SEU                                                                             ',
            'z30_call_no_2_type': '',
            'z30_call_no_2': '',
            'z30_call_no_2_key': '                                                                                ',
            'z30_description': '',
            'z30_note_opac': '',
            'z30_note_circulation': '',
            'z30_note_internal': '',
            'z30_order_number': '',
            'z30_inventory_number': '',
            'z30_inventory_number_date': '20131010',
            'z30_last_shelf_report_date': '00000000',
            'z30_price': '',
            'z30_shelf_report_number': '                    ',
            'z30_on_shelf_date': '00000000',
            'z30_on_shelf_seq': '000000',
            'z30_rec_key_2': '0000000000000000000',
            'z30_rec_key_3': '                                   00000',
            'z30_pages': '',
            'z30_issue_date': '00000000',
            'z30_expected_arrival_date': '00000000',
            'z30_arrival_date': '00000000',
            'z30_item_statistic': '',
            'z30_item_process_status': '  ',
            'z30_copy_id': '',
            'z30_hol_doc_number_x': '008887590',
            'z30_temp_location': 'N',
            'z30_enumeration_a': '',
            'z30_enumeration_b': '',
            'z30_enumeration_c': '',
            'z30_enumeration_d': '',
            'z30_enumeration_e': '',
            'z30_enumeration_f': '',
            'z30_enumeration_g': '',
            'z30_enumeration_h': '',
            'z30_chronological_i': '',
            'z30_chronological_j': '',
            'z30_chronological_k': '',
            'z30_chronological_l': '',
            'z30_chronological_m': '',
            'z30_supp_index_o': '',
            'z30_85x_type': '',
            'z30_depository_id': '',
            'z30_linking_number': '000000000',
            'z30_gap_indicator': '',
            'z30_maintenance_count': '013',
            'z30_process_status_date': '20131010',
            'z30_upd_time_stamp': '201909121206119',
            'z30_ip_last_return_v6': ''
        }

        tsv_file_reader = TsvFileReader('tests/data/mai50_z30_data')
        line1 = next(iter(tsv_file_reader))
        self.assertEqual(expected_line, line1)
