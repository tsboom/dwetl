from dwetl.processor.processor import Processor
from dwetl.data_quality_utilities import trim
import datetime
import pdb

class Preprocess(Processor):
    """
    Processor for Preprocessing, Dataquality checks, and Transforms
    of "in_values" in stage 2 tables.
    Inter-table Processing
    """

    def __init__(self, reader, writer, job_info, logger, json_config, pk_list):
        super().__init__(reader, writer, job_info, logger)
        self.json_config = json_config
        self.stg2_pk_list = pk_list

    def job_name(self):
        return 'PreprocessProcessor'

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
    def preprocess(cls, item, json_config, pk_list):
        """
        if need_preprocess is true, trim the item
        """
        preprocessed_item = {}
        invalid_keys = ['rec_type_cd', 'rec_trigger_key', '_sa_instance_state']

        for key, val in item.items():
            if key in invalid_keys:
                continue
            need_preprocess = Preprocess.need_preprocess(json_config, key)

            # convert key name to pp_keyname
            pp_key = key.replace('in_', 'pp_')

            # for every pk column, write the key and value to the preprocessed_item dict
            if key in pk_list:
                preprocessed_item[key] = val
            if need_preprocess:
                result = trim(val)
                preprocessed_item[pp_key] = result
            else:
                preprocessed_item[pp_key] = val
        return preprocessed_item

    def process_item(self, item):
        processed_item = Preprocess.preprocess(item, self.json_config, self.stg2_pk_list)
        processed_item.update(self.job_info.as_dict('update'))
        processed_item['em_update_dw_job_name'] = self.job_name()
        processed_item['em_update_tmstmp'] = datetime.datetime.now()
        return processed_item
