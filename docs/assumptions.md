# Assumptions

## Introduction

This document keeps track of things we are assuming while developing the ETL. These might change but we need remember them. The steps refer to the nine step  [ETL Processing Data Flow Diagrams](https://drive.google.com/file/d/16BcITSFaCaLhXMs4epbEsvIyguZ5RZ1h/view?usp=sharing_eil&ts=5d6e62da).



Questions: 

- mai50_z35_data has rec_trigger_key which is set to be 9 characters (like the rec_key), but the data files include rec_trigger_keys that are long numbers that look like timestamps. `2019091903453899997233`. For now we changed the character count to 22. 

- library-entity-dimension.txt, mpf_library-collection-dimension.txt are missing `usmai_mbr_lbry_cd` (2 characters)

- mpf_item-status-dimension.txt has an Integrity error.
  - ```DETAIL:  Key (db_operation_cd, usmai_mbr_lbry_cd, item_status_cd, em_create_dw_prcsng_cycle_id)=(I, BC, 38, 40) already exists.```
  - Seems like we can't use that combination of columns as the PK. Should we add effective_date into the key?
  
- item-process-status-dimension.txt has same kind of integrity error
  
  - ```DETAIL:  Key (db_operation_cd, usmai_mbr_lbry_cd, item_prcs_status_cd, em_create_dw_prcsng_cycle_id)=(U, CP, HT, 40) already exists.```
  
- material-form-dimension.txt `matrl_form_code` is 5 characters, not 2. We changed it in stage 1 but still need to make these changes across the rest of the tables. 

- mai01/39/60_z00_field_data files don't have headers or DB operation codes in them. We could manually add headers, but are not sure how to get the db operation codes. 

  - first column is rec_trigger_key and z00_doc_number
  - last column is field_txt
  - Ignore the L

  



## Execution metadata

-  We are only using the DW_PRCSNG_CYCLE table
- Not populating dw_processing_cycle_job, or dw_prcsng_cycle_job_exectn tables because it is too complicated for the moment. Need to focus on getting ETL working first. 
- 



##Step1 - File Equivalent Table Load

- The ETL only keeps last night's TSV data in the Stage 1 tables
- MPF files with no usmai_mbr_lbry_cd need 2 characters taken out of lbry_entity_cd
  - library_collection
  - library-entity-dimension.txt

## Step 2 - Copy File Stage 1 tables to DW Stage 2 Tables

- Right now we are only dealing with one night of data.
- This puts the Stg1 values into their corresponding 'IN_' values in Stg 2. 

## Step 3 - "Intra-table" Processing

- RM metadata:

  - rm_suspend_rec_flag
    - Y and N 
  - rm_suspend_rec_reason_cd
    - TBD what these codes are
  - rm_dq_check_exception_cnt
    - This count is the number of failed dq checks encountered before the record is suspended. 

- EM metadata:

  - em_create_dw_prcsng_cycle_id
  - em_create_dw_job_exectn_id
  - em_create_dw_job_name 
  - em_create_dw_job_version_no
  - em_create_user_id
  - em_create_tmstmp
  - em_update_dw_prcsng_cycle_id
  - em_update_dw_job_exectn_id
  - em_update_dw_job_name
  - em_update_dw_job_version_no
  - em_update_user_id
  - em_update_tmstmp

-  Do not do PP, DQ for Deletes
- Data quality checking: 
  - When a DQ check fails, no other DQ checks are run
  - We aren't looking at the Order in the Sheet
  - 