#--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from ..core.factory import createFactory
from ..core.pathconfig import PathConfig
from schemavalidate import SchemaValidate

SchemaReaderFactory = createFactory('SchemaReader')


class SchemaReader(SchemaReaderFactory):
    cache = {}

    @classmethod
    def read(self, name, fullpath, extension='json'):
        if name in self.cache:
            return self.cache[name]

        filename = '%s.%s' % (name, extension)
        paths = PathConfig.fullvalidpaths(fullpath, filename)
        if len(paths) == 0:
            raise IOError('The schema %s does not seem to exist, the file %s was not found in %s' % (
            name, filename, ', '.join(PathConfig.paths(fullpath))))

        reader = SchemaReaderFactory.create(extension)
        # we take the first one, if more than one was found, we assume that
        # the first one is the one to use
        schema = reader.read(paths[0])
        for s in schema:
            self.cache[s['schema']] = s
            SchemaValidate.validate(s)
        return self.cache[name]
