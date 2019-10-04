import unittest
from dwetl.reader.list_reader import ListReader
from dwetl.writer.list_writer import ListWriter
from dwetl.job_info import JobInfo
from dwetl.processor.preprocess import Preprocess
import pdb

class TestPreprocess(unittest.TestCase):
    def test_preprocess(self):
        sample_data = [
            {   # z00 don't have trims
                'in_z00_doc_number': '000019087',
                'in_z00_no_lines': None,
                'in_z00_data_len': None,
                # z13 has trims
                'in_z13_title': 'A literary history of America',
                'in_z13_author': 'Wendell, Barrett, 1855-1921',
                'in_z13_imprint': 'New York, Haskell House Publishers, 1968'
            }
        ]

        reader = ListReader(sample_data)
        writer = ListWriter()

        job_info = JobInfo(-1, 'test_user', '1', '1')

        logger = None

        sample_json_config = {
            'z00_doc_number': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z00_no_lines': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "N/A",
                    "pre_detailed_instructions": "N/A"
                }
            },
            'z13_title': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            },
            'z13_author': {
                "preprocessing_info": {
                    "pre_or_post_dq": "N/A",
                    "pre_action": "Trim",
                    "pre_detailed_instructions": "Remove leading and trailing spaces"
                }
            },
        }




        step = Preprocess(reader, writer, job_info, logger, sample_json_config)
        step.execute()
        results = step.writer.list
        pdb.set_trace()
