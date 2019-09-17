import unittest
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import func
from dwetl.job_info import JobInfo

class TestJobInfo(unittest.TestCase):
    def setUp(self):
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

    def test_create_job_info(self):
        job_info = JobInfo()
        job_info.prcsng_cycle_id
        job_info.job_exectn_id
        job_info.job_version_no
        job_info.user_id
        self.assertEqual(1, job_info.prcsng_cycle_id)
        self.assertEqual(1, job_info.job_exectn_id)
        self.assertEqual('1.0.0', job_info.job_version_no)
        self.assertEqual('thschone', job_info.user_id)

    def test_set_prcsng_cycle_id(self):
        table_base_class = self.Base.classes.dw_stg_1_mai01_z00




    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
