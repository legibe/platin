#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import os

from basic import substitute_env_variables


class PathConfig(object):
    @classmethod
    def paths(self, varname):
        path = substitute_env_variables(varname)
        return path.split(':')

    @classmethod
    def fullpaths(self, varname, filename):
        return [os.path.join(x, filename) for x in self.paths(varname)]

    @classmethod
    def fullvalidpaths(self, fullpath, filename):
        return [x for x in self.fullpaths(fullpath, filename) if os.path.exists(x)]

