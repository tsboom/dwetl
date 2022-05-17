## Docker Postgres Setup

* Install Docker v19.03.1 or later.
* Download a database dump file

1) Use Docker to run a Postgres container for the local etl db and the local test etl db:

```
docker run --rm --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:11
```

```
docker run --rm --name postgrestest -p 5439:5432 -e POSTGRES_PASSWORD=postgres postgres:11
```

2) Connect to the Docker container using a bash shell:

Open a shell of the postgres container at port 5432
```
docker exec -it postgres /bin/bash
```

In another window, open a shell of the postgrestest container at port 5439

```
docker exec -it postgrestest /bin/bash
```
3) In the Docker container for both postgres and postgrestest, create a "usmai_dw" user:

```
docker> su - postgres
docker> createuser usmai_dw
docker> mkdir pgdata
docker> chown -R postgres:root pgdata
```

4) In the both docker containers, run "psql":

```
docker> psql -U postgres
```

5) In psql for postgres and postgrestest, create the "usmai_dw_etl" and "usmai_dw_etl_test" databases, and exit:

```
postgres=# CREATE TABLESPACE usmai_dw location '/var/lib/postgresql/pgdata';
postgres=# CREATE DATABASE usmai_dw_etl OWNER usmai_dw TABLESPACE usmai_dw;
postgres=# <Ctrl-D>
```
```
postgres=# CREATE TABLESPACE usmai_dw location '/var/lib/postgresql/pgdata';
postgres=# CREATE DATABASE usmai_dw_etl_test OWNER usmai_dw TABLESPACE usmai_dw;;
postgres=# <Ctrl-D>
```

**Notes:** 

The docker container running postgres terminal shell must be kept open for the DWETL databases to be running. Keep note of the ports used to include that information in your `.env` configuration. 

If you want to use the dw-db-test.lib.umd.edu databases locally for testing, you can use an SSH tunnel from your local machine to the VM databases if your IP address is added to whitelist in the `pg_hba.conf` of the dw-db postgres instance. 

Example SSH tunnel command: 

`ssh -L 3333:dw-db-test.lib.umd.edu:5432 thschone@dw-db-test.lib.umd.edu`



## Reset the database and test database from invoke

1) Check your `.env` file to make sure your test database and database credentials are correct. 
2) Type `invoke --list` to see list of tasks available
3) Type `invoke database-reset` to reset the configured etl database using the ddl/usmai_dw_etl.sql file. 
4) Type `invoke test-database-reset` to reset the configured test etl database using the ddl_test.sql file. 


## Populate database manually from a dump

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
