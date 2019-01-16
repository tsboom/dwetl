from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json
import pdb
import pprint


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
# The ID and range of test source to target spreadsheet.
SAMPLE_SPREADSHEET_ID = '1RkxYf2YaxkGnpdLGV7oYUu9Rln81vwBQAGIaUBPROyw'

# bib record dimension range
SAMPLE_RANGE_NAME = 'Source-to-Target Mapping!A28:U59'

# function to check if row and value in spreadsheet exists
def value_if_exists(row, idx):
    try:
        return row[idx]
    except IndexError:
        return None

# function to delete the key if the cell is empty
# def delete_key_for_empty(row, )

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
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        sheet_columns = ['aleph_library', 'aleph_table', 'source_col_name', 'source_data_type', 'source_format',
        'source_mandatory', 'pre_or_post_dq', 'pre_action', 'pre_detailed_instructions', 'dq_required',
        'chg_proc_type', 'transform_action', 'action_specific', 'action_detailed_instructions',
        'historical_action', '', '', 'target_name', 'target_attribute', 'target_col_name', 'target_data_type']
        table_dict = {}
        # write dimension name to table
        table_dict['target_name'] = values[0][17]
        table_dict['fields'] = []

        for row in values:
            row_dict = {
                # target column name
                row[19]: {
                    "target_data_type": value_if_exists(row, 20),
                    "target_attribute": value_if_exists(row, 18),
                    "mandatory": value_if_exists(row, 5),  #it is no, if it's not a Y. change later
                    "tranformation_information": {
                        "source_col_name": value_if_exists(row, 2),
                        "source_data_type": value_if_exists(row, 3),
                        "aleph_table": value_if_exists(row, 2),
                        "transform_action": value_if_exists(row, 11),
                        "action_specific": value_if_exists(row, 8),
                        "action_detailed_instructions":value_if_exists(row, 13)
                    }
                }
            }
            pprint.pprint(row_dict)
            pdb.set_trace()
            table_dict['fields'].append(row_dict)
            print(row)

if __name__ == '__main__':
    main()
