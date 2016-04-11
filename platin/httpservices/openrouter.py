#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from ..core.basic import make_list
from lib.router import Router
from lib.service import Service


class OpenRouter(Router):
    def registerAction(self, endpoint, action, verbs, **kwargs):
        self._server.putChild(endpoint, Service(self, self._server))
        self._actions[endpoint] = (set(make_list(verbs)), action, kwargs)

    # for the Service 

    def findAction(self, levels, verb, request):
        endpoint = levels[0]
        if not endpoint in self._actions:
            return None, None, None
        verbs, action, kwargs = self._actions[endpoint]
        if not verb in verbs:
            return None, None, None
        return action, levels[1:], kwargs

    # for the HTTPServer

    def rootNode(self):
        return self._server
