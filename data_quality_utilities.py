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
    n = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    if (all(str(i) in input for i in n)):
        return True
# ^^^ doesn't work?


# checks if provided length is true
def is_valid_length(input, length):
    if (len(str(input)) == length):
        return True

# do these dq utilities need to return positive and negative results or does a fail return False?

# checks if less than or equal to specified length


def is_less_than_eq_to_length(input, length):
    if (len(str(input)) <= length):
        return True
# ^^^ how to check len on ints?

# # checks range
# def is_valid_range(number, a, z):
#     if number in range(a, z):
#         return True

# checks to see if there are no nulls, all spaces, or all zeros


def no_missing_values(input):
    # check for all zeros
    if input is None or input.isspace() or int(input) == 0:
        return False
    return True
# ^^^not sure if working


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
# ^^^ exception doesn't seem to work, rewrote it to be a simple if/else. Can this be altered to then throw an error?

# checks if valid date 1980-present


# need to make sure null passes missing value data quality
def is_valid_aleph_date(string_date):
    string_date_valid = datetime.datetime.strptime(
        string_date, '%Y%m%d').strftime('%Y%m%d')
    if string_date == string_date_valid and is_valid_aleph_year(string_date):
        return True
    else:
        return False
# ^^^ same issue as above I'd imagine. Also is_valid_aleph_year doesn't strip out just the year from the incoming date.
# Do we need to ensure that the incoming information is stringified?
# We then need to int the string to work with is_valid_aleph_year because it is expecting an int
# is valid aleph date gonna check if the date has occured yet? Should we have it do so?
# TypeError for nonstrings?


def is_valid_aleph_date_redux(string_date):
#    try:
        string_date_valid = datetime.datetime.strptime(string_date, '%Y%m%d').strftime('%Y%m%d')
        if string_date == string_date_valid and is_valid_aleph_year(int(string_date[0:4])):
            return True
        else:
            return False
#    except TypeError:
#        print(str(string_date) + " is not a string")

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
