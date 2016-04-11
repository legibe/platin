#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from classdecorator import ClassDecorator
import factorydecorators


class MetaFactory(type):
    def __new__(cls, name, parents, dct):
        result = super(MetaFactory, cls).__new__(cls, name, parents, dct)
        result._metafactory_ = {}

        class FactoryDecorator(ClassDecorator):
            def decorate(self, target, options, *args, **kwargs):
                print "========"
                if 'name' in options:
                    name = options['name']
                else:
                    name = target.__name__.lower()
                result.register(name, target)
                return target

        factorydecorators.addFactoryDecorator('in_%s' % result.__name__.lower(), FactoryDecorator)
        return result

    def register(this, name, what):
        this._metafactory_[name] = what

    def create(this, name, *args, **kwargs):
        if not name in this._metafactory_:
            raise IndexError('"%s" is unknown, available: %s' % (name, ', '.join(this._metafactory_.keys())))
        return this._metafactory_[name](*args, **kwargs)

    def registered(this):
        return set(this._metafactory_.keys())

    def isRegistered(this, name):
        return name in this._metafactory_

    def __str__(self):
        return str(self._metafactory_)
