#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import logging

from twisted.web import http, server

from lib.response import Response


logging.basicConfig(format='HTTP-response - %(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class BlockingResponse(Response):
    """
    This response call the enpoint and returns an http code + body
    If an exception is received during the call to the callable,
    an error is returned. If the exception has a arg array of 2 values,
    the first one is expected to be a integer (http code), the second 
    a string.
    """

    def __call__(self, converter, execute, *args, **kargs):
        if execute is not None:
            try:
                obj = converter.encode(execute(self, *args, **kargs))
                self.send(obj, http.OK, converter)
            except Exception as err:
                import traceback

                log.error('%s' % err)
                #log.error('%s' % ''.join(traceback.format_stack()))
                code = http.INTERNAL_SERVER_ERROR
                if len(err.args) > 1 and isinstance(err.args[1], int):
                    code = err.args[1]
                self.send('%s' % (err), code, converter)
        else:
            self.send(self._message, code=self._return, converter=converter)
        return server.NOT_DONE_YET
