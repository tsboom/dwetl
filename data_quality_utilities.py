import dwetl
import datetime

'''
finish is mandatory
'''
# checks if mandatory
def is_mandatory(input):
    print("temporary")

# checks if numeric only
def is_numeric(input):
    n = [0,1,2,3,4,5,6,7,8,9]
    if (all(str(i) in input for i in n)):
        return True



# checks if provided length is true
def is_specified_length(input, length):
    if (len(input) == length):
        return True

# checks if less than or equal to specified length
def is_less_than_eq_to_length(input, length):
    if (len(input) <= length):
        return True

# checks range
def is_valid_range(number, a, z):
    if number in range(a, z):
        return True

# checks to see if there are no nulls, all spaces, or all zeros
def no_missing_values(input):
    # check for all zeros
    if input == None or input.isspace() or int(input) == 0:
        return False
    return True



# def trim function no leading and trailing spaces
def trim(input):
    return input.strip()

# check if valid aleph year (1980 - Present)
def is_valid_aleph_year(year):
    current_year = datetime.datetime.now().year
    try:
        if year in range(1980, current_year):
            return True
    except ValueError:
        raise ValueError(year + ": Year is out of range.")

# checks if valid date 1980-present
def is_valid_aleph_date(string_date):
    string_date_valid = datetime.datetime.strptime(string_date, '%Y%m%d').strftime('%Y%m%d')
    try:
        if string_date == string_date_valid and is_valid_aleph_year(string_date):
            return True
    except ValueError:
        raise ValueError(string_date + ": Date is invalid")

# function create a python dict from a 2 column CSV lookup table
def create_dict_from_csv(csv_file):
    csv_file_path = os.path.join('lookup_tables', csv_file)
    with open(csv_file_path, mode='r') as f:
        reader = csv.DictReader(f, fieldnames=('code', 'description'))
        csv_dict = {}
        for row in reader:
            csv_dict[row['code']] = row['description']
        return csv_dict
