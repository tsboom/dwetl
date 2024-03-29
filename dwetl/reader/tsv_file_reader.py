import csv
import os
import pdb


class TsvFileReader:
    """
    Reads a TSV file, returning a Dictionary of key/value pairs

    This implementation assumes that the second line in the fileå
    is a tab-separated list of the keys to use.

    Lines with an initial field of "H" or "T" are skipped as header/footer
    lines.
    """
    record_count = 0
    def __init__(self, file_path):
        """
        Constructs a new TsvFileReader.

        :param file_path: the fully-qualified path to the file
        """
        self.file_path = file_path
        self.fd = open(self.file_path)
        self.reader = csv.reader(self.fd, delimiter='\t', quoting=csv.QUOTE_NONE)
        # check if file is empty
        if os.stat(self.file_path).st_size != 0:
            # Skip first two header lines
            _header1 = next(self.reader)
            self.headers = next(self.reader)


    def __iter__(self):
        r_count = 0
        for line in self.reader:
            # Skip any additional header or footer lines
            if line[0] == 'H' or line[0] == 'T':
                continue
            r_count = r_count + 1
            #pdb.set_trace()
            # Create a dictionary from headers and line values
            row_dict = {}
            for i, header in enumerate(self.headers):
                # Skip rest of headers if we run out of values
                if i < len(line):
                    row_dict[self.headers[i]] = line[i]
            yield row_dict
        self.record_count = r_count

    def __del__(self):
        if hasattr(self, 'fd') and self.fd:
            self.fd.close()

    def count_rows(self):
        for line in self.reader:
            # Skip any additional header or footer lines
            if line[0] == 'T':
                row_count = line[3]
                pdb.set_trace()
                return row_count
