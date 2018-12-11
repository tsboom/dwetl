import pdb
import re
import pytest
import dw_etl
# from dwetl import dw_etl
import pandas as pd
import csv



# extract w pandas
def read_tsv_into_dataframe():
    data = pd.read_csv('data/mai50_z305_20181115_172016_1.tsv', engine='python', sep='\t', header=2, skipfooter=1)
    return data
dataframe = read_tsv_into_dataframe()

#
# def read_tsv():
#     with open('data/mai50_z305_20181115_172016_1.tsv') as tsvin:
#         tsvin = csv.reader(tsvin, delimiter='\t')
#     csv = open("data/mai50_z305_20181115_172016_1.tsv", "w")
#     return tsvin
# read_tsv()
pdb.set_trace()


# transform
# Use a class which uses the table metadata config files and performs the transformations
# write to the intermediate database




# load to intermediate database



# load to dimension dw database
