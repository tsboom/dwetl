import dwetl.data_quality_utilities as dqu
from functools import partial

class DataQualityInfo:
    """
    This object represents a single "dataquality_info" stanza from the table config JSON
    """
    def __init__(self, json_config):
        self.exception_message = json_config['exception_message']
        self.replacement_value = json_config['replacement_value']
        self.suspend_record = DataQualityInfo.text_to_bool(json_config['suspend_record'])
        self.specific_dq_function = json_config['specific_dq_function']
        self.specific_dq_function_param_1 = json_config['specific_dq_function_param_1']

        self.function = DataQualityInfo.create_function(self.specific_dq_function, self.specific_dq_function_param_1)

    def validate(self, data_value):
        if self.function:
            return self.function(data_value)
        else:
            # Data quality function is None, so just return True
            return True

    def has_replacement_value(self):
        """
        Return True if this DataQualityInfo has a replacement value, False otherwise
        :return: True if this DataQualityInfo has a replacement value, False otherwise
        """
        if self._replacement_value is None:
            return False

        value = self._replacement_value.lower()
        if value and value == 'n/a':
            return False

        return True

    @property
    def replacement_value(self):
        if self.has_replacement_value():
            return self._replacement_value
        return None

    @replacement_value.setter
    def replacement_value(self, val):
        self._replacement_value = val

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

        return False
