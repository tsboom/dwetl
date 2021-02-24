import unittest
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import dwetl.database_credentials as database_credentials
import datetime
import dwetl
import pdb

class TestSqlAlchemyWriter(unittest.TestCase):
    @unittest.skipUnless(database_credentials.test_db_configured(), "Test database is not configured.")
    def setUp(self):
        pass

    def test_add_row_to_table(self):
        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_stg_1_mai01_z00
            error_table = dwetl.Base.classes.dw_db_errors

            row_dict = {'rec_type_cd': 'D', 'db_operation_cd': 'U', 'rec_trigger_key': '000007520',
                        'z00_doc_number': '000007520', 'z00_no_lines': '0041', 'z00_data_len': '001504'}

            # Using negative processing_cycle_id so having real data in the
            # tables won't interfere with the tests.
            processing_cycle_id = -1

            job_info = {
                'em_create_dw_prcsng_cycle_id': processing_cycle_id,
                'em_create_dw_job_exectn_id': 1,
                'em_create_dw_job_name': 'TEST',
                'em_create_dw_job_version_no': '0.0',
                'em_create_user_id': 'test_user',
                'em_create_tmstmp': datetime.datetime.now()
            }

            row_dict.update(job_info)

            writer = SqlAlchemyWriter(session, table_base_class, error_table)
            writer.write_row(row_dict)

            # Verify that the row was added
            result = session.query(table_base_class).filter(
                table_base_class.em_create_dw_prcsng_cycle_id == processing_cycle_id
                ).one()

            result_dict = result.__dict__
            self.assertEqual('000007520', result_dict['rec_trigger_key'])
            self.assertEqual('001504', result_dict['z00_data_len'])

    def test_add_row_w_null_to_error_table(self):
         with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_stg_2_ezp_sessns_snap
            error_table = dwetl.Base.classes.dw_db_errors
            row_dict = {
                'in_mbr_lbry_cd': 'cp',
                'in_ezp_sessns_snap_tmstmp': '20201205-1600',
                'in_ezp_sessns_snap_actv_sessns_cnt': None,
                'in_ezp_sessns_virtual_hosts_cnt': '2384'
            }

            # Using negative processing_cycle_id so having real data in the
            # tables won't interfere with the tests.
            processing_cycle_id = -1

            job_info = {
                'em_create_dw_prcsng_cycle_id': processing_cycle_id,
                'em_create_dw_job_exectn_id': 1,
                'em_create_dw_job_name': 'TEST',
                'em_create_dw_job_version_no': '0.0',
                'em_create_user_id': 'test_user',
                'em_create_tmstmp': datetime.datetime.now()
            }

            row_dict.update(job_info)

            writer = SqlAlchemyWriter(session, table_base_class, error_table)
            writer.write_row(row_dict)
            #pdb.set_trace()

            # Verify that if the row produced an error, that the error is caught and written to the error table
            error_string = "IntegrityError(\'(psycopg2.errors.NotNullViolation) null value in column \"ezp_sessns_snap_actv_sessns_cnt\" violates not-null constraint\\nDETAIL: Failing row contains (cp, 20201205-1600, null, 2384, 1, 1, LoadAlephTsv, 1.0.0, thschone, 2021-02-09 19:33:58.4565).\\n\')"
         
            result = session.query(error_table).filter(
                error_table.em_create_dw_prcsng_cycle_id == processing_cycle_id,
                error_table.dw_error_text == error_string
                ).one()

            result_dict = result.__dict__

            self.assertEqual('000007520', result_dict['rec_trigger_key'])
            self.assertEqual('001504', result_dict['z00_data_len'])

