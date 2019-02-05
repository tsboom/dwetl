import dwetl
import datetime


# checks if mandatory
def is_mandatory(input):
    print("temporary")

# checks if numeric only
def is_numeric(input):
    n = [0,1,2,3,4,5,6,7,8,9]
    if (all(str(i) in input for i in n)):
        return True



# checks if provided length is true
def is_valid_length(input, length):
    if (len(input) == length):
        return True

# checks range
def is_valid_range(number, a, z):
    if number in range(a, z):
        return True

# checks to see if there are no nulls, all spaces, or all zeros
def has_missing_values(input):
    # check for all zeros

    if input == None or input.isspace() or int(input)== 0:
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
