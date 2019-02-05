from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import collections
import json
import pdb
import pprint


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# The ID and range of test source to target spreadsheet.
SPREADSHEET_ID = '1RkxYf2YaxkGnpdLGV7oYUu9Rln81vwBQAGIaUBPROyw'


# library item dimension range
LIB_ITEM_DIM_RANGE = 'Source-to-Target Mapping!A69:V113'
# bib record dimension range
BIB_RECORD_DIM_RANGE = 'Source-to-Target Mapping!A28:V59'
# data quality range
DATA_QUALITY_RANGE = 'Data Quality Checks!A6:S82'

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

# function to delete the key if the cell is empty
# def delete_key_for_empty(col, )



# function that creates a dict of all field names and their values
# so that they can be searched
def get_dq_rows_dict(dq_values):
    dq_rows_dict = {}
    [dq_rows_dict.update({row_values[2] : row_values})for row_values in dq_values]
    return dq_rows_dict



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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

    #get column variable names from row 6 of spreadsheet
    sheet_columns = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                    range='Source-to-Target Mapping!A6:V6').execute().get('values', [])

    # get values by using range of all the dimensions and dq sheet
    bib_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=BIB_RECORD_DIM_RANGE).execute()
    values = bib_result.get('values', [])

    library_item_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=LIB_ITEM_DIM_RANGE).execute()
    lib_item_values = library_item_result.get('values', [])

    dq_result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                   range=DATA_QUALITY_RANGE).execute()
    dq_values = dq_result.get('values', [])
    dq_rows_dict = get_dq_rows_dict(dq_values)


    if not lib_item_values:
        print('No data found.')
    else:
        # *** should figure out how to get these names directly from the spreadsheet row
        # sheet_columns = ['aleph_library', 'aleph_table', 'source_col_name', 'source_data_type', 'source_format',
        # 'source_mandatory', 'pre_or_post_dq', 'pre_action', 'pre_detailed_instructions', 'dq_required',
        # 'chg_proc_type', 'transform_action', 'action_specific', 'action_detailed_instructions',
        # 'historical_action', 'historical_subaction', 'historical_detailed_instructions', 'target_name',
        # 'target_attribute', 'target_col_name', 'target_data_type', 'specific_transform_function']


        dimension_dict = {}
        # write dimension name to table
        dimension_dict['target_name'] = values[0][17]
        dimension_dict['fields'] = []

        for col in values:
            row_dict = {}
            # create a dict from Sheet row values using the sheet column names
            for idx, key in enumerate(sheet_columns[0]):
                row_dict[key] = value_if_exists(col, idx)

            # generate a dict describing dimension column fields (use to create JSON later)
            target_col_name = row_dict['target_col_name']
            col_dict = {}
            col_dict[target_col_name] = {
                "target_data_type": row_dict['target_data_type'],
                "target_attribute": row_dict['target_attribute'],
                "Tranformation Info": {
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
                "Preprocessing Info": {d
                    "pre_or_post_dq": row_dict['pre_or_post_dq'],
                    "pre_action": row_dict['pre_action'],
                    "pre_detailed_instructions": row_dict['pre_detailed_instructions']
                }
            }
            pdb.set_trace()
            # check if current col name exists in dq rows dict, if so write dq info
            if row_dict['source_col_name'] != 'N/A' and \
                row_dict['source_col_name'] in dq_rows_dict.keys():
                whole_row = dq_rows_dict[row_dict['source_col_name']]
                dq_json = {
                    "Data Quality Info": whole_row
                }
                col_dict.update(dq_json)

            dimension_dict['fields'].append(col_dict)

        pprint.pprint(dimension_dict)


if __name__ == '__main__':
    main()
