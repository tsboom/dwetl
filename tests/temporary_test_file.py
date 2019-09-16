import tempfile
import os


class TemporaryTestFile:
    """
    ContextManager that creates a temporary file with the given lines that is
    deleted after use.

    Usage:

    lines = ['Line 1', 'Line 2']

    with TemporaryTestFile(lines) as tempFilePath:
      # tempFilePath is the fully-qualified path to the file
    """
    def __init__(self, lines):
        self.lines = lines

    def __enter__(self):
        _fd, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            for line in self.lines:
                if not line.endswith('\n'):
                    line = line + '\n'
                f.write(line)

        self.path = path
        return self.path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and os.path.isfile(self.path):
            os.remove(self.path)
