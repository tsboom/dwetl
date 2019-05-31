# import dw_etl
import os
import pdb
import unittest
from unittest.mock import MagicMock


'''
database tests
'''

# test a bad connection


# test db connection
def test_db_connection(self):
    engine = dwetl.connect_to_db()
    assert engine == True
    #self.assertFalse(engine.closed)


# test to see that target schema is the same as input schema



# test that tables have right uniqueness constraints
# https://stackoverflow.com/questions/33878830/sqlalchemy-determine-if-unique-constraint-exists




# for a Move, test value in source and value in destination and make sure they are the same
