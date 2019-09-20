import unittest
import datetime
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.processor.data_quality_checks import DataQualityChecks
import dwetl.data_quality_utilities as dqu
import dwetl.table_transform
import os

class TestDataQualityCheck(unittest.TestCase):
    def setUp(self):
        self.job_info = {
                'em_create_dw_prcsng_cycle_id': -1,
                'em_create_dw_job_exectn_id': 1,
                'em_create_dw_job_name': 'DataQualityChecks',
                'em_create_dw_job_version_no': '0.0',
                'em_create_user_id': 'test_user',
                'em_create_tmstmp': datetime.datetime.now()
        }

        table_config_path = os.path.join('table_config', 'library_item_dimension.json')

        # load table config JSON
        self.table_config = dwetl.table_transform.load_table_config(table_config_path)

        # with dwetl.test_database_session() as session:
        #     table_base_class = dwetl.Base.classes.dw_stg_2_lbry_item_z30
        #     query_field = getattr(table_base_class, 'em_create_dw_prcsng_cycle_id')
        #     self.query = session.query(table_base_class).filter(query_field == 9999)
        #     row = next(iter(self.query.all()))
        #     print(row.__dict__)
        self.sample_row = {
            # Preprocessing - field should be trimmed
            'in_z30_call_no_key': 'E3185.-M43--41969-A                                                             ',
            # Preprocessing - No preprocessing
            'in_z30_material': 'BOOK ',
            # Preprocessing - No preprocessing
            'in_z30_pages': '',
            # Preprocessing - field should be trimmed
            'in_z30_price': '          ',
        }

    def curry(f, *params):
        def c(string):
            return f(string, *params)
        return c

    def test_data_quality_checks(self):
        # curry = getattr(dqu, 'is_valid_length')
        # result = curry(15, '123456789012345')
        f = getattr(dqu, 'is_valid_length')
        c = TestDataQualityCheck.curry(f, 15)
        result = c('123456789012345')
        print(f'result={result}')

        f = getattr(dqu, 'is_numeric')
        c = TestDataQualityCheck.curry(f)
        result = c('123456789012345A')
        print(f'result={result}')

        reader = ListReader([self.sample_row])
        self.writer = ListWriter()
        self.logger = None
        processor = DataQualityChecks.create(reader, self.writer, self.job_info, self.logger, self.table_config)
        processor.execute()
        results = self.writer.list

        self.assertEqual(1, len(results))

        # Preprocessing checks
        row = results[0]
        self.assertEqual('E3185.-M43--41969-A                                                             ', row['in_z30_call_no_key'])
        self.assertEqual('E3185.-M43--41969-A', row['pp_z30_call_no_key'])
        self.assertEqual('', row['pp_z30_pages'])
        self.assertEqual('', row['pp_z30_price'])
        self.assertEqual('BOOK ', row['pp_z30_material'])

        # Data quality checks


    def test_remove_prefix(self):
        reader = ListReader([self.sample_row])
        self.writer = ListWriter()
        self.logger = None
        processor = DataQualityChecks.create(reader, self.writer, self.job_info, self.logger, self.table_config)

        self.assertEqual('z30_material', processor.remove_prefix('in_z30_material', 'in_'))
        self.assertEqual('db_operation_cd', processor.remove_prefix('db_operation_cd', 'in_'))
        self.assertEqual(None, processor.remove_prefix(None, 'in_'))