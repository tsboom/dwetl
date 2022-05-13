from dwetl.processor.processor import Processor
import datetime
import pdb
import pprint


class CopyStage1ToStage2(Processor):
    """
    Processor for moving over FET values to in_ values in stage 2.

    This processing step simply appends the job_info to the given
    item, and returns the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger, aleph_library, error_writer):
        super().__init__(reader, writer, job_info, logger, error_writer)
        self.aleph_library = aleph_library
        self.invalid_keys = ['rec_type_cd', '_sa_instance_state', 'usmai_mbr_lbry_mbrshp_type_cd']
        self.valid_mai50_z35_event_type =['50', '52', '54', '56', '91', '58', '61', '82', '62', '63', '64']
    @classmethod
    def create(cls, reader, writer, job_info, logger, aleph_library, error_writer):
        return CopyStage1ToStage2(reader, writer, job_info, logger, aleph_library, error_writer)

    def job_name(self):
        return 'CopyStage1ToStage2'

    def process_item(self, item):
        processed_item = {}
        if 'z35_event_type' in item.keys() and item['z35_event_type'] not in self.valid_mai50_z35_event_type:
            return None

        for key, value in item.items():
            if key in self.invalid_keys:
                continue

            new_key = key
            # Put 'in_' in front of keys that need it
            # TODO: is this the best way to deal with usmai_mbr_lbry_mbrshp_type_cd?
            unaltered_keys = ['db_operation_cd', 'rec_trigger_key', 'lbry_staff_lms_user_id', 'db_operation_effective_date']
            if not (key.startswith('em') or key in unaltered_keys):
                new_key = 'in_' + key

            processed_item[new_key] = value

        # Update metadata
        if self.aleph_library:
            processed_item['dw_stg_2_aleph_lbry_name'] = self.aleph_library

        processed_item['em_create_dw_job_name'] = self.job_name()

        processed_item.update(self.job_info.as_dict('create'))
        processed_item['em_create_tmstmp'] = datetime.datetime.now()
        #pdb.set_trace()
        return processed_item
