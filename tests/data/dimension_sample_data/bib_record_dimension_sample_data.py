"""
This sample data is for DataQualityProcessor and TransformationProcessor
"""

bib_rec_sample_data = [

    # # 0. z00_doc_number missing value
    # {
    #     "db_operation_cd": "U",
    #     "dw_stg_2_aleph_lbry_name": "mai01",
    #     "em_update_dw_job_name": "Preprocessing",
    #     "in_z00_doc_number": "",
    #     "pp_z00_data": "",
    #     "pp_z00_data_len": "001970",
    #     "pp_z00_doc_number": "",
    #     "pp_z00_no_lines": "0049",
    #     "rm_dq_check_excptn_cnt": 0,
    #     "rm_suspend_rec_flag": "N",
    #     "rm_suspend_rec_reason_cd": None,
    # },
    # # 1. z00_doc_number short length
    # {
    #     "db_operation_cd": "U",
    #     "dw_stg_2_aleph_lbry_name": "mai01",
    #     "em_update_dw_job_name": "Preprocessing",
    #     "in_z00_doc_number": "000053",
    #     "pp_z00_data": "",
    #     "pp_z00_data_len": "001970",
    #     "pp_z00_doc_number": "000053",
    #     "pp_z00_no_lines": "0049",
    #     "rm_dq_check_excptn_cnt": 0,
    #     "rm_suspend_rec_flag": "N",
    #     "rm_suspend_rec_reason_cd": None,
    # },
    # # 2. z00_doc_number good record
    # {
    #     "db_operation_cd": "U",
    #     "dw_stg_2_aleph_lbry_name": "mai01",
    #     "em_update_dw_job_name": "Preprocessing",
    #     "in_z00_doc_number": "000053939",
    #     "pp_z00_data": "",
    #     "pp_z00_data_len": "001970",
    #     "pp_z00_doc_number": "000053939",
    #     "pp_z00_no_lines": "0049",
    #     "rm_dq_check_excptn_cnt": 0,
    #     "rm_suspend_rec_flag": "N",
    #     "rm_suspend_rec_reason_cd": None,
    # },
    # 
    # # 3. z13_open_date missing value
    # {
    #     "db_operation_cd": "U",
    #     "dw_stg_2_aleph_lbry_name": "mai01",
    #     "em_update_dw_job_name": "Preprocessing",
    #     "in_z13_rec_key": "000000897",
    #     "pp_z13_author": "Hoover, Dwight W., 1926-",
    #     "pp_z13_open_date": "",
    #     "pp_z13_title": "Understanding Negro history",
    #     "pp_z13_update_date" : "20130221",
    #     "pp_z13_year": "1969",
    #     "rm_dq_check_excptn_cnt": 0,
    #     "rm_suspend_rec_flag": "N",
    #     "rm_suspend_rec_reason_cd": None,
    # },
    # 
    # # 4. z13_open_date  date format error
    # {
    #     "db_operation_cd": "U",
    #     "dw_stg_2_aleph_lbry_name": "mai01",
    #     "em_update_dw_job_name": "Preprocessing",
    #     "in_z13_rec_key": "000000897",
    #     "pp_z13_author": "Hoover, Dwight W., 1926-",
    #     "pp_z13_open_date": "2099v9999",
    #     "pp_z13_title": "Understanding Negro history",
    #     "pp_z13_update_date" : "20130222",
    #     "pp_z13_year": "1969",
    #     "rm_dq_check_excptn_cnt": 0,
    #     "rm_suspend_rec_flag": "N",
    #     "rm_suspend_rec_reason_cd": None,
    # 
    # },
    # 
    # # 5. z13_open_date good record
    # {
    # 
    #     "db_operation_cd":  " U",
    #     "dw_stg_2_aleph_lbry_name": "mai01",
    #     "em_update_dw_job_name": "Preprocessing",
    #     "in_z13_rec_key": "000000897",
    #     "pp_z13_author": "Hoover, Dwight W., 1926-",
    #     "pp_z13_open_date": "20021124",
    #     "pp_z13_title": "Understanding Negro history",
    #     "pp_z13_update_date" : "20130223",
    #     "pp_z13_year": "1969",
    #     "rm_dq_check_excptn_cnt": 0,
    #     "rm_suspend_rec_flag": "N",
    #     "rm_suspend_rec_reason_cd": None ,
    # 
    # },
    # 6. z13u_user_defined_2 plain
    {

        "db_operation_cd":  "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "DataQualityProcessor",
        "in_z13u_rec_key": "004890837",
        "pp_z13u_rec_key": "004890837",
        "pp_z13u_user_defined_2": "", # empty user_defined 2
        "pp_z13u_user_defined_3": "^^^^^cam^^2200613Ia^45^0",
        "pp_z13u_user_defined_3_code": "LDR",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None ,

    },
    # 7. z13u_user_defined_2 test remove_ocm_ocn_on
    {

        "db_operation_cd":  "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "DataQualityProcessor",
        "in_z13u_rec_key": "004856341",
        "pp_z13u_rec_key": "004856341",
        "pp_z13u_user_defined_2": "ocm01870560", # transform function is to remove ocm, ocn, on
        "pp_z13u_user_defined_3": "^^^^^cam^a2200385I^^45^0",
        "pp_z13u_user_defined_3_code": "LDR",
        "pp_z13u_user_defined_4": "751202s1944^^^^nyu^^^^^^b^^^^000^0^eng^^",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None ,

    },
    # 8. z13u_user_defined_3 tests for transformations
        # BIB_REC_OCLC_NO
        # BIB_REC_MARC_REC_LEADER_FIELD_TXT
        # BIB_REC_TYPE_CD
        # BIB_REC_TYPE_DESC
        # BIB_REC_BIB_LVL_CD
        # BIB_REC_BIB_LVL_DESC
        # BIB_REC_ENCODING_LVL_CD
        # BIB_REC_ENCODING_LVL_DESC
    {
        "db_operation_cd":  "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "DataQualityProcessor",
        "in_z13u_rec_key": "002843482",
        "pp_z13u_rec_key": "002843482",
        "pp_z13u_user_defined_3": "00276pam^^2200121uu^45^0",
        "pp_z13u_user_defined_3_code": "LDR",
        "pp_z13u_user_defined_6" : "CIRC-CREATED || SUPPRESSED ||",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None ,

    },
    
    # 9. z13u_user_defined_4 test transformations 
        # BIB_REC_MARC_REC_008_FIELD_TXT
        # BIB_REC_LANGUAGE_CD
    {

        "db_operation_cd":  "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "DataQualityProcessor",
        "in_z13u_rec_key": "004856341",
        "pp_z13u_rec_key": "004856341",
        "pp_z13u_user_defined_2": "ocm01870560",
        "pp_z13u_user_defined_3": "^^^^^cam^a2200385I^^45^0",
        "pp_z13u_user_defined_3_code": "LDR",
        "pp_z13u_user_defined_4": "751202s1944^^^^nyu^^^^^^b^^^^000^0^eng^^",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None ,
    },
    # 10. z13u_user_defined_6 test
        # BIB_REC_DISPLAY_SUPPRESSED_FLAG
        # BIB_REC_ACQUISITION_CREATED_FLAG
        # BIB_REC_CIRCULATION_CREATED_FLAG
        # BIB_REC_PROVISIONAL_STATUS_FLAG
    {
        "db_operation_cd":  "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "DataQualityProcessor",
        "in_z13u_rec_key": "002843482",
        "pp_z13u_rec_key": "002843482",
        "pp_z13u_user_defined_3": "00276pam^^2200121uu^45^0",
        "pp_z13u_user_defined_3_code": "LDR",
        "pp_z13u_user_defined_6" : "CIRC-CREATED || SUPPRESSED ||",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None ,

    },

]
