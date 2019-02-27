import csv
import sqlalchemy
import logging
import datetime
import pdb
from sqlalchemy import inspect, create_engine
from sqlalchemy import exc
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
# import database_config
import database_credentials



def load_file_equivalent_table(filename, engine, bib_rec_stg1_tables):

    '''
    header pre processing
    '''

    def get_headers_footer(filename):
        with open(filename) as f:
            reader = csv.reader(f, delimiter='\t')
            header_1 = next(reader)
            header_2 = next(reader)
            for line in f:
                pass
            footer = line.strip().split('\t')
            hhf_dict = {'header_1': header_1, 'header_2': header_2, 'footer': footer}
            return hhf_dict

    def validate_header1(header1):
        print('need to validate')

    def validate_header2(header2):
        #make sure it's there
        print('need to validate')

    def validate_footer(footer):
        print('need to validate')

    hhf_dict = get_headers_footer(filename)


    def parse_tsv_filename(filename, hhf_dict):
        # tsv filename is the fourth field in header 1. ignore subdirectory name
        tsv_name = hhf_dict['header_1'][3][9:]
        tsv_name_metadata = {}
        parts = tsv_name.split('_')
        tsv_name_metadata = {
            'library':parts[0],
            'table':parts[1],
            'datetime':parts[2]+parts[3]
        }
        #the counter doesn't exist in the current filename
        return tsv_name_metadata

    tsv_name_metadata = parse_tsv_filename(filename, hhf_dict)



    '''
    load tsv into file-equivalent table
    '''

    #create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # determine if csv row is a footer
    def row_is_footer(row):
        return row[0] == 'T'

    # parse values from csv row into dict with column names as keys
    def parse_row(row, header_2):
        if row_is_footer(row):
            # validate footer here
            raise StopIteration()
        else:
            row_dict = {}
            # added code to use column headers as number of rows, ignore if more fields than that
            for i, field in enumerate(row):
                # don't continue farther than the number of header columns (temp fix)
                if i < len(header_2):
                    row_dict[header_2[i]] = field
                else:
                    logging.warning("\nNot enough column names after " + header_2[i-1] + ': ' + row[i-1] +".... skipping extra value\n\n")
                    break

            return row_dict


    '''
    alex's process id codes added for testing
    '''
    def set_dw_process_metadata(row_dict):
        # add dummy em_create_dw_prcsng_cycle_id bc it's a PK
        row_dict['em_create_dw_prcsng_cycle_id'] = 9999
        row_dict['em_create_dw_job_exectn_id'] = 9999
        row_dict['em_create_dw_job_name'] = "load FET"
        row_dict['em_create_dw_job_version_no'] = "0.0"
        row_dict['em_create_user_id'] = "thschone"
        row_dict['em_create_tmstmp'] = datetime.datetime.now()
        return row_dict

    '''
    write to FET
    '''
    # get name of the base table in sqlalchemy based on filename
    filename_only= filename.split("/")[2]
    lib_table = filename_only.split("_")[0:2]
    table_base_class = "_".join(lib_table)

    # read each line of the csv ignoring 2 headers and last line and write to the db
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        header_1 = next(reader) # row 0
        header_2 = next(reader) # row 1

        #read all lines after lines one and two
        try:
            while True:
                row = next(reader)
                row_dict = parse_row(row, header_2)
                set_dw_process_metadata(row_dict)
                try:
                    # insert the row into SQLAlchemy table base class
                    record = bib_rec_stg1_tables[table_base_class](**row_dict)
                    session.add(record)
                    session.commit()
                except exc.SQLAlchemyError as e:
                    print(e)
                    session.rollback()
        except StopIteration:
            pass
