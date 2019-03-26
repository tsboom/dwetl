from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# from collections import OrderedDict
import json
import pdb
import pprint
import os


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# The ID and range of test source to target spreadsheet.
# SPREADSHEET_ID = '1RkxYf2YaxkGnpdLGV7oYUu9Rln81vwBQAGIaUBPROyw'


# the ID of the real star schema spreadsheets
SPREADSHEET_ID = '1QyEk0qAUjplpEXPQsAHHJ4avxOWqyJWkW6LIzxQB64Y'


def set_up_sheets_api():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token_dw.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet




# column variable names from source to target sheets is_valid_range
SOURCE_TO_TARGET_COLUMN_RANGE = 'Source-to-Target Mapping!A6:V6'
# library item dimension range
LIB_ITEM_DIM_RANGE = 'Source-to-Target Mapping!A69:V113'
# bib record dimension range
# BIB_RECORD_DIM_RANGE = 'Source-to-Target Mapping!A28:V59'
BIB_RECORD_DIM_RANGE = 'Source-to-Target Mapping!A33:V63'

# data quality range
DATA_QUALITY_RANGE = 'Data Quality Checks!A6:S82'
# data quality column variable names range
DQ_COLUMN_RANGE = 'Data Quality Checks!A5:S5'

def get_sheets_values_list(sheet, spreadsheet_id, range):
    # get values in a comma separated list based on range
    sheet_values = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute().get('values')
    # if sheet_values only contains one list, return that list (for column headers)
    if len(sheet_values) == 1:
        return sheet_values[0]
    else:
        return sheet_values

# function to check if column and value in spreadsheet exists
def value_if_exists(column, idx):
    try:
        return column[idx]
    except IndexError:
        return None

# function to write an N for No if there is no Y
def write_no_if_not_yes(value):
    if value != "Y":
        return "N"

# function that creates a dict of each row dict, with the field/column name as key
# so that they can be searched
def get_dq_rows_dict(dq_values, sheet):
    dq_rows_dict = {}

    # get sheet column names from dq sheet to use as keys in row dictionary
    sheet_columns = get_sheets_values_list(sheet, SPREADSHEET_ID, DQ_COLUMN_RANGE)

    # create dq_rows_dict using field/column names as keys so that they are searchable
    for row_values in dq_values:
        row_values_dict = {}
        # add keys (from sheet_columns)to each row's values list
        for idx, key in enumerate(sheet_columns):
            row_values_dict[key] = row_values[idx]
            # i got an error whenever column S was blank. need a test to make sure column S is not blank.

        source_column_name = row_values_dict['source_column_name']
        # append dq row to existing key (if key exists)
        if dq_rows_dict.get(source_column_name, False):
            dq_rows_dict[source_column_name].append(row_values_dict)
        else:
            dq_rows_dict[source_column_name] = [row_values_dict]
    return dq_rows_dict



def main():

    sheet = set_up_sheets_api()


    # # generate values lists for column names, dq checks, and the dimensions to process
    # ranges_to_process = [SOURCE_TO_TARGET_COLUMN_RANGE, DATA_QUALITY_RANGE, LIB_ITEM_DIM_RANGE, BIB_RECORD_DIM_RANGE]

    #get column variable names from row 6 of spreadsheet
    sheet_columns = get_sheets_values_list(sheet, SPREADSHEET_ID, SOURCE_TO_TARGET_COLUMN_RANGE)

    # get values by using range of all the dimensions and dq sheet
    bib_rec_values = get_sheets_values_list(sheet, SPREADSHEET_ID, BIB_RECORD_DIM_RANGE)

    # get library item values
    lib_item_values = get_sheets_values_list(sheet, SPREADSHEET_ID, LIB_ITEM_DIM_RANGE)

    # get dq checks values
    dq_values = get_sheets_values_list(sheet, SPREADSHEET_ID, DATA_QUALITY_RANGE)
    # create a dict of dicts for every dq_check row that can be searched by key(field name)
    dq_rows_dict = get_dq_rows_dict(dq_values, sheet)

    dimension_values_list = [bib_rec_values, lib_item_values]

    for dimension_values in dimension_values_list:
        if not dimension_values:
            print('No data found.')
        else:
            dimension_dict = {}
            # write dimension name to table using first row of dimension values
            dimension_name = dimension_values[0][18]
            dimension_dict['target_dimension_name'] = dimension_name

            dimension_dict['fields'] = []

            for col in dimension_values:
                row_dict = {}
                # create a dict from Sheet row values using the sheet column names
                for idx, key in enumerate(sheet_columns):
                    row_dict[key] = value_if_exists(col, idx)

                # generate a dict describing dimension column fields (use to create JSON later)

                col_dict = {
                    "target_col_name": row_dict['target_col_name'],
                    "target_data_type": row_dict['target_data_type'],
                    "target_attribute": row_dict['target_attribute'],
                    "Transformation Info": {
                        "chg_proc_type": row_dict['chg_proc_type'],
                        "transform_action": row_dict['transform_action'],
                        "action_specific": row_dict['action_specific'],
                        "specific_transform_function": row_dict['specific_transform_function'],
                        "source_col_name": row_dict['source_col_name'],
                        "source_data_type": row_dict['source_data_type'],
                        "source_format": row_dict['source_format'],
                        "source_mandatory": write_no_if_not_yes(row_dict['source_mandatory']),
                        "aleph_table": row_dict['aleph_table'],
                        #remove '\n'
                        "action_detailed_instructions":row_dict['action_detailed_instructions'].rstrip()
                    },
                    "Preprocessing Info": {
                        "pre_or_post_dq": row_dict['pre_or_post_dq'],
                        "pre_action": row_dict['pre_action'],
                        "pre_detailed_instructions": row_dict['pre_detailed_instructions']
                    },
                    "Data Quality Info": {}
                }

                # check if current col name exists in dq rows dict, if so write dq info
                # need to make sure all the fields  needing DQ are noted as Yes
                if row_dict['dq_required'] in {'Y', 'Yes'} and \
                    row_dict['source_col_name'] in dq_rows_dict.keys():
                    all_dq_check_rows = dq_rows_dict[row_dict['source_col_name']]
                    col_dict['Data Quality Info'] = {
                        "dq_required": True,
                        "data_quality_checks": all_dq_check_rows
                        }
                else:
                    col_dict['Data Quality Info'] = {"dq_required": False}

                dimension_dict['fields'].append(col_dict)

            dirname = os.path.dirname(__file__) #current directory
            filename = dimension_name.replace(' ', '_').lower() + '.json'
            full_filename = os.path.join(dirname, '../table_config/'+filename)

            print('\n\n\n...Writing ' +  filename+'\n\n\n')
            with open(full_filename, 'w') as outfile:
                json.dump(dimension_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    main()
