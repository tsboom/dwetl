import os
import json
import pdb

#table_config_path = os.path.join('table_config','z30.json')

def load_table_config(table_config_path):
    with open(table_config_path) as f:
        TC = json.load(f)
    return TC


# # convert one field, fields metadata, and outputs SQL alchemy row ]
# transform_field(dataframe[])

#
# output_rows = []
# for source_row in dataframe:
#     output_row = # new row sqlalchemy
#     for field in TC['fields']:
#         transform_field(source_row, field, output_row)
#
#
#     output_rows.append(output_row)
#
# def transform_field(source_data, TC):
