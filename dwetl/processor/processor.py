import pdb
import pprint

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
        for row_dict in self.reader:
            processed_row_dict = self.process_item(row_dict)
            
            if processed_row_dict:
                self.writer.write_row(processed_row_dict)

    def job_name(self):
        raise NotImplementedError

    def process_item(self, item):
        raise NotImplementedError
