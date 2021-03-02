


class DWETLException(Exception):
    """
    Exception raised for errors 
    """
    def __init__(self, e):
        self.error_type = type(e).__name__
        self.error_text = str(e.orig)
        self.error_row = str(e.params)
        

    def __str__(self):
        return f'DWETLException: {self.error_type} {self.error_text}'



# class InvalidTSVException(DWETLException):
#     """ Raised when a tsv contains invalid data """
#     pass


# class FatalTransformException(DWETLException):
#     """Raised when exception suspends record"""
#     pass

class AbortException(DWETLException):
    """Raised when ETL must be aborted"""
    pass

