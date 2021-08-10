


class DWETLException(Exception):
    """
    Exception raised for errors caught from SQLAlchemyError
    """
    def __init__(self, e):
        self.error_type = type(e).__name__
        self.error_text = str(e.orig)
        self.error_row = str(e.params)
        

    def __str__(self):
        return f'DWETLException: {self.error_type} {self.error_text}'
        
class DataQualityException(Exception):
    """
    Exception raised for errors raised during data quality processor
    """
    def __init__(self, e):
        self.error_type = e['error_type']
        self.error_text = e['error_text']
        self.error_row = e['error_row']
        

    def __str__(self):
        return f'DataQualityException: {self.error_type} {self.error_text}'



# class InvalidTSVException(DWETLException):
#     """ Raised when a tsv contains invalid data """
#     pass


# class FatalTransformException(DWETLException):
#     """Raised when exception suspends record"""
#     pass

class AbortException(DWETLException):
    """Raised when ETL must be aborted"""
    pass

