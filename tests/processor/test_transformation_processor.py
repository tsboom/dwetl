import unittest
import dwetl
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.job_info import JobInfo
from dwetl.transformation_info import TransformationInfo
from dwetl.processor.transformation_processor import TransformationProcessor
from dwetl.processor.data_quality_processor import DataQualityProcessor
from tests.data.dimension_sample_data import bib_record_dimension_sample_data
from tests import test_logger
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
import datetime
import json
import logging
import pdb
import pprint


class TestTransformationProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.bib_record_dimension_sample_data_z00 = bib_record_dimension_sample_data.bib_rec_sample_data_z00

        cls.bib_record_dimension_sample_data_z13u = bib_record_dimension_sample_data.bib_rec_sample_data_z13u

        cls.logger = test_logger.logger
        with dwetl.test_database_session() as session:
            cls.error_writer = SqlAlchemyWriter(
                session, dwetl.Base.classes.dw_db_errors)

        with open('table_config/bibliographic_record_dimension.json') as json_file:
            cls.bib_rec_sample_json_config = json.load(json_file)

        with dwetl.test_database_session() as session:
            cls.error_writer = SqlAlchemyWriter(
                session, dwetl.Base.classes.dw_db_errors)

    def test_get_transformations_for_key(self):
        key = 'dq_z00_doc_number'

        json_config = self.bib_rec_sample_json_config

        result = TransformationProcessor.get_transformations_for_key(
            key, json_config)

        expected_result = [
            {
                "target_col_name": "bib_rec_source_system_id",
                "target_data_type": "Character(9)",
                "target_attribute": "- Bibliographic Record Identifier",
                "transformation_info": {
                    "chg_proc_type": "0",
                    "transform_action": "Move",
                    "action_specific": "As-Is",
                    "specific_transform_function": "",
                    "specific_transform_function_param1": "",
                    "specific_transform_function_param2": "",
                    "source_col_name": "z00_doc_number",
                    "source_data_type": "CHAR(9)",
                    "source_format": "",
                    "source_mandatory": None,
                    "aleph_table": "Z00",
                    "action_detailed_instructions": ""
                }
            }
        ]
        self.assertEqual(expected_result, result)

        # test z13u_user_defined_3
        key = 'dq_z13u_user_defined_3'
        result = TransformationProcessor.get_transformations_for_key(
            key, json_config)

        expected_result = [{'target_attribute': '- Bibliographic Record MARC Record Leader Field Text',
          'target_col_name': 'bib_rec_marc_rec_leader_field_txt',
          'target_data_type': 'VarChar(50)',
          'transformation_info': {'action_detailed_instructions': '',
                                  'action_specific': 'As-is',
                                  'aleph_table': 'Z13U',
                                  'chg_proc_type': '1',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'VARCHAR2(500)',
                                  'source_format': '',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': '',
                                  'specific_transform_function_param1': '',
                                  'specific_transform_function_param2': '',
                                  'transform_action': 'Move'}},
         {'target_attribute': '- Bibliographic Record Type Code',
          'target_col_name': 'bib_rec_type_cd',
          'target_data_type': 'Character(1)',
          'transformation_info': {'action_detailed_instructions': 'substr(z13u_user_defined_3,7,1)',
                                  'action_specific': 'Sub-String',
                                  'aleph_table': 'Z13U',
                                  'chg_proc_type': '1',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'VARCHAR2(500)',
                                  'source_format': '',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': 'substring',
                                  'specific_transform_function_param1': '6',
                                  'specific_transform_function_param2': '7',
                                  'transform_action': 'Move'}},
         {'target_attribute': '- Bibliographic Record Type Description',
          'target_col_name': 'bib_rec_type_desc',
          'target_data_type': 'VarChar(100)',
          'transformation_info': {'action_detailed_instructions': 'Look up description '
                                                                  'based on '
                                                                  'substr(z13u_user_defined_3,7,1)',
                                  'action_specific': 'Related Value',
                                  'aleph_table': 'Lookup (record_type_code.csv)',
                                  'chg_proc_type': 'N/A',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'N/A',
                                  'source_format': 'N/A',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': '',
                                  'specific_transform_function_param1': '',
                                  'specific_transform_function_param2': '',
                                  'transform_action': 'Lookup'}},
         {'target_attribute': '- Bibliographic Record Bibliographic Level Code',
          'target_col_name': 'bib_rec_bib_lvl_cd',
          'target_data_type': 'Character(1)',
          'transformation_info': {'action_detailed_instructions': 'substr(z13u_user_defined_3,8,1)',
                                  'action_specific': 'Sub-String',
                                  'aleph_table': 'Z13U',
                                  'chg_proc_type': '1',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'VARCHAR2(500)',
                                  'source_format': '',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': 'substring',
                                  'specific_transform_function_param1': '7',
                                  'specific_transform_function_param2': '8',
                                  'transform_action': 'Move'}},
         {'target_attribute': '- Bibliographic Record Bibliographic Level Description',
          'target_col_name': 'bib_rec_bib_lvl_desc',
          'target_data_type': 'VarChar(100)',
          'transformation_info': {'action_detailed_instructions': 'Look up description '
                                                                  'based on '
                                                                  'substr(z13u_user_defined_3,8,1)',
                                  'action_specific': 'Related Value',
                                  'aleph_table': 'Lookup (bibliographic_level.csv)',
                                  'chg_proc_type': 'N/A',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'N/A',
                                  'source_format': 'N/A',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': '',
                                  'specific_transform_function_param1': '',
                                  'specific_transform_function_param2': '',
                                  'transform_action': 'Lookup'}},
         {'target_attribute': '- Bibliographic Record Encoding Level Code',
          'target_col_name': 'bib_rec_encoding_lvl_cd',
          'target_data_type': 'Character(1)',
          'transformation_info': {'action_detailed_instructions': 'substr(z13u_user_defined_3,18,1)',
                                  'action_specific': 'Sub-String',
                                  'aleph_table': 'Z13U',
                                  'chg_proc_type': '1',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'VARCHAR2(500)',
                                  'source_format': '',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': 'substring',
                                  'specific_transform_function_param1': '17',
                                  'specific_transform_function_param2': '18',
                                  'transform_action': 'Move'}},
         {'target_attribute': '- Bibliographic Record Encoding Level Description',
          'target_col_name': 'bib_rec_encoding_lvl_desc',
          'target_data_type': 'VarChar(150)',
          'transformation_info': {'action_detailed_instructions': 'Look up description '
                                                                  'based on '
                                                                  'substr(z13u_user_defined_3,18,1)',
                                  'action_specific': 'Related Value',
                                  'aleph_table': 'Lookup (encoding_level.csv)',
                                  'chg_proc_type': 'N/A',
                                  'source_col_name': 'z13u_user_defined_3',
                                  'source_data_type': 'N/A',
                                  'source_format': 'N/A',
                                  'source_mandatory': 'N',
                                  'specific_transform_function': '',
                                  'specific_transform_function_param1': '',
                                  'specific_transform_function_param2': '',
                                  'transform_action': 'Lookup'}}]

        self.assertEqual(expected_result, result)


    def test_transform_bib_rec_z00(self):

        # dq check the sample data first before transforming
        reader = ListReader(self.bib_record_dimension_sample_data_z00)
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']
        data_quality_processor = DataQualityProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)
        data_quality_processor.execute()
        bib_rec_dq_results = data_quality_processor.writer.list

        # quick check that dq results are workign as expected for 'SUS'
        self.assertEqual('SUS', bib_rec_dq_results[0]['dq_z00_doc_number'])

        # item
        reader = ListReader(bib_rec_dq_results)
        writer = ListWriter()

        job_info = job_info = JobInfo(-1, 'test_user', '1', '1')

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        transformation_processor = TransformationProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)


        transformation_processor.execute()
        results = transformation_processor.writer.list

        expected_keys = sorted([
            'db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'em_update_dw_job_exectn_id', 'em_update_dw_job_name',
            'em_update_dw_job_version_no', 'em_create_dw_prcsng_cycle_id','em_update_dw_prcsng_cycle_id', 'em_update_tmstmp', 'em_update_user_id',
            'in_z00_doc_number'
        ])

        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual(expected_keys, sorted(list(results[1].keys())))

        self.assertEqual('TransformationProcessor', results[0]['em_update_dw_job_name'])

        # test first item from sample data
        self.assertEqual


        # the third item in results has successful transforms
        self.assertEqual('', results[2]['t1_z00_data__bib_rec_marc_rec_data_cntnt_txt'])
        self.assertEqual('001970',results[2]['t1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt'] )
        self.assertEqual('000053939', results[2]['t1_z00_doc_number__bib_rec_source_system_id'])




    def test_transform_bib_rec_z13u(self):

        # dq check the sample data first before transforming
        reader = ListReader(self.bib_record_dimension_sample_data_z13u)
        writer = ListWriter()
        job_info = JobInfo(-1, 'test_user', '1', '1')
        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z13u_rec_key', 'em_create_dw_prcsng_cycle_id']
        data_quality_processor = DataQualityProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)
        data_quality_processor.execute()
        bib_rec_dq_results = data_quality_processor.writer.list

        # do the transformation process using the bib_rec_dq_results
        reader = ListReader(bib_rec_dq_results)
        writer = ListWriter()

        job_info = job_info = JobInfo(-1, 'test_user', '1', '1')

        pk_list = ['db_operation_cd', 'dw_stg_2_aleph_lbry_name',
                   'in_z00_doc_number', 'em_create_dw_prcsng_cycle_id']

        transformation_processor = TransformationProcessor(
            reader, writer, job_info, self.logger, self.bib_rec_sample_json_config, pk_list, self.error_writer)


        transformation_processor.execute()
        results = transformation_processor.writer.list

        expected_keys = sorted([
            'db_operation_cd', 'dw_stg_2_aleph_lbry_name', 'em_create_dw_prcsng_cycle_id',
            't1_z13u_user_defined_2__bib_rec_oclc_no', 't1_z13u_user_defined_3__bib_rec_marc_rec_leader_field_txt',
            't2_z13u_user_defined_3__bib_rec_type_cd', 't3_z13u_user_defined_3__bib_rec_type_desc',
            't4_z13u_user_defined_3__bib_rec_bib_lvl_cd', 't5_z13u_user_defined_3__bib_rec_bib_lvl_desc',
            't6_z13u_user_defined_3__bib_rec_encoding_lvl_cd', 't7_z13u_user_defined_3__bib_rec_encoding_lvl_desc',
            't1_z13u_user_defined_4__bib_rec_marc_rec_008_field_txt', 't2_z13u_user_defined_4__bib_rec_language_cd',
            't1_z13u_user_defined_5__bib_rec_issn', 't1_z13u_user_defined_6__bib_rec_display_suppressed_flag',
            't2_z13u_user_defined_6__bib_rec_acquisition_created_flag',
            't3_z13u_user_defined_6__bib_rec_circulation_created_flag',
            't4_z13u_user_defined_6__bib_rec_provisional_status_flag',
            'em_update_dw_prcsng_cycle_id', 'em_update_user_id',
            'em_update_dw_job_exectn_id', 'em_update_dw_job_version_no',
            'em_update_dw_job_name', 'em_update_tmstmp'
        ])

        # make sure expected keys are in the results for an item
        self.assertEqual(expected_keys, sorted(list(results[0].keys())))
        self.assertEqual('TransformationProcessor', results[0]['em_update_dw_job_name'])

        # check each transformation for items in results
        # first item
        self.assertEqual('00001605', results[0]['t1_z13u_user_defined_2__bib_rec_oclc_no'])
        # TODO: ask david if these are right expected results for user defined 3
        self.assertEqual('^^^^^nam^^2200241d1^45^0', results[0]['t1_z13u_user_defined_3__bib_rec_marc_rec_leader_field_txt'])
        self.assertEqual('a', results[0]['t2_z13u_user_defined_3__bib_rec_type_cd'])
        self.assertEqual('Language material', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        self.assertEqual('m', results[0]['t4_z13u_user_defined_3__bib_rec_bib_lvl_cd'])
        self.assertEqual('Monograph/Item', results[0]['t5_z13u_user_defined_3__bib_rec_bib_lvl_desc'])
        self.assertEqual('d', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        self.assertEqual('Invalid', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])


        # 
        # self.assertEqual('^', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Full-level by authorized national bibliographic agencies and libraries participating in PCC (BIBCO and CONSER).', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('1', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Full-level, material not examined.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('2', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Less-than-full level, material not examined.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('3', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Abbreviated level.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('4', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Core-level.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('5', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Partial (preliminary) level.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('7', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Minimal-level.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('8', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Prepublication level.', results[0]['t7_z13u_user_defined_3__bib_rec_encoding_lvl_desc'])
        # self.assertEqual('I', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Full-level input by OCLC participants.', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # self.assertEqual('K', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Minimal-level input by OCLC participants.', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # self.assertEqual('L', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Added from a batch process.', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # self.assertEqual('M', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Added from a batch process.', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # self.assertEqual('J', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Deleted record.', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # self.assertEqual('u', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Unknown', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # self.assertEqual('z', results[0]['t6_z13u_user_defined_3__bib_rec_encoding_lvl_cd'])
        # self.assertEqual('Not applicable', results[0]['t3_z13u_user_defined_3__bib_rec_type_desc'])
        # t3_z13u_user_defined_3__bib_rec_bib_lvl_cd
        # t4_z13u_user_defined_3__bib_rec_encoding_lvl_cd
        #
        #
        # t1_z13u_user_defined_4__bib_rec_marc_rec_008_field_txt
        # t2_z13u_user_defined_4__bib_rec_language_cd
        #
        # t1_z13u_user_defined_5__bib_rec_issn
        #
        # t1_z13u_user_defined_6__bib_rec_display_suppressed_flag
        # t2_z13u_user_defined_6__bib_rec_acquisition_created_flag
        # t3_z13u_user_defined_6__bib_rec_circulation_created_flag
        # t4_z13u_user_defined_6__bib_rec_provisional_status_flag
        #
        # self.assertEqual('', results[2]['t1_z00_data__bib_rec_marc_rec_data_cntnt_txt'])
        # self.assertEqual('001970',results[2]['t1_z00_data_len__bib_rec_marc_rec_data_cntnt_len_cnt'] )
        # self.assertEqual('000053939', results[2]['t1_z00_doc_number__bib_rec_source_system_id'])
        #
        # # fourth index sample data item tests z13_open_date date format
        # self.assertEqual(None, results[3]['t1_z13_open_date__bib_rec_create_dt'])
        # self.assertEqual(None, results[4]['t1_z13_open_date__bib_rec_create_dt'])
