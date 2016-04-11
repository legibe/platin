#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import re
import sys
import platin.core.factory as factory
from platin.core.date import Second, Day
from platin.core.basic import bigNumber

factory.createFactory('TypeCreation')
class Types(factory.TypeCreationFactory):
    @classmethod
    def create(self,name,*args,**kwargs):
        try:
            result = super(Types,self).create(name,*args,**kwargs)
        except IndexError:
            result = getattr(sys.modules['__builtin__'],name)(*args,**kwargs)
        return result

class Price(float):
    def __new__(cls,value):
        if isinstance(value,str):
            value = float(re.sub(',','',value))
        return float.__new__(cls,value)

    def __str__(self):
        s = super(Price,self).__str__()
        return bigNumber(s)

class Volume(int):
    def __new__(cls,value):
        if isinstance(value,str):
            value = int(re.sub(',','',value))
        return int.__new__(cls,value)

    def __str__(self):
        s = super(Volume,self).__str__()
        return bigNumber(s)

class DateTime(object):
    def __new__(cls,value):
        # will issue an exception if the date is not valid
        v = Second(value).stringvalue()
        return str.__new__(str,v)

class FormattedDateTime(object):
    def __new__(cls,value):
        # will issue an exception if the date is not valid
        v = Second(value)
        return str.__new__(str,v)
        
class FormattedDateNoTime(object):
    def __new__(cls,value):
        # will issue an exception if the date is not valid
        v = Day(value)
        return str.__new__(str,v)

class PyDateTime(object):
    def __new__(cls,value):
        # will issue an exception if the date is not valid
        v = Second(value)
        return v.datetime()

class Boolean(object):
    def __new__(cls,value):
        result = False
        if isinstance(value,basestring):
            value = value.lower()
            if value == 'yes' or value == 'y':
                result = True
        elif isinstance(value,bool):
            result = value
        elif isinstance(value,int):
            result = value != 0
        return result


Types.register('price',Price)
Types.register('volume',Volume)
Types.register('datetime',DateTime)
Types.register('formatteddatetime',FormattedDateTime)
Types.register('formatteddatenotime',FormattedDateNoTime)
Types.register('pydatetime',PyDateTime)
Types.register('boolean',Boolean)

