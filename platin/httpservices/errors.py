#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
"""
Trying to encapsulate errors linked to the http protocol
"""

__all__ = ['BadRequest', 'Unauthorized', 'Forbidden', 'NotFound', 'MethodNotAllowed', 'InternalServerError',
           'NotImplemented', 'HTTPVersionNotSupported']


class HTTPFail(Exception):
    def __init__(self, err, attempts=1):
        self.code = err.code
        self.msg = err.read()
        self.attempts = attempts
        self._err = err

    def __str__(self):
        return self._err.__str__() + ' ' + self.msg


class BadRequest(HTTPFail):
    pass


class Unauthorized(HTTPFail):
    pass


class Forbidden(HTTPFail):
    pass


class NotFound(HTTPFail):
    pass


class MethodNotAllowed(HTTPFail):
    pass


class InternalServerError(HTTPFail):
    pass


class NotImplemented:
    pass


class HTTPVersionNotSupported:
    pass


class URLFail(Exception):
    def __init__(self, err, attempts=1):
        self.code = err.reason[0]
        self.msg = err.reason[1]
        self.attempts = attempts
        self._err = err

    def __str__(self):
        return self._err.__str__()
