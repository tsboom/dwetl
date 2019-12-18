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
    def suspend_record(cls, key, data_quality_info):
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
        Takes values from 'pp_' fields and runs DQ checks, adding replacement
        values if needed.

        Suspends record if needed.
        """
        out_dict = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']

        for key, val in item.items():
            if key in invalid_keys:
                continue

            # add the pks to the out_dict so the row can be inserted later
            if key in pk_list:
                out_dict[key] = val

            # skip keys from invalid_keys and keys that aren't 'pp_'
            if not key.startswith('pp_'):
                continue

            # get DQ checks for current key
            dq_list = DataQualityProcessor.get_dq_checks_for_key(key, json_config)
            dq_key = key.replace('pp_', 'dq_')

            if dq_list:
                for dq_check in dq_list:
                    # create DataQualityInfo for each DQ check
                    data_quality_info = DataQualityInfo(dq_check)
                    # determine if value passes check
                    is_passing = data_quality_info.validate(val)

                    if is_passing:
                        # write value to out_dict because it passes
                        out_dict[dq_key] = val
                    else:
                        # check for suspend record
                        if data_quality_info.suspend_record:
                            print('SUSPEND ', key, val)
                            
                            #TODO: how exactly to suspend a record again?
                        else:
                            # find replacement and use it if needed
                            out_dict[dq_key] = data_quality_info.replacement_value
            else:
                # if there are no dq checks, output the pp value to dq
                out_dict[dq_key] = val

        return out_dict


    def process_item(self, item):
        processed_item = DataQualityProcessor.check_data_quality(item, self.json_config, self.stg2_pk_list)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
