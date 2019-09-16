class ListReader:
    """
    Reads a List, returning each line one at a time.
    """
    def __init__(self, lines):
        self.lines = lines
        self.iterator = iter(self.lines)

    def __iter__(self):
        return self.iterator


