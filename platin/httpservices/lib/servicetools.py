#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from core.classdecorator import ClassDecorator

__all__ = ['endpoint']
__registrations__ = {}

class endpoint(ClassDecorator):
    global __registrations__
    required = set(['uri','verb'])
    def decorate(self,target,options,**kwargs):
        if self.required.intersection(set(options.keys())) != self.required:
            raise ValueError('Required arguments for registering an endpoint are: %s' % ', '.join(self.required))
        __registrations__[target.__name__] = (id(target.__code__,options['uri'],options['verb'],kwargs))


def registerService(self,service,router):
    global __registrations__
    for name, args in __registrations__:
        if hasattr(service,name):
            method = getattr(self,service)
            if id(method.__func__.__code__) == args[0]:
                router.registerAction(args[1],method,args[2],**args[3])
