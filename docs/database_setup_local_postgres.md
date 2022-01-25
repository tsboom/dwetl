# Local Postgres Setup

* Install Postgres v11 or later
* Reset the database to create it with the right schema. 

The following assumes that a "postgres" user exists for communicating with Postgres (which should be the default when installing Postgres):

1) Log in to the Postgres using "psql":

```
psql -U postgres
```

2) In psql, create a "usmai_dw_etl" database and "usmai_dw" role. Do the same for an "usmai_dw_etl_test" database. Both databases can use port 5432. 

```
postgres=# CREATE ROLE usmai_dw;
postgres=# GRANT usmai_dw TO postgres;
postgres=# CREATE DATABASE usmai_dw_etl;
postgres=# CREATE DATABASE usmai_dw_etl_test;
postgres=# <Ctrl-D>
```

3) `If you want to use a database dump, restore the "usmai_dw_etl" database. 

```
pg_restore -d usmai_dw_etl -U postgres <DATABASE_DUMP_FILENAME>`
```
Note: You can also create an empty database  (see Database setup)[database_setup.md]

4) In the ".env" file the following properties can be used:

```
#Database settings

# The username to use in connecting to the database
DB_USER=postgres
# The password to use in connecting to the database
DB_PASSWORD=postgres
# The name of the database
DB_NAME=usmai_dw_etl
# The hostname/IP address of the Postgres server
DB_HOST_NAME=127.0.0.1
# The port to use to connect to the Postgres server
DB_PORT=5432


#Test database settings

#These settings are used for configuring the database used
#by the tests. They should NOT be set in a production
#environment.

# The username to use in connecting to the database
TEST_DB_USER=postgres
# The password to use in connecting to the database
TEST_DB_PASSWORD=postgres
# The name of the database
TEST_DB_NAME=usmai_dw_etl_test
# The hostname/IP address of the Postgres server
TEST_DB_HOST_NAME=127.0.0.1
# The port to use to connect to the Postgres server on port 5439 for test
TEST_DB_PORT=5432
```

5. To reset the dwetl and dwetl test databases. This will delete all of the data inside thesee databases. 
    `invoke database-reset`
    `invoke test-database-reset`


