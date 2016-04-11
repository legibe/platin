#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from twisted.internet import reactor

from ..core.date import utcNow


"""
A convenience class to use some of the features of the twisted reactor.
Here it is about scheduling jobs, in the different methods, any extra 
arguments, either named or not are sent to the action when it is called.
- repeatAction: periodic action every "repeat" seconds.
- delayAction: excutes a task once only after the given delay in seconds.
- repeatRoundTimeAction: same as repeat action but calls the action on round
  values of time, e.g. every n minutes. The argument 'delay' is added to the
  round time. For example:
  repeatRoundTimeAction(action,3600,300) will call action every hour,
  5 minutes after the hour.
- run: to call to start the twisted reactor loop. If you are using
  an http server as well, class HTTPServer, just call server.run(...)
"""


class Scheduler(object):
    def repeatAction(self, action, repeat, *args, **kwargs):
        def wrapper(*args, **kwargs):
            reactor.callLater(repeat, wrapper, *args, **kwargs)
            action(*args, **kwargs)

        reactor.callLater(repeat, wrapper, *args, **kwargs)

    def delayAction(self, action, delay, *args, **kwargs):
        reactor.callLater(delay, action, *args, **kwargs)

    def repeatRoundTimeAction(self, action, increment, delay=0, *args, **kwargs):
        def wrapper(currentcall, *args, **kwargs):
            action(increment, delay, *args, **kwargs)
            nextcall = currentcall + increment
            now = utcNow()
            incr = max(nextcall - now + 1, 0)
            reactor.callLater(incr, wrapper, nextcall, *args, **kwargs)

        nextcall, incr = self.nextCall(increment, delay)
        reactor.callLater(incr, wrapper, nextcall, *args, **kwargs)

    def run(self):
        reactor.run()

    def nextCall(self, increment, delay):
        now = utcNow()
        then = now.nextRoundMultiple(increment) + delay
        incr = then - now + 1
        if incr < 0:
            incr = 0
        return then, incr
