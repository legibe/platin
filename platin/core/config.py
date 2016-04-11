#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from basic import substitute_env_variables


class Config(object):
    cache = {}

    @classmethod
    def read(self, path, cache=True):
        path = substitute_env_variables(path)
        if not cache or not path in self.cache:
            l = path.split('.')
            with open(path) as f:
                if l[-1] == 'json':
                    import json

                    self.cache[path] = json.load(f)
                elif l[-1] == 'yaml':
                    import yaml

                    self.cache[path] = yaml.load(f)
                else:
                    raise IOError('Cannot handle that kind of file %s' % l[-1])
        return self.cache[path]

    """
    Expects a dictionary
    """

    @classmethod
    def find(self, data, entries):
        for k, i in data.items():
            found = True
            for kk, ii in entries.items():
                found &= (kk in i) and i[kk] == ii
            if found:
                return i
        return None
