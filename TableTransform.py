import os
import json
import pdb

table_config_path = os.path.join('table_config','bibliographic_record_dimension.json')

def load_table_config(table_config_path):
    with open(table_config_path) as f:
        table_config = json.load(f)
    return table_config


# convert one row, fields metadata, and outputs SQL alchemy row ]
# def transform_field(reader, table_config):
#     output_rows = []
#     for source_row in dataframe:
#         output_row = # new row sqlalchemy
#         for field in TC['fields']:
#             transform_field(source_row, field, output_row)
#
#
#         output_rows.append(output_row)
