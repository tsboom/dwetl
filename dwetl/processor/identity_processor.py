from dwetl.processor.processor import Processor


class IdentityProcessor(Processor):
    """
    Processing step for that simply passes the data, unchanged, from the
    reader to the writer.

    This class is primarily intended for testing.
    """
    def __init__(self, reader, writer, job_info, logger, error_writer):
        super().__init__(reader, writer, job_info, logger, error_writer)

    def job_name(self):
        return 'IdentityProcessor'

    def process_item(self, item):
        return item


