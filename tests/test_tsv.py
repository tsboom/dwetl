from dwetl import dw_etl

# check to see if tsv can be imported
def test_import_tsv():
    assert dwetl.read_tsv_into_dataframe() == True

# TSV lines can be read
def test_rows_read():
    assert "temporary"

#
