import unittest
from dwetl.reader.list_reader import ListReader


class TestListReader(unittest.TestCase):
    def test_simple_array(self):
        array = [
            'Line 1',
            'Line 2'
        ]

        reader = ListReader(array)
        self.assertEqual(array[0], next(iter(reader)))
        self.assertEqual(array[1], next(iter(reader)))
