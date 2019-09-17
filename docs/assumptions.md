# Assumptions

## Introduction

This document keeps track of things we are assuming while developing the ETL. These might change but we need remember them. The steps refer to the nine step  [ETL Processing Data Flow Diagrams](https://drive.google.com/file/d/16BcITSFaCaLhXMs4epbEsvIyguZ5RZ1h/view?usp=sharing_eil&ts=5d6e62da).



Questions: 

- Is it okay to only use the DW_PRCSNG_CYCLE table?
- 



## Execution metadata

-  We are only using the DW_PRCSNG_CYCLE table
- Not populating dw_processing_cycle_job, or dw_prcsng_cycle_job_exectn tables because it is too complicated for the moment. Need to focus on getting ETL working first. 
- 



##Step1 - File Equivalent Table Load

- The ETL only keeps last night's TSV data in the Stage 1 tables

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