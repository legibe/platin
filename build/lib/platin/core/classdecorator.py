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
class declarations.
Example:

class in_factory(ClassDecorator):
    def decorate(self,target,options,*args,**kwargs):
        factory = 'default'
        if 'factory' in options:
            factory = options['factory']
        print "register in %s factory" % factory
        return target
         
@in_factory
class Router1(object):
    pass

@in_factory(factory='hello')
class Router2(object):
    pass

register in default factory
register in hello factory

"""


class ClassDecorator(object):
    def __new__(cls, __target__=None, **options):
        if __target__ is not None:
            a = object.__new__(cls).__init__(__target__, **options)
            return __target__
        return object.__new__(cls)

    def __init__(self, __target__=None, **options):
        self._options = options
        if __target__ is not None:
            self.decorate(__target__, self._options)

    def __call__(self, target):
        return self.__class__(target, **self._options)

    def decorate(target, options, *args, **kwargs):
        raise NotImplemented('abstract method')
