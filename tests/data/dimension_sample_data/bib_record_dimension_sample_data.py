"""
This sample data is for DataQualityProcessor
"""

bib_rec_sample_data_z00 = [

    # 0. z00_doc_number missing values
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z00_doc_number": "",
        "pp_z00_data": "",
        "pp_z00_data_len": "001970",
        "pp_z00_doc_number": "",
        "pp_z00_no_lines": "0049",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },
    # 1. z00_doc_number short length
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z00_doc_number": "000053",
        "pp_z00_data": "",
        "pp_z00_data_len": "001970",
        "pp_z00_doc_number": "000053",
        "pp_z00_no_lines": "0049",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },
    # 2. z00_doc_number good record
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z00_doc_number": "000053939",
        "pp_z00_data": "",
        "pp_z00_data_len": "001970",
        "pp_z00_doc_number": "000053939",
        "pp_z00_no_lines": "0049",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    }]

bib_rec_sample_data_z13 = [
    # 0. z13_open_date missing value
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13_rec_key": "000000897",
        "pp_z13_author": "Hoover, Dwight W., 1926-",
        "pp_z13_open_date": "",
        "pp_z13_title": "Understanding Negro history",
        "pp_z13_update_date" : "20130221",
        "pp_z13_year": "1969",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },

    # 1. z13_open_date date format error
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13_rec_key": "000000897",
        "pp_z13_author": "Hoover, Dwight W., 1926-",
        "pp_z13_open_date": "2099v9999",
        "pp_z13_title": "Understanding Negro history",
        "pp_z13_update_date" : "20130222",
        "pp_z13_year": "1969",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,

    },

    # 2. z13_open_date good record
    {

        "db_operation_cd":  " U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13_rec_key": "000000897",
        "pp_z13_author": "Hoover, Dwight W., 1926-",
        "pp_z13_open_date": "20021124",
        "pp_z13_title": "Understanding Negro history",
        "pp_z13_update_date" : "20130223",
        "pp_z13_year": "1969",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None ,

    }]
    
bib_rec_sample_data_z13u = [
    # 0. z13u normal record
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13u_rec_key": "000000897",
        "pp_z13u_user_defined_2": "ocm00001605",
        "pp_z13u_user_defined_3": "^^^^^nam^^2200241d1^45^0",
        "pp_z13u_user_defined_4": "690424s1969^^^^ilu^^^^^^b^^^^001^0^eng^^",
        "pp_z13u_user_defined_5": "0194-5947",
        "pp_z13u_user_defined_6":"",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },

    # 1. z13u pp_z13u_user_defined_2 contains wrong format ocm w 9 digits
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13u_rec_key": "000000897",
        "pp_z13u_user_defined_2": "ocm000016050",
        "pp_z13u_user_defined_3": "^^^^^nam^^2200241d1^45^0",
        "pp_z13u_user_defined_4": "690424s1969^^^^ilu^^^^^^b^^^^001^0^eng^^",
        "pp_z13u_user_defined_5": "0194-5947",
        "pp_z13u_user_defined_6": "",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },

    # 2. z13u pp_z13u_user_defined_2 is empty string
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13u_rec_key": "000000897",
        "pp_z13u_user_defined_2": "",
        "pp_z13u_user_defined_3": "^^^^^nam^^2200241d1^45^0",
        "pp_z13u_user_defined_4": "690424s1969^^^^ilu^^^^^^b^^^^001^0^eng^^",
        "pp_z13u_user_defined_5": "0194-5947",
        "pp_z13u_user_defined_6":"",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },
    # 3. z13u pp_z13u_user_defined_2 is None
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "in_z13u_rec_key": "000000897",
        "pp_z13u_user_defined_2": None,
        "pp_z13u_user_defined_3": "^^^^^nam^^2200241d1^45^0",
        "pp_z13u_user_defined_4": "690424s1969^^^^ilu^^^^^^b^^^^001^0^eng^^",
        "pp_z13u_user_defined_5": "0194-5947",
        "pp_z13u_user_defined_6":"",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    }]