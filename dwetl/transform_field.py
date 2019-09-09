import pdb
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
            "dq" : [],
            "transforms" : []
        }

    def record_pp(self, result):
        self.record['pp'] = result

    def record_dq(self, result):
        self.record['dq'].append(result)

    def record_transform(self, result):
        self.record["transforms"].append(result)

    def is_valid(self):
        # if all dq checks are good, continue
        result = True
        for check in self.record['dq']:
            if check['check_passed'] == False:
                result = False
                break
        return result
