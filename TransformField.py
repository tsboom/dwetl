'''
Transform Field

A class to represent a field to be transformed with optional isbn/issn code
'''

class TransformField:

    def __init__(self, name, value, isbn_issn_code = None):
        self.name = name
        self.value = value
        self.isbn_issn_code = isbn_issn_code
        self.record = {
            "pp": None,
            "dq" : None,
            "transforms" : []
        }

    def record_transforms(self, transform_name, result):
        self.record["transforms"].append({name: transform_name, result: result})

    def record_pp(self, result):
        self.record['pp'] = result

    def record_dq(self, result):
        self.record['dq'] = result
