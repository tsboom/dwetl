from dwetl.processor.processor import Processor
from dwetl.data_quality_info import DataQualityInfo
import dwetl.data_quality_utilities as dqu
from dwetl.exceptions import DataQualityException
from sqlalchemy import func
import dwetl
import datetime
import pdb
import pprint

# utility class to hold dq failure info
class DataQualityFailure:
    def __init__(self, out_dict, error):
        self.out_dict = out_dict
        self.error = error    

class DataQualityProcessor(Processor):


    '''
    Processor for doing data quality checks
    '''

    def __init__(self, reader, writer, job_info, logger, json_config, pk_list, error_writer):
        super().__init__(reader, writer, job_info, logger, error_writer)
        self.json_config = json_config
        self.stg2_pk_list = pk_list


    def job_name(self):
        return 'DataQualityProcessor'

    @classmethod
    def get_dq_checks_for_key(cls, key, json_config, item):
        # get list of DQ check objects from json_config 
        # TODO: need to do only the checks for the right aleph library.
        try:
            key_json = json_config[key]
            dq_list = key_json['dataquality_info']
            aleph_library = item['dw_stg_2_aleph_lbry_name']
            
            matching_library_dq_list = []
            # need to find the dq checks for the current aleph library
            for dq in dq_list:
                # sometimes there are more than one library listed
                libraries = [x.lower() for x in dq['aleph_library'].split(',')]
                if aleph_library in libraries:
                    matching_library_dq_list.append(dq)
            return matching_library_dq_list
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
        
    @classmethod
    def check_mandatory(cls, key, value, json_config):
        # check if Mandatory
        key_json = json_config[key]
        mandatory = key_json['transformation_steps'][0]['transformation_info']['source_mandatory']
            
        if mandatory == 'Y':
            try:
                # check if value is not None
                # an empty string is not None. it is True
                if value:
                    pass
            except DWETLException as e:
                #TODO: raise exception if key is mandatory but its value is missing
                pdb.set_trace() 
    
    @classmethod
    def handle_failed_dq(cls, logger, out_dict, data_quality_info, item, dq_key, val):
        # suspend the record if needed
        if data_quality_info.suspend_record:
            
            # out_dict for the current dq_ key contains same value.
            out_dict[dq_key] = 'SUS'

            # change suspend record flag
            suspend_record_flag = "Y"
            out_dict['rm_suspend_rec_flag'] = suspend_record_flag

            # get suspend record code
            suspend_record_code = DataQualityProcessor.get_suspend_record_code(dq_key, data_quality_info)
            out_dict['rm_suspend_rec_reason_cd'] = suspend_record_code
            
            # raise and log error exception
            error_text = f'SUSPENDED RECORD. {dq_key} with value of {val} failed {data_quality_info.type}.'
            error = {
                "error_type": data_quality_info.type,
                "error_text": error_text,
                "error_row": str(item)
            }
            logger.error(error_text)

        else:
            # find replacement and use it if needed
            out_dict[dq_key] = data_quality_info.replacement_value
        
            error_text = f'FAILED. {dq_key} failed {data_quality_info.type}. Replacement value is {data_quality_info.replacement_value}.'
            error = {
                "error_type": data_quality_info.type,
                "error_text": error_text,
                "error_row": str(item)
            }
            logger.error(error_text)
        failed_dq = DataQualityFailure(out_dict, error)
        return failed_dq
            
            
                
    @classmethod
    def check_data_quality(cls, item, json_config, pk_list, logger, error_writer):
        """
        Takes values from 'pp_' fields and runs DQ checks, adding replacement
        values if needed.

        Suspends record if needed.
        """
        # out dict to hold the processed item
        out_dict = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']
        
        # keep track of total dq exception number
        dq_exception_count = 0

        for key, value in item.items():


            if key in invalid_keys:
                continue

            # add the pks to the out_dict so the row can be inserted later
            if key in pk_list:
                out_dict[key] = value

            # skip keys from invalid_keys and keys that aren't 'pp_'
            if not key.startswith('pp_'):
                continue

            # if 'pp_' value Mandatory and is empty, raise DWETLException and skip item
            clean_key = key[3:]
            key_json = json_config[clean_key]

            # check if mandatory and raise exception if not
            DataQualityProcessor.check_mandatory(clean_key, value, json_config)

            # get DQ checks for current key
            dq_list = DataQualityProcessor.get_dq_checks_for_key(clean_key, json_config, item)
            dq_key = key.replace('pp_', 'dq_')
            
            # create dict of dq_key's exceptions 
            current_key_exception_count = {}
            current_key_exception_count[dq_key] = 0
            
            # do DQ checks if exist
            if dq_list:
                for dq_check in dq_list:
                    
                    # create DataQualityInfo for each DQ check
                    data_quality_info = DataQualityInfo(dq_check)
                    

                    
                    # if the *current* value has an exception count of 1, it likely has a missing value
                    # skip the check if it has "only if data exists" flag
                    if current_key_exception_count[dq_key] == 1 and data_quality_info.only_if_data_exists:
                        break
                        
                    # trim trailing spaces of the value
                    # might cause problems for sublibrary code and collection code
                    if value:
                        val = value.rstrip()
                    else:
                        val = value
                    
                    
                        
                    # determine if value passes check
                    is_passing = data_quality_info.validate(val)
                        
                        
                    if is_passing:
                        # write value to out_dict because it passes
                        out_dict[dq_key] = val
                        out_dict['rm_dq_check_excptn_cnt'] = dq_exception_count
                        continue
                    else:
                        # handle failing dq check
                        current_key_exception_count[dq_key] = current_key_exception_count[dq_key] + 1
                        dq_exception_count = dq_exception_count + 1
                        out_dict['rm_dq_check_excptn_cnt'] = dq_exception_count
                    

                        
                        failed_dq = DataQualityProcessor.handle_failed_dq(logger, out_dict, data_quality_info, item, dq_key, val)
                        
                        # handle out dict
                        out_dict = failed_dq.out_dict
                        
                        # Get the error message and write to the error table
                        error = failed_dq.error
                        
                        # Increment dw_error_id value from the table or set as 1 for the first time
                        error_table_base_class = dwetl.Base.classes['dw_db_errors']
                        
                        max_dw_error_id = error_writer.session.query(func.max(error_table_base_class.dw_error_id)).scalar()
                        if max_dw_error_id ==  None: 
                            dw_error_id = 1
                        else:
                            dw_error_id = max_dw_error_id + 1
                        
                        # create error row dictionary that will be added to the error table
                        error_row_dict = {
                            'dw_error_id': dw_error_id,
                            'dw_error_type': error['error_type'],
                            'dw_error_text': error['error_text'],
                            'dw_error_row': error['error_row'],
                            'em_create_dw_prcsng_cycle_id': item['em_create_dw_prcsng_cycle_id'],
                            'em_create_dw_job_name': item['em_create_dw_job_name'],
                            'em_create_dw_job_version_no': item['em_create_dw_job_version_no'],
                            'em_create_user_id': item['em_create_user_id'],
                            'em_create_tmstmp': item['em_create_tmstmp'],
                            'em_create_dw_job_exectn_id': item['em_create_dw_job_exectn_id'],

                        }
                        # write error to the error table
                        error_record = error_writer.write_row(error_row_dict)

            else:
                # if there are no dq checks, output the pp value to dq
                out_dict[dq_key] = value
        return out_dict


    def process_item(self, item):
        processed_item = DataQualityProcessor.check_data_quality(item, self.json_config, self.stg2_pk_list, self.logger, self.error_writer)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        # if 'in_z13u_user_defined_2' in item:
        #     if item['in_z13u_user_defined_2'] == 'osm00001986':
        #         pdb.set_trace()
        return processed_item
