#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from twisted.internet import defer, reactor
from twisted.web import http,server

"""
Encapsulate what a response to an http request should do, so that
multi or single thread management is made transparent
"""

class Response(object):

    def __init__(self,request=None,body=True):
        self.request = request
        self._return = None
        self._headers = {}
        self._message = ''
        self._body = body

    def getRequest(self):
        return self.request

    def getVerb(self):
        return self.request.method

    def send_http_response(self,response,converter):
        # sending the http response to the server, included
        # encoded body
        # merge local header with standard one, overwrite standard
        # with local is relevant
        for k,i in dict(converter.httpheaders(),**self._headers).items():
            self.request.setHeader(k, i)
        if self._return is not None:
            self.request.setResponseCode(self._return)
        if self._body:
            self.request.write(data=response)
        self.request.finish()

    def send(self,response,code = http.OK,converter = None):
        self.request.setResponseCode(code)
        self.send_http_response(response,converter)

    def __call__(self,service,execute,*args,**kargs):
        # this is what should be redefined
        raise SystemError('Not implemented')

    def setReturnStatus(self,code,headers={},message=''):
        self._return = code
        self._headers = headers
        self._message = message
