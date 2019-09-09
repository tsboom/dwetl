
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

Setup the database. See "Database Setup".


## Database Setup

There are three ways to setup the database for use in development:
 
* Use the pgcommondev server
* Local Postgres installation
* Docker Postgres container

Each method uses the `config/database_credentials.py` file for configuration. Copy the "config/database_credentials_TEMPLATE.py" file to "config/database_credentials.py", and then edit the file as appropriate for the method you are using.

### Obtaining a Database Dump

The "Local Postgres" and "Docker Postgres" setups require a database dump file to populate the database.  Database dump files can be obtained from the pgcommondev.lib.umd.edu server:

1) Log in to the server:

2) Switch to the "/nfsdbbackup/pgsql" directory:

```
cd /nfsdbbackup/pgsql
```

3) Get a list of "dump-usmai_dw_etl" database dumps:

```
ls -ltr dump-usmai_dw_etl*
```

4) On your local workstation, use "scp" to copy the file:

```
scp <USERNAME>@pgcommondev.lib.umd.edu:/nfsdbbackup/pgsql/<DATABASE_DUMP_FILENAME> .
```

where \<USERNAME> is your username, and \<DATABASE_DUMP_FILENAME> is the name of the file to retrieve. For example, if your username is "jsmith" and the database dump file was named "dump-usmai_dw_etl9.custom.Tuesday-pm", the command would be:

```
scp jsmith@pgcommondev.lib.umd.edu:/nfsdbbackup/pgsql/dump-usmai_dw_etl9.custom.Tuesday-pm .
```

### pgcommondev Setup

**Note:** Changes made to the pgcommondev.lib.umd.edu server will be visible to all users of that server, so it is not recommended when doing local development that might result in destructive changes to the database.

To connect to Postgres running on pgcommondev, it is recommended that an SSH tunnel be used so that you can work on this project from any IP address.

To start an SSH tunnel to port 3333, open a terminal window and type:

`ssh -L 3333:pgcommondev.lib.umd.edu:5439 <your username>@pgcommondev.lib.umd.edu`

Enter your username and password and leave this tunnel open in your terminal window.

In the "config/database_credentials.py" file the following properties can be used:

```
DB_USER = 'usmai_dw'
DB_PASSWORD = '<USMAI_DW_USER_PASSWORD>'
DB_NAME = 'usmai_dw_etl'
DB_HOST_NAME= '127.0.0.1'
DB_PORT= '3333'
```

where \<USMAI_DW_USER_PASSWORD> is the password for the "usmai_dw" Postgres user.

### Local Postgres Setup

* Install Postgres v9.5.16 or later.
* Download a database dump file

The following assumes that a "postgres" user exists for communicating with Postgres (which should be the default when installing Postgres):

1) Log in to the Postgres using "psql":

```
psql -U postgres
```

2) In psql, create a "usmai_dw_etl" database and "usmai_dw" role:

```
postgres=# CREATE ROLE usmai_dw;
postgres=# GRANT usmai_dw TO postgres;
postgres=# CREATE DATABASE usmai_dw_etl;
postgres=# <Ctrl-D>
```

3) Using a database dump, restore the "usmai_dw_etl" database:

```
pg_restore -d usmai_dw_etl -U postgres <DATABASE_DUMP_FILENAME>
```

4) In the "config/database_credentials.py" file the following properties can be used:

```
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'usmai_dw_etl'
DB_HOST_NAME= '127.0.0.1'
DB_PORT= '5432'
```

### Docker Postgres Setup

* Install Docker v19.03.1 or later.
* Download a database dump file

1) Use Docker to run a Postgres container:

```
docker run --rm --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:9.6
```

2) Connect to the Docker container using a bash shell:

```
docker exec -it postgres /bin/bash
```

3) In the Docker container, create a "usmai_dw" user:

```
docker> su - postgres
docker> createuser usmai_dw
```

4) In the Docker container, run "psql":

```
docker> psql -U postgres
```

5) In psql, create the "usmai_dw_etl" database, and exit:

```
postgres=# CREATE DATABASE usmai_dw_etl;
postgres=# CREATE ROLE usami_dw;
postgres=# <Ctrl-D>
```

6) In a separate (non-Docker) terminal, use "docker cp" to copy the database dump file into the "/tmp" directory of the "postgres" container:

```
docker cp <DATABASE_DUMP_FILENAME> postgres:/tmp
```

where \<DATABASE_DUMP_FILENAME> is the name of the database dump. For example, if the name of the database dump is "dump-usmai_dw_etl9.custom.Tuesday-pm", the command would be:

```
docker cp dump-usmai_dw_etl9.custom.Tuesday-pm postgres:/tmp
```

7) In the Docker container, switch to the "/tmp" directory and and restore the dump:

```
docker> cd /tmp
docker> pg_restore -d usmai_dw_etl -U postgres <DATABASE_DUMP_FILENAME>
```

where \<DATABASE_DUMP_FILENAME> is the name of the database dump. For example, if the  database dump file was named "dump-usmai_dw_etl9.custom.Tuesday-pm", the command would be:

```
docker> pg_restore -d usmai_dw_etl -U postgres dump-usmai_dw_etl9.custom.Tuesday-pm
```

8) In the "config/database_credentials.py" file the following properties can be used:

```
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'usmai_dw_etl'
DB_HOST_NAME= '127.0.0.1'
DB_PORT= '5432'
```

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


### Project structure
```
dwetl/

├── logs
│   ├── dwetl.log
│   ├── sqlalchemy.engine.log
├── lookup_tables
│   ├── bibliographic_level.csv
│   ├── call_no_type.csv
│   ├── encoding_level.csv
│   ├── holding_own_code.csv
│   └── record_type_code.csv
├── scripts
│   ├── credentials.json
│   ├── sheetstojson.py
│   └── token_dw.json
├── table_config
│   ├── bibliographic_record_dimension.json
│   └── library_item_dimension.json
├── tests
│   ├── data
│   ├── test_database.py
│   ├── test_dataquality.py
│   ├── test_table_transform.py
│   └── test_tsv.py
└── __init__.py
├── LICENSE.md
├── README.md
├── requirements.txt
├── TransformField.py
├── table_transform.py
├── data_quality_specific_functions.py
├── data_quality_utilities.py
├── database_credentials.py
├── database_tables.py
├── dwetl.log
├── exceptions.py
├── loadstg1.py
├── loadstg2.py
├── specific_transform_functions.py
└── dw_etl.py
```


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
