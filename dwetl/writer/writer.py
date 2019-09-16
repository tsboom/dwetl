class Writer:
    """
    Abstract class that encapsulates a writing a row to an output.

    Subclasses should implement the "write_row" method.
    """

    def write_row(self):
        raise NotImplementedError