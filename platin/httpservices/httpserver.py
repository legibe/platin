#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from twisted.internet import reactor, ssl
from twisted.web import server

from blockingresponse import BlockingResponse
from jsonformat import JSONFormat
from lib.resource import Resource


"""
The heart of the system and the class to instanciate. Call the run method
to start the server. It runs forever.
"""


class HTTPServer(Resource):
    def __init__(self, response=BlockingResponse, converter=JSONFormat()):
        Resource.__init__(self)
        self.converter = converter
        self.response = response

    def run(self, port, router, ssl_options=None):
        if ssl_options is not None:
            reactor.listenSSL(
                port, server.Site(router.rootNode()),
                ssl.DefaultOpenSSLContextFactory(
                    ssl_options.get('keyfile'),
                    ssl_options.get('certfile')))
        else:
            reactor.listenTCP(port, server.Site(router.rootNode()))
        return reactor.run()

