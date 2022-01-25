# Database Setup

## Introduction

This document describes how to setup and configure the a database for
use by the application. For information about programmatically accessing
the database, see [Database Usage](database_usage.md).
 
There are two ways to setup the database for use in development:

* [Docker Postgres container](database_setup_docker_postgres.md)
* [Local Postgres installation](database_setup_local_postgres.md)

For the reporting databse (used for looking up data), an SSH tunnel to dw-db-test is used during development. 

The `.env` file, in conjunction with the `config/database_credentials.py` file,
provides the database connection information.

The configuration provides for an "application" database and a "test" database.
The "application" database is used when actually running the application. The
"test" database is used by unit/integration tests that require a database
connection.

In development, the same database can be used for both "application" and "test"
as the tests are designed to rollback any changes on completion.

In production, only the "application" database settings should be configured.

## Setting up a clean database

The DDL for the entire database is located in the "ddl" directory and named
"usmai_dw_etl.sql".

The DDL in the "usmai_dw_etl.sql" file was originally generated using the following
command:

```
> pg_dump -U postgres -h localhost -p 5432 usmai_dw_etl -Fp --create --clean --schema-only -f Development/usmai_dw_etl.sql
```

The "usmai_dw_etl.sql" file should be updated whenever there is a change to the
database schema.

There is also a "usmai_dw_etl_test.sql" file used to generate the test database. This was copied from "usmai_dw_etl.sql".

To recreate the database from the "usmai_dw_etl.sql",  run the following
command:

**Note:** This command will DESTROY the existing db and create a new empty
"usmai_dw_etl" database.

```
> invoke database-reset
```

To 

### Database Migrations 

This section describe how `dwetl/ddl/migrations` files were used early on to track changes to the database. We don't use it now and instead are tracking changes to usmai_dw_etl.sql and usmai_dw_etl_test.sql the ddl file using git. 

To set up the etl database with all tables and fields from pgcommondev, but no data. In the dwetl/ddl directory there are postgres dump files for generating the clean database. The first file was generated from pgcommondev using the following command:

```
> pg_dump -U usmai_dw -h pgcommondev.lib.umd.edu -p 5439 usmai_dw_etl -Fp --schema-only -f /tmp/00001_usmai_dw_etl.sql
```

The files in the ddl directory should all be run in numeric order.

1) To load a particular ddl file using psql, run the following command:

```
> psql -d usmai_dw_etl -f <DDL_FILENAME>.sql
```

Where DDL_FILENAME is the name of the file in dwetl/ddl that you want to load.

For example, if the name of the file is "00002_execution_metadata_tables.sql", the command would be:

```
> psql -d usmai_dw_etl -f 00002_execution_metadata_tables.sql
```

## Obtaining a Database Dump

The "Local Postgres" and "Docker Postgres" setups require a database dump file to populate the data from pgcommondev.lib.umd.edu..  

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

## Using dw-db-test for development to look into the test reporting database. 


To connect to the reporting database running on dw-db-test.lib.umd.edu, it is recommended that an SSH tunnel be used so that you can work on this project from any IP address.

To start an SSH tunnel to port 3333, open a terminal window and type:

`ssh -L 3333:dw-db-test.lib.umd.edu:5432 thschone@dw-db-test.lib.umd.edu`

Enter your username and password and leave this tunnel open in your terminal window.

In the .env file the following properties can be used for the repoting database:

```
# The username to use in connecting to the database
REPORTING_DB_USER=usmai_dw
# The password to use in connecting to the database
REPORTING_DB_PASSWORD=<password>
# The name of the database
REPORTING_DB_NAME=usmai_dw_reporting
# The hostname/IP address of the Postgres server
#REPORTING_DB_HOST_NAME=dw-db-test.lib.umd.edu
REPORTING_DB_HOST_NAME=localhost
# The port to use to connect to the Postgres server
REPORTING_DB_PORT=3333
```

where <password> is the password for the "usmai_dw" Postgres user on dw-db-test.
