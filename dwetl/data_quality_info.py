import dwetl.data_quality_utilities as dqu
from functools import partial
import pdb
import pprint

class DataQualityInfo:
    """
    This object represents a single "dataquality_info" stanza from the table config JSON
    """
    def __init__(self, json_config):
        self.exception_message = json_config['exception_message']
        self.replacement_value = DataQualityInfo.replacement_value(json_config['replacement_value'])
        self.suspend_record = DataQualityInfo.text_to_bool(json_config['suspend_record'])
        self.always = DataQualityInfo.text_to_bool(json_config['always'])
        self.only_if_data_exists = DataQualityInfo.text_to_bool(json_config['only_if_data_exists'])
        self.type = json_config['type']
        self.specific_dq_function = json_config['specific_dq_function']
        self.specific_dq_function_param_1 = json_config['specific_dq_function_param_1']
        self.function = DataQualityInfo.create_function(self.specific_dq_function, self.specific_dq_function_param_1)

    def validate(self, data_value):
        if self.function:
            #pdb.set_trace()
            return self.function(data_value)
        else:
            # Data quality function is None, so just return True
            return True
            
    def has_replacement_value(self):
        """
        Return True if this DataQualityInfo has a replacement value, False otherwise
        :return: True if this DataQualityInfo has a replacement value, False otherwise
        """
        if self.replacement_value is None:
            return False

        value = self.replacement_value.lower()
        if value and value == 'n/a':
            return False
        if value and value == 'None':
            return False
        if value == '(null)':
            return None
        return True    
        
    @classmethod
    def replacement_value(self, replacement_value):

        if replacement_value is None:
            return None

        value = replacement_value.lower()
        if value and value == 'n/a':
            return None
        if value == '(null)':
            return None
        return replacement_value

    @classmethod
    def create_function(cls, function_name, *param_values):
        if function_name is None:
            return None

        function_name = function_name.lower().strip()
        if function_name == 'n/a' or function_name == '':
            return None

        actual_params = []
        if param_values is not None:
            for param in param_values:
                if param == '':
                    continue
                actual_params.append(param)

        if not actual_params:
            actual_params = None

        try:
            f = getattr(dqu, function_name)
            if actual_params is not None:
                # Note: partial works if is_valid_length arguments are reversed
                # return partial(f, *actual_params)
                def curry(string):
                    return f(string, *actual_params)
                return curry
            else:
                return f
        except AttributeError:
            print(f"function_name '{function_name}' is not a valid data quality action")



    @classmethod
    def text_to_bool(cls, text):
        if text is None:
            return False
        text = text.lower()
        if text == 'yes':
            return True
        elif text == 'x':
            return True
        return False
