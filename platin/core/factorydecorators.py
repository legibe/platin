#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import sys


def addFactoryDecorator(name, decorator):
    me = sys.modules[__name__]
    if not hasattr(me, name):
        setattr(me, name, decorator)
