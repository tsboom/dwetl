from invoke import task, exceptions
import dwetl.database_credentials

@task
def sheets_to_json(c):
    """
    Generates the JSON files in the table_config/ subdirectory from Google Sheets.
    """
    c.run('cd scripts; python sheetstojson.py', pty=True)

@task
def database_reset(c):
    """
    Resets the application database. WARNING: This will DESTORY any existing data in the database.
    """
    db_settings = dwetl.database_credentials.db_settings()
    db_user = db_settings['DB_USER']
    db_host = db_settings['DB_HOST_NAME']
    db_port = db_settings['DB_PORT']
    db_password = db_settings['DB_PASSWORD']
    reset_database(c, db_host, db_port, db_user, db_password)

@task
def test_database_reset(c):
    """
    Resets the test database.

    WARNING: This task will DESTROY any existing data in the test
    database.
    """
    test_db_settings = dwetl.database_credentials.test_db_settings()
    test_db_user = test_db_settings['TEST_DB_USER']
    test_db_host = test_db_settings['TEST_DB_HOST_NAME']
    test_db_port = test_db_settings['TEST_DB_PORT']
    test_db_password = test_db_settings['TEST_DB_PASSWORD']
    reset_database(c, test_db_host, test_db_port, test_db_user, test_db_password)


# Task helper function
def reset_database(context, db_host, db_port, db_user, db_password):
    pg_password=f'PGPASSWORD={db_password} '
    psql_cmd = f'psql -U {db_user} -d postgres --host={db_host} --port={db_port}'

    ask_for_confirmation = True
    if (db_host == 'localhost' or db_host == '127.0.0.1') and db_port == '5432':
        # Assume localhost:5432 and 127.0.0.1:5432 are local Postgres
        ask_for_confirmation = False

    if ask_for_confirmation:
        confirm = input(f"Are you sure you want to reset {db_host}:{db_port}? ")
        confirm = confirm.lower()
        if not((confirm == 'y') or (confirm == 'yes')):
            print("Database has not been reset.")
            exit()

    print(f'Resetting database at {db_host}:{db_port}')
    print('-----------')
    print('Terminating sessions and dropping database')
    terminate_sessions = psql_cmd + ' -f ddl/drop_db.sql'
    print('\t' + terminate_sessions)

    if context.run(pg_password + terminate_sessions):
        print('-----------')
        print('Sessions terminated')
    else:
        raise Exception()
        print('An error has occurred')

    print('Creating database from DDL')
    load_ddl = psql_cmd + ' -f ddl/usmai_dw_etl.sql'
    print(load_ddl)
    if context.run(pg_password + load_ddl):
        print('-----------')
        print('Database reset')

