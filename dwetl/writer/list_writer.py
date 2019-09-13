class ListWriter:
    """
    Simple Writer that stores all the rows in a list.

    This writer is mainly intended for testing.
    """
    def __init__(self):
        self.list = []

    def write_row(self, row):
        self.list.append(row)
