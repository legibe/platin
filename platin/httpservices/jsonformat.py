#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------

"""
By default we use JSON encoded data. You can provide your own classmethod
implemeting the three method as class methods.
"""

try:
    import ujson as json
except ImportError:
    import json


class JSONFormat(object):
    @classmethod
    def decode(self, headers, string):
        return json.loads(string)

    @classmethod
    def encode(self, data):
        return json.dumps(data)

    @classmethod
    def httpheaders(self):
        return {'Content-Type': 'application/json',
                #'Access-Control-Allow-Origin': '*'
        }
