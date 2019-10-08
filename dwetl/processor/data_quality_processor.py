from dwetl.processor.processor import Processor
from dwetl.data_quality_info import DataQualityInfo
from dwetl.data_quality_utilities import trim
import datetime
import pdb

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
    def check_data_quality(cls, item, json_config, pk_list):
        """
        if need_preprocess is true, trim the item
        """
        data_quality_checked_item = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']

        for key, val in item.items():
            if key in invalid_keys:
                continue
            pdb.set_trace()

            # get list of DQ objects from json_config
            if key.startswith('in_'):
                orig_key = key[3:]
            try:
                key_json = json_config[orig_key]
            except:
                print(orig_key, 'not found')
                pass

            # get DQ checks for current key

            # create DataQualityInfo for each DQ check
            data_quality_info = DataQualityInfo(json_config)

            #data quality check is applid only on keys with 'pp_' prefix




            #
            # # convert key name to pp_keyname
            # dq_key = key.replace('pp_', 'dq_')
        #
        #
        #     if need_preprocess:
        #         result = trim(val)
        #         preprocessed_item[pp_key] = result
        #     else:
        #         preprocessed_item[pp_key] = val
        # return preprocessed_item

    def process_item(self, item):
        processed_item = DataQualityProcessor.check_data_quality(item, self.json_config, self.stg2_pk_list)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
