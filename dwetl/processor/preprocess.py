from dwetl.processor.processor import Processor
import datetime
import pdb
import pprint

class Preprocess(Processor):
    """
    Processor for Preprocessing
    """

    def __init__(self, reader, writer, job_info, logger, json_config, pk_list, error_writer):
        super().__init__(reader, writer, job_info, logger, error_writer)
        self.json_config = json_config
        self.stg2_pk_list = pk_list

    def job_name(self):
        return 'Preprocessing'

    @classmethod
    def need_preprocess(cls, json_config, key):
        """
        Given a key from item, returns True if preprocess is needed
        based on the json_config
        """
        try:
            # find matching key in the json_config remove the "in_"
            key_json = json_config[key[3:]]
            # get preprocess stanza out
            if key_json['preprocessing_info']['pre_action'] == 'Trim':
                return True
            else:
                return False
        except KeyError:
            # TODO: not sure about this
            return False
        
    @classmethod
    def is_mandatory(cls, json_config, key):
        """
        Given a key from item, returns True if field is mandatory
        """
        try:
            # find matching key in the json_config remove the "in_"
            key_json = json_config[key[3:]]
            # get preprocess stanza out
            if key_json['preprocessing_info']['pre_action'] == 'Trim':
                return True
            else:
                return False
        except KeyError:
            # TODO: not sure about this
            return False

    @classmethod
    def preprocess(cls, item, json_config, pk_list):
        """
        if need_preprocess is true, trim the item
        """

        out_dict = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']

        for key, val in item.items():
            # skip invalid keys and dq and t and pp keys
            if key in invalid_keys or key.startswith('dq_') or key.startswith('t') or key.startswith('rm_') or key.startswith('pp_'):
                continue

            # add primary keys and values to result
            if key in pk_list:
                out_dict[key] = val

            # find out if the in_ key needs preprocessing
            need_preprocess = Preprocess.need_preprocess(json_config, key)            

            # convert key name to pp_keyname
            pp_key = key.replace('in_', 'pp_')
            
            if need_preprocess:
                # strip if None,
                if val == '':
                    result = val
                elif val:
                    result = val.strip()
                else:
                    result = val
                out_dict[pp_key] = result
            else:
                out_dict[pp_key] = val
        return out_dict

    def process_item(self, item):
        processed_item = Preprocess.preprocess(item, self.json_config, self.stg2_pk_list)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
