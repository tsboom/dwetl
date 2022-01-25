# Database Usage

## Introduction

This document provides information about programmatically accessing the
database.

For information about setting up the database, see
[Database Setup](database_setup.md)

## Context Managers

As recommended in the [SQL Alchemy documentation](https://docs.sqlalchemy.org/en/13/orm/session_basics.html)
(see the "When do I construct a Session, when do I commit it, and when do I close
it?" section) database access is performed within a Python "context manager".

There are two context manager functions in the "dwetl/__init.py___" file for
accessing the database:

* dwetl.database_session
* dwetl.test_database_session

The "dwetl.database_session" is used by the application when the changes should
actually be stored in the database. All changes made within the session are
committed, unless an exception is raised, in which case all the changes are
rolled back.

The "dwetl.test_database_session" is used by unit/integration tests. Any changes
made within the session are automatically rolled back when the session exits.

Both the "dwetl .database_session" and "dwetl.test_database_session" are used
in the same way:

```
import dwetl

...

with dwetl.database_session() as session:
  # Do database access
```

When writing a record to the database, an explicit "session.commit()" should
_not_ be used.

