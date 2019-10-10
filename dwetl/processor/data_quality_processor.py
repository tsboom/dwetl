from dwetl.processor.processor import Processor
from dwetl.data_quality_info import DataQualityInfo
import datetime
import pdb
import pprint

class DataQualityProcessor(Processor):


    '''
    Processor for doing data quality checks
    '''

    def __init__(self, reader, writer, job_info, logger, json_config, pk_list):
        super().__init__(reader, writer, job_info, logger)
        self.json_config = json_config
        self.stg2_pk_list = pk_list


    def job_name(self):
        return 'DataQualityProcessor'

    @classmethod
    def get_dq_checks_for_key(cls, key, json_config):
        # get list of DQ check objects from json_config
        try:
            key_json = json_config[key[3:]]
            dq_list = key_json['dataquality_info']
            return dq_list
        except:
            return None


    @classmethod
    def check_data_quality(cls, item, json_config, pk_list):
        """
        if need_preprocess is true, trim the item
        """
        out_dict = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']

        for key, val in item.items():
            # skip keys from invalid_keys and keys that aren't 'pp_'
            if key in invalid_keys:
                continue
            if not key.startswith('pp_'):
                continue

            if key in pk_list:
                out_dict[key] = val


            # get DQ checks for current key
            dq_list = DataQualityProcessor.get_dq_checks_for_key(key, json_config)

            if dq_list:
                for dq_check in dq_list:
                    # create DataQualityInfo for each DQ check
                    data_quality_info = DataQualityInfo(dq_check)

                # # convert key name to pp_keyname
                # dq_key = key.replace('pp_', 'dq_')


    def process_item(self, item):
        processed_item = DataQualityProcessor.check_data_quality(item, self.json_config, self.stg2_pk_list)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
