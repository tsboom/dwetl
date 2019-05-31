#date check
#dependency transformations
#valid value lookups

'''
specific transform functions that are used in more than one dimension
'''
from TransformField import TransformField

# substring based on start and end index
def substring(field, start, end):
    substring = field.value[start:end]
    return substring

# return 'Standard'
# LBRY_HOLDING_REC_TYPE_DESC
# BIB_RECORD_REC_TYPE_DESC
# LBRY_ITEM_LOC_REC_TYPE_DESC
def output_standard(field):
    return 'Standard'


# Check to see if SUPPRESSED flag is there
# LBRY_HOLDING_DISPLAY_SUPPRESSED_FLAG
# BIB_REC_DISPLAY_SUPPRESSED_FLAG
def is_suppressed(field):
    if "SUPPRESSED" in field.value.upper():
        return "Y"
    else:
        return "N"




'''
bibliographic record dimension transform functions
'''

# # source field Z13_ISBN_ISSN_CODE
# def isbn_code_020(field):
#     if
#
# def issn_code_022(field):


# source field Z13U_USER_DEFINED_2
def remove_ocm_ocn_on(field):
    if field.value[0:3] == "ocm":
        return field.value[3:]
    elif field.value[0:3] == "ocn":
        return field.value[3:]
    elif field.value[0:2] == "on":
        return field.value[2:]


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


#ref should be path to csv lookup table
#works for z30_call_no_type and z30_call_no_2_type


#z13u_user_defined_3 value parsing (can this be combined with the command above? requires substring handling based on check)
""" with the optional start and stop arguments, this should work for full strings or substrings (I think) """
import csv
def subLookUp(field, ref, start=0, end=None):
    with open(ref, 'r') as f:
        lookup_table = csv.reader(f)
        for (key,value) in lookup_table:
                if field.value[start:end] in key:
                    return value


def z13cond(field):
    #field input is value from record's z13_isbn_issn_code field, while field is the value of z13_isbn_issn field
    if str(field.value)[0:3] == "020" or str(field.value)[0:3] == "022":
        return field.value
    else:
        return None

#^need to stringify numbers

#itemProcessStatus
#z35eventChecksReallyNotClearOnHowTheseAreSupposedToWork
