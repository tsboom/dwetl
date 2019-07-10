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

    def last(self):
        # get the value of the last not null value in a list
        def get_last(value_list):
            last = [i for i in value_list if i][-1]
            return last['result']

        if self.record['transforms']:
            last_value = get_last(self.record['transforms'])
        elif self.record['dq']:
            last_value = get_last(self.record['dq'])
        else:
            last_value = self.record['pp']
        return last_value
