Detailed information
# Information about the steps of dwetl project

## Data Quality check

For data quality check step, we first refer to the spreadsheet named 'LIBRARY ITEM Star Schema Specifications' to find the tables which require data quality check. This information is in column 'DQ Required?'. For tables that require DQ, we can then go to the 'Data Quality Checks' spreadsheet, and find the quality checks corresponding to the certain column in certain tables.
We can also find the data quality checks for the columns in the library_item_dimension.json file which is located under the table_config folder.



**data quality story:**

z00_doc_number

1) `pp_z00_doc_number` value is used  

2) DQ check list is found

3) Each DQ is turned into a DQ_Info

4) First DQ check happens, (no_missing), returns True

​	- DQ_ value is the pp_value

5) Second DQ check happens (), returns True

- DQ_value is last DQ value

6) 

