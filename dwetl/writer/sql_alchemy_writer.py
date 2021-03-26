from sqlalchemy.exc import SQLAlchemyError
from dwetl.writer.writer import Writer
from dwetl.exceptions import DWETLException
import pdb
import dwetl


class SqlAlchemyWriter(Writer):
    """
    Updates a database table using the given row dictionary.
    """
    def __init__(self, session, table_base_class):
        """
        Constructs the writer
        :param session: the SqlAlchemy session object to use
        :param table_base_class: the SqlAlchemy table base class to write to
        """
        self.session = session
        self.table_base_class = table_base_class
        

    def write_row(self, row_dict):
        # check to see if row_dict contains uneeded columns
        # some values are in stage 2, but do not move forward in ETL
        # ex: in_z13_call_no in dw_stg_2_bib_rec_z13
        relevant_row_dict = {}
        for key, val in row_dict.items():
            columns = self.table_base_class.__table__.columns.keys()
            if key in columns:
                relevant_row_dict[key] = val
        record = self.table_base_class(**relevant_row_dict)

        # get list of primary keys from table_base_class
        pk_list = []
        pk_values = self.table_base_class.__table__.primary_key.columns.values()
        for i, key in enumerate(pk_values):
            pk_list.append(pk_values[i].name)

        # check to see if list of pks are in the row_dict
        for pk in pk_list:
            in_dict = False
            if pk in row_dict:
                in_dict = True
            else:
                in_dict = False


        # Update the row if PK list is found in row
        if in_dict == True:
            self.session.merge(record)
        else:
        # Add new row if PK list is not found in row
            self.session.add(record)

        # flush record and catch exceptions. 
        # the commit happens later in __init__.py of dwetl
        try:
            self.session.flush()

        except SQLAlchemyError as e:
            # undo the adding of the relevant record
            self.session.rollback()
            raise DWETLException(e)
        
            