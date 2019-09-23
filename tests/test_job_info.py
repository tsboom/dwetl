import unittest
import datetime
import getpass
import pdb
from sqlalchemy.sql.expression import func
import dwetl.database_credentials as database_credentials
from dwetl.job_info import JobInfo, JobInfoFactory
import dwetl


class TestJobInfo(unittest.TestCase):
    def test_create_job_info(self):
        job_info = JobInfo(-1, 'thschone', '1.0.0', 1)

        self.assertEqual(-1, job_info.prcsng_cycle_id)
        self.assertEqual('thschone', job_info.user_id)
        self.assertEqual('1.0.0', job_info.job_version_no)
        self.assertEqual(1, job_info.job_exectn_id)

    def test_job_info_as_dict(self):
        job_info = JobInfo(-1, 'thschone', '1.0.0', 1)
        result = job_info.as_dict('create')
        expected_keys = [
            'em_create_dw_prcsng_cycle_id',
            'em_create_user_id',
            'em_create_dw_job_version_no',
            'em_create_dw_job_exectn_id'
        ]
        actual_keys = list(result.keys())
        expected_keys.sort()
        actual_keys.sort()
        self.assertEqual(expected_keys, actual_keys)
        self.assertEqual(-1, result['em_create_dw_prcsng_cycle_id'])
        self.assertEqual('thschone', result['em_create_user_id'])
        self.assertEqual('1.0.0', result['em_create_dw_job_version_no'])
        self.assertEqual(1, result['em_create_dw_job_exectn_id'])

    def get_max_prcsng_cycle_id(self, session, table_base_class):
        current_prcsng_cycle_id = session.query(func.max(table_base_class.dw_prcsng_cycle_id)).scalar()
        if not current_prcsng_cycle_id:
            current_prcsng_cycle_id = 0
        return current_prcsng_cycle_id

    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    def test_job_info_factory_create_from_db(self):
        # expected user
        expected_user = getpass.getuser()

        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_prcsng_cycle
            prcsng_cycle_id = self.get_max_prcsng_cycle_id(session, table_base_class)
            next_pcid = prcsng_cycle_id + 1
            job_info = JobInfoFactory.create_job_info_from_db(session, table_base_class)
            self.assertEqual(next_pcid, job_info.prcsng_cycle_id)
            self.assertEqual(1, job_info.job_exectn_id)
            self.assertEqual(dwetl.version, job_info.job_version_no)
            self.assertEqual(expected_user, job_info.user_id)

            added_record = session.query(table_base_class).filter(table_base_class.dw_prcsng_cycle_id == next_pcid).one().__dict__
            self.assertEqual(next_pcid, added_record['dw_prcsng_cycle_id'])
            self.assertEqual(expected_user, added_record['em_create_user_id'])

    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    def test_job_info_factory_create_from_db_existing(self):
        '''test when there are existing entries in the dw_prcsng_cycle table'''
        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_prcsng_cycle
            prcsng_cycle_id = self.get_max_prcsng_cycle_id(session, table_base_class)

            job_info = JobInfoFactory.create_job_info_from_db(session, table_base_class)
            self.assertEqual(prcsng_cycle_id + 1, job_info.prcsng_cycle_id)

            expected_version = dwetl.version
            self.assertEqual(expected_version, job_info.job_version_no)

            self.assertEqual(1, job_info.job_exectn_id)

            job_info = JobInfoFactory.create_job_info_from_db(session, table_base_class)
            self.assertEqual(prcsng_cycle_id + 2, job_info.prcsng_cycle_id)

            expected_version = dwetl.version
            self.assertEqual(expected_version, job_info.job_version_no)
