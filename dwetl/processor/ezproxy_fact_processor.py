from dwetl.processor.processor import Processor

import dwetl
import datetime
import pdb
import pprint


class EzproxyFactProcessor(Processor):
    """
    Processor for moving final values from intertable processing into fact table

    This processing step simply appends the job_info to the given
    item, and returns the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger, max_ezp_sessns_snap_fact_key):
        super().__init__(reader, writer, job_info, logger)
        self.invalid_keys = ['_sa_instance_state']
        self.primary_keys = ['em_create_dw_prcsng_cycle_id', 'in_ezp_sessns_snap_tmstmp', 'in_mbr_lbry_cd']
        self.em_create_keys = ['em_create_dw_job_exectn_id', 'em_create_dw_job_name', 'em_create_dw_job_version_no', 'em_create_user_id', 'em_create_tmstmp']
        self.max_ezp_sessns_snap_fact_key = max_ezp_sessns_snap_fact_key
        self.em_metadata_keys = ['em_update_dw_job_exectn_id', 'em_create_dw_job_version_no', 'em_update_user_id' ]

    def job_name(self):
        return 'EzproxyFactProcessor'


    @classmethod
    def create(cls, reader, writer, job_info, logger, max_ezp_sessns_snap_fact_key):
        return EzproxyFactProcessor(reader, writer, job_info, logger, max_ezp_sessns_snap_fact_key)

    def job_name(self):
        return 'EzproxyFactProcessor'

    def process_item(self, item):
        processed_item = {}

        new_key = ''
        for key, value in item.items():
            if key in self.invalid_keys:
                continue
            if key in self.primary_keys:
                processed_item[key] = value
            if key in self.em_create_keys:
                processed_item[key] = value
            if key in self.em_metadata_keys:
                processed_item[key] = value
            if key.startswith('t'):
                key_split =key.split('__')
                # get target col name from transform
                if len(key_split) == 2:
                    new_key = key.split('__')[1]
                else:
                    target_col_name_list = key.split('_')[1:]
                    new_key = '_'.join(target_col_name_list)

                processed_item[new_key] = value

        processed_item['em_update_dw_job_name'] = self.job_name()

        processed_item.update(self.job_info.as_dict('create'))
        processed_item['em_update_tmstmp'] = datetime.datetime.now()

        #self.max_ezp_sessns_snap_fact_key = self.max_ezp_sessns_snap_fact_key + 1
        #ezp_essns_snap_fact_key = self.max_ezp_sessns_snap_fact_key

        #processed_item['ezp_sessns_snap_fact_key'] = ezp_essns_snap_fact_key
        pprint.pprint(item)
        pprint.pprint(processed_item)
        return processed_item
