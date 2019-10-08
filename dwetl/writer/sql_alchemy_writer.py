from sqlalchemy import exc
from dwetl.writer.writer import Writer
import pdb


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
        try:
            # insert the matching keys row into SQLAlchemy table base class
            record = self.table_base_class(**row_dict)

            # get list of primary keys from table_base_class
            pk_list = []
            pk_values = self.table_base_class.__table__.primary_key.columns.values()
            for i, key in enumerate(pk_values):
                # index = pk_values.index(key)
                pk_list.append(pk_values[i].name)

            # Update the row if PK list is found in row

            for pk in pk_values:
                in_dict = False
                if pk in row_dict.keys():
                    in_dict == True
                else:
                    in_dict == False
            pdb.set_trace()
            if in_dict == True:
                pdb.set_trace()
                self.session.merge(record)
            else:
                # Add new row if PK list is not found in row
                self.session.add(record)

        except exc.SQLAlchemyError as e:
            self.session.rollback()
