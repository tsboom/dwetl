class Processor:
    """
    Abstract class that encapsulates a processing step.

    Subclasses should implement the "job_name" and "process_item" methods.
    """
    def __init__(self, reader, writer, job_info, logger):
        self.reader = reader
        self.writer = writer
        self.job_info = job_info
        self.logger = logger

    def execute(self):
        for item in self.reader:
            result = self.process_item(item)
            self.writer.write_row(result)

    def job_name(self):
        raise NotImplementedError

    def process_item(self, item):
        raise NotImplementedError
