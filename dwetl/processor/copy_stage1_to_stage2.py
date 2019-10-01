from dwetl.processor.processor import Processor
import datetime


class CopyStage1ToStage2(Processor):
    """
    Processor for creating the file equivalent tables from
    TSV files.

    This processing step simply appends the job_info to the given
    item, and returns the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger, aleph_library):
        super().__init__(reader, writer, job_info, logger)
        self.aleph_library = aleph_library

    @classmethod
    def create(cls, reader, writer, job_info, logger, aleph_library):
        return CopyStage1ToStage2(reader, writer, job_info, logger, aleph_library)

    def job_name(self):
        return 'CopyStage1ToStage2'

    def process_item(self, item):
        processed_item = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']

        for key, value in item.items():
            if key in invalid_keys:
                continue

            new_key = key
            if not (key.startswith('em') or key == 'db_operation_cd'  or key =='dw_stg_1_marc_rec_field_seq_no'):
                new_key = 'in_' + key

            processed_item[new_key] = value

        # Update metadata
        if self.aleph_library:
            processed_item['dw_stg_2_aleph_lbry_name'] = self.aleph_library

        processed_item['em_create_dw_job_name'] = self.job_name()

        processed_item.update(self.job_info.as_dict('create'))
        processed_item['em_create_tmstmp'] = datetime.datetime.now()
        return processed_item
