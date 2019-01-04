import dwetl
import os
import pdb






'''
database tests
'''

# test db connection
def test_db_connection():
    engine = dwetl.connect_to_db()
    assert engine == True


# test to see that target schema is the same as input schema




# for a Move, test value in source and value in destination and make sure they are the same
