# Tasks

## Introduction

This document describes the tasks available via the "invoke" task runner.

## The "invoke" task runner

See [http://docs.pyinvoke.org/en/1.3/](http://docs.pyinvoke.org/en/1.3/) for
documentation on the "invoke" package.

To see the list of available tasks, run:

```
> invoke --list
```

To run a particular task, use:

```
> invoke <TASK_NAME>
```

where \<TASK_NAME> is the name of the task.


## Tasks

### database-reset

Drops the application database, and restores an empty database using the
"ddl/usmai_dw_etl.sql" file.

**Warning:** This task will DESTROY the existing database.

This task also terminates all active sessions to the database (this is
needed to actually drop the database).

### sheets-to-json

Generates the JSON files in the "table_config/" subdirectory from the Google
Sheets document.

This task will prompt for OAuth authorization, if needed.

### test-database-teset

Drops the test database, and restores an empty database using the
"ddl/usmai_dw_etl.sql" file.

**Note:** If, as is commonly the case in local development, the "application"
and "test" database are the same database, this command would also drop and
restore the application database.

This task also terminates all active sessions to the database (this is
needed to actually drop the database).

### run-migration

Runs a database migration from an sql file. 

Run the script using an argument which is the path to the sql file migration.

`invoke run-migration ddl/migration/{file_name}`

### update-db-ddl

Generates a new "ddl/usmai_dw_etl.sql" file from what is inside of usmai_dw_etl.sql. This task is done after database migrations are executed. 



