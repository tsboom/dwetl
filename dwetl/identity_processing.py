from dwetl.processing_step import ProcessingStep


class IdentityProcessing(ProcessingStep):
    """
    Processing step for that simply passes the data, unchanged, from the
    reader to the writer.

    This class is primarily intended for testing.
    """
    def __init__(self, reader, writer, job_info, logger):
        super().__init__(reader, writer, job_info, logger)

    @classmethod
    def create(cls, reader, writer, job_info, logger):
        return IdentityProcessing(reader, writer, job_info, logger)

    def job_name(self):
        return 'IdentityProcessing'

    def process_item(self, item):
        return item


