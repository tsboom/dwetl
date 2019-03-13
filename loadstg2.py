from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
import datetime
import pdb
import pprint
from colorama import init, Fore, Back, Style
init()
# import database_config
import database_credentials




'''
main function to load stg_2 table using nested functions
'''
def load_stg2_table(engine, bib_rec_stg1_tables, bib_rec_stg2_tables, dwetl_logger):

    # func to remove some keys from becoming 'in_val_' column names
    def without_keys(d, invalid_keys):
        return {x: d[x] for x in d if x not in invalid_keys}

    # temporary dict to hold job metadata for now
    em_dict = {
        'em_create_dw_prcsng_cycle_id': '1',
        'em_create_dw_job_name': 'load stg 2',
        'em_create_dw_job_version_no': '1.0',
        'em_create_dw_job_exectn_id': '1',
        'em_create_user_id': 'thschone',
        'em_create_tmstmp': datetime.datetime.now(),
        'em_update_dw_prcsng_cycle_id': '1',
        'em_update_dw_job_name': 'load stg 2 update',
        'em_update_dw_job_version_no': '1.0',
        'em_update_dw_job_exectn_id': '1',
        'em_update_tmstmp': datetime.datetime.now()
    }

    def build_stg2_row(em_dict, row_dict):
        # create stg2 row
        stg2_row = {}
        for key, val in row_dict.items():
            # add metadata
            stg2_row.update({'dw_stg_2_aleph_lbry_name': 'mai01'})
            stg2_row.update(em_dict)
            # add in val to everything but em metadata and db_operation_cd
            if key not in em_dict and key != 'db_operation_cd':
                stg2_row.update({'in_'+ key:row_dict[key]})
            else:
                stg2_row.update({key: row_dict[key]})
        return stg2_row

    def print_debug_colors(row_dict, stg2_row):
        print(Fore.RED + str(row_dict))
        print(Back.GREEN + str(stg2_row))
        print(Style.RESET_ALL)



    def write_row_to_table(dwetl_logger, session, stg2_row, stg2_key):
        # write the stage 2 table 'in_val_'s
        try:
            # insert the row into SQLAlchemy table base class
            record = bib_rec_stg2_tables[stg2_key](**stg2_row)
            session.add(record)
            session.commit()
        except exc.SQLAlchemyError as e:
            print(e)
            dwetl_logger.error('\n---\n' + str(e) + '\n---\n')
            session.rollback()

    # do mai01_z00 to stg 2 table first
    # for each row, use its row dict to take column names out, and add 'in_val_' in front
    def process_and_write_row(Session, row, stg2_key):
        session = Session()
        # get unwanted column names out
        row_dict = row.__dict__
        # iterate over column names (ignore rec_type_cd and rec_trigger_key)
        # add dw_stg_2_aleph_lbry_name column after db_operation_cd
        # get value from each column name, insert into same column name in stg 2\
        # with 'in_val_' in front of each column name
        invalid_keys = {'rec_type_cd', 'rec_trigger_key', '_sa_instance_state'}
        row_dict = without_keys(row_dict, invalid_keys)
        stg2_row = build_stg2_row(em_dict, row_dict)
        print_debug_colors(row_dict, stg2_row)
        write_row_to_table(dwetl_logger, session, stg2_row, stg2_key)

    # doesn't work for z00_field
    def get_stg2_key(key):
        table = key.split('_')[1]
        stg2_key = 'bib_rec_' + table
        return stg2_key


    #create session
    Session = sessionmaker(bind=engine)
    session = Session()

    for key, base_class in bib_rec_stg1_tables.items():
        stg2_key = get_stg2_key(key)
        for row in session.query(base_class).all():
            process_and_write_row(Session, row, stg2_key)
