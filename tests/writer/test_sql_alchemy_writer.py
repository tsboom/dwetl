import unittest
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import dwetl.database_credentials as database_credentials
import datetime
import dwetl

class TestSqlAlchemyWriter(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    def setUp(self):
        pass

    def test_add_row_to_table(self):
        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_stg_1_mai01_z00

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

            writer = SqlAlchemyWriter(session, table_base_class)
            writer.write_row(row_dict)

            # Verify that the row was added
            result = session.query(table_base_class).filter(table_base_class.em_create_dw_prcsng_cycle_id == '9999').one()

            result_dict = result.__dict__
            self.assertEqual('000007520', result_dict['rec_trigger_key'])
            self.assertEqual('001504', result_dict['z00_data_len'])
