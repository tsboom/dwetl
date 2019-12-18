from dwetl.processor.copy_stage1_to_stage2 import CopyStage1ToStage2
from dwetl.reader.sql_alchemy_reader import SqlAlchemyReader
from dwetl.writer.sql_alchemy_writer import SqlAlchemyWriter
from dwetl.job_info import JobInfoFactory
import dwetl
import sys
import re
import pdb


def aleph_library(table_name):
    """
    Returns a string representing the Aleph library from the given table name

    :param table_name: the name of the table being processed
    :return: a string representing the Aleph library from the given table name
    """
    m = re.search('dw_stg_1_(.*?)_.*', table_name)
    library = m.group(1)

    if library == 'mpf':
        return None
    return library


def load_stage_2(job_info):

    print('Loading stage 2...')

    stage1_to_stage2_table_mappings = {
        "dw_stg_1_mai39_z13": "dw_stg_2_bib_rec_z13",
        'dw_stg_1_mai01_z13': "dw_stg_2_bib_rec_z13",
        "dw_stg_1_mai01_z13u": "dw_stg_2_bib_rec_z13u",
        "dw_stg_1_mai01_z00": "dw_stg_2_bib_rec_z00",
        "dw_stg_1_mai39_z00": "dw_stg_2_bib_rec_z00",
        "dw_stg_1_mai39_z13u": "dw_stg_2_bib_rec_z13u",
        # "dw_stg_1_mai60_z00": "dw_stg_2_lbry_holding_z00",
        # "dw_stg_1_mai60_z13": "dw_stg_2_lbry_holding_z13",
        # "dw_stg_1_mai60_z13u": "dw_stg_2_lbry_holding_z13u",
        # "dw_stg_1_mai50_z30": "dw_stg_2_lbry_item_z30",
        # "dw_stg_1_mai50_z35": "dw_stg_2_lbry_item_event_z35",
        # "dw_stg_1_mai01_z00_field": "dw_stg_2_bib_rec_z00_field",
        # "dw_stg_1_mai39_z00_field": "dw_stg_2_bib_rec_z00_field",
        # "dw_stg_1_mai60_z00_field": "dw_stg_2_lbry_holding_z00_field",
        # "dw_stg_1_mpf_mbr_lbry": "dw_stg_2_mpf_mbr_lbry",
        # "dw_stg_1_mpf_lbry_entity": "dw_stg_2_mpf_lbry_entity",
        # "dw_stg_1_mpf_collection": "dw_stg_2_mpf_collection",
        # "dw_stg_1_mpf_item_status": "dw_stg_2_mpf_item_status",
        # "dw_stg_1_mpf_item_prcs_status": "dw_stg_2_mpf_item_prcs_status",
        # "dw_stg_1_mpf_matrl_form": "dw_stg_2_mpf_matrl_form"
    }

    logger = None

    processing_cycle_id = job_info.prcsng_cycle_id
    for stage1_table, stage2_table in stage1_to_stage2_table_mappings.items():
        print(stage1_table)
        library = aleph_library(stage1_table)

        with dwetl.database_session() as session:
            stage1_table_class = dwetl.Base.classes[stage1_table]
            stage2_table_class = dwetl.Base.classes[stage2_table]
            reader = SqlAlchemyReader(session, stage1_table_class, 'em_create_dw_prcsng_cycle_id', processing_cycle_id)
            writer = SqlAlchemyWriter(session, stage2_table_class)
            processor = CopyStage1ToStage2.create(reader, writer, job_info, logger, library)
            processor.execute()

'''
main function for running script from the command line
'''
if __name__=='__main__':
    arguments = sys.argv

    if len(arguments) != 2:
        print('Usage: ')
        print('\tload_stage_2.py [prcsng_cycle_id]')
        sys.exit(1)

    prcsng_cycle_id = arguments[1]

    job_info = JobInfoFactory.create_from_prcsng_cycle_id(prcsng_cycle_id)
    load_stage_2(job_info)
