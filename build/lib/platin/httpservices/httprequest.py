#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import urllib2
import ssl
import time
from errors import *

"""
This class implements the opening of a URL and the sending of an 
HTTP request. It attempts the connection depending on the following
arguments:
- urln: the number of times to try and connect to the server. This value is high
  by default to wait for the server to spawn. Pass a negative value to try forever.
- ssln: number of tries if an ssl error occurs (not always relevant)
- httpn: the number of tries when encountering a non-fatal http error.
"""


class HTTPRequest(object):
    map = {
        400: BadRequest,
        401: Unauthorized,
        403: Forbidden,
        404: NotFound,
        405: MethodNotAllowed,
        407: Unauthorized,
        500: InternalServerError,
        501: NotImplemented,
        505: HTTPVersionNotSupported,
    }

    fatal = set(map.keys() + [400, 406, 409, 410, 411, 412, 413, 414, 415, 416, 417, 502, 503, 504])

    @classmethod
    def exception(self, err, *args):
        if err.code in self.map:
            return self.map[err.code](err, *args)
        return HTTPFail(err)

    @classmethod
    def urlopen(self, request, data=None, timeout=10, httpn=10, ssln=5, urln=1000):
        httpattempts = httpn
        urlattempts = urln
        sslattempts = ssln
        done = False
        response = None
        while not done:
            try:
                response = urllib2.urlopen(request, data, timeout)
            except urllib2.HTTPError as err:
                if err.code in self.fatal:
                    raise self.exception(err)
                httpattempts -= 1
                if httpattempts == 0:
                    raise self.exception(err, httpattempts)
                time.sleep(2)
            except urllib2.URLError as err:
                urlattempts -= 1
                if urlattempts == 0:
                    raise URLFail(err)
                time.sleep(2)
            except ssl.SSLError:
                sslattempts -= 1
                if sslattempts == 0:
                    raise
                time.sleep(2)
            else:
                done = True
        return response
