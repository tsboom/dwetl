from dwetl.processor.processor import Processor
import datetime


class LoadAlephTsv(Processor):
    """
    Processor for creating the file equivalent tables from
    TSV files.

    This processing step simply appends the job_info to the given
    item, and returns the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger):
        super().__init__(reader, writer, job_info, logger)

    @classmethod
    def create(cls, reader, writer, job_info, logger):
        return LoadAlephTsv(reader, writer, job_info, logger)

    def job_name(self):
        return 'LoadAlephTsv'

    def process_item(self, item):
        item.update(self.job_info.as_dict('create'))
        item['em_create_dw_job_name'] = self.job_name()
        item['em_create_tmstmp'] = datetime.datetime.now()
        return item
