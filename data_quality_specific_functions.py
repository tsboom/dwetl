import csv
import os
import pdb

# function create a python dict from a 2 column CSV lookup table
def create_dict_from_csv(csv_file):
    csv_file_path = os.path.join('lookup_tables', csv_file)
    with open(csv_file_path, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=('code', 'description'))
        csv_dict = {}
        for row in reader:
            csv_dict[row['code']] = row['description']
        return csv_dict



def dq_z13u_user_defined_10_valid_holding_own_code(code):
    holding_own_dict = create_dict_from_csv('holding_own_code.csv')
    try:
        holding_own_dict[code]

    except KeyError as error:
        print(error, ': Incorrect holding own code.')


def dq_z13u_user_defined_2(input):
    if "ocm" in input:
