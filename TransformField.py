'''
Transform Field

A class to represent a field to be transformed with optional isbn/issn code
'''

class TransformField:

    def __init__(self, name, value, isbn_issn_code = None):
        self.name = name
        self.value = value
        self.isbn_issn_code = isbn_issn_code
        self.log = {
            "pp": None,
            "dq" : None,
            "transforms" : []
        }

    def log_transform_result(self, transform_name, result):
        self.log["transforms"].append({name: transform_name, result: result})

    def log_pp(self, result):
        self.log['pp'] = result

    def log_dq(self, result):
        self.log['dq'] = result
