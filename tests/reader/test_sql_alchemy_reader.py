import unittest
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
import dwetl.database_credentials as database_credentials
import datetime
import dwetl


class TestSqlAlchemyReader(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    
    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_stg_1_mai01_z00
            # delete results from test_read_rows_from_table and test_read_rows_from_table_with_multiple_processing_ids
            first_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id== -1)
            first_results.delete()
            
            second_results = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id== -2)
            second_results.delete()
            
            session.commit()
            
    def setup_rows(self, session, base_table_class, rows):
        for row_dict in rows:
            record = base_table_class(**row_dict)
            session.add(record)

    def append_job_info(self, row_dict, processing_cycle_field_name, processing_cycle_id):
        job_info = {
            processing_cycle_field_name: processing_cycle_id,
            'em_create_dw_job_exectn_id': 1,
            'em_create_dw_job_name': 'TEST',
            'em_create_dw_job_version_no': '0.0',
            'em_create_user_id': 'test_user',
            'em_create_tmstmp': datetime.datetime.now()
        }

        row_dict.update(job_info)

    def test_read_empty_table(self):
        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_stg_1_mai01_z00

            # Use negative processing cycle id, so any actual data in the tables
            # won't interfere with the tests.
            processing_cycle_id = -3
            reader = SqlAlchemyReader(session, table_base_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)

            results = []
            for row in reader:
                results.append(row)

            self.assertEqual(0, len(results))

    def test_read_rows_from_table(self):
        with dwetl.test_database_session() as session:
            # Add some sample rows to the "dw_stg_1_mai01_z00" table
            table_base_class = dwetl.Base.classes.dw_stg_1_mai01_z00

            rows = [
                {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000205993',
                 'z00_doc_number': '000205993', 'z00_no_lines': '0043', 'z00_data_len': '001583'},
                {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000245526'}
            ]

            # Use negative processing cycle id, so any actual data in the tables
            # won't interfere with the tests.
            processing_cycle_id = -1

            for row in rows:
                self.append_job_info(row, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)

            self.setup_rows(session, table_base_class, rows)

            reader = SqlAlchemyReader(session, table_base_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
            results = []
            for row in reader:
                results.append(row)

            self.assertEqual(2, len(results))
            self.assertEqual('000205993', results[0]['rec_trigger_key'])
            self.assertEqual('000245526', results[1]['rec_trigger_key'])

    def test_read_rows_from_table_with_multiple_processing_ids(self):
        with dwetl.test_database_session() as session:
            # Add some sample rows to the "dw_stg_1_mai01_z00" table
            table_base_class = dwetl.Base.classes.dw_stg_1_mai01_z00

            rows = [
                {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000205993',
                 'z00_doc_number': '000205993', 'z00_no_lines': '0043', 'z00_data_len': '001583'},
                {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000245526',
                'z00_doc_number': '000205966', 'z00_no_lines': '0066', 'z00_data_len': '001566'}
            ]

            # Use different em_create_dw_prcsng_cycle_ids for each row
            #
            # Using negative processing_cycle_ids so having real data in the
            # tables won't interfere with the tests.
            self.append_job_info(rows[0], 'em_create_dw_prcsng_cycle_id', -2)
            self.append_job_info(rows[1], 'em_create_dw_prcsng_cycle_id', -2)

            self.setup_rows(session, table_base_class, rows)

            reader = SqlAlchemyReader(session, table_base_class, 'em_create_dw_prcsng_cycle_id', -2)
            results = []
            for row in reader:
                results.append(row)

            # Two rows should be returned with processing cycle id of -2
            self.assertEqual(2, len(results))
            self.assertEqual('000205993', results[0]['rec_trigger_key'])
            self.assertEqual('000245526', results[1]['rec_trigger_key'])