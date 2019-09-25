from dwetl.processor.processor import Processor
import datetime


class LoadZ00FieldTsv(Processor):
    """
    Processor for creating the file equivalent tables from
    Z00 Field TSV files.

    """
    def __init__(self, reader, writer, job_info, logger):
        super().__init__(reader, writer, job_info, logger)

    @classmethod
    def create(cls, reader, writer, job_info, logger):
        return LoadZ00FieldTsv(reader, writer, job_info, logger)

    def job_name(self):
        return 'LoadZ00FieldTsv'


    def process_item(self, item):
        # create new dict because item needs extra processing
        # to remove/duplicate columns
        processed_item = {}

        # rec_type_cd is 'D' for data
        processed_item['rec_type_cd'] = 'D'
        # db_operation_cd is I for insert because this table is for new events
        processed_item['db_operation_cd'] = 'I'
        # repeat z00_doc_number
        processed_item['rec_trigger_key'] = item['z00_doc_number']
        processed_item['z00_doc_number'] = item['z00_doc_number']

        processed_item['z00_marc_rec_field_cd'] = item['z00_marc_rec_field_cd']
        processed_item['z00_marc_rec_field_txt'] = item['z00_marc_rec_field_txt']

        processed_item.update(self.job_info.as_dict('create'))
        processed_item['em_create_dw_job_name'] = self.job_name()
        processed_item['em_create_tmstmp'] = datetime.datetime.now()
        return processed_item
