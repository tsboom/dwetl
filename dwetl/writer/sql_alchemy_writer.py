from sqlalchemy import exc


class SqlAlchemyWriter:
    def __init__(self, session, table_base_class):
        self.session = session
        self.table_base_class = table_base_class

    def write_row(self, row_dict):
        try:
            # insert the row into SQLAlchemy table base class
            record = self.table_base_class(**row_dict)
            self.session.add(record)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
