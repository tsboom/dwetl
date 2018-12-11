import dw_etl


# checks if mandatory
def is_mandatory(input):
    print("temporary")

# checks if numeric only
def is_numeric(input):
    return input.isdigit()



# checks length
def is_good_length(input, length):
    if (len(input) == length):
        return True




# checks to see if there are no nulls, all spaces, or all zeros
def no_missing_values(input):
    if (input = None or input.isspace() or input )


# def trim function no leading and trailing spaces
def trim(input):
    return input.strip()
