import csv
import pdb


class EzproxyReader:
    """
    Reads an ezproxy session TSV file, returning a Dictionary of key/value pairs

    This implementation assumes that the first line in the file
    is a tab-separated list of the keys to use.
    """

    def __init__(self, file_path):
        """
        Constructs a new EzproxyReader.

        :param file_path: the fully-qualified path to the file
        """
        self.file_path = file_path
        self.fd = open(self.file_path)
        self.reader = csv.reader(self.fd, delimiter='\t')
        # Assume first line is the header line
        self.headers = ['mbr_lbry_cd', 'ezp_sessns_snap_tmstmp',
                        'ezp_sessns_snap_actv_sessns_cnt', 'ezp_sessns_virtual_hosts_cnt']

    def __iter__(self):
        for line in self.reader:
            # Create a dictionary from headers and line values
            result = {}

            # set the headers
            for i, header in enumerate(self.headers):
                # Skip rest of headers if we run out of values
                if i < len(line):
                    result[self.headers[i]] = line[i]
                    # # make sure that if the line is '', it is still added as None
                    # if not line[i]:
                    #     result[self.headers[i]] = None
                    # else:
                    #     result[self.headers[i]] = line[i]
            yield result

    def __del__(self):
        if hasattr(self, 'fd') and self.fd:
            self.fd.close()
