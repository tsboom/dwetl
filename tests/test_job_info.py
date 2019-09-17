import unittest
import pdb
import datetime
import getpass
import dwetl.database_credentials as database_credentials
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import func
from dwetl.job_info import JobInfo, JobInfoFactory
import dwetl

class TestJobInfo(unittest.TestCase):

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
        job_info = JobInfo(4, 'thschone', '1.0.0', 1)

        self.assertEqual(4, job_info.prcsng_cycle_id)
        self.assertEqual('thschone', job_info.user_id)
        self.assertEqual('1.0.0', job_info.job_version_no)
        self.assertEqual(1, job_info.job_exectn_id)

    def test_job_info_factory_create_from_db(self):
        # expected user
        expected_user = getpass.getuser()

        table_base_class = self.Base.classes.dw_prcsng_cycle
        job_info = JobInfoFactory.create_job_info_from_db(self.session, table_base_class)
        self.assertEqual(1, job_info.prcsng_cycle_id)
        self.assertEqual(1, job_info.job_exectn_id)
        self.assertEqual(dwetl.version, job_info.job_version_no)
        self.assertEqual(expected_user, job_info.user_id)
        
        added_record = self.session.query(table_base_class).filter(table_base_class.dw_prcsng_cycle_id == 1).one().__dict__
        self.assertEqual(1, added_record['dw_prcsng_cycle_id'])
        self.assertEqual(expected_user, added_record['em_create_user_id'])


    def test_job_info_factory_create_from_db_existing(self):
        '''test when there are existing entries in the dw_prcsng_cycle table'''
        #add existing entry
        row = {
            'dw_prcsng_cycle_id': 3,
            'dw_prcsng_cycle_planned_dt': datetime.datetime.now(),
            'dw_prcsng_cycle_stat_type_cd': '',
            'dw_prcsng_cycle_freq_type_cd': '',
            'dw_prcsng_cycle_exectn_start_tmstmp': datetime.datetime.now(),
            'em_create_tmstmp': datetime.datetime.now(),
            'em_create_user_id': 'thschone'
        }
        table_base_class = self.Base.classes.dw_prcsng_cycle
        record = table_base_class(**row)
        self.session.add(record)
        self.session.commit()

        job_info = JobInfoFactory.create_job_info_from_db(self.session, table_base_class)
        self.assertEqual(4, job_info.prcsng_cycle_id)

        expected_version = dwetl.version
        self.assertEqual(expected_version, job_info.job_version_no)

        self.assertEqual(1, job_info.job_exectn_id)



    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()
