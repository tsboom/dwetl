#date check
#dependency transformations
#valid value lookups

#ifSuppressed
def suppCheck(field):
    if "SUPPRESSED" in field:
        return "Y"
    else:
        return "N"

#for these checks, should we standardize for upper or lower?
#nice way to combine them all because they are all checks against z13u_user_defined_6 field
#z13u_user_defined_3 also checked for suppressed. Problematic to have that check combined with the others?
#ifAcqCreatedCircCreatedProvisional
def z13u_check(field):
    if "SUPPRESSED" in field.upper() or if "ACQ-CREATED" in field.upper() or "CIRC-CREATED" in field.upper() or "PROVISIONAL" in field.upper():
        return "Y"
    else:
        return "N"

#ref should be path to csv lookup table
#works for z30_call_no_type and z30_call_no_2_type


#z13u_user_defined_3 value parsing (can this be combined with the command above? requires substring handling based on check)
""" with the optional start and stop arguments, this should work for full strings or substrings (I think) """
import csv
def subLookUp(field, ref, start=0, end=None):
    with open(ref, 'r') as f:
        lookup_table = csv.reader(f)
        for (key,value) in lookup_table:
                if field[start:end] in key:
                    return value

def look_up_


def z13cond(field):
    #field input is value from record's z13_isbn_issn_code field, while field is the value of z13_isbn_issn field
    if field[0:3] == "020" or field[0:3] == "022":
        return field
    else:
        return None

#itemProcessStatus
#z35eventChecksReallyNotClearOnHowTheseAreSupposedToWork
