from dwetl.processor.processor import Processor
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
        self.invalid_keys = ['_sa_instance_state', 'usmai_mbr_lbry_mbrshp_type_cd']

    @classmethod
    def create(cls, reader, writer, job_info, logger):
        return EzproxyFactProcessor(reader, writer, job_info, logger)

    def job_name(self):
        return 'EzproxyFactProcessor'

    def process_item(self, item):
        processed_item = {}
        
        new_key = ''
        for key, value in item.items():
            if key.startswith('t'):
                key_split =key.split('__')
                # get target col name from transform
                if len(key_split) == 2:
                    new_key = key.split('__')[1]
                else:
                    target_col_name_list = key.split('_')[1:]
                    new_key = '_'.join(target_col_name_list)

                processed_item[new_key] = value
        
        processed_item['em_create_dw_job_name'] = self.job_name()

        processed_item.update(self.job_info.as_dict('create'))
        processed_item['em_create_tmstmp'] = datetime.datetime.now()
        
        return processed_item
