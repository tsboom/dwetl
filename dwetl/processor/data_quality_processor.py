from dwetl.processor.processor import Processor
from dwetl.data_quality_info import DataQualityInfo
import dwetl.data_quality_utilities as dqu
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
    def get_suspend_record_code(cls, key, data_quality_info):
        # write suspend record reason code (use lookup table)
        suspend_record_dict = dqu.create_dict_from_csv('suspend_record_reason_code.csv')
        suspend_record_type = data_quality_info.type
        for k, v in suspend_record_dict.items():
            if v == data_quality_info.type:
                suspend_record_code = k
        return suspend_record_code
        
        

        
    # @classmethod
    # def write_to_log(cls, )
        

    @classmethod
    def check_data_quality(cls, item, json_config, pk_list):
        """
        Takes values from 'pp_' fields and runs DQ checks, adding replacement
        values if needed.

        Suspends record if needed.
        """
        # out dict to hold the processed item
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
            
            

            # keep track of dq exception number
            dq_exception_count = 0 
            
            # do DQ checks if exist
            if dq_list:
                for dq_check in dq_list:
                    # create DataQualityInfo for each DQ check
                    data_quality_info = DataQualityInfo(dq_check)
                    
                    # trim trailing spaces of the value 
                    # might cause problems for sublibrary code and collection code
                    val = val.rstrip()
                    
                    # determine if value passes check
                    is_passing = data_quality_info.validate(val)
                    
                    # if the value has an exception count of 1, it likely has a missing value 
                    # skip the check if it has "only if data exists" flag
                    if dq_exception_count == 1 and data_quality_info.only_if_data_exists: 
                        continue 

                    if is_passing:
                        # write value to out_dict because it passes
                        out_dict[dq_key] = val
            
                    else:
                        # check for suspend record is True
                        if data_quality_info.suspend_record:
                            # out_dict for the current dq_ key contains same value. 
                            out_dict[dq_key] = 'SUS'
                            
                            # change suspend record flag 
                            suspend_record_flag = "Y"
                            out_dict['rm_suspend_rec_flag'] = suspend_record_flag
                            # increment exception count
                            dq_exception_count = dq_exception_count + 1
                            
                            out_dict['rm_dq_check_excptn_cnt'] = dq_exception_count
                            
                            # get suspend record code
                            suspend_record_code = DataQualityProcessor.get_suspend_record_code(dq_key, data_quality_info)
                            out_dict['rm_suspend_rec_reason_cd'] = suspend_record_code
                            
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
