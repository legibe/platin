#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
"""
A router to which we pass a list of callables, an http verb and a "path".
Paths can be added dynamically, for example:
router.registerAction('/store/definition',action)
In this approach, arguments are supposed to be urlencoded or sent
in the body of a POST request.
"""
from ..core.basic import make_list
from lib.service import Service
from lib.router import Router


class TreeRouter(Router):
    def registerAction(self, path, action, verbs, **kwargs):
        levels = path.split('/')
        self._server.putChild(levels[0], Service(self, self._server))
        self._actions = self.storeAction(self._actions, action, levels, set(make_list(verbs)), kwargs)

    # for the Service 
    def findAction(self, levels, verb, request):
        node = self._actions
        for level in levels:
            if level in node:
                node = node[level]
            else:
                return None, None, None
        verbs = node[1]
        kwargs = node[2]
        node = node[0]
        if callable(node):
            if verb in verbs:
                return node, None, kwargs
        return None, None, None

    # protected 
    def storeAction(self, where, action, levels, verbs, kwargs):
        if len(levels) > 0:
            level = levels[0]
            if level in where:
                entry = where[level]
            else:
                entry = {}
            where[level] = self.storeAction(entry, action, levels[1:], verbs, kwargs)
        else:
            return (action, verbs, kwargs)
        return where

    # for the HTTPServer

    def rootNode(self):
        return self._server
