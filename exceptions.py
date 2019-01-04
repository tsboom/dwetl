class FatalTransformException(Exception):
    """Raised when exception suspends record"""
    pass

class AbortException(Exception):
    """Raised when ETL must be aborted"""
    pass
