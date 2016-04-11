#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import logging

from twisted.internet import threads, defer, reactor
from twisted.web import http, server

from lib.response import Response


logging.basicConfig(format='HTTP-response - %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class NonBlockingResponse(Response):
    """
    This response call defers the call to the enpoint and returns immediately.
    The action is then called in a separate thread, the response is sent in 
    the main thread.
    """

    def success(self, response, converter):
        self.request.setResponseCode(http.OK)
        reactor.callFromThread(self.send_http_response, response, converter)

    def failure(self, response, converter):
        code = http.INTERNAL_SERVER_ERROR
        if len(response.value.args) > 1:
            code = response.value.args[1]
        self.request.setResponseCode(code)
        reactor.callFromThread(self.send_http_response, response.__str__(), converter)

    def __call__(self, converter, deferred, *args, **kargs):
        # defer the call to our wrapper method to another thread and return
        # straight away.
        if deferred is not None:
            threads.deferToThread(self.execute, deferred, converter, *args, **kargs)
        else:
            self.send(self._message, code=self._return, converter=converter)
        return server.NOT_DONE_YET

    def execute(self, deferred, converter, *args, **kargs):
        def wrap(*args, **kargs):
            return converter.encode(deferred(self, *args, **kargs))

        # this method is called in another thread. maybeDeferred will probably call
        # our action straight away or as soon as it is suitable.
        d = defer.maybeDeferred(wrap, *args, **kargs)
        # register callbacks for handling success, failure.
        d.addCallback(self.success, converter)
        d.addErrback(self.failure, converter)
