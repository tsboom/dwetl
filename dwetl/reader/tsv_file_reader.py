import csv
import os


class TsvFileReader:
    """
    Reads a TSV file, returning a Dictionary of key/value pairs

    This implementation assumes that the second line in the file
    is a tab-separated list of the keys to use.

    Lines with an initial field of "H" or "T" are skipped as header/footer
    lines.
    """
    def __init__(self, file_path):
        """
        Constructs a new TsvFileReader.

        :param file_path: the fully-qualified path to the file
        """
        self.file_path = file_path
        self.fd = open(self.file_path)
        self.reader = csv.reader(self.fd, delimiter='\t', quoting=csv.QUOTE_NONE)
        #self.reader = csv.reader(self.fd, delimiter='\t')
        # check if file is empty
        if os.stat(self.file_path).st_size is not 0:
            # Skip first two header lines
            _header1 = next(self.reader)
            self.headers = next(self.reader)

    def __iter__(self):
        for line in self.reader:
            # Skip any additional header or footer lines
            if line[0] == 'H' or line[0] == 'T':
                continue

            # Create a dictionary from headers and line values
            row_dict = {}
            for i, header in enumerate(self.headers):
                # Skip rest of headers if we run out of values
                if i < len(line):
                    row_dict[self.headers[i]] = line[i]

            yield row_dict

    def __del__(self):
        if hasattr(self, 'fd') and self.fd:
            self.fd.close()
