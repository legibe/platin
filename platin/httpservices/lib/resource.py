#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from twisted.web import http, resource

"""
A thin layer between twisted.web.resource.Resource and our code. For security, attach a method on
all HTTP verbs to return http code "not allowed"
"""

class Resource(resource.Resource):

    def __init__(self):
        resource.Resource.__init__(self)

    def unimplemented(self, request):
        request.setResponseCode(http.NOT_ALLOWED)
        return ""

    render_CONNECT = unimplemented
    render_DELETE = unimplemented
    render_GET = unimplemented
    render_HEAD = unimplemented
    render_OPTIONS = unimplemented
    render_POST = unimplemented
    render_PUT = unimplemented
    render_TRACE = unimplemented

    def connectionInfo(self,request):
        info = {}
        info['host'] = request.getRequestHostname()
        info['port'] = request.getHost().port
        info['title'] = "services on host: %s, port %d" % (info['host'],info['port'])
        return info
