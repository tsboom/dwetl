import os
import sys
from dotenv import load_dotenv
load_dotenv()

'''
Application Database Settings

Database settings for use when running the application.
'''
# The username to use in connecting to the database
DB_USER = os.getenv("DB_USER")
# The password to use in connecting to the database
DB_PASSWORD = os.getenv("DB_PASSWORD")
# The name of the database
DB_NAME = os.getenv("DB_NAME")
# The hostname/IP address of the Postgres server
DB_HOST_NAME = os.getenv("DB_HOST_NAME")
# The port to use to connect to the Postgres server
DB_PORT = os.getenv("DB_PORT")

DB_CONNECTION_STRING = None
if DB_USER and DB_PASSWORD and DB_HOST_NAME and DB_PORT and DB_NAME:
    DB_CONNECTION_STRING = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST_NAME}:{DB_PORT}/{DB_NAME}'

if not DB_CONNECTION_STRING:
    print("ERROR. Application database has not been configured. Exiting.")
    sys.exit(1)

'''
Test Database Settings

Database settings for use in conjunction with the tests.

Note: In production, these settings should probably not be set.
'''
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_HOST_NAME = os.getenv("TEST_DB_HOST_NAME")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")

TEST_DB_CONNECTION_STRING = None
if TEST_DB_USER and TEST_DB_PASSWORD and TEST_DB_NAME and TEST_DB_HOST_NAME and TEST_DB_PORT:
    TEST_DB_CONNECTION_STRING = f'postgresql+psycopg2://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_NAME}:{TEST_DB_HOST_NAME}/{TEST_DB_PORT}'

# Boolean used by tests requiring an actual database to determine whether the test database has been configured
if TEST_DB_CONNECTION_STRING:
    TEST_DB_CONFIGURED = True
else:
    TEST_DB_CONFIGURED = False
