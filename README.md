
# DW ETL

Dwetl is a python program which handles the Extract Transform and Load of incremental data from Aleph tables into the UMD CLAS Data Warehouse used for reporting.

This application reads several TSV files representing different tables in Aleph, and combines this data into  data warehouse dimensions after data is processed and organized in a different granularity.


## Getting Started

Prerequisites: Python 3.7, pip, virtualenv

Start by cloning the repo and unzipping it into your /apps/git directory, or wherever your UMD Libraries repos are stored on your local machine.

Go into the repo's root directory.

`cd dwetl`

Create a virtualenv called venv using Python 3.

`virtualenv venv`

Enter your virtual environment and check to see if `python --version` shows python 3.7.

`source venv/bin/activate`

Make sure your python version is Python 3.7. If it isn't, delete that venv directory and create a new one.

`python3 -m venv venv`


Make sure when you are inside your virtual environment `(venv)` should show up in your terminal on the left-hand side, and your python --version should be Python 3.

`pip install -r requirements.txt`

If you get an error about psycopg2, you will need to make sure you have postgresql installed.
You can do it with homebrew `brew install postgresql` and try installing the requirements again.

Copy the "env_example" file to ".env" and edit the .env file with your environment information:

`cp env_example .env`

Setup the database. See [Database Setup](docs/database_setup.md) in docs.

See [Database Usage](docs/database_usage.md) for information about
programmatically accessing to the database.

## "invoke" Task Runner

A number of administrative tasks are available using the "invoke" task runner.

`invoke database-reset` and `invoke test-database-reset` are often used to erase the databases during local development. Make sure that you do not accidentally delete real data from the production databases here by checking the `.env` configurations. 

See [Tasks](docs/tasks.md) for more information about the available tasks.

To see the list of available tasks, run:

```
> invoke --list
```

## Running the application

To run the entire Aleph tables and MPF files ETL process, use  `python dwetl.py` from inside of your dwetl directory. `dwetl.py` will try to run yesterday's date for Aleph processing. To configure data directory and database settings for the run of dwetl, modify the `.env` file per your local environment. 

EZProxy processing is run with `python ezproxy_etl.py`. 

DWETL.py and the tests depend on having an ETL database and ETL test database set up, and also need a connection to the reporting database in order to do lookups for some steps. 

To access the reporting database from your local environment, an SSH tunnel can be used if your local IP is added to the whitelist in postgres's `pg_hba.conf`. This tunnel must remain open in addition to your local databases for the etl, tests and lookups to work. Make sure to modify the `.env` file to use this SSH tunnel port. 

Example:

`ssh -L 3333:dw-db-test.lib.umd.edu:5432 thschone@dw-db-test.lib.umd.edu`

## DWETL Architecture overview

