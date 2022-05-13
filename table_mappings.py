
'''
table mapping for load_stage_1
'''

stg_1_table_mapping = {'ALEPH_TSV_TABLE_MAPPING':
        {
        # "mai01_z00_data": "dw_stg_1_mai01_z00",
        # "mai39_z00_data": "dw_stg_1_mai39_z00",
        # "mai01_z13_data": "dw_stg_1_mai01_z13",
        # "mai39_z13_data": "dw_stg_1_mai39_z13",
        # "mai01_z13u_data": "dw_stg_1_mai01_z13u",
        # "mai39_z13u_data": "dw_stg_1_mai39_z13u"

        # "mai60_z00_data": "dw_stg_1_mai60_z00",
        # "mai60_z13_data": "dw_stg_1_mai60_z13",
        # "mai60_z13u_data": "dw_stg_1_mai60_z13u",
        # "mai60_z103_bib_data": "dw_stg_1_mai50_z103_bib",
        # "mai50_z30_data": "dw_stg_1_mai50_z30",
        # "mai50_z35_data": "dw_stg_1_mai50_z35",
        # "mai50_z30_full_data": "dw_stg_1_mai50_z30_full",
        # "mai50_z103_bib_full_data": "dw_stg_2_lbry_item_z103_bib_full",
        # }
        # ,
        # 'Z00_FIELD_TABLE_MAPPING': {
        #     "mai01_z00_field_data": "dw_stg_1_mai01_z00_field",
        #     "mai39_z00_field_data": "dw_stg_1_mai39_z00_field",
        #     "mai60_z00_field_data": "dw_stg_1_mai60_z00_field",
        },
        'MPF_TABLE_MAPPING' : {
            "member-library-dimension.txt": "dw_stg_1_mpf_mbr_lbry",
            "library-entity-dimension.txt": "dw_stg_1_mpf_lbry_entity",
            "library-collection-dimension.txt": "dw_stg_1_mpf_collection",
            "item-status-dimension.txt": "dw_stg_1_mpf_item_status",
            "item-process-status-dimension.txt": "dw_stg_1_mpf_item_prcs_status",
            #"material-form-dimension.txt": "dw_stg_1_mpf_matrl_form"
        }
        }


'''
table mapping for load_stage_2
'''

stg_1_to_stg_2_table_mapping = {
    # "dw_stg_1_mai39_z13": "dw_stg_2_bib_rec_z13",
    # 'dw_stg_1_mai01_z13': "dw_stg_2_bib_rec_z13",
    # "dw_stg_1_mai01_z13u": "dw_stg_2_bib_rec_z13u",
    # "dw_stg_1_mai01_z00": "dw_stg_2_bib_rec_z00",
    # "dw_stg_1_mai39_z00": "dw_stg_2_bib_rec_z00",
    # "dw_stg_1_mai39_z13u": "dw_stg_2_bib_rec_z13u",

    # "dw_stg_1_mai60_z00": "dw_stg_2_lbry_holding_z00",
    # "dw_stg_1_mai60_z13": "dw_stg_2_lbry_holding_z13",
    # "dw_stg_1_mai60_z13u": "dw_stg_2_lbry_holding_z13u",
    # "dw_stg_1_mai50_z30": "dw_stg_2_lbry_item_z30",
    # "dw_stg_1_mai50_z35": "dw_stg_2_lbry_item_event_z35",
    # "dw_stg_1_mai01_z00_field": "dw_stg_2_bib_rec_z00_field",
    # "dw_stg_1_mai39_z00_field": "dw_stg_2_bib_rec_z00_field",
    # "dw_stg_1_mai60_z00_field": "dw_stg_2_lbry_holding_z00_field",
    "dw_stg_1_mpf_mbr_lbry": "dw_stg_2_mpf_mbr_lbry",
    "dw_stg_1_mpf_lbry_entity": "dw_stg_2_mpf_lbry_entity",
    "dw_stg_1_mpf_collection": "dw_stg_2_mpf_collection",
    "dw_stg_1_mpf_item_status": "dw_stg_2_mpf_item_status",
    "dw_stg_1_mpf_item_prcs_status": "dw_stg_2_mpf_item_prcs_status"
    #"dw_stg_1_mpf_matrl_form": "dw_stg_2_mpf_matrl_form"
}

'''
table mapping for stage 2 intertable processing into dimension tables
'''

stg_2_table_dim_mapping = {
        'dw_stg_2_bib_rec_z00': 'bibliographic_record_dimension',
        'dw_stg_2_bib_rec_z13': 'bibliographic_record_dimension',
        'dw_stg_2_bib_rec_z13u': 'bibliographic_record_dimension',
    }
