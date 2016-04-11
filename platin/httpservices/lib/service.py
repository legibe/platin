#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from twisted.web import server
from response import Response
from resource import Resource

class Service(Resource):

    # all services are leaves, this means that twisted will call the
    # verb handling methods even if the url has more levels. I do
    # that because I couldn't get this to work properly using the tools
    # provided in Twisted (putChild). I handle the tree of enpoints myself.
    isLeaf = True

    def __init__(self,router,server):
        Resource.__init__(self)
        self._responseMaker = server.response
        self._converter = server.converter
        self._router = router

    def renderPoint(self,request,body,verb):
        response = self._responseMaker(request=request)
        # we re-create the full url
        path = [ x for x in request.prepath + request.postpath if x != '' ]
        # find the callable associated with this endpoint
        action,args,kwargs = self._router.findAction(path,verb,request)
        if action is None:
            # nothing is registered for that endpoint so 404 seems appropriate
            response.setReturnStatus(403,message='Forbidden')
            return response(self._converter,action,body,path)
        else:
            if args is not None:
                body = args
            # call the action registered for that endpoint.
            return response(self._converter,action,body,path,**kwargs)

    def render_POST(self, request):
        body = request.content.read()
        headers = {}
        if hasattr(request,'received_headers'):
            headers = request.received_headers
        body = self._converter.decode(headers,body)
        return self.renderPoint(request,body,'POST')

    def render_GET(self, request):
        return self.renderPoint(request,request.args,'GET')

    def render_DELETE(self, request):
        return self.renderPoint(request,request.args,'DELETE')

    def render_HEAD(self, request):
        return self.renderPoint(request,request.args,'HEAD')

    def render_OPTIONS(self, request):
        return self.renderPoint(request,request.args,'OPTIONS')

    def render_PUT(self, request):
        return self.renderPoint(request,request.args,'PUT')

    def render_CONNECT(self, request):
        return self.renderPoint(request,request.args,'CONNECT')

    def render_TRACE(self, request):
        return self.renderPoint(request,request.args,'TRACE')

