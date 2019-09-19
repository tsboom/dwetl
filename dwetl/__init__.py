from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
import dwetl.database_credentials as database_credentials
from contextlib import contextmanager

version = "1.0.0"

Base = None

@contextmanager
def database_session():
    """
    Returns a database session for application use.

    All changes made in the session will be committed, unless an exception is
    raised. If an exception is raised, all uncommitted changes will be rolled
    back.

    The database session will automatically commit the changes when the
    session exits, so no explicit commit is needed by the code.

    Sample Usage:

      with dwetl.database_session() as session:
         <Access datatabase>

    :return: a database session for application use.
    """
    global Base
    # See https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
    db_settings = database_credentials.db_settings()
    engine = create_engine(db_settings['DB_CONNECTION_STRING'])

    # Populate Base class, if needed.
    if Base is None:
        Base = automap_base()
        Base.prepare(engine, reflect=True)

    # connect to the database
    connection = engine.connect()

    # bind an individual Session to the connection
    s = sessionmaker()
    session = s(bind=connection)

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

@contextmanager
def test_database_session():
    """
    Returns a database session for use with testing.

    All changes made in the session will be rolled back when the session
    exits.

    Sample Usage:

      with dwetl.test_database_session() as session:
         <Access datatabase>

    :return: a database session for use with testing that always rolls back,
             removing the changes made in the session.
    """
    global Base
    # See https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
    test_db_settings = database_credentials.test_db_settings()
    engine = create_engine(test_db_settings['TEST_DB_CONNECTION_STRING'])

    # Populate Base class, if needed.
    if Base is None:
        Base = automap_base()
        Base.prepare(engine, reflect=True)

    # connect to the database
    connection = engine.connect()

    # begin a non-ORM transaction
    # Using a transactiom, so that we can rollback, even if there
    # are session.commit() calls
    trans = connection.begin()

    # bind an individual Session to the connection
    s = sessionmaker()
    session = s(bind=connection)

    try:
        # begin a non-ORM transaction
        yield session
        # Never commit as we are just testing
    except:
        session.rollback()
        raise
    finally:
        # Always rollback
        session.rollback()
        trans.rollback()
