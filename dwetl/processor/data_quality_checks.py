from dwetl.processor.processor import Processor
import dwetl.data_quality_utilities as dqu

class DataQualityChecks(Processor):
    """
    Processor for performing data quality checks.

    This processing steps performs the data quality checks and
    updates the given item, returning the resulting dictionary.
    """
    def __init__(self, reader, writer, job_info, logger, table_config):
        super().__init__(reader, writer, job_info, logger)
        self.table_config = table_config

    @classmethod
    def create(cls, reader, writer, job_info, logger, table_config):
        return DataQualityChecks(reader, writer, job_info, logger, table_config)

    def job_name(self):
        return 'DataQualityChecks'

    def process_item(self, item):
        in_field_names = [key for (key) in item.keys() if key.startswith('in_')]
        for field_name in in_field_names:
            field_value = item[field_name]
            base_field_name = self.remove_prefix(field_name, 'in_')
            field_config = self.field_config(self.table_config, base_field_name)

            # preprocess
            item = self.preprocess(item, base_field_name, field_config, field_value)

            field_value = item['pp_' + base_field_name]

        return item

    def preprocess(self, item, field_name, field_config, field_value):
        pp_field_name = 'pp_' + field_name
        if field_config:
            result = self.preprocess_field(field_value, field_config)
            item[pp_field_name] = result
        else:
            item[pp_field_name] = field_value

        return item




    def field_config(self, table_config, field_name):
        if field_name in table_config:
            return table_config[field_name]
        return None

    def preprocess_field(self, field_value, field_config):
        try:
            # only process the first object which is info for first transformation
            if field_config['preprocessing_info']['pre_action'] == 'Trim':
                return dqu.trim(field_value)
            return field_value
        except KeyError:
            # print(field.name + " does not exist in table_config")
            return field_value

    def remove_prefix(self, string, prefix):
        if string and string.startswith(prefix):
            return string[len(prefix):]
        return string

