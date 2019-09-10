
# DW ETL

Dwetl is a python program which handles the Extract Transform and Load of incremental data from Aleph tables into the UMD CLAS Data Warehouse used for reporting.

This application reads several TSV files representing different tables in Aleph, and combines this data into  data warehouse dimensions after data is processed and organized in a different granularity.


## Getting Started

Prerequisites: Python 3, pip, virtualenv

Start by cloning the repo and unzipping it into your /apps/git folder.

`cd dwetl`

Create a virtualenv called venv.

`virtualenv venv`

Enter your virtual environment

`source venv/bin/activate`

Download the requirements

`pip install -r requirements.txt`

Setup the database. See (Database Setup)[docs/database_setup.md] in docs.



## Running the application

To run the entire ETL process, use  `python dw_etl.py` from inside of your dwetl directory.

### Project overview

These steps correlate with (Alex's high level ETL diagram)[https://drive.google.com/drive/folders/1z2UkgnvhqQJioESxjUPkUpInaKnBoo3t], and also with the dwetl program. They will need to be refined some more, as Tiffany typed these up from some old notes, but they might be missing details.


- **Step 1**. Read tab-separated files into a file-equivalent (Stage 1) table in pgcommon dev.

  - *loadstg1.py*
- **Step 2.** Write fields and values from stg 1 into the "IN_" fields in stg 2 tables.

  - *loadstg2.py*
- **Step 3.** Populate Stage 2 tables with preprocessing, data quality checks, and transform results.
- *TransformField.py* - class to hold value of pp, dq, and transforms,
  - *table_transform.py*

  - Preprocess fields, write result to field object
    - Data quality checks on fields, write results of field object.
      - *data_quality_specific_functions.py*
      - *data_quality_utilities.py*
    - Transform field, write result to field object
      - *specific_transform_functions.py*
  - Write field values  to corresponding PP, DQ, and T1, T2, T3... rows and columns in the Stage 2 table.
- **Step 4. ** intertable processing on the Library Item Event Z35 stage 2 table. Make sure that the Library Item ID is unique and if so, add Last Loan, Last Renew, and Last Return details to the Library Item Z30 stage 2 table.
- **Step 5.** Grab final value of fields from Stage 2 tables and put into the Stg 3 Dimension tables.

  - Pay special attention to z13, z00, z13u because we might get an updated record for z00 but not z13 or z13u. Even though z13 and z13u are blank, they should not override the reporting databases's values with blank information.
- **Step 6** Assess processing readiness for Stage 3 tables
	- **6a**. If there's an "I" in stage 3, and the dimension's natural key already has that record, suspend if there is no sunsetted record with a matching key.
	- **6b.** If there is a "D" in stage 3, check to see if the key exists. If the effective-to date is less than today, the deleted key was re-added.
	- **6c**. If there is a "U" in stage 3, find the natural key in the Bib Dimension. Check the stg 3 value against the reporting database and see if the value has changed. Update flags after change checks are made. Find the active record and compare the Change_check_flag fields, set change detected to Yes.
	- **6d.** See if it's a Type 1 (change values all the way back) or a Type 2 change (set active flag to no, and active to date to the day before, set the active from date of the new record to the date of the extract.) Use type_1_chng_dtctd_flag, type_2_chng_dtctd_flag.
- **Step 7**. If U type 1 update: update every existing dimension record associated with that business key
- **Step 8.** If U type 2: sunset previous record, insert new dimension record
- **Step 8c**. Process deletes
- **Step 8d.** Process I and U field records. If getting I and U for dw_stg_3_bib_rec_field_outrigger, delete what is there and replace checks. If you don't find the bib_rec_id in fields, then sunset that record. After this step, all dimensions will be loaded and processed.
- **Step 9**. Intertable Fact Processing. Dw_stg_2_lbry_item_z30_full gets holding collection id, bib rec id. source lbry_item_holding_loc_collection_cd.
- **Step 10.** Create fact table using surrogate key from each dimension. The fact table links all dimensions together. Using natural keys, populate the fact table with surrogate keys.




## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

** Future ** Explain what these tests test and why

```
Give an example
​```
```


## Built With

* [SQLAlchemy](http://www.dropwizard.io/1.0.2/docs/) - The web framework used



## License


See the [LICENSE](LICENSE.md) file for license rights and limitations (Apache 2.0).
