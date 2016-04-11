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
A package with utilities to implement an http service. To create one you will need to look at:
- HTTPServer
- One of the routers, either MatchRouter or TreeRouter
- There are defaults behaviours defined, to change them, please take a look at JSONFormat and BlockingResponse and NonBlockingResponses.
- The Scheduler can help you schedule task as 'crons', either with an HTTP service or on their own.
"""