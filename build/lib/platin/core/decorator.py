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
Some generic decorator class which works with or without named arguments to decorate
methods and functions. Subclass and redefine the decorate method which should 
return whatever needs to be returned after some action is taken
(most of the time the target itself or a wrapper).
Example:

class cost(Decorator):
    value = 0

    def decorate(self,target,options,*args,**kwargs):
        print options
        increment = 1
        if 'weight' in options:
            increment = options['weight']
        cost.value += increment
        return target(*args,**kwargs)

@cost
def callResource(value):
    return value

@cost(weight=4)
def callRemoteResource(value):
    return value


print callResource(4)
print callRemoteResource(12)
print cost.value

result:
{}
4
{'weight': 4}
12
5

"""


class Decorator(object):
    def __init__(self, __target__=None, **options):
        self._target = None
        self._options = options
        if __target__ is not None:
            self._target = __target__

    def __call__(self, *args, **kwargs):
        if self._target is None:
            self._target = args[0]
            return self.__class__(args[0], **self._options)
        else:
            return self.decorate(self._target, self._options, None, *args, **kwargs)

    def methodCall(self,*args,**kwargs):
        return self.decorate(self._target, self._options, self._object, *args, **kwargs)

    def __get__(self,obj,klass=None):
        if klass is not None:
            self._object = obj
        else:
            self._object = None
        return self.methodCall
        
    def decorate(target, options, *args, **kwargs):
        raise NotImplemented('abstract method')


