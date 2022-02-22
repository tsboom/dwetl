Detailed information
# Information about the steps of dwetl project

## Data Quality checks

For data quality check step, we first refer to the spreadsheet named 'LIBRARY ITEM Star Schema Specifications' to find the tables which require data quality check. This information is in column 'DQ Required?'. For tables that require DQ, we can then go to the 'Data Quality Checks' spreadsheet, and find the quality checks corresponding to the certain column in certain tables.
We can also find the data quality checks for the columns in the library_item_dimension.json file which is located under the table_config folder.



**Data Quality story:**

z00_doc_number

1) `pp_z00_doc_number` value is used  

2) DQ check list is found

3) Each DQ is turned into a DQ_Info

4) First DQ check happens, (no_missing), returns True

- DQ_ value is the pp_value
- if False, 
    - Check to see if suspend record is Yes:
         - Suspend the record, and don't continue to the next check
              - rm_suspend_rec_flag = Y
              - rm_suspend_rec_reason_cd = 
     - If suspend record is NO:
          - replace failing value with a replacement value

5) Second DQ check happens (), returns True

- DQ_value is last DQ value
- if False,
  - Check to see if suspend record is Yes:
    - Suspend the record, and don't continue to the next check
  - If suspend record is NO:
    - replace failing value with a replacement value







## Questions

1. what should the  default valuue of chg_chk_flag be? Answer; N
2. Review record alignment check to handle blank z13s.
3. Why does dw_stg_2_dim_mbr_lbry feed into the next library entity and library item location tables?
4. 

