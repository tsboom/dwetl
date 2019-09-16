import unittest
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import datetime


class TestSqlAlchemyWriter(unittest.TestCase):
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

    def test_add_row_to_table(self):
        table_base_class = self.Base.classes.dw_stg_1_mai01_z00

        row_dict = {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000007520',
                    'z00_doc_number': '000007520', 'z00_no_lines': '0041', 'z00_data_len': '001504'}

        job_info = {
            'em_create_dw_prcsng_cycle_id': 9999,
            'em_create_dw_job_exectn_id': 9999,
            'em_create_dw_job_name': 'TEST',
            'em_create_dw_job_version_no': '0.0',
            'em_create_user_id': 'test_user',
            'em_create_tmstmp': datetime.datetime.now()
        }

        row_dict.update(job_info)

        writer = SqlAlchemyWriter(self.session, table_base_class)
        writer.write_row(row_dict)

        # Verify that the row was added
        result = self.session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id == '9999').one()

        result_dict = result.__dict__
        self.assertEqual('000007520', result_dict['rec_trigger_key'])
        self.assertEqual('001504', result_dict['z00_data_len'])

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
