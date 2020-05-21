from dwetl.processor.processor import Processor
from sqlalchemy import func
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
    def __init__(self, reader, writer, job_info, logger):
        super().__init__(reader, writer, job_info, logger)
        self.invalid_keys = ['_sa_instance_state']
        self.primary_keys = ['em_create_dw_prcsng_cycle_id', 'in_ezp_sessns_snap_tmstmp', 'in_mbr_lbry_cd']
        self.em_create_keys = ['em_create_dw_job_exectn_id', 'em_create_dw_job_name', 'em_create_dw_job_version_no', 'em_create_user_id', 'em_create_tmstmp']
        self.em_metadata_keys = ['em_update_dw_job_exectn_id', 'em_create_dw_job_version_no', 'em_update_user_id' ]
    def job_name(self):
        return 'EzproxyFactProcessor'

    @staticmethod
    def get_ezp_sessns_snap_fact_key():

        with dwetl.reporting_database_session() as session2:
            fact_table = dwetl.ReportingBase.classes['fact_ezp_sessns_snap']
            max_ezp_sessns_snap_fact_key = session2.query(func.max(fact_table.ezp_sessns_snap_fact_key)).scalar()
            print(max_ezp_sessns_snap_fact_key)


        # increments ezp_sessns_snap_fact_key by 1
        if max_ezp_sessns_snap_fact_key == None:
            ezp_sessns_snap_fact_key = 1
        else:
            ezp_sessns_snap_fact_key = max_ezp_sessns_snap_fact_key + 1

        return ezp_sessns_snap_fact_key



    @classmethod
    def create(cls, reader, writer, job_info, logger):
        return EzproxyFactProcessor(reader, writer, job_info, logger)

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

        ezp_essns_snap_fact_key = EzproxyFactProcessor.get_ezp_sessns_snap_fact_key()
        processed_item['ezp_sessns_snap_fact_key'] = ezp_essns_snap_fact_key
        pprint.pprint(processed_item)
        return processed_item
