# Database Setup

There are three ways to setup the database for use in development:

* Use the pgcommondev server
* [Docker Postgres container](database_setup_docker_postgres.md)
* [Local Postgres installation](database_setup_local_postgres.md)


Each method uses the `config/database_credentials.py` file for configuration. Copy the "config/database_credentials_TEMPLATE.py" file to "config/database_credentials.py", and then edit the file as appropriate for the method you are using.


## Setting up a clean database

 Set up the etl database with all tables and fields, but no data. In the dwetl/ddl directory there are postgres dump files for generating the clean database. The first file was generated from pgcommondev using the following command:

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

## Using pgcommondev for development

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



