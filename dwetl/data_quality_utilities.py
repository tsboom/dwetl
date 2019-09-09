import datetime
import os
import csv
import pdb

# use pdb.set_trace() to set a breakpoint

'''
finish is mandatory
'''
# checks if mandatory


def is_mandatory(input):
    print("temporary")

# checks if numeric only
def is_numeric(input):
    if input.isnumeric() is True:
        return True
    else:
        return False

# checks if provided length is true
def is_valid_length(input, length):
    # len() outputs an integer so need to cast length to int
    if (len(str(input)) == int(length)):
        return True
    else:
        return False

# checks if less than or equal to specified length
def is_less_than_eq_to_length(input, length):
    # len() outputs an integer so need to cast length to int
    if (len(str(input)) <= int(length)):
        return True
    else:
        return False


# checks to see if there are no nulls, empty string, all spaces, or all zeros
def no_missing_values(input):
    output = True
    # check for all zeros nulls, or white spaces
    if input is None:
        output = False
    elif input is '':
        output = False
    elif input.isspace():
        output = False
    elif input.isnumeric():
        if int(input) == 0:
            output = False
    return output


# def trim function no leading and trailing spaces
def trim(input):
    return input.strip()

# check if valid aleph year (1980 - Present)


def is_valid_aleph_year(year):
    current_year = datetime.datetime.now().year
    if year not in range(1980, current_year+1):
        return False
    else:
        return True

def no_leading_space(input):
    if input[0].isspace():
        return False
    else:
        return True


# need to make sure null passes missing value data quality
def is_valid_aleph_date(string_date):
    string_date_valid = datetime.datetime.strptime(
        string_date, '%Y%m%d').strftime('%Y%m%d')
    if string_date == string_date_valid and is_valid_aleph_year(string_date):
        return True
    else:
        return False


# # checks if hour is valid HHMM format
def is_valid_hour(hhmm):
    hhmm_form = ('{0:04d}'.format(hhmm))
    if int(str(hhmm_form)[0:2]) in range(00,25):
        return True
    else:
        return False
            #^^looking at z35-event-hour goes from xxnn to nnnn, not sure how to parse this for our check

# function create a python dict from a 2 column CSV lookup table in the lookup_tables directory


def create_dict_from_csv(csv_file):
    csv_file_path = os.path.join('lookup_tables', csv_file)
    with open(csv_file_path, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=('code', 'description'))
        csv_dict = {}
        for row in reader:
            csv_dict[row['code']] = row['description']
        return csv_dict

#^^^^ will we make this an absolute path to lookup_tables?
#^^^^ will this only work on 2 column CSVs? Any situation where this would need to be extensible?

def create_dict_from_csv_redux(csv_file):
#    csv_file_path = os.path.join('lookup_tables', csv_file)
    with open(csv_file, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=('code', 'description'))
        csv_dict = {}
        for row in reader:
            csv_dict[row['code']] = row['description']
        return csv_dict
