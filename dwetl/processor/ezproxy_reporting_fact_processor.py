from dwetl.processor.processor import Processor

import dwetl
import datetime
import pdb
import pprint


class EzproxyReportingFactProcessor(Processor):
    """
    Processor for moving final values from fact table to the reporting db

    This processing step simply appends the job_info to the given
    item, and returns the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger):
        super().__init__(reader, writer, job_info, logger)
        self.invalid_keys = ['_sa_instance_state']


    @classmethod
    def create(cls, reader, writer, job_info, logger):
        return EzproxyReportingFactProcessor(reader, writer, job_info, logger)

    def job_name(self):
        return 'EzproxyReportingFactProcessor'

    def process_item(self, item):
        processed_item = {}
        new_key = ''
        for key, value in item.items():
            if key in self.invalid_keys:
                continue
            else:
                processed_item[key] = value
        # add rm metadata
        processed_item['rm_rec_type_cd'] = "R"
        processed_item['rm_current_rec_flag'] = "Y"
        processed_item['rm_rec_version_no'] = "1"
        processed_item['rm_rec_type_desc'] = "Regular Fact Record"
        processed_item['rm_rec_effective_to_dt'] = "9999-12-31"
        processed_item['rm_rec_effective_from_dt'] = item['ezp_sessns_snap_tmstmp']

        processed_item['em_create_dw_job_name'] = self.job_name()

        processed_item.update(self.job_info.as_dict('create'))
        processed_item['em_create_tmstmp'] = datetime.datetime.now()
        return processed_item
