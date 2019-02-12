class DWETLException(Exception):




class FatalTransformException(DWETLException):
    """Raised when exception suspends record"""
    pass

class AbortException(DWETLException):
    """Raised when ETL must be aborted"""
    pass

class MissingValueException(DWETLException, field)
    print(field + 'is missing')
