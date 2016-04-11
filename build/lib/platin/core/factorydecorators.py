#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import sys


def addFactoryDecorator(name, decorator):
    me = sys.modules[__name__]
    if not hasattr(me, name):
        setattr(me, name, decorator)
