#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
import json

from schemareader import SchemaReader


class JSONReader(object):
    def read(self, filename):
        with open(filename) as f:
            try:
                schema = json.load(f)
            except:
                print filename
                raise
            if not isinstance(schema, list):
                schema = [schema]
            return schema


SchemaReader.register('json', JSONReader)
