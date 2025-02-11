
class RedirectRulesException(Exception):
    """ Base exception class for redirect rules exceptions """
    pass

class RedirectRulesNotFoundException(RedirectRulesException):
    """ Not found exception class for redirect rules exceptions """
    pass