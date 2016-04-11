#--------------------------------------------------------------------------------
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from ..core.basic import make_list, no_list


class SchemaValidate(object):
    schema = {
        'schema': {
            'type': str,
            'required': True
        },
        'inherit': {
            'required': False,
            'unique': False
        },
        'items': {
            'type': dict,
            'required': True
        },
        'help': {
            type: str,
            'required': False
        }
    }

    item = {
        'required': {
            'required': False,
            'default': True,
            'type': bool,
            'show_in_help': True
        },
        'unique': {
            'required': False,
            'default': True,
            'type': bool,
            'show_in_help': True
        },
        'uncountable': {
            'required': False,
            'default': False,
            'type': bool,
            'show_in_help': False
        },
        'validate': {
            'required': False,
            'type': list,
            'show_in_help': True
        },
        'default': {
            'required': False,
            'show_in_help': True
        },
        'type': {
            'required': False,
            'show_in_help': True
        },
        'delete': {
            'required': False,
            'default': False,
            'show_in_help': False
        },
        'help': {
            'required': False,
            'show_in_help': False
        },
        'field_dependent_schema': {
            'required': False,
            'show_in_help': True
        },
        'field_dependent_schema_namespaced': {
            'required': False,
            'show_in_help': True
        },
        'schema': {
            'required': False,
            'show_in_help': True
        },
        'excludes': {
            'required': False,
            'show_in_help': True,
            'type': list
        },
        'cloneinto': {
            'required': False,
            'type': list
        },
        'alias': {
            'required': False,
            'type': list,
            'show_in_help': True
        }
    }

    @classmethod
    def validate(self, other):
        text = self._validate(other, self.schema)
        if 'items' in other:
            for k, item in other['items'].items():
                text += self._validate(item, self.item)
        if len(text) > 0:
            print
            for t in text:
                print t
            print
            raise SystemError('Invalid schema definition')

    @classmethod
    def _validate(self, other, what):
        text = []
        selfk = set([x for x in what.keys()])
        otherk = set(other.keys())
        if selfk != otherk:
            diff = selfk.difference(otherk)
            for d in diff:
                if what[d]['required']:
                    text.append('-- Missing keyword "%s" is required' % d)
            diff = otherk.difference(selfk)
            for d in diff:
                text.append('-- Invalid keyword "%s"' % d)
        # set defaults first
        for k in selfk:
            if not k in other:
                if 'default' in what[k]:
                    other[k] = what[k]['default']
        for k in otherk:
            if k in what:
                entry = other[k]
                schema = what[k]
                if 'type' in schema:
                    error = '-- Type error: %s[%s] should be of type %s' % (k, entry, schema['type'].__name__)
                    if schema['type'] == list:
                        other[k] = make_list(entry)
                    elif schema['type'] == dict:
                        if not isinstance(entry, dict):
                            text.append(error)
                    else:
                        try:
                            new = schema['type'](entry)
                            other[k] = new
                        except:
                            text.append(error)
                if 'unique' in what[k]:
                    if not what[k]['unique']:
                        other[k] = make_list(entry)
                    else:
                        other[k] = no_list(entry)
        return text
