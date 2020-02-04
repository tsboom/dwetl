import dwetl.data_quality_utilities as dqu
from functools import partial
import pdb


class TransformationInfo:
    """
    This object represents a single "transformation_steps" stanza from the table config JSON
    """
    def __init__(self, json):
        self.target_col_name = json['target_col_name']
        self.target_data_type = json['target_data_type']
        self.target_attribute = json['target_attribute']
        self.chg_proc_type = json['transform_info']['chg_proc_typ']
        self.transform_action = json['transform_info']['transform_action']
        self.action_specific = json['transform_info']['action_specific']
        self.specific_transform_function = json['transform_info']['specific_transform_function']
        self.specific_transform_function_param1 = json['transform_info']['specific_transform_function_param1']
        self.specific_transform_function_param2 = json['transform_info']['specific_transform_function_param2']
        self.source_col_name = json['transform_info']['source_col_name']
        self.source_data_type = json['transform_info']['source_data_type']
        self.source_format = json['transform_info']['source_format']
        self.source_mandatory = json['transform_info']['source_mandatory']
        self.aleph_table = json['transform_info']['aleph_table']
        self.action_detailed_instructions = json['transform_info']['action_detailed_instructions']
        self.function = TransformationInfo.create_function(self.specific_transform_function, self.specific_transform_function_param1, self.specific_transform_function_param2)
        
    def transform(self, data_value):
        if self.function:
            return self.function(data_value)
        else:
            # return original value if there's no transform function
            return data_value
            
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