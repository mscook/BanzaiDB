class NestedJSONError(Exception):
    """
    The conversion of JSON to CSV does not support nested JSON
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class CouldNotParseJSONError(Exception):
    """
    The conversion only takes a single JSON element, not a list of elements
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)
