"""
This sample data is for DataQualityProcessor and TransformationProcessor
"""

bib_rec_sample_data = [

    # z00_doc_number missing value
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "pp_z00_data": "",
        "pp_z00_data_len": "001970",
        "pp_z00_doc_number": "",
        "pp_z00_no_lines": "0049",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },
    # z00_doc_number short length
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "pp_z00_data": "",
        "pp_z00_data_len": "001970",
        "pp_z00_doc_number": "000053",
        "pp_z00_no_lines": "0049",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    },
    # z00_doc_number GOOD record
    {
        "db_operation_cd": "U",
        "dw_stg_2_aleph_lbry_name": "mai01",
        "em_update_dw_job_name": "Preprocessing",
        "pp_z00_data": "",
        "pp_z00_data_len": "001970",
        "pp_z00_doc_number": "000053939",
        "pp_z00_no_lines": "0049",
        "rm_dq_check_excptn_cnt": 0,
        "rm_suspend_rec_flag": "N",
        "rm_suspend_rec_reason_cd": None,
    }

    
]





