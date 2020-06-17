# Local Postgres Setup

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

3) If you want to use a database dump, restore the "usmai_dw_etl" database. 

```
pg_restore -d usmai_dw_etl -U postgres <DATABASE_DUMP_FILENAME>
```
Note: You can also create an empty database  (see Database setup)[database_setup.md]

4) In the ".env" file the following properties can be used:

```
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'usmai_dw_etl'
DB_HOST_NAME= '127.0.0.1'
DB_PORT= '5432'
```



