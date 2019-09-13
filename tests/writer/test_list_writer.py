import unittest
from dwetl.writer.list_writer import ListWriter


class TestListWriter(unittest.TestCase):
    def test_initialization(self):
        writer = ListWriter()
        self.assertEqual([], writer.list)

    def test_single_write(self):
        writer = ListWriter()
        writer.write_row('Line 1')
        self.assertEqual(['Line 1'], writer.list)

    def test_multiple_writes(self):
        writer = ListWriter()
        writer.write_row('Line 1')
        writer.write_row('Line 2')
        self.assertEqual(['Line 1', 'Line 2'], writer.list)
