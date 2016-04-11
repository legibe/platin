#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
"""
A router to which we pass a list of callables, an http verb and a regular expression.
At runtime, regular expressions are evaluated against the URI, if a match occurs
and the http verb corresponds, the callable is executed. 

Evaluation is stopped when a match occurs. Regular expressions are evaluated
in the order they are passed to the router at initialisation time.
"""
import re

from ..core.basic import make_list
from lib.service import Service
from lib.rooter import Rooter


class MatchRouter(Rooter):
    def registerAction(self, regex, action, verbs, **kwargs):
        self._actions.append((regex, action, set(make_list(verbs)), kwargs))

    # for the Service

    def findAction(self, levels, verb, request):
        levels = '/' + '/'.join(levels)
        for match in self._actions:
            verbs = match[2]
            if verb in verbs:
                regex = match[0]
                kwargs = match[3]
                m = re.match(regex, levels)
                if m:
                    arg = m.groupdict()
                    if len(arg) == 0:
                        arg = m.groups()
                        if len(arg) == 0:
                            arg = None
                    return match[1], arg, kwargs
        return None, None, None

    # for the HTTPServer

    def rootNode(self):
        return Service(self, self._server)
