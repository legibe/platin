#.--------------------------------------------------------------------------------
# Copyright (c) 2013, MediaSift Ltd
# All rights reserved.
# Distribution of this software is strictly forbidden under the terms of this
# license.
#
# Author: Claude Gibert
#
#--------------------------------------------------------------------------------
from ..core.basic import make_list, no_list, is_sequence_and_not_string, is_sequence_and_not_string
from schemareader import SchemaReader
from validate import Validate
from types import Types

class Language(object):

    """ 
    if many requests from the same schema need to be evaluated, it is
    more efficient to create an instance of Language for a particular 
    schema and to call the method 'validate' repeatedly.
    """

    def __init__(self,schema,schemapath=None):
        self._help = None
        self._schemaNames = [schema]
        self._schemapath = schemapath
        self._name = schema
        self._schema = self.prepareSchema(schema)

    def validate(self,request):
        request = self.resolveAliases(request)
        s = self._schema
        skeys = set([ x for x in s.keys() if x[0] != '_' ])
        rkeys = set(request.keys())
        cloning = {}
        # if request has keywords which are not in the schema, we
        # shutdown straight away
        if not skeys.issuperset(rkeys):
            raise ValueError('Unknown keyword(s) in %s: %s' % (self._name,', '.join(rkeys.difference(skeys))))

        # if the request does not have keywords which are required, we also
        # shutdown straight away (they could have a default value though
        # in that case we assign them).
        required = []
        for key in skeys.difference(rkeys):
            if s[key]['required']:
                required.append(key)

        excludes = []
        for key in s:
            if 'excludes' in s[key]:
                excluded = set()
                excluded.add(key)
                for ex in s[key]['excludes']:
                    excluded.add(ex)
                excludes.append(excluded)
            if 'cloneinto' in s[key]:
                targets = []
                for target in s[key]['cloneinto']:
                    if not target in request:
                        targets.append(target)
                cloning[key] = targets
        allexcluded = set()
        for group in excludes:
            allexcluded = allexcluded.union(group)

        if len(required) > 0:
            remaining = []
            for key in required:
                if 'default' in s[key]:
                    request[key] = s[key]['default']
                elif not key in allexcluded:
                    remaining.append(key)
            if len(remaining) > 0:
                raise ValueError('Required keyword(s) are missing in %s: %s' % (self._name,', '.join(remaining)))

        for group in excludes:
            v,r = self.find_excluded(request,group,s)
            if len(v) == 0:
                if len(r) > 0:
                    raise ValueError('In "%s", at least one of "%s" is required' % (self._name,', '.join(group)))
            elif len(v) > 1:
                    raise ValueError('In "%s", only one of "%s" is required, your specifed "%s"' % (self._name,', '.join(group), ', '.join(v)))

        # deal with lists and non-lists
        # also expand sub-schemas
        for k,i in request.items():
            if not s[k]['uncountable']:
                if s[k]['unique']:
                    if is_sequence_and_not_string(i) and len(i) > 1:
                        raise ValueError('In %s, the keyword "%s" allows one value, not a list' % (self._name,k))
                    request[k] = no_list(i)
                else:
                    request[k] = make_list(i)
                    #if len(request[k]) == 0 and s[k]['required']:
                    #    raise ValueError('In %s, the keyword "%s" cannot be an empty list' % (self._name,k))
            sub_schema = self.hasSchema(k,s[k],request)
            if sub_schema is not None:
                if s[k]['unique']:
                    lang = Language(sub_schema,schemapath=self._schemapath)
                    request[k] = lang.validate(i)
                else:
                    i = make_list(i)
                    for index,entry in enumerate(i):
                        lang = Language(sub_schema,schemapath=self._schemapath)
                        i[index] = lang.validate(entry)

        # now validate the values in the request if we can
        for k,i in request.items():
            if "type" in s[k]:
                request[k] = self.createType(s[k]["type"],request[k])
            if 'validate' in s[k]:
                assert(Validate.isRegistered(s[k]['validate'][0]))
                f = Validate.create(s[k]['validate'][0],*s[k]['validate'][1:])
                request[k] = f(self._schemaNames,k,request[k],request)

        # as a last thing we clone whatever needs to be cloned
        for clone, targets in cloning.items():
            if clone in request:
                for target in targets:
                    if not s[clone]['unique'] and s[target]['unique']:
                        request[target] = request[clone][0]
                    else:
                        request[target] = request[clone]

        return request

    def createType(self,typeName,value):
        if is_sequence_and_not_string(value):
            result = []
            for v in value:
                result.append(Types.create(typeName,v))
            return result
        return Types.create(typeName,value)

    def remove_invalid(self,request):
        s = self._schema
        skeys = set([ x for x in s.keys() if x[0] != '_' ])
        deletes = []
        for k in request.keys():
            k = str(k)
            if not k in skeys:
                deletes.append(k)
            else:
                sub_schema = self.hasSchema(k,s[k],request)
                if sub_schema is not None:
                    if s[k]['unique']:
                        lang = Language(sub_schema,schemapath=self._schemapath)
                        request[k] = lang.remove_invalid(request[k])
                    else:
                        new = []
                        for index,entry in enumerate(request[k]):
                            lang = Language(sub_schema,schemapath=self._schemapath)
                            new.append(lang.remove_invalid(entry))
                        request[k] = new
        for k in deletes:
            del(request[k])
        return request

    def find_excluded(self,request,group,schema):
        keys = []
        required = set()
        for i in group:
            if i in request:
                keys.append(i)
            if i in schema and schema[i]['required']:
                required.add(i)
        return keys, required


    """
    This part deals with schemas only, nothing is being validated here,
    the data for validating is prepared, by interpreting schema statements
    such as 'inherit' or 'delete'
    """
    def prepareSchema(self,schema):
        schema = SchemaReader.read(schema,fullpath=self._schemapath)
        if self._help is None and 'help' in schema:
            self._help = schema['help']
        schema = self.handleInheritance(schema)
        for k,i in schema.items():
            if 'alias' in i:
                schema[k]['alias'] = set(i['alias'])
        return schema

    def handleInheritance(self,schema):
        if 'inherit' in schema:
            parents = schema['inherit']
            schema = schema['items']
            for parent in parents:
                self._schemaNames.append(parent)
                parent = self.prepareSchema(parent)
                schema = self.inherit(schema,parent)
        else:
            return schema['items']
        return schema

    def inherit(self,me,parent):
        delete = []
        for k,i in parent.items():
            if not k in me:
                me[k] = i
            else:
                if me[k]['delete']:
                    delete.append(k)
                else:
                    for kk,ii in i.items():
                        if not kk in me[k]:
                            me[k][kk] = ii
        for k in delete:
            del(me[k])
        return me

    def hasSchema(self,parent,data,request):
        if 'schema' in data:
            return data['schema']
        if 'field_dependent_schema' in data:
            key = data['field_dependent_schema']
            if not key in request:
                raise ValueError('Field dependent schema: the key %s is missing' % key)
            return request[key]
        if 'field_dependent_schema_namespaced' in data:
            key = data['field_dependent_schema_namespaced']
            if not key in request:
                raise ValueError('Field dependent schema: the key %s is missing' % key)
            return parent + '_' + request[key]
        return None

    def validFields(self):
        return self._schema.keys()

    def resolveAliases(self,request):
        def findOriginal(s,value):
            for k,i in s.items():
                if 'alias' in i:
                    if value in i['alias']:
                        return k
            return value

        if isinstance(request,dict):
            s = self._schema
            result = {}
            for k, i in request.items():
                if not k in s:
                    result[findOriginal(s,k)] = i
                else:
                    result[k] = i
            return result       
        else:
            return request
