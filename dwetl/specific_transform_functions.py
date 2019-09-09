import pdb

'''
specific transform functions that are used in more than one dimension
'''


# substring based on start and end index
def substring(field, start, end):
    output = field.value[int(start):int(end)]
    return output

# return 'Standard'
# LBRY_HOLDING_REC_TYPE_DESC
# BIB_RECORD_REC_TYPE_DESC
# LBRY_ITEM_LOC_REC_TYPE_DESC
def output_standard(field):
    return 'Standard'


'''
bibliographic record dimension transform functions
'''

# # source field Z13_ISBN_ISSN using optional_isbn_code
def isbn_code_020(field):
    if field.isbn_issn_code == '020':
        isbn_issn = field.value
    else:
        # Alex says "treat as empty field" not sure if this is empty string or None
        isbn_issn = ''
    return isbn_issn

def issn_code_022(field):
    if field.isbn_issn_code == '022':
        isbn_issn = field.value
    else:
        isbn_issn = ''
    return isbn_issn


# source field Z13U_USER_DEFINED_2
def remove_ocm_ocn_on(field):
    if field.value[0:3] == "ocm":
        return field.value[3:]
    elif field.value[0:3] == "ocn":
        return field.value[3:]
    elif field.value[0:2] == "on":
        return field.value[2:]




# source field Z13U_USER_DEFINED_6 specific transform
# Check to see if SUPPRESSED flag is there
# LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG
# BIB_REC_DISPLAY_SUPPRESSED_FLAG
def is_suppressed(field):
    if "SUPPRESSED" in field.value.upper():
        return "Y"
    else:
        return "N"

# source field Z13U_USER_DEFINED_6 specific transform
# target fields:
# BIB_REC_ACQUISITION_CREATED_FLAG
# BIB_REC_CIRCULATION_CREATED_FLAG
# BIB_REC_PROVISIONAL_STATUS_FLAG
def is_acq_created(field):
    if "ACQ-CREATED" in field.value.upper():
        return 'Y'
    else:
        return 'N'
#^^^ not sure what 'N' conditions should be, but I tested 'not-acq-created' and it passed. I imagine it is the same with the other check functions. Just a thought...

def is_circ_created(field):
    if "CIRC-CREATED" in field.value.upper():
        return 'Y'
    else:
        return 'N'


def is_provisional(field):
    if "PROVISIONAL" in field.value.upper():
        return 'Y'
    else:
        return 'N'

#z13u_user_defined_3 value parsing (can this be combined with the command above? requires substring handling based on check)
""" with the optional start and stop arguments, this should work for full strings or substrings (I think) """
import csv
def sub_look_up(field, ref, start=0, end=None):
    with open(ref, 'r') as f:
        lookup_table = csv.reader(f)
        for (key,value) in lookup_table:
            if field.value[start:end] in key:
                return value
#^^^ what substring will we be checking against, I'm not clear.



#itemProcessStatus
#z35eventChecksReallyNotClearOnHowTheseAreSupposedToWork
