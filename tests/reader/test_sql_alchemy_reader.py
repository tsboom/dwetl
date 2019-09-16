import unittest
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import datetime


class TestSqlAlchemyReader(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    def setUp(self):
        # See https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
        test_db_settings = database_credentials.test_db_settings()
        self.engine = create_engine(test_db_settings['TEST_DB_CONNECTION_STRING'])
        # connect to the database
        self.connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        s = sessionmaker()
        self.session = s(bind=self.connection)

        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)

    def setup_rows(self, session, base_table_class, rows):
        for row_dict in rows:
            record = self.table_base_class(**row_dict)
            self.session.add(record)
            self.session.commit()

    def append_job_info(self, row_dict, processing_cycle_field_name, processing_cycle_id):
        job_info = {
            'em_create_dw_job_exectn_id': 9999,
            'em_create_dw_job_name': 'TEST',
            'em_create_dw_job_version_no': '0.0',
            'em_create_user_id': 'test_user',
            'em_create_tmstmp': datetime.datetime.now(),
            processing_cycle_field_name: processing_cycle_id
        }

        row_dict.update(job_info)

    def test_read_empty_table(self):
        self.table_base_class = self.Base.classes.dw_stg_1_mai01_z00
        reader = SqlAlchemyReader(self.session, self.table_base_class, 'em_create_dw_prcsng_cycle_id', 9999)

        results = []
        for row in reader:
            results.append(row)

        self.assertEqual(0, len(results))

    def test_read_rows_from_table(self):
        # Add some sample rows to the "dw_stg_1_mai01_z00" table
        self.table_base_class = self.Base.classes.dw_stg_1_mai01_z00

        rows = [
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000205993',
             'z00_doc_number': '000205993', 'z00_no_lines': '0043', 'z00_data_len': '001583'},
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000245526'}
        ]

        for row in rows:
            self.append_job_info(row, 'em_create_dw_prcsng_cycle_id', 9999)

        self.setup_rows(self.session, self.table_base_class, rows)

        reader = SqlAlchemyReader(self.session, self.table_base_class, 'em_create_dw_prcsng_cycle_id', 9999)
        results = []
        for row in reader:
            results.append(row)

        self.assertEqual(2, len(results))
        self.assertEqual('000205993', results[0]['rec_trigger_key'])
        self.assertEqual('000245526', results[1]['rec_trigger_key'])

    def test_read_rows_from_table_with_multiple_processing_ids(self):
        # Add some sample rows to the "dw_stg_1_mai01_z00" table
        self.table_base_class = self.Base.classes.dw_stg_1_mai01_z00

        rows = [
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000205993',
             'z00_doc_number': '000205993', 'z00_no_lines': '0043', 'z00_data_len': '001583'},
            {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000245526'}
        ]

        # Use different em_create_dw_prcsng_cycle_ids for each row
        self.append_job_info(rows[0], 'em_create_dw_prcsng_cycle_id', 1234)
        self.append_job_info(rows[1], 'em_create_dw_prcsng_cycle_id', 9876)

        self.setup_rows(self.session, self.table_base_class, rows)

        reader = SqlAlchemyReader(self.session, self.table_base_class, 'em_create_dw_prcsng_cycle_id', 9876)
        results = []
        for row in reader:
            results.append(row)

        # Only the row matching the em_create_dw_prcsng_cycle_id should be returned
        self.assertEqual(1, len(results))
        self.assertEqual('000245526', results[0]['rec_trigger_key'])

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
