import unittest
import pytest
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.exceptions import DWETLException
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

            writer = SqlAlchemyWriter(session, table_base_class)
            writer.write_row(row_dict)

            # Verify that the row was added
            result = session.query(table_base_class).filter(
                table_base_class.em_create_dw_prcsng_cycle_id == processing_cycle_id
                ).one()

            result_dict = result.__dict__
            self.assertEqual('000007520', result_dict['rec_trigger_key'])
            self.assertEqual('001504', result_dict['z00_data_len'])
    
    
    def test_add_row_w_null_to_error_table_exception(self):
        with pytest.raises(DWETLException):
            with dwetl.test_database_session() as session:
                table_base_class = dwetl.Base.classes.dw_stg_1_ezp_sessns_snap
                error_table = dwetl.Base.classes.dw_db_errors

                # testing the row as it comes in from the TSV (during the ezproxy_load.load_stage_1)
                row_dict = {
                    'mbr_lbry_cd': 'cp',
                    'ezp_sessns_snap_tmstmp': '20201205-1600',
                    'ezp_sessns_snap_actv_sessns_cnt': '', # data comes in as an empty string 
                    'ezp_sessns_virtual_hosts_cnt': '2384',
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

                writer = SqlAlchemyWriter(session, table_base_class)
                # this method should raise a DWETLException
                writer.write_row(row_dict)
    
        
    def test_update_row_w_null_to_error_table_exception(self):
        with dwetl.test_database_session() as session:
            table_base_class = dwetl.Base.classes.dw_stg_1_ezp_sessns_snap
            error_table = dwetl.Base.classes.dw_db_errors

            # first write a row that is normal
            row_dict = {
                'mbr_lbry_cd': 'cp',
                'ezp_sessns_snap_tmstmp': '20201205-1600',
                'ezp_sessns_snap_actv_sessns_cnt': '1234', # data is normal
                'ezp_sessns_virtual_hosts_cnt': '2384',
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

            writer = SqlAlchemyWriter(session, table_base_class)
            writer.write_row(row_dict)

            # test throwing an exception when updating the row with an empty string
            with pytest.raises(DWETLException):

                # testing the row as it comes in from the TSV (during the ezproxy_load.load_stage_1)
                update_row_dict = {
                    'mbr_lbry_cd': 'cp',
                    'ezp_sessns_snap_tmstmp': '20201205-1600',
                    'ezp_sessns_snap_actv_sessns_cnt': '', # data is empty
                    'ezp_sessns_virtual_hosts_cnt': '2384',
                }
                # Using negative processing_cycle_id so having real data in the
                # tables won't interfere with the tests.
                processing_cycle_id = -1

                job_info = {
                    'em_create_dw_prcsng_cycle_id': processing_cycle_id,
                    'em_create_dw_job_exectn_id': 1,
                    'em_update_dw_job_name': 'TEST',
                    'em_update_dw_job_version_no': '0.0',
                    'em_update_user_id': 'test_user',
                    'em_update_tmstmp': datetime.datetime.now()
                }

                update_row_dict.update(job_info)

                writer = SqlAlchemyWriter(session, table_base_class)
                # this method should raise a DWETLException
                writer.write_row(update_row_dict)


  
      

