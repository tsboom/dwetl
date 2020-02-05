"""
file for functions that are shared across pytests
"""

from data.dimension_sample_data import bib_record_dimension_sample_data
import pytest


@pytest.fixture(scope="module")
def bib_rec_sample_data():
    return bib_record_dimension_sample_data
    
    


    
    