DWETL at the highest level is a Python application which reads a set of daily TSV files from an Integrated Library System, and processes the columns in each table according to a set of specifications in a Google Sheet to finally copy cleaned column data into a Data Warehouse. The original TSV files have columns that are checked for data quality errors, and are transformed into new formats and new column names. While most columns from the TSV files are moved as-is into their new columns, many columns need extra analysis and processing. The requirements for each column that is transformed are laid out in the DW - LIBRARY ITEM Star Schema Specifications  [Google Sheet](https://docs.google.com/spreadsheets/d/1QyEk0qAUjplpEXPQsAHHJ4avxOWqyJWkW6LIzxQB64Y/edit#gid=1813469208).

This sheet is converted into JSON format within `dwetl/table_config` for each dimension, and this JSON is referenced during the ETL process. The Data Warehouse CLAS uses is accessible in Jasperreports Server, which allows self-service report generation from the reporting database (usmai_dw_reporting). 

1. TSV tables are loaded into Stage 1 tables which are just all the original data put into columns in the database per table. Stage 1 tables are also called "File-equivalent tables", and serve the purpose of being a record of the data that was in the Aleph extract in database form so that it can be easily accessed and queried. 
2. Stage 1 tables are combined if needed and copied over to Stage 2 tables. 
3. Stage 2 tables are written to during the Preprocessing, Data Quality checks, and Transformation process. The final values are the Transformation values, which are then copied over to the Stage 3 dimension tables. 
3. Final values from the stage 3 tables are copied over to the reporting database. DWETL determines the current record based on looking things up in the reporting database. 



**Data sources**

DWETL processes three different kinds of data sources in TSV form. 

1. Aleph files
   - These files are large and have complex requirements. The majority of DWETL logic deals with these 
2. MPF files
   - These are manually maintained files within Aleph. Copies of these files are located in `dwetl/data` for development. 
3. EZ Proxy files
   - EzProxy TSVs are simple and are processed using `ezproxy_processor.py`, `ezp_fact_processor.py`, and `ezproxy_reporting_fact_processor.py` and run with `ezproxy_etl.py`. 

**Databases**

The production databases are on the dw-db VM. Test databases on the dw-db-test VM. Local development usually uses local docker instances of the etl and test databases.

- usmai_dw_etl 
  - stores data from the ETL process starting with stage 1 tables and ending in the dimension tables. 
- usmai_dw_etl_test
  - A copy of the usmai_dw_etl database for running tests. It is kept clean. 
- usmai_dw_reporting
  - This is the current data warehouse database that is used by Jasperreports Server. It is used for lookups during ETL to ensure the latest data is preserved, and older records are sunsetted. 

 See [Database Setup](docs/database_setup.md) in docs. 

### ETL steps detailed overview

Note: This is just another general overview of the ETL steps, but please do not use these as a complete specifications for the steps in ETL. For that, use the "Detail File Process Flow" from Lucid Chart, and the more detailed specifications documents provided by Alex in the USMAI Data Warehouse shared Google Drive.  CLAS Data Warehouse directory in Google Drive containing detailed specifications documentation: [Data Warehouse](https://drive.google.com/drive/folders/10DqR4S1fcY3Z81zK4ZsRZWGLP6z5I6fd?usp=sharing). (You must be in CLAS to see this.)

In `dwetl/docs/diagrams`, there is a helpful PDF ` USMAI Data Warehouse ETL Design (2019.02.28) - Detail File Process Flow.pdf` containing a detailed diagram showing all steps of ETL and the files and tables that are changing.


- **Step 1**. Read tab-separated files into a file-equivalent (Stage 1) table in pgcommon dev.
  - Configure `.env` file to use the etl database, reporting database, and test database credentials you need. Configure a temporary Docker container running Postgres to hold local databases if needed. See `docs/database_setup_docker_postgres.md`. 
  - Dwetl is configured to process last night's data from the Aleph extract. This will be different on the dw-etl VM from your local environment. Configure the `DATA_DIRECTORY` and `INPUT_DIRECTORY`to match the location where some test Aleph data is located. A set of aleph date directories are located in `dwetl/data/incoming` for testing if you do not want to download the latest data from Aleph into this directory. 
  - *load_stage_1.py* uses table_mappings.py as the list of tables to process and copy to stage 2 tables. If you want to process only certain tables, comment tables out of this file. 
- **Step 2.** Write fields and values from stg 1 into the "IN_" fields in stg 2 tables.

  - *load_stg_2.py*
- **Step 3.** Populate Stage 2 tables with preprocessing, data quality checks, and transform results.
  - Preprocess fields, write result to field object. The Preprocessing column headers start with `pp_`. 
  - Data quality checks on fields, write results of field object into `dq_` column headers. 
    - *data_quality_specific_functions.py* - contains column specific data quality checks. 
    - *data_quality_utilities.py*  - contains reusable data quality methods. 
  - Transform field, write result to field object into `t_`column headers. 
    - *specific_transform_functions.py* - contains column specific transform functions. 
  - Write field values  to corresponding PP, DQ, and T1, T2, T3... rows and columns in the Stage 2 table.
- **Step 4.** intertable processing on the Library Item Event Z35 stage 2 table. Make sure that the Library Item ID is unique and if so, add Last Loan, Last Renew, and Last Return details to the Library Item Z30 stage 2 table.
- **Step 5.** Grab final value of `t_` fields from Stage 2 tables and put into the Stg 3 Dimension tables.
- **Record Alignment** - Pay special attention to the z13, z00, z13u  record alignment because we might get an updated record for z00 but not z13 or z13u. Even though z13 and z13u are blank, they should not override the reporting databases's values with blank information. More instructions are laid out in a powerpoint and LIBILS-564. 
- **Step 6** Assess processing readiness for Stage 3 tables
  - **6a**. If there's an "I" in stage 3, and the dimension's natural key already has that record, suspend if there is no sunsetted record with a matching key.
  - **6b.** If there is a "D" in stage 3, check to see if the key exists. If the effective-to date is less than today, the deleted key was re-added.
  - **6c**. If there is a "U" in stage 3, find the natural key in the Bib Dimension. Check the stg 3 value against the reporting database and see if the value has changed. Update flags after change checks are made. Find the active record and compare the Change_check_flag fields, set change detected to Yes.
  - **6d.** See if it's a Type 1 (change values all the way back) or a Type 2 change (set active flag to no, and active to date to the day before, set the active from date of the new record to the date of the extract.) Use type_1_chng_dtctd_flag, type_2_chng_dtctd_flag.
- **Step 7**. If U type 1 update: update every existing dimension record associated with that business key
- **Step 8.** If U type 2: sunset previous record, insert new dimension record
- **Step 8c**. Process Deletes
- **Step 8d.** Process I and U field records. If getting I and U for dw_stg_3_bib_rec_field_outrigger, delete what is there and replace checks. If you don't find the bib_rec_id in fields, then sunset that record. After this step, all dimensions will be loaded and processed.
- **Step 9**. Intertable Fact Processing. Dw_stg_2_lbry_item_z30_full gets holding collection id, bib rec id. source lbry_item_holding_loc_collection_cd.
- **Step 10.** Create fact table using surrogate key from each dimension. The fact table links all dimensions together. Using natural keys, populate the fact table with surrogate keys.



## Data processing architecture: Readers, Processors, and Writers

A majority of the application is build around the idea of "readers", "processors", and "writers".

DWETL uses classes to reduce repeated logic during the ETL process. The primary data structure that is passed between stages is a Python dictionary of column names and values. 

### Readers

A reader provides data from some data source. It is expected to operate as a Python "generator" so that it can be used in a "for" loop.

In this application, a reader will typically provide a single Dictionary object for each line/row in the data source.

* Readers - `dwetl/dwetl/reader`
  - Ezproxy reader
  - list reader
  - mpf file reader
  - sql alchemy reader
  - tsv file reader
  - z00 field reader

### Processors

A processor converts data from the reader into data appropriate for the writer.

In this application, a processor will typically get a single Dictionary object from the reader for each line/row, and then modify that Dictionary object, and passing it to the writer.

A processor will typically operate on one row/line at a time, and iterate through all the rows/lines using a "for" loop.

Processors contain the 'meat' of the code that changes the data values in the ETL process. Unique data processing flows such as the MPF files and Ezproxy files have their own processors. 

Processors - `dwetl/dwetl/processor`

- Superclass: `processor.py`
- copy_stage_1_to_stage2.py
- data_quality_processor.py
- ezproxy_fact_processor.py
- ezproxy_reporting_fact_processor.py
- load_aleph_tsv.py
- load_mpf_tsv.py
- load_z00_field_tsv.py
- preprocess.py
- transformation_processor.py

### Writers

A writer sends data to some output.

In this application, a writer will typically receive a single Dictionary object for each line/row in the data source. When used with SQLAlchemy, the Dictionary object is equivalent to the row in the database table being written to.

A commonly used writer is "SqlAlchemyWriter", which writes the data to a
particular database table.

The "ListWriter" is commonly used for unit testing, in place of the
"SqlAlchemyWriter", to verify the output of a processor.

Writers - `dwetl/dwetl/writer`

- Superclass: `writer.py`

## Testing

Tests are located in the `dwetl/tests` directory. They are written in Unittest but Pytest will run them with better color output and features. 

Some tests require looking things up in the reporting database, or writing to the test database, so make sure these are configured correctly in `.env`. 

Tests also depend on test data within `dwetl/tests/data`

- dimension_sample_data
  - contains fake records for each dimension to test regular processing and special cases. 
- incoming_test
  - contains test data-directories copied over from the aleph extract incoming dates. More dates can be added here and processed for more realistic testing. 

#### Testing scopes

- Unit tests for DWETL loading steps are located in `dwetl/tests`. 
- Unit tests for each reader, writer, and processor are located in `tests` in `reader`, `writer`, and `processor`. These tests are quick and use dictionaries to imitate reading and processing rows from the ETL database. 
- An end-to-end DWETL test per dimension is done within `dwetl/tests` ie: `test_bib_rec_etl.py`.  These tests use the test database and write to the various stage tables. 

#####  Running the tests

`pytest` from the root directory to run all tests.
`pytest tests/{FILE_NAME}` to run tests from one file.
`pytest tests/{reader, writer, processor}/{FILE_NAME}` runs the tests for a Reader, Writer, or Processor. 



## Built With

* [SQLAlchemy](http://www.dropwizard.io/1.0.2/docs/) - The database ORM to read and write from the database. 
* PostgresQL
* Python



## License


See the [LICENSE](LICENSE.md) file for license rights and limitations (Apache 2.0).

