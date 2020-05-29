import os
import sys
from dotenv import load_dotenv
load_dotenv()


def db_settings():
    # The username to use in connecting to the database
    db_user = os.getenv("DB_USER")
    # The password to use in connecting to the database
    db_password = os.getenv("DB_PASSWORD")
    # The name of the database
    db_name = os.getenv("DB_NAME")
    # The hostname/IP address of the Postgres server
    db_host_name = os.getenv("DB_HOST_NAME")
    # The port to use to connect to the Postgres server
    db_port = os.getenv("DB_PORT")

    db_connection_string = None
    application_database_settings = None
    if db_user and db_password and db_host_name and db_port and db_name:
        application_database_settings = {
            'DB_USER': db_user,
            'DB_PASSWORD': db_password,
            'DB_NAME': db_name,
            'DB_HOST_NAME': db_host_name,
            'DB_PORT': db_port,
            'DB_CONNECTION_STRING': f'postgresql+psycopg2://{db_user}:{db_password}@{db_host_name}:{db_port}/{db_name}'
        }
    else:
        print("ERROR. Application database has not been configured. Exiting.")
        sys.exit(1)

    return application_database_settings

def test_db_settings():
    # The username to use in connecting to the database
    test_db_user = os.getenv("TEST_DB_USER")
    # The password to use in connecting to the database
    test_db_password = os.getenv("TEST_DB_PASSWORD")
    # The name of the database
    test_db_name = os.getenv("TEST_DB_NAME")
    # The hostname/IP address of the Postgres server
    test_db_host_name = os.getenv("TEST_DB_HOST_NAME")
    # The port to use to connect to the Postgres server
    test_db_port = os.getenv("TEST_DB_PORT")

    test_database_settings = None
    if test_db_user and test_db_password and test_db_host_name and test_db_port and test_db_name:
        test_database_settings = {
            'TEST_DB_USER': test_db_user,
            'TEST_DB_PASSWORD': test_db_password,
            'TEST_DB_NAME': test_db_name,
            'TEST_DB_HOST_NAME': test_db_host_name,
            'TEST_DB_PORT': test_db_port,
            'TEST_DB_CONNECTION_STRING':
                f'postgresql+psycopg2://{test_db_user}:{test_db_password}@{test_db_host_name}:{test_db_port}/{test_db_name}'
        }
    return test_database_settings


def reporting_db_settings():
    # The username to use in connecting to the database
    reporting_db_user = os.getenv("REPORTING_DB_USER")
    # The password to use in connecting to the database
    reporting_db_password = os.getenv("REPORTING_DB_PASSWORD")
    # The name of the database
    reporting_db_name = os.getenv("REPORTING_DB_NAME")
    # The hostname/IP address of the Postgres server
    reporting_db_host_name = os.getenv("REPORTING_DB_HOST_NAME")
    # The port to use to connect to the Postgres server
    reporting_db_port = os.getenv("REPORTING_DB_PORT")

    reporting_database_settings = None
    if reporting_db_user and reporting_db_password and reporting_db_host_name and reporting_db_port and reporting_db_name:
        reporting_database_settings = {
            'REPORTING_DB_USER': reporting_db_user,
            'REPORTING_DB_PASSWORD': reporting_db_password,
            'REPORTING_DB_NAME': reporting_db_name,
            'REPORTING_DB_HOST_NAME': reporting_db_host_name,
            'REPORTING_DB_PORT': reporting_db_port,
            'REPORTING_DB_CONNECTION_STRING':
                f'postgresql+psycopg2://{reporting_db_user}:{reporting_db_password}@{reporting_db_host_name}:{reporting_db_port}/{reporting_db_name}'
        }
    return reporting_database_settings


def test_db_configured():
    if test_db_settings():
        return True
    return False
