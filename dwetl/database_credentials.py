import os
from dotenv import load_dotenv
load_dotenv()

'''
database credentials
'''

# The username to use in connecting to the database
DB_USER = os.getenv("DB_USER")
# The password to use in connecting to the database
DB_PASSWORD = os.getenv("DB_PASSWORD")
# The name of the database
DB_NAME = os.getenv("DB_NAME") or 'usmai_dw_etl'
# The hostname/IP address of the Postgres server
DB_HOST_NAME = os.getenv("DB_HOST_NAME") or '127.0.0.1'
# The port to use to connect to the Postgres server
DB_PORT= os.getenv("DB_PORT") or '5432'

DB_CONNECTION_STRING = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST_NAME}:{DB_PORT}/{DB_NAME}'
