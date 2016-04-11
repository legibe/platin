#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from collections import OrderedDict

class Schema(OrderedDict):
    """
    This is a utility class, using the description of a table it is able
    to validate data
    """

    map = {
        'tinyint':      int,
        'smallint':     int,
        'mediumint':    int,
        'int':          int,
        'bigint':       int,
        'decimal':      int,
        'numeric':      int,
        'bit':          int,
        'float':        float,
        'real':         float,
        'double':       float,
        'text':         str,
        'varchar':      str,
        'tinytext':     str,
        'longtext':     str,
        'enum':         str,
        'set':          str,
    }

    def __init__(self,*args,**kwargs):
        super(Schema,self).__init__(*args,**kwargs)
        for k,i in self.items():
            typename = i.split('(')[0]
            if typename in self.map:
                self[k] = self.map[typename]
            else:
                # if we don't know the type we keep values as they are
                self[k] = lambda x: x
    
    def checkColumns(self,fields):
        return set(self.keys()) == set(fields.keys())