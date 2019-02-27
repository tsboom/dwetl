


class DWETLException(Exception):
    pass


class InvalidTSVException(DWETLException):
    """ Raised when a tsv contains invalid data """
    pass


class FatalTransformException(DWETLException):
    """Raised when exception suspends record"""
    pass

class AbortException(DWETLException):
    """Raised when ETL must be aborted"""
    pass

class MissingValueException(DWETLException, field)
    print(field + 'is missing')
