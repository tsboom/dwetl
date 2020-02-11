"""
This sample data is for DataQualityProcessor and TransformationProcessor
"""

bib_rec_sample_data = [

    # # z00_doc_number missing value
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
    # # z00_doc_number short length
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
    # # z00_doc_number good record
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

  # z13_doc_number missing value
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

    # z13_doc_number date format error
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

    # z13_doc_number good record
    {

        "db_operation_cd": "U",
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
        "rm_suspend_rec_reason_cd": None,

    }

]
