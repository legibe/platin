#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import sys

"""
A factory to hold classes under registered strings. Factory classes are generated
automatically by the function createFactory. New classes are also added to the
module's namespace so they become visible by importers.
createFactory('Object') creates the class called ObjectFactory
"""

class Factory(object):

    @classmethod
    def register(self,name,what):
        self._members[name] = what

    # if set, any unknown name will create one of those
    @classmethod
    def registerDefault(self,what):
        self._default = what

    @classmethod
    def create(self,name,*args,**kwargs):
        if not name in self._members:
            if self._default is not None:
                return self._default(*args,**kwargs)
            else:
                raise IndexError('%s "%s" is unknown, available: %s' % (self._name,name,', '.join(self._members.keys())))
        return self._members[name](*args,**kwargs)

    @classmethod
    def registered(self):
        return set(self._members.keys())

    @classmethod
    def isRegistered(self,name):
        return name in self._members

def createFactory(name):
    me = sys.modules[__name__]
    name = '%sFactory' % name
    if not hasattr(me,name):
        setattr(sys.modules[__name__],name,type(name,(Factory,), { '_name': name, '_members': {}, '_default': None  }))
    return getattr(me,name)
