import csv
import pdb
import re


class Z00FieldReader:
    """
    Reads a Z00 Field TSV file, returning a Dictionary of key/value pairs

    This implementation assumes that the second in the file
    is a tab-separated list of the keys to use.

    This class is temporary until the extract files are tab separated.
    """
    def __init__(self, file_path):
        """
        Constructs a new Z00FileReader.

        :param file_path: the fully-qualified path to the file
        """
        self.file_path = file_path
        self.fd = open(self.file_path)
        self.reader = csv.reader(self.fd, delimiter='\t')
        # skip first line
        first_line = next(self.reader)
        self.headers = next(self.reader)

    def __iter__(self):
        for line in self.reader:
            # match with regex to tab separate line values
            match = re.search(r'(\S+)\s+(\S+)\s+(\S+)\s+(.*)', line[0])

            # Create a dictionary from headers and line values
            result = {}
            # save one header for each regex match group
            result[self.headers[0]] = match.group(1)
            result[self.headers[1]] = match.group(2)
            result[self.headers[2]] = match.group(3)
            result[self.headers[3]] = match.group(4)
            pdb.set_trace()
            yield result

    def __del__(self):
        if hasattr(self, 'fd') and self.fd:
            self.fd.close()
