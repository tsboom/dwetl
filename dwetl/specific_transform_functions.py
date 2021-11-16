import pdb
import csv

'''
specific transform functions that are used in more than one dimension
'''


# substring based on start and end index
def substring(value, start, end):
    output = value[int(start):int(end)]
    return output

# return 'Standard'
# LBRY_HOLDING_REC_TYPE_DESC
# BIB_RECORD_REC_TYPE_DESC
# LBRY_ITEM_LOC_REC_TYPE_DESC
def output_standard(value):
    return 'Standard'


'''
bibliographic record dimension transform functions
'''

# # source value Z13_ISBN_ISSN using optional_isbn_code
def isbn_code_020(value):
    if value.isbn_issn_code == '020':
        isbn_issn = value.value
    else:
        # Alex says "treat as empty value" not sure if this is empty string or None
        isbn_issn = ''
    return isbn_issn

def issn_code_022(value):
    if value.isbn_issn_code == '022':
        isbn_issn = value.value
    else:
        isbn_issn = ''
    return isbn_issn


# source value Z13U_USER_DEFINED_2
def remove_ocm_ocn_on(value):
    if value[0:3] == "ocm":
        return value[3:]
    elif value[0:3] == "ocn":
        return value[3:]
    elif value[0:2] == "on":
        return value[2:]
        

# source value z13u_user_defined_3, translate record type to record description
def lookup_record_type(value):
    # first take substring from index 6-7
    record_type_code = value[6:7]
    # translate record type code to description 
    with open('lookup_tables/record_type_code.csv', 'r') as f:
        lookup_table = csv.reader(f)
        for key, value in lookup_table: 
            if key == record_type_code:
                return value
                

    
    



# source value Z13U_USER_DEFINED_6 specific transform
# Check to see if SUPPRESSED flag is there
# LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG
# BIB_REC_DISPLAY_SUPPRESSED_FLAG
def is_suppressed(value):
    if "SUPPRESSED" in value.upper():
        return "Y"
    else:
        return "N"

# source value Z13U_USER_DEFINED_6 specific transform
# target values:
# BIB_REC_ACQUISITION_CREATED_FLAG
# BIB_REC_CIRCULATION_CREATED_FLAG
# BIB_REC_PROVISIONAL_STATUS_FLAG
def is_acq_created(value):
    if "ACQ-CREATED" in value.upper():
        return 'Y'
    else:
        return 'N'
#^^^ not sure what 'N' conditions should be, but I tested 'not-acq-created' and it passed. I imagine it is the same with the other check functions. Just a thought...

def is_circ_created(value):
    if "CIRC-CREATED" in value.upper():
        return 'Y'
    else:
        return 'N'


def is_provisional(value):
    if "PROVISIONAL" in value.upper():
        return 'Y'
    else:
        return 'N'

#z13u_user_defined_3 value parsing (can this be combined with the command above? requires substring handling based on check)
""" with the optional start and stop arguments, this should work for full strings or substrings (I think) """
import csv
def sub_look_up(value, ref, start=0, end=None):
    with open(ref, 'r') as f:
        lookup_table = csv.reader(f)
        for (key,value) in lookup_table:
            if value[start:end] in key:
                return value
#^^^ what substring will we be checking against, I'm not clear.



#itemProcessStatus
#z35eventChecksReallyNotClearOnHowTheseAreSupposedToWork
