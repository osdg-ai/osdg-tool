from config import QUERY_SYMBOL_LIMIT


class NgramTokensNotFound(Exception):
    """ Raised when the amount of ngrams is lower than the threshold defined in config.py """
    def __init__(self, message):
        super(NgramTokensNotFound, self).__init__(message)
        self.query_error = "The query you entered does not contain any valid tokens or is shorter than 20 words. Try adjusting the query."


class UnsupportedTextLanguageError(Exception):
    """ Raised when english language is not detected """
    def __init__(self, message):
        super(UnsupportedTextLanguageError, self).__init__(message)
        self.query_error = "ERROR : Language is not supported."


class QuerySymbolLimitError(Exception):
    """ Raised when query exceed symbols limit defined in config.py """
    def __init__(self, message):
        super(QuerySymbolLimitError, self).__init__(message)
        self.query_error = f"ERROR : Query is too long. The query exceeds the {QUERY_SYMBOL_LIMIT} symbol limit."
