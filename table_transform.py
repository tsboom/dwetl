import os
import json
import pdb
from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData



def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config


def transform_field:


'''
main function to load stg_2 table PP, DQ, T1, T1.. etc
'''
def transform_stg2_table(engine, table_config, bib_rec_stg2_tables, dwetl_logger):
    Session = sessionmaker(bind=engine)
    session = Session()


    #convert one row, fields metadata, and outputs SQL alchemy row ]
    def transform_field(reader, table_config):
        output_rows = []
        for source_row in sqlalchemy:
            output_row = # new row sqlalchemy
            for field in TC['fields']:
                transform_field(source_row, field, output_row)


            output_rows.append(output_row)
