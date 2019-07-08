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

'''
Configure ranges for each table
'''

# column variable names from source to target sheets is_valid_range
SOURCE_TO_TARGET_COLUMN_RANGE = 'Source-to-Target Mapping!A6:X6'


LIBRARY_HOLDING_DIM_RANGE = 'Source-to-Target Mapping!A7:X30'
LIBRARY_HOLDING_MARC_RECORD_FIELD_OUTRIGGER_RANGE = 'Source-to-Target Mapping!A66:X70'
BIB_RECORD_DIM_RANGE = 'Source-to-Target Mapping!A35:X64'
BIBLIOGRAPHIC_RECORD_MARC_RECORD_FIELD_OUTRIGGER_DIM_RANGE = 'Source-to-Target Mapping!A7:X30'
LIB_ITEM_LOCATION_DIM_RANGE = 'Source-to-Target Mapping!A72:X79'
LIB_ITEM_DIM_RANGE = 'Source-to-Target Mapping!A80:X138'
LIBRARY_ITEM_MATERIAL_FORM_DIM_RANGE = 'Source-to-Target Mapping!A139:X141'
LIBRARY_ITEM_PROCESS_STATUS_DIM_RANGE = 'Source-to-Target Mapping!A142:X146'
LIBRARY_ITEM_STATUS_DIM_RANGE = 'Source-to-Target Mapping!A147:X149'
# Date dimension has blanks in the spreadsheet. (will be implemented in the future)
# DATE_DIMENSION_RANGE = 'Source-to-Target Mapping!A150:X167'
LIBRARY_ITEM_FACT_RANGE = 'Source-to-Target Mapping!A168:X183'

table_ranges = {
    # 'library_holding': LIBRARY_HOLDING_DIM_RANGE,
    # 'library_holding_marc_record_field_outrigger': LIBRARY_HOLDING_MARC_RECORD_FIELD_OUTRIGGER_RANGE,
    # 'bib_record': BIB_RECORD_DIM_RANGE,
    # 'bib_record_marc_record_field_outrigger': BIBLIOGRAPHIC_RECORD_MARC_RECORD_FIELD_OUTRIGGER_DIM_RANGE,
    # 'lib_item_location': LIB_ITEM_LOCATION_DIM_RANGE,
    'lib_item': LIB_ITEM_DIM_RANGE
    # 'lib_item_material_form': LIBRARY_ITEM_MATERIAL_FORM_DIM_RANGE,
    # 'lib_item_process_status': LIBRARY_ITEM_PROCESS_STATUS_DIM_RANGE,
    # 'lib_item_status': LIBRARY_ITEM_STATUS_DIM_RANGE,
    # 'lib_item_fact': LIBRARY_ITEM_FACT_RANGE
    }

#_data quality range real star scheme sheet
DATA_QUALITY_RANGE = 'Data Quality Checks!A6:U83'
# data quality column variable names range real star scheme sheet
DQ_COLUMN_RANGE = 'Data Quality Checks!A5:U5'

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
            # i got an error whenever column T was blank. need a test to make sure column T is not blank.
        source_column_name = row_values_dict['source_column_name']
        # append dq row to existing key (if key exists)

        if dq_rows_dict.get(source_column_name, False):
            dq_rows_dict[source_column_name].append(row_values_dict)
        else:
            dq_rows_dict[source_column_name] = [row_values_dict]
    return dq_rows_dict



def main():

    sheet = set_up_sheets_api()

    #get column variable names from row 6 of spreadsheet
    sheet_columns = get_sheets_values_list(sheet, SPREADSHEET_ID, SOURCE_TO_TARGET_COLUMN_RANGE)

    # get dq checks values
    dq_values = get_sheets_values_list(sheet, SPREADSHEET_ID, DATA_QUALITY_RANGE)
    # create a dict of dicts for every dq_check row that can be searched by key(field name)
    dq_rows_dict = get_dq_rows_dict(dq_values, sheet)

    # get values by using range of all the dimensions and dq sheet
    bib_rec_values = get_sheets_values_list(sheet, SPREADSHEET_ID, BIB_RECORD_DIM_RANGE)

    # get library item values
    lib_item_values = get_sheets_values_list(sheet, SPREADSHEET_ID, LIB_ITEM_DIM_RANGE)

    # get spreadsheet values for each dimension and fact range in a list
    dimension_values_list = []

    # use spreadsheet ranges to get values for each dim and fact
    for range_name, sheet_range in table_ranges.items():
        current_values = get_sheets_values_list(sheet, SPREADSHEET_ID, sheet_range)
        dimension_values_list.append(current_values)
        print(range_name + ' values were found and added to dimension_values_list')





    '''
    create JSON for each dimension and fact
    '''
    for dimension_values in dimension_values_list:
        if not dimension_values:
            print('No data found.')
        else:
            dimension_dict = {}
            # write dimension name to table using first row of dimension values. dimension name is in index 20
            dimension_name = dimension_values[0][20]
            dimension_dict['target_dimension_name'] = dimension_name

            dimension_dict['fields'] = []

            for col in dimension_values:
                row_dict = {}

                # create a dict from Sheet row values using the sheet column names
                for idx, key in enumerate(sheet_columns):
                    row_dict[key] = value_if_exists(col, idx)
                    pdb.set_trace()

                # Using the row_dict just created from the list of every column's values,
                # We need to rearrange this data into JSON that makes sense for the ETL.
                # Generate a dict describing dimension column fields and subset transformations and dq Checks
                # used to create JSON. 
                col_dict = {
                    "target_col_name": row_dict['target_col_name'],
                    "target_data_type": row_dict['target_data_type'],
                    "target_attribute": row_dict['target_attribute'],
                    "Transformation Info": {
                        "chg_proc_type": row_dict['chg_proc_type'],
                        "transform_action": row_dict['transform_action'],
                        "action_specific": row_dict['action_specific'],
                        "specific_transform_function": row_dict['specific_transform_function'],
                        "specific_transform_function_param1": row_dict['specific_transform_function_param1'],
                        "specific_transform_function_param2": row_dict['specific_transform_function_param2'],
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


                # Add Data Quality: check if current col name exists in dq rows dict
                # need to make sure all the fields needing DQ are noted as Yes
                # TODO: Deal with discerning dq checks for source columns vs. sourcecolumns after doing a substring.
                # modify dq part so that list of dqs only occur per target col name using target_column_name in dq spreadsheet
                if row_dict['dq_required'] in {'Y', 'Yes'} and \
                    row_dict['source_col_name'] in dq_rows_dict.keys():
                    # get only the dq check rows for current target column
                    all_dq_check_rows = dq_rows_dict[row_dict['source_col_name']]
                    target_col_checks = [i for i in all_dq_check_rows if i['target_column_name'] == row_dict['target_col_name']]
                    col_dict['Data Quality Info'] = {
                        "dq_required": True,
                        "data_quality_checks": target_col_checks
                        }
                else:
                    col_dict['Data Quality Info'] = {"dq_required": False}

                dimension_dict['fields'].append(col_dict)

            dirname = os.path.dirname(__file__) #current directory
            filename = dimension_name.replace(' ', '_').lower() + '.json'
            full_filename = os.path.join(dirname, '../table_config/'+filename)

            print('\n...Writing ' +  filename+'\n')
            with open(full_filename, 'w') as outfile:
                json.dump(dimension_dict, outfile, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    main()
