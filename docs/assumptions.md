# Assumptions

## Introduction

This document keeps track of things we are assuming while developing the ETL. These might change but we need remember them. The steps refer to the nine step  [ETL Processing Data Flow Diagrams](https://drive.google.com/file/d/16BcITSFaCaLhXMs4epbEsvIyguZ5RZ1h/view?usp=sharing_eil&ts=5d6e62da).



Questions: 

- Do we have DDLs for every table in the DW? We could use them to generate a clean postgres db to test with. 


## TSV files

Extract files are located on dw_etl.lib.umd.edu in:
`/home/hans/incoming`

Manual extract files are located in alephprod: 

`/lims/22/dw/manual-files`





## Execution metadata

- Processing cycle - starting from beginning of ETL starts the cycle
  - if one step fails. start new processing cycle
  - if step 2 fails, restart step 2 with job execution +1 in the same cycle. 
  - status type code - Success, Fail
  - frequency type code - daily, DA, WE, Ni
- Where do we get DW Processing Cycle id? where to get job id?
  - Job execution id is figured out automatically by seeing what's already in the db
    - get ID, check if existing job execution ID is there and increment
- **JOB NAMES** 100 characters
  - Step 1. Load file equivalent tables. (load stg 1)
  - Step 2. Populate 'in_' values in stage 2 from stg 1(load stg 2)
  - Step 3. Intra-table processing
  - Step 4. Library item z35 and z30 stg 2 processing.* 
  - Step 5. Populate stg 3 tables. 
  - 

##Step1 - File Equivalent Table Load

- The ETL only keeps daily TSV data in the Stage 1 tables. Data is appended every night and DW Processing Cycle field is how we tell them apart. 

  

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

-  Do not do PP, DQ for Deletes. The row value (usually only the ID) is moved, but other fields are empty because nothing happens. 
- Data quality checking: 
  - When a DQ check fails, no other DQ checks are run
  - We aren't looking at the Order in the Sheet
  - 