import os
import pdb

'''
This function should take filename as input and output the sa SQLAlchemy Base class for that table
'''

filename = 'mai50_z30_20190220_034001_data'

Base = {}

# name_mapping = {
#     'mai01_z00':
#
# }


def get_class_by_tablename(Base, tablename):
    """Return table class based on name"""
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c

def get_table_name(filename):
    # get date out of filename
    filename = filename.split('_')
    # ignore time and 'data'
    filename_parts = filename[:-2]

    # parse out table info from filename
    library = filename_parts[0]
    table = filename_parts[1]
    # for mai50_z30_bib, mai50_z00_field, mai01_z00_field
    # filename parts are different
    if len(filename_parts)== 4:
        bibfull = filename_parts[2]

    # combine table_info into table_name
    # table_long_name = '_'.join(f"{val}".format(str(val)) for (key,val) in table_info.items())
    fn_parts = ['dw', 'stg', '1', library, table]
    if bibfull:
        fn_parts.append(bibfull)
    table_long_name = '_'.join(fn_parts)
    return table_long_name


def get_table_class(filename, Base):
    table_name = get_table_name(filename)

    table_class = get_class_by_tablename(Base, tablename)
    return table_class
