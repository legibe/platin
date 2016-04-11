#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#---------------------------------------------------------------------------------
class Router(object):

    def __init__(self,server):
        self._server = server
        self._actions = {}
