from dwetl.writer.writer import Writer


class PrintWriter(Writer):
    """
    Writer that sends each row to standard out.

    This writer is mainly intended for tst.
    """
    def write_row(self, row):
        print(row)
