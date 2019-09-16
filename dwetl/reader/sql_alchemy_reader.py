import csv


class SqlAlchemyReader:
    """
    Reads a SQLAlchemy table from the database, returning a Dictionary of
    key/value pairs.

    """
    def __init__(self, session, table_base_class, processing_cycle_field_name, processing_cycle_id):
        """
        Constructs a new SqlAlchemyReader.

        :param session: the SqlAlchemy session object to use
        :param table_base_class: the SqlAlchemy table base class to write to
        """
        self.session = session
        self.table_base_class = table_base_class
        self.process_cycle_field_name = processing_cycle_field_name
        self.processing_cycle_id = processing_cycle_id
        query_field = getattr(self.table_base_class, processing_cycle_field_name)
        self.query = self.session.query(self.table_base_class).filter(query_field == processing_cycle_id)

    def __iter__(self):
        for row in self.query.all():
            yield row.__dict__
