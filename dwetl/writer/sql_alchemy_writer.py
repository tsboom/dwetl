from sqlalchemy import exc
from dwetl.writer.writer import Writer


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
            # TODO: check if row_dict keys are in the db, only put matching keys and
            # values into the record
            matching_row_dict = {}
            # insert the row into SQLAlchemy table base class
            record = self.table_base_class(**matching_row_dict)
            self.session.add(record)
        except exc.SQLAlchemyError as e:
            self.session.rollback()
