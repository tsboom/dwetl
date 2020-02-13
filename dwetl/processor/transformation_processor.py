from dwetl.processor.processor import Processor
from dwetl.transformation_info import TransformationInfo
import dwetl.specific_transform_functions as specific_transform_functions
import datetime
import pdb
import pprint

class TransformationProcessor(Processor):
    '''
    Processor for running transform functions
    '''
    
    def __init__(self, reader, writer, job_info, logger, json_config, pk_list):
        super().__init__(reader, writer, job_info, logger)
        self.json_config = json_config
        self.stg2_pk_list = pk_list
        
    def job_name(self):
        return 'TransformationProcessor'
        
    @classmethod
    def get_transformations_for_key(cls, key, json_config):
        try:
            key_json = json_config[key[3:]]
            transform_steps = key_json['transformation_steps']
            
            return transform_steps
        except:
            return None 
    
    @classmethod 
    def transform_item(cls, item, json_config, pk_list, logger):
        """
        Takes values from the 'dq' field and runs transformations. 
        Transformed values are stored in t1_, t2_, t3_, ...
        """
        
        # out dict to hold the transformed item info 
        out_dict = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']
        
        # transform keys and vals within current item
        for key, val in item.items():
            
            # skip invalid keys
            if key in invalid_keys:
                continue

            # add the pks to the out_dict so the row can be inserted later 
            if key in pk_list:
                out_dict[key] = val

            # only process dq values. skip keys from invalid_keys and keys that aren't 'dq_'
            if not key.startswith('dq_'):
                continue
            
            # skip suspended records 
            if item.get('rm_suspend_rec_flag') == 'Y':
                # dont' do anything for suspended records
                continue

            # get transformations for current key
            transform_steps = TransformationProcessor.get_transformations_for_key(key, json_config)
            
            # transform 
            if transform_steps:
                for transformation in transform_steps:
                    # create TransformationInfo per transformation 
                    transformation_info = TransformationInfo(transformation)
                    
                    # get index of current transformation (for t1, t2, etc)
                    index = transform_steps.index(transformation)
                    transform_number = index + 1
                    
                    # run transformation 
                    transform_result = transformation_info.transform(val)
                    
                    # form the column name to write to for t1_sourcecolumn_targetcolumn, t2...
                    target_column = transformation_info.target_col_name
                    source_column = transformation_info.source_col_name
                    
                    transform_column_name = f"t{transform_number}_{source_column}__{target_column}"
                    
                    # write to outdict 
                    out_dict[transform_column_name] = transform_result
                    
        return out_dict
                    
                    
    def process_item(self, item):
        processed_item = TransformationProcessor.transform_item(item, self.json_config, self.stg2_pk_list, self.logger)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
    
            
